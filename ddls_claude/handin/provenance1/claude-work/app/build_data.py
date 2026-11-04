#!/usr/bin/env python3
"""Collect every analysis result the dashboard shows into a single data.js file.

Writes `const DATA = {...}` so the page works when opened directly from disk as well
as when served over a local HTTP server.
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ANA = ROOT / 'ouput' / 'analysis'
CLA = ROOT / 'ddls_claude' / 'analysis'
OUT = Path(__file__).resolve().parent

MAIN = ['Blot 1', 'Blot 2', 'Blot 3']


def clean(obj):
    """Make NaN/numpy types JSON-safe."""
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return None if (obj is None or (isinstance(obj, float) and np.isnan(obj))) else round(float(obj), 6)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if obj is None or (isinstance(obj, float) and np.isnan(obj)):
        return None
    return obj


def recs(df):
    return clean(df.replace({np.nan: None}).to_dict(orient='records'))


gene = pd.read_csv(CLA / 'sp_gene_identity_and_standing.csv')[['peptide_id', 'gene']].drop_duplicates()

summary = pd.read_csv(ANA / 'replicate_summary_by_peptide.csv').merge(gene, on='peptide_id', how='left')
long = pd.read_csv(ANA / 'replicate_values_long.csv')
assoc = pd.read_csv(ANA / 'step4' / 'associations_robust_mean.csv')
perm = pd.read_csv(ANA / 'step4' / 'permutation_multiplicity_test.csv').iloc[0]
rel = pd.read_csv(ANA / 'step5' / 'measurement_reliability.csv')
cv = pd.read_csv(ANA / 'step6' / 'model_cv_performance.csv')
insample = pd.read_csv(ANA / 'step6' / 'in_sample_vs_out_of_fold.csv')
rbs = pd.read_csv(CLA / 'rbs_hypothesis_test.csv').iloc[0]
improved = pd.read_csv(CLA / 'improved_features.csv')
uni = pd.read_csv(CLA / 'uniprot_native_sp_comparison.csv')
cross = pd.read_csv(CLA / 'cross_assay_shared_peptides.csv')
qc = pd.read_csv(ANA / 'step3' / 'sequence_qc_summary.csv').iloc[0]

# Rank stability: mean vs median
m = summary[summary.block.isin(MAIN)].copy()
m['rank_mean'] = m.groupby('block')['mean'].rank(ascending=False)
m['rank_median'] = m.groupby('block')['median'].rank(ascending=False)
m['rank_shift'] = (m.rank_mean - m.rank_median).abs()

# RBS scatter data: feature vs outcome, per blot
scatter = (m.merge(improved[['peptide_id', 'dg_rbs_plus48', 'dg_cds_only48', 'gravy_kd',
                             'net_charge_ph7']], on='peptide_id'))

uni_cols = ['peptide_id', 'gene', 'accession', 'supplied_length', 'native_signal_length',
            'supplied_last3', 'native_last3', 'exact_match', 'c_terminus_differs']
uni_out = uni[[c for c in uni_cols if c in uni.columns]].copy()

native_counts = (uni[uni.native_last3.notna()].native_last3.value_counts()
                 .rename_axis('motif').reset_index(name='n'))

data = dict(
    meta=dict(
        n_peptides=int(qc.n_peptides),
        blots=[{'blot': b, 'n': int((m.block == b).sum())} for b in MAIN],
        generated='from ouput/analysis and ddls_claude/analysis',
    ),
    qc=dict(
        translations_match=bool(qc.all_translations_match),
        starts_with_met=bool(qc.all_start_with_met),
        aa_len_min=int(qc.aa_length_min), aa_len_max=int(qc.aa_length_max),
    ),
    summary=recs(m[['block', 'peptide_id', 'gene', 'mean', 'median', 'sd', 'cv', 'min', 'max',
                    'rank_mean', 'rank_median', 'rank_shift']]),
    replicates=recs(long[long.block.isin(MAIN)][['block', 'peptide_id', 'replicate', 'value']]),
    validation=recs(long[long.block == 'Validation blot'][['block', 'peptide_id', 'replicate', 'value']]),
    associations=recs(assoc[['feature', 'rho_blot1', 'rho_blot2', 'rho_blot3', 'combined_rho',
                             'combined_lo95', 'combined_hi95', 'all_same_direction',
                             'family_wise_p_maxstat']]),
    permutation=dict(
        observed=float(perm.observed_max_abs_combined_rho),
        best_feature=str(perm.best_feature),
        null_median=float(perm.null_median_max_abs_rho),
        null_p95=float(perm.null_p95),
        family_wise_p=float(perm.family_wise_p_value),
        n_features=int(perm.n_features_screened),
        n_perm=int(perm.n_permutations),
    ),
    reliability=recs(rel),
    rbs=dict(
        rho=float(rbs.observed_combined_rho),
        blot1=float(rbs.rho_blot1), blot2=float(rbs.rho_blot2), blot3=float(rbs.rho_blot3),
        p_single=float(rbs.one_sided_p_single_hypothesis),
        p_family=float(rbs.one_sided_p_family_of_3_windows),
        n_perm=int(rbs.n_permutations),
    ),
    scatter=recs(scatter[['block', 'peptide_id', 'gene', 'mean', 'dg_rbs_plus48',
                          'dg_cds_only48', 'gravy_kd', 'net_charge_ph7']]),
    models=recs(cv[['cv_scheme', 'model', 'mean_within_blot_spearman', 'mae']]),
    insample=recs(insample),
    uniprot=recs(uni_out),
    native_motifs=recs(native_counts),
    cross_assay=recs(cross),
)

js = 'const DATA = ' + json.dumps(clean(data), indent=1) + ';\n'
(OUT / 'data.js').write_text(js, encoding='utf-8')
print(f'Wrote {OUT / "data.js"}  ({len(js) / 1024:.0f} KB)')
for k, v in data.items():
    print(f'  {k}: {len(v) if isinstance(v, (list, dict)) else v}')
