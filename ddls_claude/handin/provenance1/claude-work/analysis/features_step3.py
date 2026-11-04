#!/usr/bin/env python3
"""Step 3: sequence QC and interpretable feature derivation for the 32 signal peptides.

Every feature here is a *descriptor computed from the supplied sequences*. None of them
is evidence of mechanism, and none of them has been validated against secretion.
Region boundaries (n/h/c) are produced by a transparent, documented heuristic, not by
SignalP or any trained predictor; see `feature_definitions.md` for the exact rules and
the sensitivity analysis that reports how stable those boundaries are.

Outputs are written beneath ouput/analysis/step3/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint

import RNA

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'data' / 'Information_for_Baris_corrected.xlsx'
OUT = ROOT / 'ouput' / 'analysis' / 'step3'
OUT.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------------------
# Documented constants
# --------------------------------------------------------------------------------------

# Kyte & Doolittle (1982) hydropathy scale. Used for the h-region search and for GRAVY.
KD = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5, 'Q': -3.5, 'E': -3.5, 'G': -0.4,
    'H': -3.2, 'I': 4.5, 'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6, 'S': -0.8,
    'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}

# Eisenberg et al. (1984) consensus scale, used only as a sensitivity check on the
# hydrophobicity-driven segmentation so conclusions do not rest on one scale.
EISENBERG = {
    'A': 0.62, 'R': -2.53, 'N': -0.78, 'D': -0.90, 'C': 0.29, 'Q': -0.85, 'E': -0.74,
    'G': 0.48, 'H': -0.40, 'I': 1.38, 'L': 1.06, 'K': -1.50, 'M': 0.64, 'F': 1.19,
    'P': 0.12, 'S': -0.18, 'T': -0.05, 'W': 0.81, 'Y': 0.26, 'V': 1.08,
}

VALID_AA = set('ACDEFGHIKLMNPQRSTVWY')

GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S',
    'TCG': 'S', 'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*', 'TGT': 'C', 'TGC': 'C',
    'TGA': '*', 'TGG': 'W', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'CCT': 'P',
    'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
    'ATG': 'M', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N',
    'AAA': 'K', 'AAG': 'K', 'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GTT': 'V',
    'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
    'GGG': 'G',
}


def translate(nt: str) -> str:
    return ''.join(GENETIC_CODE.get(nt[i:i + 3], '?') for i in range(0, len(nt) - 2, 3))


# --------------------------------------------------------------------------------------
# h-region segmentation
# --------------------------------------------------------------------------------------

def find_h_region(aa: str, scale: dict, threshold: float, min_len: int = 5):
    """Return (start, end) inclusive 0-based indices of the most hydrophobic segment.

    Maximum-subarray (Kadane) search on `scale[residue] - threshold`. The segment with
    the largest total excess hydrophobicity above `threshold` is taken as the h-region.
    This is a transparent one-parameter rule, chosen so that the boundary decision can be
    audited and varied, NOT a validated signal-peptide prediction.

    Constraints: the segment may not start at position 0 (the initiator methionine is
    assigned to the n-region by construction) and may not extend to the final residue, so
    a c-region of at least one residue always exists. Segments shorter than `min_len` are
    rejected; if no admissible segment exists the function returns (None, None).
    """
    scores = [scale[r] - threshold for r in aa]
    lo, hi = 1, len(aa) - 2  # inclusive bounds on admissible segment positions
    best = (-np.inf, None, None)
    for start in range(lo, hi + 1):
        total = 0.0
        for end in range(start, hi + 1):
            total += scores[end]
            if end - start + 1 >= min_len and total > best[0]:
                best = (total, start, end)
    if best[1] is None:
        return None, None
    return best[1], best[2]


def region_split(aa: str, scale: dict, threshold: float):
    """Split into (n, h, c) strings using the h-region found above."""
    start, end = find_h_region(aa, scale, threshold)
    if start is None:
        return None, None, None, None, None
    return aa[:start], aa[start:end + 1], aa[end + 1:], start, end


def hydrophobic_core(aa: str, scale: dict, width: int = 9):
    """Return (start, mean_score) of the fixed-width window with the highest mean score.

    This is the ROBUST companion to `find_h_region`. Because the width is fixed, the only
    free quantity is the window position, which the sensitivity analysis shows is stable
    across hydrophobicity scales and thresholds, whereas the variable-length h-region end
    is not. Features derived from this window are therefore preferred for association
    testing, and the variable-length segmentation is reported as sensitivity only.
    """
    best = (-np.inf, None)
    for start in range(1, len(aa) - width):
        m = float(np.mean([scale[r] for r in aa[start:start + width]]))
        if m > best[0]:
            best = (m, start)
    return best[1], best[0]


def frac(seq: str, residues: str) -> float:
    return sum(seq.count(r) for r in residues) / len(seq) if seq else np.nan


# --------------------------------------------------------------------------------------
# Load sequences
# --------------------------------------------------------------------------------------

feeding = pd.read_excel(INPUT, sheet_name='Information for feeding', header=None)

records = []
for ridx in range(4, 36):
    pid = feeding.iat[ridx, 0]
    if pd.isna(pid):
        continue
    records.append(dict(
        peptide_id=str(pid).strip(),
        source_cell=f'Information for feeding!A{ridx + 1}',
        sp_origin=str(feeding.iat[ridx, 1]).strip(),
        aa=str(feeding.iat[ridx, 2]).strip().upper(),
        nt=str(feeding.iat[ridx, 3]).strip().upper(),
    ))

print(f'Loaded {len(records)} peptide rows from the sequence sheet.')

# --------------------------------------------------------------------------------------
# Per-peptide features
# --------------------------------------------------------------------------------------

PRIMARY_THRESHOLD = 1.0  # KD units; see feature_definitions.md
SENSITIVITY = [('KD', KD, 0.5), ('KD', KD, 1.0), ('KD', KD, 1.5), ('Eisenberg', EISENBERG, 0.0)]

rows = []
sens_rows = []

for rec in records:
    pid, aa, nt = rec['peptide_id'], rec['aa'], rec['nt']

    # ---- QC -------------------------------------------------------------------------
    aa_ok = not (set(aa) - VALID_AA)
    nt_ok = not (set(nt) - set('ACGT'))
    in_frame = len(nt) == 3 * len(aa)
    translation_matches = in_frame and translate(nt) == aa

    prot = ProteinAnalysis(aa)

    # ---- region segmentation ---------------------------------------------------------
    # Variable-length h-region: reported, but its END is unstable across settings
    # (see h_region_stability_summary.csv). Treat h_region_length / c_region_length and
    # anything derived from them as FRAGILE.
    n_reg, h_reg, c_reg, h_start, h_end = region_split(aa, KD, PRIMARY_THRESHOLD)

    # Robust alternative: fixed 9-residue maximal-hydrophobicity window.
    core_start, core_kd = hydrophobic_core(aa, KD, width=9)
    core = aa[core_start:core_start + 9]
    # n-proximal region = everything before the hydrophobic core (stable boundary).
    n_prox = aa[:core_start]
    # c-proximal region = fixed last 6 residues, independent of any h/c boundary choice.
    c_prox = aa[-6:]

    # ---- sensitivity of the segmentation --------------------------------------------
    for scale_name, scale, thr in SENSITIVITY:
        s, e = find_h_region(aa, scale, thr)
        sens_rows.append(dict(
            peptide_id=pid, scale=scale_name, threshold=thr,
            h_start_1based=None if s is None else s + 1,
            h_end_1based=None if e is None else e + 1,
            h_length=None if s is None else e - s + 1,
        ))

    # ---- C-terminal cleavage-motif descriptors ---------------------------------------
    # ASSUMPTION (unverified): the listed sequence ends immediately before the cleavage
    # site, so the final three residues correspond to positions -3, -2, -1.
    p4, p3, p2, p1 = aa[-4], aa[-3], aa[-2], aa[-1]
    axa_like = int(p3 in 'AGSC' and p1 in 'AGSC')
    strict_axa = int(p3 == 'A' and p1 == 'A')

    # ---- nucleotide / transcript descriptors ------------------------------------------
    gc_all = frac(nt, 'GC')
    gc3 = np.mean([nt[i + 2] in 'GC' for i in range(0, len(nt) - 2, 3)])
    gc_first30 = frac(nt[:30], 'GC')

    # mRNA folding free energy of 5' windows of the signal-peptide coding sequence.
    # CAVEAT: the true translation-initiation region includes the 5'UTR/RBS and the
    # vector context, which the owner has not yet supplied. These windows therefore
    # describe the start of the coding sequence only and are NOT the initiation-region
    # folding energy reported by Fu et al. (2018).
    def mfe(seq_nt: str) -> float:
        if len(seq_nt) < 10:
            return np.nan
        return float(RNA.fold(seq_nt.replace('T', 'U'))[1])

    dg30 = mfe(nt[:30])
    dg48 = mfe(nt[:48])
    dg60 = mfe(nt[:60])
    dg_full = mfe(nt)

    row = dict(
        peptide_id=pid,
        sp_origin=rec['sp_origin'],
        source_cell=rec['source_cell'],
        # QC
        aa_length=len(aa),
        nt_length=len(nt),
        aa_alphabet_valid=aa_ok,
        nt_alphabet_valid=nt_ok,
        nt_is_3x_aa=in_frame,
        translation_matches_aa=translation_matches,
        starts_with_met=aa.startswith('M'),
        qc_flag='' if (translation_matches and aa.startswith('M')) else
                'AA/NT disagree at residue 1 or no initiator Met - NOT silently corrected',
        # whole-peptide composition / physicochemistry
        gravy_kd=prot.gravy(),
        aromaticity=prot.aromaticity(),
        instability_index=prot.instability_index(),
        isoelectric_point=IsoelectricPoint(aa).pi(),
        net_charge_ph7=prot.charge_at_pH(7.0),
        kr_count=aa.count('K') + aa.count('R'),
        de_count=aa.count('D') + aa.count('E'),
        kr_minus_de=aa.count('K') + aa.count('R') - aa.count('D') - aa.count('E'),
        frac_hydrophobic_AVILMFWY=frac(aa, 'AVILMFWY'),
        frac_leucine=frac(aa, 'L'),
        frac_alanine=frac(aa, 'A'),
        frac_glycine=frac(aa, 'G'),
        frac_proline=frac(aa, 'P'),
        frac_serine=frac(aa, 'S'),
        frac_helix_breaker_GPS=frac(aa, 'GPS'),
        cysteine_count=aa.count('C'),
        # ---- ROBUST region descriptors (fixed-width core; stable boundary) ----------
        h_core9_start_1based=core_start + 1,
        h_core9_mean_kd=core_kd,
        h_core9_sequence=core,
        h_core9_frac_leucine=frac(core, 'L'),
        h_core9_frac_hydrophobic=frac(core, 'AVILMFWY'),
        h_core9_frac_helix_breaker_GPS=frac(core, 'GPS'),
        n_prox_length=len(n_prox),
        n_prox_kr_count=n_prox.count('K') + n_prox.count('R'),
        n_prox_net_charge_ph7=ProteinAnalysis(n_prox).charge_at_pH(7.0) if n_prox else np.nan,
        n_prox_frac_basic_KR=frac(n_prox, 'KR'),
        c_prox6_sequence=c_prox,
        c_prox6_gravy=float(np.mean([KD[r] for r in c_prox])),
        c_prox6_frac_polar_STNQ=frac(c_prox, 'STNQ'),
        c_prox6_frac_small_AGS=frac(c_prox, 'AGS'),
        # ---- FRAGILE region descriptors (variable-length segmentation) ---------------
        h_start_1based=h_start + 1,
        h_end_1based=h_end + 1,
        n_region=n_reg,
        h_region=h_reg,
        c_region=c_reg,
        n_region_length=len(n_reg),
        h_region_length=len(h_reg),
        c_region_length=len(c_reg),
        # n-region descriptors
        n_region_kr_count=n_reg.count('K') + n_reg.count('R'),
        n_region_net_charge_ph7=ProteinAnalysis(n_reg).charge_at_pH(7.0) if n_reg else np.nan,
        n_region_frac_basic_KR=frac(n_reg, 'KR'),
        n_region_gravy=np.mean([KD[r] for r in n_reg]) if n_reg else np.nan,
        # h-region descriptors
        h_region_gravy=np.mean([KD[r] for r in h_reg]),
        h_region_frac_hydrophobic=frac(h_reg, 'AVILMFWY'),
        h_region_frac_leucine=frac(h_reg, 'L'),
        h_region_frac_helix_breaker_GPS=frac(h_reg, 'GPS'),
        h_region_max_kd_window7=max(
            np.mean([KD[r] for r in h_reg[i:i + 7]]) for i in range(max(1, len(h_reg) - 6))
        ),
        # c-region / cleavage-motif descriptors
        c_region_gravy=np.mean([KD[r] for r in c_reg]) if c_reg else np.nan,
        c_region_frac_polar_STNQ=frac(c_reg, 'STNQ'),
        pos_minus4=p4,
        pos_minus3=p3,
        pos_minus2=p2,
        pos_minus1=p1,
        axa_like_motif=axa_like,
        strict_AxA_motif=strict_axa,
        # nucleotide / transcript descriptors
        nt_gc_fraction=gc_all,
        nt_gc3_fraction=float(gc3),
        nt_gc_first30=gc_first30,
        mrna_dg_first30nt=dg30,
        mrna_dg_first48nt=dg48,
        mrna_dg_first60nt=dg60,
        mrna_dg_full_sp_cds=dg_full,
        mrna_dg_full_per_nt=dg_full / len(nt),
        aa_sequence=aa,
        nt_sequence=nt,
    )
    rows.append(row)

feat = pd.DataFrame(rows)
feat.to_csv(OUT / 'peptide_features.csv', index=False)

sens = pd.DataFrame(sens_rows)
sens.to_csv(OUT / 'h_region_segmentation_sensitivity.csv', index=False)

# How stable is the h-region under the alternative settings?
pivot = sens.pivot(index='peptide_id', columns=['scale', 'threshold'], values='h_length')
stability = pd.DataFrame({
    'h_length_min': pivot.min(axis=1),
    'h_length_max': pivot.max(axis=1),
    'h_length_range': pivot.max(axis=1) - pivot.min(axis=1),
})
start_pivot = sens.pivot(index='peptide_id', columns=['scale', 'threshold'], values='h_start_1based')
stability['h_start_range'] = start_pivot.max(axis=1) - start_pivot.min(axis=1)
stability.to_csv(OUT / 'h_region_stability_summary.csv')

print('Segmentation stability (range of h-region length across 4 settings):')
print(stability['h_length_range'].describe())

# --------------------------------------------------------------------------------------
# QC assertions reported rather than silently assumed
# --------------------------------------------------------------------------------------
qc = dict(
    n_peptides=len(feat),
    duplicate_ids=int(feat.peptide_id.duplicated().sum()),
    duplicate_aa_sequences=int(feat.aa_sequence.duplicated().sum()),
    all_aa_alphabet_valid=bool(feat.aa_alphabet_valid.all()),
    all_nt_alphabet_valid=bool(feat.nt_alphabet_valid.all()),
    all_in_frame=bool(feat.nt_is_3x_aa.all()),
    all_translations_match=bool(feat.translation_matches_aa.all()),
    all_start_with_met=bool(feat.starts_with_met.all()),
    aa_length_min=int(feat.aa_length.min()),
    aa_length_max=int(feat.aa_length.max()),
)
pd.DataFrame([qc]).to_csv(OUT / 'sequence_qc_summary.csv', index=False)
print('QC summary:', qc)

# --------------------------------------------------------------------------------------
# Feature collinearity: these descriptors are not independent tests.
# --------------------------------------------------------------------------------------
# Robust descriptors: preferred for association testing in step 4.
ROBUST = [
    'aa_length', 'gravy_kd', 'aromaticity', 'instability_index', 'isoelectric_point',
    'net_charge_ph7', 'kr_count', 'kr_minus_de', 'frac_hydrophobic_AVILMFWY',
    'frac_leucine', 'frac_alanine', 'frac_glycine', 'frac_proline', 'frac_serine',
    'frac_helix_breaker_GPS', 'h_core9_start_1based', 'h_core9_mean_kd',
    'h_core9_frac_leucine', 'h_core9_frac_hydrophobic', 'h_core9_frac_helix_breaker_GPS',
    'n_prox_length', 'n_prox_kr_count', 'n_prox_net_charge_ph7', 'n_prox_frac_basic_KR',
    'c_prox6_gravy', 'c_prox6_frac_polar_STNQ', 'c_prox6_frac_small_AGS',
    'axa_like_motif', 'nt_gc_fraction', 'nt_gc3_fraction', 'nt_gc_first30',
    'mrna_dg_first30nt', 'mrna_dg_first48nt', 'mrna_dg_first60nt', 'mrna_dg_full_per_nt',
]
# Fragile descriptors: depend on the unstable variable-length h/c boundary.
FRAGILE = [
    'n_region_length', 'n_region_kr_count', 'n_region_net_charge_ph7',
    'n_region_frac_basic_KR', 'h_region_length', 'h_region_gravy',
    'h_region_frac_hydrophobic', 'h_region_frac_leucine',
    'h_region_frac_helix_breaker_GPS', 'h_region_max_kd_window7', 'c_region_length',
    'c_region_frac_polar_STNQ',
]
# Zero-variance descriptors carry no information about differences between peptides and
# are excluded from association testing. They are reported because a library-wide
# constant is itself a finding: it means that property cannot explain any variation.
constant = [c for c in ROBUST + FRAGILE if feat[c].nunique() <= 1]
pd.DataFrame([
    dict(feature=c, constant_value=feat[c].iloc[0],
         note='invariant across all 32 peptides; cannot explain between-peptide differences')
    for c in constant
]).to_csv(OUT / 'constant_features.csv', index=False)
if constant:
    print(f'Excluding {len(constant)} zero-variance features from association testing: {constant}')
ROBUST = [c for c in ROBUST if c not in constant]
FRAGILE = [c for c in FRAGILE if c not in constant]

NUMERIC = ROBUST + FRAGILE
pd.DataFrame(
    [dict(feature=f, stability='robust') for f in ROBUST]
    + [dict(feature=f, stability='fragile_depends_on_h_c_boundary') for f in FRAGILE]
).to_csv(OUT / 'feature_stability_classification.csv', index=False)
corr = feat[NUMERIC].corr(method='spearman')
corr.to_csv(OUT / 'feature_collinearity_spearman.csv')

fig, ax = plt.subplots(figsize=(15, 13))
sns.heatmap(corr, cmap='RdBu_r', center=0, vmin=-1, vmax=1, square=True,
            linewidths=.3, cbar_kws={'label': 'Spearman rho'}, ax=ax)
ax.set_title('Feature-feature Spearman correlation (n=32 peptides)\n'
             'Descriptors are strongly inter-correlated: they are not independent tests.')
fig.tight_layout()
fig.savefig(OUT / 'feature_collinearity_heatmap.png', dpi=170)
plt.close(fig)

# Flag redundant pairs so the association step does not treat them as separate evidence.
pairs = []
for i, a in enumerate(NUMERIC):
    for b in NUMERIC[i + 1:]:
        r = corr.loc[a, b]
        if abs(r) >= 0.8:
            pairs.append(dict(feature_a=a, feature_b=b, spearman_rho=r))
pd.DataFrame(pairs).sort_values('spearman_rho', key=abs, ascending=False).to_csv(
    OUT / 'feature_redundant_pairs.csv', index=False)
print(f'{len(pairs)} feature pairs with |rho| >= 0.8 recorded in feature_redundant_pairs.csv')

# --------------------------------------------------------------------------------------
# Feature distributions
# --------------------------------------------------------------------------------------
PANEL = [
    'aa_length', 'n_prox_length', 'h_core9_start_1based', 'h_core9_mean_kd',
    'gravy_kd', 'net_charge_ph7', 'n_prox_kr_count', 'isoelectric_point',
    'h_core9_frac_leucine', 'h_core9_frac_helix_breaker_GPS', 'c_prox6_frac_small_AGS',
    'frac_alanine', 'nt_gc_fraction', 'nt_gc3_fraction', 'mrna_dg_first48nt',
    'mrna_dg_full_per_nt',
]
fig, axes = plt.subplots(4, 4, figsize=(17, 13))
for ax, col in zip(axes.flat, PANEL):
    sns.histplot(feat[col], bins=12, ax=ax, color='#4c72b0')
    sns.rugplot(feat[col], ax=ax, color='#c44e52', height=.08)
    ax.set_title(col, fontsize=10)
    ax.set_xlabel('')
fig.suptitle('Distribution of derived descriptors across all 32 signal peptides', y=1.0)
fig.tight_layout()
fig.savefig(OUT / 'feature_distributions.png', dpi=170)
plt.close(fig)

# Region-composition picture: what the heuristic segmentation actually produced.
fig, ax = plt.subplots(figsize=(11, 9))
order = feat.sort_values('aa_length').peptide_id.tolist()
plot = feat.set_index('peptide_id').loc[order]
ax.barh(order, plot.n_region_length, color='#5b8ff9', label='n-region (before h)')
ax.barh(order, plot.h_region_length, left=plot.n_region_length, color='#f6bd16',
        label='h-region (max hydrophobic segment)')
ax.barh(order, plot.c_region_length,
        left=plot.n_region_length + plot.h_region_length, color='#5ad8a6',
        label='c-region (after h)')
ax.set_xlabel('Residue position')
ax.set_title('Heuristic n/h/c segmentation (Kyte-Doolittle, threshold 1.0)\n'
             'Boundaries are computed, not experimentally determined.')
ax.legend(loc='lower right')
fig.tight_layout()
fig.savefig(OUT / 'region_segmentation.png', dpi=170)
plt.close(fig)

print(f'Wrote step 3 outputs to {OUT}')
