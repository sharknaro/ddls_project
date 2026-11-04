#!/usr/bin/env python3
"""Split the project into Pi-authored and Claude-authored bundles, with a provenance guide.

Classification basis, in order of reliability:
  1. Direct record — files created or edited during the Claude session are known exactly.
  2. Everything else pre-existed that session or was written by Pi afterwards.
File timestamps corroborate but are not treated as proof.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'ddls_claude' / 'handin' / 'provenance'
OUT.mkdir(parents=True, exist_ok=True)

PI = [
    # Project framing and specification (authored before the Claude session)
    'ouput/md/AGENTS.md', 'ouput/md/spec.md', 'ouput/md/data.md', 'ouput/md/literature.md',
    'ouput/md/analysis_plan.md', 'ouput/md/row_level_data_inventory.md',
    'ouput/md/analysis_steps_2_8_report.md', 'ouput/md/final_analysis_part1.md',
    'ouput/csv/row_level_data_inventory.csv',
    # Pi's own analysis code
    'ouput/analysis/run_steps_2_8.py',
    'ouput/analysis/build_documented_features.py',
    'ouput/analysis/exploratory_peptide_models.py',
    # Pi's analysis outputs
    'ouput/analysis/replicate_summary_by_peptide.csv', 'ouput/analysis/replicate_values_long.csv',
    'ouput/analysis/replicate_rank_concordance.csv', 'ouput/analysis/replicate_values_by_blot.png',
    'ouput/analysis/validation_paired_shared_peptides.csv',
    'ouput/analysis/validation_comparison_stats.csv',
    'ouput/analysis/validation_shared_peptides.png',
    'ouput/analysis/sequence_qc_and_features.csv',
    'ouput/analysis/sequence_descriptors_exploratory.csv',
    'ouput/analysis/within_blot_feature_associations.csv',
    'ouput/analysis/within_blot_feature_associations.png',
    'ouput/analysis/other_protein_categories_long.csv',
    'ouput/analysis/other_protein_categories_matrix.csv',
    'ouput/analysis/other_protein_category_counts.csv',
    'ouput/analysis/other_protein_categories_heatmap.png',
    'ouput/analysis/documented_feature_dictionary.csv',
    'ouput/analysis/documented_sequence_features.csv',
    'ouput/analysis/exploratory_model_metrics_by_blot.csv',
    'ouput/analysis/exploratory_model_loo_predictions.csv',
    'ouput/analysis/README.md',
    'ouput/analysis/documented_sequence_features_README.md',
    'ouput/analysis/exploratory_peptide_models_README.md',
    # Pi working notes. The two PDF text extractions (ideas_extracted.txt,
    # thesis_extracted.txt) are deliberately EXCLUDED: one is a copyrighted
    # published paper, the other the data owner's unpublished thesis chapter.
    'ouput/txt/cat_rows.txt', 'ouput/txt/changed_cells.txt',
    'ouput/txt/ddls_project_md_prompt.txt', 'ouput/txt/ddls_project_pi_check_prompt.txt',
    # Pi session logs
    'submissions/analysis-transcript-1.md', 'submissions/analysis-transcript-2.md',
]

CLAUDE_FILES = [
    'ouput/analysis/features_step3.py', 'ouput/analysis/associations_step4.py',
    'ouput/analysis/context_step5.py', 'ouput/analysis/modeling_step6.py',
    'ouput/md/feature_definitions.md', 'ouput/md/final_analysis_part2.md',
    'ouput/md/owner_message_draft.md',
]
CLAUDE_DIRS = [
    'ouput/analysis/step3', 'ouput/analysis/step4', 'ouput/analysis/step5',
    'ouput/analysis/step6', 'ddls_claude/analysis', 'ddls_claude/app',
    'ddls_claude/md', 'ddls_claude/handin/package',
]
SHARED = ['ouput/md/questions.md']


def add(z, rel, arc=None):
    p = ROOT / rel
    if not p.exists():
        print(f'  skip (missing): {rel}')
        return 0
    z.write(p, arc or rel)
    return 1


def bundle(name, files, dirs=()):
    path = OUT / name
    n = 0
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            n += add(z, f)
        for d in dirs:
            for p in sorted((ROOT / d).rglob('*')):
                if p.is_dir() or '__pycache__' in p.parts or p.suffix == '.pyc':
                    continue
                if p.name in ('findings_standalone.html',):   # already in app.zip
                    continue
                z.write(p, str(p.relative_to(ROOT)))
                n += 1
    print(f'{name}: {n} files, {path.stat().st_size/1024:.0f} KB')
    return n


print('Building pi-work.zip …')
n_pi = bundle('pi-work.zip', PI + SHARED)
print('Building claude-work.zip …')
n_cl = bundle('claude-work.zip', CLAUDE_FILES + SHARED, CLAUDE_DIRS)
print(f'\nTotal: {n_pi} Pi files, {n_cl} Claude files')
