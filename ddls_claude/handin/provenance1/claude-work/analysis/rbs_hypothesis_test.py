#!/usr/bin/env python3
"""Honest test of ONE pre-specified, literature-derived hypothesis.

The hypothesis is not ours and was not chosen after looking at these results. Fu et al. (2018)
propose that a less negative folding free energy in the translation-initiation region leaves the
ribosome-binding site and start codon more accessible, and so favours secretion. That predicts a
POSITIVE rank correlation between dG and secretion. The thesis supplies the shared 5' context
needed to compute it.

This matters because the step 4 permutation null (95th percentile 0.60) was calibrated for an
exploratory screen of 34 features, where the relevant question is how large the BEST of many
correlated descriptors gets by chance. That null is the right one for a screen and the wrong one
for a single hypothesis specified in advance with a predicted direction.

Here the family is the three RBS-aware window sizes (30, 48, 60 nt), the window size being a
nuisance parameter rather than a separate hypothesis. The null is therefore the maximum over
those three windows only, one-sided in the predicted direction.

Outputs are written beneath ddls_claude/analysis/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

RNG = np.random.default_rng(20261103)
N_PERM = 20000

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']

FAMILY = ['dg_rbs_plus30', 'dg_rbs_plus48', 'dg_rbs_plus60']
PRESPECIFIED = 'dg_rbs_plus48'

new = pd.read_csv(OUT / 'improved_features.csv')
summary = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'replicate_summary_by_peptide.csv')
data = summary[summary.block.isin(MAIN)].merge(new, on='peptide_id', validate='one_to_one')

ns = {b: (data.block == b).sum() for b in MAIN}
X = {b: data[data.block == b][FAMILY].to_numpy(dtype=float) for b in MAIN}
y = {b: data[data.block == b]['mean'].to_numpy(dtype=float) for b in MAIN}


def combined_rho(outcome):
    """Fisher-z meta-analysis of per-blot Spearman rho, for every feature at once."""
    zs, ws = [], []
    for b in MAIN:
        n = ns[b]
        R = pd.DataFrame(X[b]).rank().to_numpy()
        yy = pd.Series(outcome[b]).rank().to_numpy()
        Rc = R - R.mean(0)
        yc = yy - yy.mean()
        r = (Rc * yc[:, None]).sum(0) / np.sqrt((Rc ** 2).sum(0) * (yc ** 2).sum())
        zs.append(np.arctanh(np.clip(np.nan_to_num(r), -0.999999, 0.999999)) * (n - 3))
        ws.append(n - 3)
    return np.tanh(np.sum(zs, axis=0) / np.sum(ws))


observed = combined_rho(y)
obs = dict(zip(FAMILY, observed))
obs_pre = obs[PRESPECIFIED]
obs_max = float(np.max(observed))

null_pre = np.empty(N_PERM)
null_max = np.empty(N_PERM)
for i in range(N_PERM):
    perm = {b: RNG.permutation(y[b]) for b in MAIN}
    c = combined_rho(perm)
    null_pre[i] = c[FAMILY.index(PRESPECIFIED)]
    null_max[i] = np.max(c)

# One-sided: the literature predicts a POSITIVE correlation.
p_pre = float((np.sum(null_pre >= obs_pre) + 1) / (N_PERM + 1))
p_family = float((np.sum(null_max >= obs_max) + 1) / (N_PERM + 1))

res = dict(
    prespecified_feature=PRESPECIFIED,
    observed_combined_rho=float(obs_pre),
    rho_blot1=float(spearmanr(data[data.block == 'Blot 1'][PRESPECIFIED],
                              data[data.block == 'Blot 1']['mean']).statistic),
    rho_blot2=float(spearmanr(data[data.block == 'Blot 2'][PRESPECIFIED],
                              data[data.block == 'Blot 2']['mean']).statistic),
    rho_blot3=float(spearmanr(data[data.block == 'Blot 3'][PRESPECIFIED],
                              data[data.block == 'Blot 3']['mean']).statistic),
    one_sided_p_single_hypothesis=p_pre,
    one_sided_p_family_of_3_windows=p_family,
    n_permutations=N_PERM,
    direction_predicted_by_literature='positive (less negative dG favours secretion)',
)
pd.DataFrame([res]).to_csv(OUT / 'rbs_hypothesis_test.csv', index=False)

print('Pre-specified hypothesis (Fu et al. 2018): less negative initiation-region dG')
print('leaves the RBS/start accessible and favours secretion -> positive rank correlation.\n')
for k, v in res.items():
    print(f'  {k}: {v}')

print('\nPer-window observed combined rho:')
for f in FAMILY:
    print(f'  {f}: {obs[f]:+.3f}')

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.hist(null_max, bins=60, color='#9bb7d4', edgecolor='white',
        label='null: best of the 3 window sizes')
ax.axvline(obs_max, color='#c44e52', lw=2.5,
           label=f'observed = {obs_max:+.2f}  (one-sided p = {p_family:.4f})')
ax.axvline(np.percentile(null_max, 95), color='#555', ls='--', lw=1.2,
           label=f'null 95th pct = {np.percentile(null_max, 95):.2f}')
ax.set_xlabel('combined Spearman rho')
ax.set_ylabel('Permutations')
ax.set_title('RBS-aware initiation-region folding energy vs secretion\n'
             'One pre-specified hypothesis, not a 34-feature screen')
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(OUT / 'rbs_hypothesis_null.png', dpi=170)
plt.close(fig)

print(f'\nWrote outputs to {OUT}')
