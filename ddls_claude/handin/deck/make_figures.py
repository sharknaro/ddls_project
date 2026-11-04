#!/usr/bin/env python3
"""Render slide-grade figures for the PowerPoint deck.

Sized and typeset for projection: large fonts, no chart junk, light surface, and the
CVD-validated palette used throughout the project.
"""
from pathlib import Path
from matplotlib.ticker import FormatStrFormatter

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
ANA = ROOT / 'ouput' / 'analysis'
CLA = ROOT / 'ddls_claude' / 'analysis'
OUT = Path(__file__).resolve().parent / 'fig'
OUT.mkdir(parents=True, exist_ok=True)

INK, INK2, MUTED = '#16202a', '#52514e', '#8a8882'
GRID, AXIS, PAPER = '#e9e8e2', '#c3c2b7', '#ffffff'
S1, S2, S3, S4 = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
CB = {'Blot 1': S1, 'Blot 2': S2, 'Blot 3': S3}
MAIN = ['Blot 1', 'Blot 2', 'Blot 3']

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Calibri', 'Carlito', 'DejaVu Sans'],
    'font.size': 15, 'axes.labelsize': 15, 'axes.titlesize': 16,
    'xtick.labelsize': 13.5, 'ytick.labelsize': 13.5, 'legend.fontsize': 14,
    'text.color': INK, 'axes.labelcolor': INK2,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'figure.facecolor': PAPER, 'axes.facecolor': PAPER, 'savefig.facecolor': PAPER,
    'axes.edgecolor': AXIS, 'axes.linewidth': 1.1,
    'grid.color': GRID, 'grid.linewidth': 1.0,
    'axes.grid': True, 'axes.axisbelow': True,
    'savefig.dpi': 200, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.18,
})


def tidy(ax, xgrid=False):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(AXIS)
    ax.spines['bottom'].set_color(AXIS)
    ax.grid(axis='x' if xgrid else 'y')
    ax.set_axisbelow(True)


summary = pd.read_csv(ANA / 'replicate_summary_by_peptide.csv')
longdf = pd.read_csv(ANA / 'replicate_values_long.csv')
assoc = pd.read_csv(ANA / 'step4' / 'associations_robust_mean.csv')
perm = pd.read_csv(ANA / 'step4' / 'permutation_multiplicity_test.csv').iloc[0]
insample = pd.read_csv(ANA / 'step6' / 'in_sample_vs_out_of_fold.csv')
rbsrow = pd.read_csv(CLA / 'rbs_hypothesis_test.csv').iloc[0]
improved = pd.read_csv(CLA / 'improved_features.csv')
uni = pd.read_csv(CLA / 'uniprot_native_sp_comparison.csv')

LBL = {
    'h_core9_mean_kd': 'Hydrophobic core · mean hydropathy',
    'mrna_dg_first30nt': 'mRNA ΔG · first 30 nt',
    'c_prox6_frac_polar_STNQ': 'C-terminal 6 · polar fraction',
    'h_core9_frac_hydrophobic': 'Hydrophobic core · hydrophobic fraction',
    'frac_hydrophobic_AVILMFWY': 'Whole peptide · hydrophobic fraction',
    'aromaticity': 'Aromaticity', 'aa_length': 'Peptide length',
    'isoelectric_point': 'Isoelectric point', 'frac_leucine': 'Leucine fraction',
    'n_prox_net_charge_ph7': 'N-region · net charge (pH 7)',
}

# ---------------------------------------------------------------- 1. replicates
fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.0))
for ax, b in zip(axes, MAIN):
    rows = summary[summary.block == b].sort_values('mean')
    rep = longdf[longdf.block == b]
    pos = {p: i for i, p in enumerate(rows.peptide_id)}
    for _, r in rep.iterrows():
        ax.scatter(pos[r.peptide_id] + np.random.uniform(-.13, .13), r.value,
                   s=46, color=CB[b], alpha=.75, zorder=3,
                   edgecolors=PAPER, linewidths=.9)
    ax.scatter(range(len(rows)), rows['mean'], marker='_', s=620, color=INK,
               linewidths=3.0, zorder=4)
    ax.axhline(1, color=AXIS, ls='--', lw=1.5, zorder=1)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(rows.peptide_id, rotation=60, ha='right', fontsize=11.5)
    ax.set_title(f'{b}   ·   {len(rows)} peptides', fontsize=16, fontweight='600',
                 color=INK, loc='left', pad=11)
    ax.set_xlim(-.7, len(rows) - .3)
    tidy(ax)
