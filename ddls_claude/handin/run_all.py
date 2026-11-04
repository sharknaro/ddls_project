#!/usr/bin/env python3
"""Run every analysis script in dependency order, stopping at the first failure.

Run from the repository root:  python ddls_claude/handin/run_all.py
Requires data/Information_for_Baris_corrected.xlsx (not redistributed; see REPRODUCE.md).
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STEPS = [
    ('ouput/analysis/run_steps_2_8.py', 'descriptive pass', False),
    ('ouput/analysis/features_step3.py', 'sequence QC and 34 features', False),
    ('ouput/analysis/associations_step4.py', 'within-blot associations + permutation', False),
    ('ouput/analysis/context_step5.py', 'reliability, validation blot, other proteins', False),
    ('ouput/analysis/modeling_step6.py', 'model cross-validation', False),
    ('ddls_claude/analysis/sp_identity_and_cross_assay.py', 'SP identity and cross-assay', False),
    ('ddls_claude/analysis/improved_features_step8.py', 'RBS-aware mRNA features', False),
    ('ddls_claude/analysis/rbs_hypothesis_test.py', 'pre-specified RBS hypothesis test', False),
    ('ddls_claude/analysis/uniprot_native_sp_check.py', 'UniProt native comparison', True),
]

workbook = ROOT / 'data' / 'Information_for_Baris_corrected.xlsx'
if not workbook.exists():
    sys.exit(f'Input workbook not found at {workbook}\n'
             'It is the data owner\'s unpublished data and is not redistributed. See REPRODUCE.md.')

print(f'Repository root: {ROOT}\n')
failures = []
for i, (script, label, needs_net) in enumerate(STEPS, 1):
    net = '  (needs internet)' if needs_net else ''
    print(f'[{i}/{len(STEPS)}] {label}{net}\n        {script}', flush=True)
    t = time.time()
    r = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT)
    dt = time.time() - t
    if r.returncode == 0:
        print(f'        ok  ({dt:.0f}s)\n', flush=True)
    elif needs_net:
        print(f'        FAILED ({dt:.0f}s) — continuing, since this step needs internet\n', flush=True)
        failures.append(script)
    else:
        sys.exit(f'        FAILED ({dt:.0f}s) — stopping. Fix this before continuing.')

if failures:
    print(f'Completed with {len(failures)} non-fatal failure(s): {", ".join(failures)}')
else:
    print('All steps completed.')
print('\nTo refresh the dashboard:\n'
      '  python ddls_claude/app/build_data.py\n'
      '  python ddls_claude/app/build_standalone.py')
