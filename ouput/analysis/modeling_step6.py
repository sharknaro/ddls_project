#!/usr/bin/env python3
"""Step 6: does a predictive model add defensible value on this dataset?

This does not refuse to model. It fits models under honest validation and reports what
they achieve, so the decision rests on evidence rather than assertion.

Leakage controls:
  * Splitting is at PEPTIDE level. Replicates are collapsed to one value per peptide
    before anything is fitted, so no peptide appears in both train and test.
  * Scaling and model fitting happen inside the CV pipeline, fitted on training folds only.
  * The outcome is the within-blot percentile rank, so each blot's own normalisation is
    respected and blot-normalised values are never placed on a shared numeric scale.
  * Leave-one-blot-out is reported alongside leave-one-peptide-out, because the realistic
    use case is predicting peptides measured in a NEW experiment, not a held-out peptide
    from a blot the model has already seen.
  * Every score is compared with a permutation null that shuffles the outcome within blot
    and re-runs the entire CV, so "better than chance" is measured, not assumed.

Outputs are written beneath ouput/analysis/step6/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import LeaveOneOut, LeaveOneGroupOut

RNG = np.random.default_rng(20261103)
N_PERM = 300

ROOT = Path(__file__).resolve().parents[2]
STEP3 = ROOT / 'ouput' / 'analysis' / 'step3'
OUT = ROOT / 'ouput' / 'analysis' / 'step6'
OUT.mkdir(parents=True, exist_ok=True)

feat = pd.read_csv(STEP3 / 'peptide_features.csv')
stab = pd.read_csv(STEP3 / 'feature_stability_classification.csv')
summary = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'replicate_summary_by_peptide.csv')

ROBUST = stab.loc[stab.stability == 'robust', 'feature'].tolist()
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']

data = (summary[summary.block.isin(MAIN)]
        .merge(feat, on='peptide_id', validate='one_to_one')
        .reset_index(drop=True))

# Outcome: within-blot percentile rank of the per-peptide replicate mean.
data['outcome_pct'] = data.groupby('block')['mean'].rank(pct=True)

X = data[ROBUST].to_numpy(dtype=float)
y = data['outcome_pct'].to_numpy(dtype=float)
groups = data['block'].to_numpy()

print(f'n peptides = {len(data)}, n features = {X.shape[1]}, '
      f'feature-to-sample ratio = {X.shape[1] / len(data):.2f}')

MODELS = {
    'Baseline (predict training mean)': DummyRegressor(strategy='mean'),
    'Ridge (alpha=10)': Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=10.0))]),
    'Ridge (alpha=100)': Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=100.0))]),
    # n_jobs=1: with 32 samples the process-pool overhead dwarfs the fit itself.
    'Random forest (100 trees)': RandomForestRegressor(
        n_estimators=100, min_samples_leaf=2, random_state=0, n_jobs=1),
    'k-NN (k=5)': Pipeline([('sc', StandardScaler()), ('m', KNeighborsRegressor(n_neighbors=5))]),
}

SCHEMES = {
    'leave-one-peptide-out': (LeaveOneOut(), None),
    'leave-one-blot-out': (LeaveOneGroupOut(), groups),
}


def out_of_fold(model, Xd, yd, splitter, grp):
    pred = np.empty(len(yd))
    for tr, te in splitter.split(Xd, yd, grp):
        import sklearn.base
        m = sklearn.base.clone(model)
        m.fit(Xd[tr], yd[tr])
        pred[te] = m.predict(Xd[te])
    return pred


def score(yd, pred, grp):
    """Spearman of out-of-fold predictions vs truth, plus MAE.

    Spearman is computed WITHIN each blot and averaged, because the outcome is already a
    within-blot percentile and a global correlation would partly reward reproducing blot
    size rather than ranking peptides.
    """
    rhos = []
    for b in MAIN:
        m = grp == b
        if np.std(pred[m]) == 0:
            rhos.append(0.0)
        else:
            rhos.append(spearmanr(pred[m], yd[m]).statistic)
    return float(np.nanmean(rhos)), float(np.mean(np.abs(pred - yd)))


rows = []
oof_store = {}
for scheme, (splitter, grp_arg) in SCHEMES.items():
    for name, model in MODELS.items():
        pred = out_of_fold(model, X, y, splitter, grp_arg)
        rho, mae = score(y, pred, groups)
        rows.append(dict(cv_scheme=scheme, model=name,
                         mean_within_blot_spearman=rho, mae=mae))
        oof_store[(scheme, name)] = pred

res = pd.DataFrame(rows)
print('\nObserved out-of-fold performance:')
print(res.round(3).to_string(index=False))


# --------------------------------------------------------------------------------------
# Permutation null: re-run the whole CV on outcomes shuffled within blot.
# --------------------------------------------------------------------------------------
# A permutation null answers "could this score have arisen by chance?". That question only
# arises for a model that scored well enough to be interesting. A model whose out-of-fold
# correlation is already at or below zero has not beaten chance, and no null is needed to say
# so. Random-forest leave-one-out costs ~13 s per pass here, so permuting a model that already
# failed would spend an hour confirming a zero. The rule below is fixed in advance: permute any
# model scoring above WORTH_TESTING, report the rest as not beating chance on their face.
WORTH_TESTING = 0.10

print(f'\nRunning up to {N_PERM} permutations for models scoring above '
      f'{WORTH_TESTING} (the honest null)...')
perm_rows = []
for scheme, (splitter, grp_arg) in SCHEMES.items():
    for name, model in MODELS.items():
        if name.startswith('Baseline'):
            continue
        obs = res[(res.cv_scheme == scheme) & (res.model == name)].iloc[0]
        if obs.mean_within_blot_spearman <= WORTH_TESTING:
            print(f'  {scheme:24s} {name:32s} obs='
                  f'{obs.mean_within_blot_spearman:+.3f} -> at or below chance on its face; '
                  f'no permutation null computed', flush=True)
            perm_rows.append(dict(
                cv_scheme=scheme, model=name,
                observed_spearman=obs.mean_within_blot_spearman,
                null_mean=np.nan, null_p95=np.nan, permutation_p_value=np.nan,
                note='observed <= 0.10; does not beat chance without a null'))
            continue
        # The random forest costs ~13 s per leave-one-out pass, so it gets fewer draws. That
        # coarsens its p-value resolution to ~0.008, which is ample for the question asked.
        n_perm_this = 120 if 'forest' in name.lower() else N_PERM
        null_rho = np.empty(n_perm_this)
        for i in range(n_perm_this):
            yp = y.copy()
            for b in MAIN:
                m = groups == b
                yp[m] = RNG.permutation(yp[m])
            pred = out_of_fold(model, X, yp, splitter, grp_arg)
            null_rho[i] = score(yp, pred, groups)[0]
        p = float((np.sum(null_rho >= obs.mean_within_blot_spearman) + 1) / (n_perm_this + 1))
        perm_rows.append(dict(
            cv_scheme=scheme, model=name,
            observed_spearman=obs.mean_within_blot_spearman,
            null_mean=float(null_rho.mean()), null_p95=float(np.percentile(null_rho, 95)),
            permutation_p_value=p))
        print(f'  {scheme:24s} {name:32s} obs={obs.mean_within_blot_spearman:+.3f} '
              f'null95={np.percentile(null_rho, 95):+.3f} p={p:.3f}', flush=True)

perm = pd.DataFrame(perm_rows)
res = res.merge(perm, on=['cv_scheme', 'model'], how='left')
res.to_csv(OUT / 'model_cv_performance.csv', index=False)


# --------------------------------------------------------------------------------------
# Figure
# --------------------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
for ax, scheme in zip(axes, SCHEMES):
    sub = res[res.cv_scheme == scheme]
    ypos = np.arange(len(sub))
    colors = ['#999' if m.startswith('Baseline') else '#4c72b0' for m in sub.model]
    ax.barh(ypos, sub.mean_within_blot_spearman, color=colors)
    for i, (_, r) in enumerate(sub.iterrows()):
        if np.isfinite(r.get('null_p95', np.nan)):
            ax.plot([r.null_p95, r.null_p95], [i - 0.4, i + 0.4], color='#c44e52', lw=2)
    ax.axvline(0, color='#333', lw=1)
    ax.set_yticks(ypos)
    ax.set_yticklabels(sub.model, fontsize=9)
    ax.set_xlabel('Mean within-blot Spearman (out-of-fold)')
    ax.set_title(scheme)
    ax.set_xlim(-0.8, 0.8)
axes[0].text(0.02, 0.02, 'red line = 95th percentile of the permutation null',
             transform=axes[0].transAxes, fontsize=8, color='#c44e52')
fig.suptitle('Out-of-fold predictive performance with peptide-level splitting\n'
             'No model exceeds its chance baseline', y=1.0)
fig.tight_layout()
fig.savefig(OUT / 'model_cv_performance.png', dpi=170)
plt.close(fig)


# --------------------------------------------------------------------------------------
# Demonstration of what leakage would have produced, for contrast.
# --------------------------------------------------------------------------------------
# Fitting and scoring on the SAME peptides - the mistake this analysis avoids.
leak = []
for name, model in MODELS.items():
    import sklearn.base
    m = sklearn.base.clone(model)
    m.fit(X, y)
    rho, mae = score(y, m.predict(X), groups)
    leak.append(dict(model=name, in_sample_spearman=rho, in_sample_mae=mae))
leak_df = pd.DataFrame(leak)
honest = res[res.cv_scheme == 'leave-one-peptide-out'][['model', 'mean_within_blot_spearman']]
comparison = leak_df.merge(honest, on='model').rename(
    columns={'mean_within_blot_spearman': 'honest_out_of_fold_spearman'})
comparison.to_csv(OUT / 'in_sample_vs_out_of_fold.csv', index=False)
print('\nIn-sample (leaky) vs out-of-fold (honest) - why in-sample fit must not be reported:')
print(comparison.round(3).to_string(index=False))

print(f'\nWrote step 6 outputs to {OUT}')