axes[0].set_ylabel('fold-change')
fig.tight_layout(w_pad=2.4)
fig.savefig(OUT / 'replicates.png'); plt.close(fig)

# ---------------------------------------------------------------- 2. forest
rows = assoc.head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(14.5, 6.2))
y = np.arange(len(rows))
ax.axvspan(-perm.null_p95, perm.null_p95, color=GRID, zorder=0)
ax.axvline(0, color=AXIS, lw=1.4, zorder=1)
ax.hlines(y, rows.combined_lo95, rows.combined_hi95, color=AXIS, lw=2.0, zorder=2)
for off, col, c, lab in [(-.0, 'rho_blot1', S1, 'Blot 1'), (0, 'rho_blot2', S2, 'Blot 2'),
                         (0, 'rho_blot3', S3, 'Blot 3')]:
    ax.scatter(rows[col], y, s=78, color=c, zorder=3, edgecolors=PAPER,
               linewidths=1.2, label=lab)
ax.scatter(rows.combined_rho, y, marker='D', s=104, color=INK, zorder=4,
           edgecolors=PAPER, linewidths=1.2, label='Combined (95% CI)')
ax.set_yticks(y); ax.set_yticklabels([LBL.get(f, f) for f in rows.feature], fontsize=14)
ax.set_xlim(-1.02, 1.02); ax.set_xlabel('Spearman ρ with secretion — combined across blots')
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.01), ncol=4, frameon=False,
          fontsize=13, columnspacing=1.8, handletextpad=.5)
tidy(ax, xgrid=True); ax.grid(axis='y', visible=False)
fig.tight_layout(); fig.savefig(OUT / 'forest.png'); plt.close(fig)

# ---------------------------------------------------------------- 3. null
fig, ax = plt.subplots(figsize=(9.6, 5.6))
x = np.linspace(0, .9, 400)
sd = (perm.null_p95 - perm.null_median_max_abs_rho) / 1.645
d = np.exp(-.5 * ((x - perm.null_median_max_abs_rho) / sd) ** 2)
ax.fill_between(x, d, color=S1, alpha=.16)
ax.plot(x, d, color=S1, lw=2.8)
ax.axvline(perm.observed_max_abs_combined_rho, color=S2, lw=3.0)
ax.axvline(perm.null_median_max_abs_rho, color=S1, lw=3.0)
ax.annotate(f'observed\n{perm.observed_max_abs_combined_rho:.2f}',
            (perm.observed_max_abs_combined_rho, 1.04), ha='right', va='bottom',
            color=S2, fontsize=15, fontweight='600', xytext=(-8, 0),
            textcoords='offset points')
ax.annotate(f'chance\n{perm.null_median_max_abs_rho:.2f}',
            (perm.null_median_max_abs_rho, 1.04), ha='left', va='bottom',
            color=S1, fontsize=15, fontweight='600', xytext=(8, 0),
            textcoords='offset points')
ax.set_ylim(0, 1.34); ax.set_yticks([])
ax.set_xlabel('largest |ρ| found when the outcome is shuffled')
tidy(ax); ax.grid(False); ax.spines['left'].set_visible(False)
fig.tight_layout(); fig.savefig(OUT / 'null.png'); plt.close(fig)

# ---------------------------------------------------------------- 4. ceiling
fig, ax = plt.subplots(figsize=(9.6, 5.6))
obs = assoc.combined_rho.abs().dropna()
ax.hist(obs, bins=np.linspace(0, 1, 21), color=S1, alpha=.8, edgecolor=PAPER, linewidth=1.4)
ax.axvline(perm.observed_max_abs_combined_rho, color=S2, lw=3.0)
ax.axvline(.86, color=S3, lw=3.0)
ax.annotate('observed best\n0.37', (perm.observed_max_abs_combined_rho, 8.5), ha='right',
            color=S2, fontsize=14.5, fontweight='600', xytext=(-9, 0),
            textcoords='offset points')
ax.annotate('reliability ceiling\n0.86', (.86, 8.5), ha='right', color=S3,
            fontsize=14.5, fontweight='600', xytext=(-9, 0), textcoords='offset points')
ax.set_xlim(0, 1); ax.set_ylim(0, 10)
ax.set_xlabel('|combined ρ| for each of the 34 features')
ax.set_ylabel('features')
tidy(ax)
fig.tight_layout(); fig.savefig(OUT / 'ceiling.png'); plt.close(fig)

