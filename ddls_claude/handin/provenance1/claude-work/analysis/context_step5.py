#!/usr/bin/env python3
"""Step 5: measurement reliability, the validation blot, and the other-protein table.

These are treated as SEPARATE context, not as additional training or validation data.
No cross-blot conversion is fitted.

Three questions:
  1. How reproducible is the outcome itself? This sets a ceiling on any feature-outcome
     correlation that could be detected, and is needed to interpret the step 4 result.
  2. Do the seven shared peptides behave consistently between their original blot and the
     separate validation blot?
  3. What do the four-peptide other-protein categories show, on their own terms?

Outputs are written beneath ouput/analysis/step5/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
ANA = ROOT / 'ouput' / 'analysis'
OUT = ANA / 'step5'
OUT.mkdir(parents=True, exist_ok=True)

feat = pd.read_csv(ANA / 'step3' / 'peptide_features.csv')
stab = pd.read_csv(ANA / 'step3' / 'feature_stability_classification.csv')
summary = pd.read_csv(ANA / 'replicate_summary_by_peptide.csv')
conc = pd.read_csv(ANA / 'replicate_rank_concordance.csv')
assoc = pd.read_csv(ANA / 'step4' / 'associations_robust_mean.csv')
cats = pd.read_csv(ANA / 'other_protein_categories_long.csv')

ROBUST = stab.loc[stab.stability == 'robust', 'feature'].tolist()
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']

# --------------------------------------------------------------------------------------
# 1. Measurement reliability and the attenuation ceiling
# --------------------------------------------------------------------------------------
# Inter-replicate rank agreement estimates how much of the observed peptide ordering is
# reproducible signal rather than assay noise. Spearman-Brown then gives the reliability
# of the MEAN of k replicates, and sqrt(reliability) is the largest correlation a perfect
# predictor of true secretion could show against these measurements.

rel_rows = []
for block, g in conc.groupby('block'):
    k = summary[summary.block == block].n.max()
    rbar = float(g.spearman_rho.mean())
    sb = (k * rbar) / (1 + (k - 1) * rbar) if rbar > 0 else np.nan
    rel_rows.append(dict(
        block=block, n_replicates=int(k), n_replicate_pairs=len(g),
        mean_inter_replicate_spearman=rbar,
        min_inter_replicate_spearman=float(g.spearman_rho.min()),
        max_inter_replicate_spearman=float(g.spearman_rho.max()),
        spearman_brown_reliability_of_mean=sb,
        max_detectable_correlation=np.sqrt(sb) if np.isfinite(sb) else np.nan))
rel = pd.DataFrame(rel_rows)
rel.to_csv(OUT / 'measurement_reliability.csv', index=False)
print('Measurement reliability by blot:')
print(rel.round(3).to_string(index=False))

main_ceiling = float(rel[rel.block.isin(MAIN)].max_detectable_correlation.mean())
print(f'\nMean attenuation ceiling across the three main blots: {main_ceiling:.2f}')
print('A feature perfectly predicting true secretion could correlate with these')
print(f'measurements at about {main_ceiling:.2f}, not 1.0.')

# --------------------------------------------------------------------------------------
# 2. Validation blot: descriptive only
# --------------------------------------------------------------------------------------
val = summary[summary.block == 'Validation blot'].merge(feat, on='peptide_id')
val_rows = []
for f in ROBUST:
    if val[f].nunique() < 3:
        continue
    rho, p = spearmanr(val[f], val['mean'])
    main_rho = assoc.loc[assoc.feature == f, 'combined_rho']
    mr = float(main_rho.iloc[0]) if len(main_rho) else np.nan
    val_rows.append(dict(feature=f, validation_rho=rho, validation_p=p, n=len(val),
                         main_blots_combined_rho=mr,
                         same_direction_as_main=bool(np.sign(rho) == np.sign(mr))))
valdf = pd.DataFrame(val_rows).sort_values('validation_rho', key=abs, ascending=False)
valdf.to_csv(OUT / 'validation_blot_feature_directions.csv', index=False)

agree = int(valdf.same_direction_as_main.sum())
print(f'\nValidation blot (n=7, descriptive only): {agree} of {len(valdf)} features point '
      f'the same way as the main-blot combined estimate.')
print('Expected by chance alone: about half. With n=7 every one of these has a confidence')
print('interval spanning most of the possible range.')

# Shared-peptide reproducibility between the original blot and the validation blot.
pair = pd.read_csv(ANA / 'validation_paired_shared_peptides.csv')
rho_pair, p_pair = spearmanr(pair.main_mean, pair.validation_mean)
shared = dict(
    n_shared_peptides=len(pair),
    rank_spearman_original_vs_validation=float(rho_pair),
    p_value=float(p_pair),
    n_lower_in_validation=int((pair.mean_difference_validation_minus_main < 0).sum()),
    median_shift=float(pair.mean_difference_validation_minus_main.median()),
)
pd.DataFrame([shared]).to_csv(OUT / 'shared_peptide_reproducibility.csv', index=False)
print('\nShared peptides, original blot vs validation blot:')
for k, v in shared.items():
    print(f'  {k}: {v}')
print('The ordering is broadly preserved while the scale shifts downward, which is exactly')
print('why the owner\'s warning against pooling blot-normalised values is followed here.')
print('No conversion between blots has been fitted.')

# --------------------------------------------------------------------------------------
# 3. Other-protein categories: separate, categorical, no thresholds
# --------------------------------------------------------------------------------------
cats['category'] = cats.category.str.strip()
order = ['No', 'Low', 'Medium', 'High']
tab = cats.pivot(index='peptide_id', columns='protein_construct', values='category')

by_pep = (cats.groupby(['peptide_id', 'category']).size().unstack(fill_value=0)
          .reindex(columns=order, fill_value=0))
by_pep.to_csv(OUT / 'other_protein_counts_by_peptide.csv')
by_con = (cats.groupby(['protein_construct', 'category']).size().unstack(fill_value=0)
          .reindex(columns=order, fill_value=0))
by_con.to_csv(OUT / 'other_protein_counts_by_construct.csv')

print('\nOther-protein categories by peptide (4 peptides x 7 constructs):')
print(by_pep.to_string())
print('\n"No" means product not produced (owner, meeting 2). Low/Medium/High have NO stated')
print('thresholds and are not calibrated to the fold-change scale, so they are not converted')
print('to numbers and not used as an outcome anywhere in this analysis.')

# How do those four peptides rank in their own main blots? Descriptive juxtaposition only.
four = ['SP3', 'SP5', 'SP19', 'SP26']
ctx = summary[(summary.peptide_id.isin(four)) & (summary.block.isin(MAIN))][
    ['peptide_id', 'block', 'mean', 'within_block_mean_rank_desc']]
ctx = ctx.merge(by_pep.reset_index(), on='peptide_id', how='left')
ctx.to_csv(OUT / 'other_protein_peptides_main_blot_context.csv', index=False)
print('\nThose four peptides in their own main blots (juxtaposition, not a comparison):')
print(ctx.round(3).to_string(index=False))

# --------------------------------------------------------------------------------------
# Figure: reliability ceiling vs observed associations
# --------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
obs = assoc.combined_rho.abs().dropna()
ax.hist(obs, bins=14, color='#9bb7d4', edgecolor='white',
        label='observed |combined rho| per feature')
ax.axvline(main_ceiling, color='#55a868', lw=2.5,
           label=f'reliability ceiling ~{main_ceiling:.2f}')
perm = pd.read_csv(ANA / 'step4' / 'permutation_multiplicity_test.csv').iloc[0]
ax.axvline(perm.null_p95, color='#c44e52', lw=2, ls='--',
           label=f'null 95th pct for best-of-panel ({perm.null_p95:.2f})')
ax.axvline(perm.observed_max_abs_combined_rho, color='#333', lw=2,
           label=f'observed best ({perm.observed_max_abs_combined_rho:.2f})')
ax.set_xlabel('|combined Spearman rho|')
ax.set_ylabel('Number of features')
ax.set_title('Observed associations sit below both the chance threshold\n'
             'and the measurement-reliability ceiling')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / 'reliability_vs_observed.png', dpi=170)
plt.close(fig)

print(f'\nWrote step 5 outputs to {OUT}')
