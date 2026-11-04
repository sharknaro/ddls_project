#!/usr/bin/env python3
"""Step 4: feature-outcome association testing, respecting blot boundaries.

Design rules enforced here:
  * The three main blots are analysed SEPARATELY. Blot-normalised values are never pooled
    on a common numeric scale.
  * Replicates are summarised to one value per peptide before testing. Replicate rows are
    never treated as independent observations.
  * All candidates in a blot are used - never only the top performers.
  * Only the `robust` feature set from step 3 is tested; fragile h/c-boundary features are
    reported separately as sensitivity.
  * Multiplicity is calibrated by a within-blot permutation test on the maximum statistic,
    because 30+ correlated descriptors across 3 small blots will produce a large |rho| by
    chance alone.

Outputs are written beneath ouput/analysis/step4/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, norm

RNG = np.random.default_rng(20261103)
N_PERM = 5000

ROOT = Path(__file__).resolve().parents[2]
STEP3 = ROOT / 'ouput' / 'analysis' / 'step3'
OUT = ROOT / 'ouput' / 'analysis' / 'step4'
OUT.mkdir(parents=True, exist_ok=True)

feat = pd.read_csv(STEP3 / 'peptide_features.csv')
stab = pd.read_csv(STEP3 / 'feature_stability_classification.csv')
summary = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'replicate_summary_by_peptide.csv')

ROBUST = stab.loc[stab.stability == 'robust', 'feature'].tolist()
FRAGILE = stab.loc[stab.stability != 'robust', 'feature'].tolist()

MAIN_BLOTS = ['Blot 1', 'Blot 2', 'Blot 3']
main = summary[summary.block.isin(MAIN_BLOTS)].copy()
data = main.merge(feat, on='peptide_id', validate='one_to_one')
assert len(data) == 32, f'expected 32 main-blot peptides, got {len(data)}'
print('Peptides per blot:', data.groupby('block').size().to_dict())


# --------------------------------------------------------------------------------------
# Core statistics
# --------------------------------------------------------------------------------------

def fisher_combine(rhos, ns):
    """Combine per-blot Spearman rho by inverse-variance Fisher-z meta-analysis.

    This combines EFFECTS estimated separately within each blot. It does not pool the
    blot-normalised values themselves onto a shared scale, which the data owner warned
    against. Each blot contributes its own rank correlation, weighted by n-3.
    """
    rhos = np.asarray(rhos, dtype=float)
    ns = np.asarray(ns, dtype=float)
    ok = np.isfinite(rhos) & (ns > 3)
    if ok.sum() == 0:
        return np.nan, np.nan, np.nan, np.nan
    z = np.arctanh(np.clip(rhos[ok], -0.999999, 0.999999))
    w = ns[ok] - 3
    zbar = float(np.sum(w * z) / np.sum(w))
    se = float(np.sqrt(1 / np.sum(w)))
    lo, hi = zbar - 1.96 * se, zbar + 1.96 * se
    return float(np.tanh(zbar)), float(np.tanh(lo)), float(np.tanh(hi)), zbar / se


def per_blot_stats(df, feature, outcome='mean'):
    rhos, ns, ps = [], [], []
    for b in MAIN_BLOTS:
        g = df[df.block == b]
        if g[feature].nunique() < 3:
            rhos.append(np.nan); ns.append(len(g)); ps.append(np.nan)
            continue
        rho, p = spearmanr(g[feature], g[outcome])
        rhos.append(rho); ns.append(len(g)); ps.append(p)
    return rhos, ns, ps


# --------------------------------------------------------------------------------------
# Primary analysis: robust features, outcome = per-peptide replicate mean
# --------------------------------------------------------------------------------------

def run_panel(df, features, outcome, label):
    rows = []
    for f in features:
        rhos, ns, ps = per_blot_stats(df, f, outcome)
        comb, lo, hi, zstat = fisher_combine(rhos, ns)
        finite = [r for r in rhos if np.isfinite(r)]
        rows.append(dict(
            feature=f,
            rho_blot1=rhos[0], rho_blot2=rhos[1], rho_blot3=rhos[2],
            p_blot1=ps[0], p_blot2=ps[1], p_blot3=ps[2],
            n_blot1=ns[0], n_blot2=ns[1], n_blot3=ns[2],
            combined_rho=comb, combined_lo95=lo, combined_hi95=hi,
            combined_p_unadjusted=2 * norm.sf(abs(zstat)) if np.isfinite(zstat) else np.nan,
            n_blots_positive=sum(r > 0 for r in finite),
            n_blots_negative=sum(r < 0 for r in finite),
            all_same_direction=len(finite) > 0 and (
                all(r > 0 for r in finite) or all(r < 0 for r in finite)),
            max_abs_rho=max((abs(r) for r in finite), default=np.nan),
        ))
    out = pd.DataFrame(rows).sort_values('combined_rho', key=abs, ascending=False)
    out.insert(0, 'outcome', outcome)
    out.insert(0, 'panel', label)
    return out


primary = run_panel(data, ROBUST, 'mean', 'robust')
fragile = run_panel(data, FRAGILE, 'mean', 'fragile_sensitivity')
primary.to_csv(OUT / 'associations_robust_mean.csv', index=False)
fragile.to_csv(OUT / 'associations_fragile_sensitivity.csv', index=False)

print('\nTop 8 robust features by |combined rho|:')
print(primary[['feature', 'rho_blot1', 'rho_blot2', 'rho_blot3', 'combined_rho',
               'combined_lo95', 'combined_hi95', 'all_same_direction']].head(8).round(3).to_string(index=False))


# --------------------------------------------------------------------------------------
# Multiplicity calibration: permutation null for the MAXIMUM statistic
# --------------------------------------------------------------------------------------
# Under the null of no feature-outcome relation, shuffling the outcome WITHIN each blot
# preserves blot size and the feature correlation structure. The null distribution of
# max |combined rho| over the whole feature panel tells us how large the best-looking
# association gets by chance when 30+ correlated descriptors are screened.

feat_matrix = {b: data[data.block == b][ROBUST].to_numpy(dtype=float) for b in MAIN_BLOTS}
out_vec = {b: data[data.block == b]['mean'].to_numpy(dtype=float) for b in MAIN_BLOTS}
ns_blot = [len(out_vec[b]) for b in MAIN_BLOTS]


def rank(a, axis=0):
    return pd.DataFrame(a).rank().to_numpy()


def combined_rho_all(perm_out):
    """Vectorised combined rho for every feature at once, given per-blot outcomes."""
    zs, ws = [], []
    for b, n in zip(MAIN_BLOTS, ns_blot):
        if n <= 3:
            continue
        X = rank(feat_matrix[b])
        y = pd.Series(perm_out[b]).rank().to_numpy()
        Xc = X - X.mean(0)
        yc = y - y.mean()
        denom = np.sqrt((Xc ** 2).sum(0) * (yc ** 2).sum())
        with np.errstate(invalid='ignore', divide='ignore'):
            r = (Xc * yc[:, None]).sum(0) / denom
        zs.append(np.arctanh(np.clip(np.nan_to_num(r), -0.999999, 0.999999)) * (n - 3))
        ws.append(n - 3)
    return np.tanh(np.sum(zs, axis=0) / np.sum(ws))


observed = combined_rho_all(out_vec)
obs_max = np.nanmax(np.abs(observed))

null_max = np.empty(N_PERM)
for i in range(N_PERM):
    perm = {b: RNG.permutation(out_vec[b]) for b in MAIN_BLOTS}
    null_max[i] = np.nanmax(np.abs(combined_rho_all(perm)))

fwer_p = float((np.sum(null_max >= obs_max) + 1) / (N_PERM + 1))
null_q = np.percentile(null_max, [50, 90, 95, 99])

perm_summary = dict(
    n_permutations=N_PERM,
    n_features_screened=len(ROBUST),
    observed_max_abs_combined_rho=float(obs_max),
    best_feature=ROBUST[int(np.nanargmax(np.abs(observed)))],
    null_median_max_abs_rho=float(null_q[0]),
    null_p90=float(null_q[1]),
    null_p95=float(null_q[2]),
    null_p99=float(null_q[3]),
    family_wise_p_value=fwer_p,
)
pd.DataFrame([perm_summary]).to_csv(OUT / 'permutation_multiplicity_test.csv', index=False)
print('\nPermutation multiplicity test:')
for k, v in perm_summary.items():
    print(f'  {k}: {v}')

# Per-feature family-wise adjusted p-values from the same max-statistic null.
primary['family_wise_p_maxstat'] = [
    float((np.sum(null_max >= abs(r)) + 1) / (N_PERM + 1)) if np.isfinite(r) else np.nan
    for r in primary.combined_rho
]
primary.to_csv(OUT / 'associations_robust_mean.csv', index=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(null_max, bins=50, color='#9bb7d4', edgecolor='white')
ax.axvline(obs_max, color='#c44e52', lw=2,
           label=f'observed best |rho| = {obs_max:.2f}\n(family-wise p = {fwer_p:.3f})')
ax.axvline(null_q[2], color='#555', ls='--', lw=1, label=f'null 95th pct = {null_q[2]:.2f}')
ax.set_xlabel('max |combined rho| across the screened feature panel')
ax.set_ylabel('Permutations')
ax.set_title('What the best-looking association looks like under the null\n'
             f'({N_PERM} within-blot permutations, {len(ROBUST)} features screened)')
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(OUT / 'permutation_null_maxstat.png', dpi=170)
plt.close(fig)


# --------------------------------------------------------------------------------------
# Sensitivity: alternative outcome summaries and influential-point checks
# --------------------------------------------------------------------------------------
sens = [run_panel(data, ROBUST, 'median', 'robust_median_outcome')]

no_sp9 = data[data.peptide_id != 'SP9']
sens.append(run_panel(no_sp9, ROBUST, 'mean', 'robust_excluding_SP9'))

# Leave-one-peptide-out range for the combined rho of each feature.
loo_rows = []
for f in ROBUST:
    vals = []
    for pid in data.peptide_id:
        d = data[data.peptide_id != pid]
        rhos, ns, _ = per_blot_stats(d, f, 'mean')
        vals.append(fisher_combine(rhos, ns)[0])
    vals = np.array(vals, dtype=float)
    full = primary.loc[primary.feature == f, 'combined_rho'].iloc[0]
    loo_rows.append(dict(
        feature=f, combined_rho_full=full,
        loo_min=np.nanmin(vals), loo_max=np.nanmax(vals),
        loo_range=np.nanmax(vals) - np.nanmin(vals),
        sign_flips_under_loo=int(np.sum(np.sign(vals) != np.sign(full))),
        most_influential_peptide=data.peptide_id.iloc[int(np.nanargmax(np.abs(vals - full)))],
    ))
loo = pd.DataFrame(loo_rows).sort_values('loo_range', ascending=False)
loo.to_csv(OUT / 'leave_one_peptide_out_stability.csv', index=False)

pd.concat(sens).to_csv(OUT / 'associations_sensitivity.csv', index=False)

print('\nLeave-one-peptide-out stability (top 6 features by |combined rho|):')
top6 = primary.feature.head(6).tolist()
print(loo[loo.feature.isin(top6)][
    ['feature', 'combined_rho_full', 'loo_min', 'loo_max', 'sign_flips_under_loo']
].round(3).to_string(index=False))


# --------------------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------------------
# Forest-style view: per-blot rho plus combined estimate with CI, all features.
plot_df = primary.head(18).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 10))
ypos = np.arange(len(plot_df))
for off, col, mark, colr in [
        (-0.26, 'rho_blot1', 'o', '#4c72b0'),
        (0.00, 'rho_blot2', 's', '#dd8452'),
        (0.26, 'rho_blot3', '^', '#55a868')]:
    ax.scatter(plot_df[col], ypos + off, marker=mark, s=42, color=colr, zorder=3,
               label=col.replace('rho_blot', 'Blot '))
ax.errorbar(plot_df.combined_rho, ypos,
            xerr=[plot_df.combined_rho - plot_df.combined_lo95,
                  plot_df.combined_hi95 - plot_df.combined_rho],
            fmt='D', color='#333', ms=6, capsize=3, lw=1.4, zorder=4, label='Combined (95% CI)')
ax.axvline(0, color='#999', lw=1)
ax.axvspan(-null_q[2], null_q[2], color='#eee', zorder=0,
           label=f'within null 95th pct ({null_q[2]:.2f})')
ax.set_yticks(ypos)
ax.set_yticklabels(plot_df.feature, fontsize=9)
ax.set_xlabel('Spearman rho with per-peptide mean fold-change')
ax.set_title('Feature-outcome association within each blot\n'
             'Combined estimate is a meta-analysis of per-blot effects, not pooled values')
ax.legend(fontsize=8, loc='lower right')
ax.set_xlim(-1.05, 1.05)
fig.tight_layout()
fig.savefig(OUT / 'association_forest.png', dpi=170)
plt.close(fig)

# Scatter panel for the four strongest features, faceted by blot.
top4 = primary.feature.head(4).tolist()
fig, axes = plt.subplots(4, 3, figsize=(14, 16))
for r, f in enumerate(top4):
    for c, b in enumerate(MAIN_BLOTS):
        g = data[data.block == b]
        ax = axes[r, c]
        ax.scatter(g[f], g['mean'], s=45, color='#4c72b0')
        for _, rr in g.iterrows():
            ax.annotate(rr.peptide_id, (rr[f], rr['mean']), xytext=(3, 3),
                        textcoords='offset points', fontsize=7)
        st = primary[primary.feature == f].iloc[0]
        rho = st[f'rho_blot{c + 1}']
        ax.set_title(f'{b}: rho={rho:.2f}, n={len(g)}', fontsize=10)
        ax.set_xlabel(f, fontsize=9)
        if c == 0:
            ax.set_ylabel('Mean fold-change\n(within-blot scale)', fontsize=9)
fig.suptitle('Four strongest robust features, shown separately within each blot\n'
             'Each blot has its own normalisation; y-axes are not comparable across columns',
             y=1.0)
fig.tight_layout()
fig.savefig(OUT / 'top_features_by_blot.png', dpi=170)
plt.close(fig)

print(f'\nWrote step 4 outputs to {OUT}')