# ---------------------------------------------------------------- 5. models
rows = insample[~insample.model.str.startswith('Baseline')].iloc[::-1]
fig, ax = plt.subplots(figsize=(14.5, 5.4))
y = np.arange(len(rows)); h = .34
ax.barh(y + h / 2 + .02, rows.in_sample_spearman, height=h, color=S4,
        label='In-sample — fitted and scored on the same peptides', zorder=3)
ax.barh(y - h / 2 - .02, rows.honest_out_of_fold_spearman, height=h, color=S1,
        label='Out-of-fold — predicting held-out peptides', zorder=3)
for yy, v in zip(y + h / 2 + .02, rows.in_sample_spearman):
    ax.text(v + .02, yy, f'+{v:.2f}', va='center', fontsize=14, color=INK2, fontweight='600')
for yy, v in zip(y - h / 2 - .02, rows.honest_out_of_fold_spearman):
    ax.text(v - .02, yy, f'−{abs(v):.2f}', va='center', ha='right', fontsize=14,
            color=INK2, fontweight='600')
ax.axvline(0, color=AXIS, lw=1.4, zorder=2)
ax.set_yticks(y); ax.set_yticklabels(rows.model, fontsize=14.5)
ax.set_xlim(-1.02, 1.12)
ax.set_xlabel('Spearman ρ between predicted and actual ranking')
ax.legend(loc='upper left', bbox_to_anchor=(0, 1.16), ncol=2, frameon=False, fontsize=13.5)
tidy(ax, xgrid=True); ax.grid(axis='y', visible=False)
fig.tight_layout(); fig.savefig(OUT / 'models.png'); plt.close(fig)

# ---------------------------------------------------------------- 6. motif
counts = uni[uni.native_last3.notna()].native_last3.value_counts()
fig, ax = plt.subplots(figsize=(9.6, 6.4))
labels = list(counts.index) + ['', 'ASA']
vals = list(counts.values) + [0, 32]
cols = [S1 if m == 'ASA' else AXIS for m in counts.index] + [PAPER, S2]
y = np.arange(len(labels))[::-1]
ax.barh(y, vals, color=cols, height=.68, zorder=3)
for yy, v in zip(y[:-1], vals[:-1]):
    if v:
        ax.text(v + .5, yy, str(v), va='center', fontsize=13.5, color=INK2)
ax.text(32.8, y[-1], '32  —  supplied library', va='center', fontsize=14.5,
        color=S2, fontweight='700')
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=13.5)
ax.set_xlim(0, 40); ax.set_xlabel('peptides')
ax.set_title('native C-terminus, as annotated in UniProt',
             fontsize=14, color=MUTED, loc='left', pad=12)
tidy(ax, xgrid=True); ax.grid(axis='y', visible=False)
fig.tight_layout(); fig.savefig(OUT / 'motif.png'); plt.close(fig)

# ---------------------------------------------------------------- 7. RBS
sc = summary[summary.block.isin(MAIN)].merge(improved, on='peptide_id')
fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8))
for ax, b, i in zip(axes, MAIN, [1, 2, 3]):
    g = sc[sc.block == b]
    ax.scatter(g.dg_rbs_plus48, g['mean'], s=108, color=CB[b], alpha=.82,
               edgecolors=PAPER, linewidths=1.3, zorder=3)
    z = np.polyfit(g.dg_rbs_plus48, g['mean'], 1)
    xs = np.linspace(g.dg_rbs_plus48.min(), g.dg_rbs_plus48.max(), 20)
    ax.plot(xs, np.polyval(z, xs), color=CB[b], lw=2.0, alpha=.45, zorder=2)
    ax.set_title(f'{b}      ρ = +{rbsrow["rho_blot%d" % i]:.2f}', fontsize=16,
                 fontweight='600', color=INK, loc='left', pad=11)
    ax.set_xlabel('ΔG (kcal/mol)  →  less structured', fontsize=14)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    tidy(ax)
axes[0].set_ylabel('fold-change')
fig.tight_layout(w_pad=2.4)
fig.savefig(OUT / 'rbs.png'); plt.close(fig)

print('figures written to', OUT)
for p in sorted(OUT.glob('*.png')):
    print(f'  {p.name:16s} {p.stat().st_size/1024:6.0f} KB')
