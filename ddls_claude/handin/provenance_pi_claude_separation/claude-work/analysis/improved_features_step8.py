#!/usr/bin/env python3
"""Two literature-driven improvements to the feature analysis.

(A) RBS-aware mRNA folding energy.
    The thesis states every construct carries the same upstream context: a USER overhang plus
    the ribosome-binding site AGGAGGAATATAC, then ATG and the signal-peptide CDS. Folding
    energies computed earlier started at ATG and so could not represent the
    translation-initiation region that Fu et al. (2018) associate with secretion. Prepending
    the real 5' context does not by itself create differences between peptides - it is shared -
    but it changes the folding landscape, because the RBS can pair with signal-peptide coding
    sequence. That interaction is peptide-specific and is what the published feature is about.

    STILL APPROXIMATE: the true transcription start site of the P3P promoter is not stated, so
    the window remains shorter than the 170 nt Fu et al. used. This is better, not exact.

(B) Non-monotonic tests for GRAVY and charge.
    Grasso et al. (2023) report an interior optimum - GRAVY near 1.0 is best and strongly
    negative is detrimental; charge below +2 is better. Every test run so far was rank-based
    and therefore blind to an interior optimum by construction. This script tests distance from
    the published optimum, and checks whether this library even spans the informative range.

Outputs are written beneath ddls_claude/analysis/.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import RNA

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']

# Upstream context shared by every construct, from the thesis forward-primer overhang
# GGCGAUAGGAGGAATATACATG... (U is the USER-cloning uracil; read as T for folding).
# RBS proper is AGGAGGAATATAC.
SHARED_5PRIME = 'GGCGATAGGAGGAATATAC'

feat = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'step3' / 'peptide_features.csv')
summary = pd.read_csv(ROOT / 'ouput' / 'analysis' / 'replicate_summary_by_peptide.csv')


def mfe(seq_nt: str) -> float:
    return float(RNA.fold(seq_nt.replace('T', 'U'))[1])


rows = []
for _, r in feat.iterrows():
    nt = r.nt_sequence
    rows.append(dict(
        peptide_id=r.peptide_id,
        # (A) RBS-aware windows: shared 5' context + the first N bases of the SP CDS.
        dg_rbs_plus30=mfe(SHARED_5PRIME + nt[:30]),
        dg_rbs_plus48=mfe(SHARED_5PRIME + nt[:48]),
        dg_rbs_plus60=mfe(SHARED_5PRIME + nt[:60]),
        # Coding-sequence-only equivalents, for the direct comparison.
        dg_cds_only30=r.mrna_dg_first30nt,
        dg_cds_only48=r.mrna_dg_first48nt,
        dg_cds_only60=r.mrna_dg_first60nt,
        # (B) distance from the published optima
        gravy_kd=r.gravy_kd,
        gravy_dist_from_1=abs(r.gravy_kd - 1.0),
        net_charge_ph7=r.net_charge_ph7,
        charge_excess_over_2=max(0.0, r.net_charge_ph7 - 2.0),
    ))
new = pd.DataFrame(rows)
new.to_csv(OUT / 'improved_features.csv', index=False)

print('=== (A) Does adding the real RBS context change the folding feature? ===')
for w in (30, 48, 60):
    a, b = new[f'dg_cds_only{w}'], new[f'dg_rbs_plus{w}']
    rho, _ = spearmanr(a, b)
    print(f'  {w:>2} nt window: CDS-only mean {a.mean():6.2f}  RBS-aware mean {b.mean():6.2f}  '
          f'rank corr between them = {rho:+.2f}')
print('  A low correlation means the RBS-aware feature is genuinely a different quantity,')
print('  not a shifted copy of the old one.')

data = (summary[summary.block.isin(MAIN)]
        .merge(new, on='peptide_id', validate='one_to_one')
        .merge(feat[['peptide_id']], on='peptide_id'))

TEST = ['dg_rbs_plus30', 'dg_rbs_plus48', 'dg_rbs_plus60',
        'dg_cds_only30', 'dg_cds_only48', 'dg_cds_only60',
        'gravy_dist_from_1', 'charge_excess_over_2']

out = []
for f in TEST:
    rhos, ns = [], []
    for b in MAIN:
        g = data[data.block == b]
        if g[f].nunique() < 3:
            rhos.append(np.nan); ns.append(len(g)); continue
        rhos.append(spearmanr(g[f], g['mean']).statistic); ns.append(len(g))
    finite = [r for r in rhos if np.isfinite(r)]
    z = np.arctanh(np.clip(finite, -0.999999, 0.999999))
    w = np.array([n - 3 for r, n in zip(rhos, ns) if np.isfinite(r)])
    comb = float(np.tanh(np.sum(w * z) / np.sum(w)))
    out.append(dict(feature=f, rho_blot1=rhos[0], rho_blot2=rhos[1], rho_blot3=rhos[2],
                    combined_rho=comb,
                    all_same_direction=all(r > 0 for r in finite) or all(r < 0 for r in finite)))
res = pd.DataFrame(out).sort_values('combined_rho', key=abs, ascending=False)
res.to_csv(OUT / 'improved_feature_associations.csv', index=False)

print('\n=== Associations with secretion, within blot (combined by meta-analysis) ===')
print(res.round(3).to_string(index=False))

# The step 4 permutation null for best-of-panel was 0.60 at the 95th percentile.
NULL_P95 = 0.5978
print(f'\nFor reference, the step 4 permutation null 95th percentile was {NULL_P95:.2f}.')
best = res.iloc[0]
print(f'Best here: {best.feature} at {best.combined_rho:+.2f} - '
      f'{"ABOVE" if abs(best.combined_rho) > NULL_P95 else "still below"} that threshold.')

print('\n=== (B) Does this library span the informative range? ===')
print(f'  GRAVY:  min {new.gravy_kd.min():.2f}  median {new.gravy_kd.median():.2f}  '
      f'max {new.gravy_kd.max():.2f}   (published optimum ~1.0)')
within = ((new.gravy_kd > 0.6) & (new.gravy_kd < 1.4)).sum()
print(f'  {within} of 32 peptides lie between GRAVY 0.6 and 1.4, i.e. clustered near the '
      f'published optimum.')
print(f'  Charge: min {new.net_charge_ph7.min():.2f}  median '
      f'{new.net_charge_ph7.median():.2f}  max {new.net_charge_ph7.max():.2f}   '
      f'(published optimum < +2)')
above2 = (new.net_charge_ph7 > 2).sum()
print(f'  {above2} of 32 peptides carry net charge above +2, i.e. above the published optimum.')

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
axes[0].scatter(new.dg_cds_only48, new.dg_rbs_plus48, s=40, color='#4c72b0')
axes[0].set_xlabel('CDS-only dG, 48 nt'); axes[0].set_ylabel('RBS-aware dG, 48 nt')
axes[0].set_title('Adding the real 5\' context\nchanges the feature')
axes[1].hist(new.gravy_kd, bins=14, color='#9bb7d4', edgecolor='white')
axes[1].axvline(1.0, color='#c44e52', lw=2, label='published optimum ~1.0')
axes[1].set_xlabel('GRAVY (Kyte-Doolittle)'); axes[1].set_ylabel('Peptides')
axes[1].set_title('Library clusters near the optimum'); axes[1].legend(fontsize=8)
axes[2].hist(new.net_charge_ph7, bins=14, color='#9bb7d4', edgecolor='white')
axes[2].axvline(2.0, color='#c44e52', lw=2, label='published optimum < +2')
axes[2].set_xlabel('Net charge at pH 7'); axes[2].set_ylabel('Peptides')
axes[2].set_title('Most peptides sit above it'); axes[2].legend(fontsize=8)
fig.suptitle('Literature-driven checks: restricted range as an explanation for the null result')
fig.tight_layout()
fig.savefig(OUT / 'improved_features.png', dpi=170)
plt.close(fig)

print(f'\nWrote outputs to {OUT}')
