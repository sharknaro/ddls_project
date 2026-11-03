#!/usr/bin/env python3
"""Cross-assay comparison: these 32 signal peptides are named B. subtilis genes.

The thesis chapter's plasmid/primer tables identify every SP in the library. They are all
native B. subtilis 168 signal peptides amplified from genomic DNA, not anonymous sequences.
That makes the library directly comparable with published B. subtilis SP screens.

Five of them were also among the 15 best performers in Fu et al. (2018), who measured
alpha-amylase (AmyS) secretion by enzyme activity rather than collagen by Western blot. This
script asks whether a peptide's standing for amylase predicts its standing for collagen.

IMPORTANT CAVEATS, enforced in how results are reported:
  * The SP->gene mapping is read from the thesis chapter, not from the supplied workbook. It
    must be confirmed by the data owner before being relied on.
  * The five shared peptides sit in THREE different blots with no common scale, so they
    cannot be ranked against one another on raw fold-change. Within-blot percentile rank is
    used instead, which is itself only a partial remedy.
  * Different reporter protein, host background, promoter, and assay chemistry. A negative
    result here is expected under the target-dependence hypothesis and is not a defect.
  * n = 5. This is descriptive. No inference is drawn from the p-value.

Outputs are written beneath ddls_claude/analysis/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------------------
# SP -> source gene, from the thesis plasmid aliases (pBS008-pBS039) and primer names.
# NEEDS OWNER CONFIRMATION.
# --------------------------------------------------------------------------------------
SP_GENE = {
    'SP1': 'AmyE', 'SP2': 'AprE', 'SP3': 'Bpr', 'SP4': 'Epr', 'SP5': 'Mpr', 'SP6': 'Pel',
    'SP7': 'PenP', 'SP8': 'PhoA', 'SP9': 'PhoB', 'SP10': 'Vpr', 'SP11': 'XynA',
    'SP12': 'YbdN', 'SP13': 'YlqB', 'SP14': 'YncM', 'SP15': 'YoaW', 'SP16': 'YocH',
    'SP17': 'YqxI', 'SP18': 'YvgO', 'SP19': 'YwaD', 'SP20': 'YweA', 'SP21': 'YwtF',
    'SP22': 'YxaL', 'SP23': 'NprB', 'SP24': 'SacB', 'SP25': 'SacC', 'SP26': 'AbnA',
    'SP27': 'BglS', 'SP28': 'YolA', 'SP29': 'Csn', 'SP30': 'Bsn', 'SP31': 'CwlO',
    'SP32': 'EglS',
}

# --------------------------------------------------------------------------------------
# Fu et al. (2018) Figure 5 / Table S2: shake-flask AmyS activity, U/mL, for their 15 best.
# Reporter: alpha-amylase AmyS. Host: B. subtilis 1A751p. Promoter: aprE.
# Native-SP benchmark derivable at approximately 883 U/mL (pel reported as +68.4%).
# --------------------------------------------------------------------------------------
FU_ACTIVITY = {
    'YvcE': 1064.05, 'YoqM': 1211.85, 'YuaB': 1153.40, 'Pel': 1487.85, 'PelB': 1360.00,
    'YoaW': 871.00, 'YqxI': 1394.15, 'LipA': 1191.60, 'LipB': 1238.25, 'YoqH': 1181.75,
    'YbfO': 1270.10, 'SacB': 1019.10, 'BglS': 1379.55, 'YddT': 882.05, 'YobB': 1096.20,
}
FU_NATIVE_SP_BENCHMARK = 883.0

summary = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'replicate_summary_by_peptide.csv')
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']
main = summary[summary.block.isin(MAIN)].copy()
main['gene'] = main.peptide_id.map(SP_GENE)
assert main.gene.notna().all(), 'unmapped peptide id'

# Within-blot percentile rank: the only cross-blot-safe standing available.
main['within_blot_pct'] = main.groupby('block')['mean'].rank(pct=True)
main['within_blot_rank'] = main.groupby('block')['mean'].rank(ascending=False)
main['blot_n'] = main.groupby('block')['mean'].transform('size')

main[['peptide_id', 'gene', 'block', 'mean', 'median', 'within_blot_rank', 'blot_n',
      'within_blot_pct']].sort_values(['block', 'within_blot_rank']).to_csv(
    OUT / 'sp_gene_identity_and_standing.csv', index=False)

# --------------------------------------------------------------------------------------
# The overlap
# --------------------------------------------------------------------------------------
shared = main[main.gene.isin(FU_ACTIVITY)].copy()
shared['fu_amys_activity_U_per_mL'] = shared.gene.map(FU_ACTIVITY)
shared['fu_fold_vs_native_sp'] = shared.fu_amys_activity_U_per_mL / FU_NATIVE_SP_BENCHMARK
shared = shared.sort_values('fu_amys_activity_U_per_mL', ascending=False)

cols = ['peptide_id', 'gene', 'block', 'blot_n', 'mean', 'within_blot_rank',
        'within_blot_pct', 'fu_amys_activity_U_per_mL', 'fu_fold_vs_native_sp']
shared[cols].to_csv(OUT / 'cross_assay_shared_peptides.csv', index=False)

print(f'Signal peptides shared with the Fu et al. top-15 list: {len(shared)}')
print(shared[cols].round(3).to_string(index=False))

if len(shared) >= 3:
    rho, p = spearmanr(shared.within_blot_pct, shared.fu_amys_activity_U_per_mL)
    print(f'\nSpearman(collagen within-blot percentile, AmyS activity) = {rho:.2f}  '
          f'p = {p:.2f}  n = {len(shared)}')
    print('Positive would mean a peptide good for amylase is also good for collagen.')
    pd.DataFrame([dict(
        n_shared=len(shared), spearman_rho=rho, p_value=p,
        interpretation='descriptive only; n too small for inference; different reporter, '
                       'host, promoter and assay; the 5 peptides span 3 blots with no '
                       'common scale',
    )]).to_csv(OUT / 'cross_assay_rank_agreement.csv', index=False)

# --------------------------------------------------------------------------------------
# Which of the library's own peptides are the classic high-secretion workhorses?
# --------------------------------------------------------------------------------------
WORKHORSES = ['AmyE', 'AprE', 'NprB', 'SacB', 'XynA', 'Pel', 'BglS', 'EglS']
wh = main[main.gene.isin(WORKHORSES)][
    ['peptide_id', 'gene', 'block', 'mean', 'within_blot_rank', 'blot_n']]
wh.sort_values(['block', 'within_blot_rank']).to_csv(
    OUT / 'classic_workhorse_sp_standing.csv', index=False)
print('\nClassic, heavily used B. subtilis secretion signal peptides, as they performed here:')
print(wh.sort_values(['block', 'within_blot_rank']).round(3).to_string(index=False))

print(f'\nWrote cross-assay outputs to {OUT}')
