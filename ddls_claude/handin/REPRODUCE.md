# Reproducing the analysis

## Input data is not included

The analysis reads `data/Information_for_Baris_corrected.xlsx`, the data owner's **unpublished**
experimental workbook. It is deliberately **not redistributed** in this package. To reproduce
the analysis you need that file, placed at `data/Information_for_Baris_corrected.xlsx` relative
to the repository root.

Everything else — all code, all generated outputs, and the interactive dashboard — is included.

## Requirements

Python 3.14 (developed on 3.14.6). Install:

```bash
pip install -r requirements.txt
```

The UniProt step additionally needs internet access. Every other step runs offline.

## Run everything

```bash
python run_all.py
```

This executes the scripts in dependency order and stops at the first failure. Expected runtime
is roughly 3–6 minutes, dominated by the permutation tests.

## Or run the steps individually

From the repository root, in this order:

| # | Script | Writes | Notes |
|---|---|---|---|
| 1 | `ouput/analysis/run_steps_2_8.py` | `ouput/analysis/` | Descriptive pass: replicate summaries, validation blot, other-protein categories |
| 2 | `ouput/analysis/features_step3.py` | `ouput/analysis/step3/` | 34 sequence descriptors, QC, segmentation stability |
| 3 | `ouput/analysis/associations_step4.py` | `ouput/analysis/step4/` | Within-blot associations; 5,000-permutation multiplicity test (~1 min) |
| 4 | `ouput/analysis/context_step5.py` | `ouput/analysis/step5/` | Reliability ceiling, validation blot, other-protein context |
| 5 | `ouput/analysis/modeling_step6.py` | `ouput/analysis/step6/` | Model cross-validation (~2 min) |
| 6 | `ddls_claude/analysis/sp_identity_and_cross_assay.py` | `ddls_claude/analysis/` | SP→gene mapping, cross-assay comparison |
| 7 | `ddls_claude/analysis/improved_features_step8.py` | `ddls_claude/analysis/` | RBS-aware mRNA folding features |
| 8 | `ddls_claude/analysis/rbs_hypothesis_test.py` | `ddls_claude/analysis/` | 20,000-permutation pre-specified test (~1 min) |
| 9 | `ddls_claude/analysis/uniprot_native_sp_check.py` | `ddls_claude/analysis/` | **Needs internet.** Queries UniProt REST |

Steps 2–5 depend on 1. Steps 7–8 depend on 2. Step 8 depends on 7.

## Determinism

Random seeds are fixed at `20261103` in the permutation and modelling scripts, and
`random_state=0` in the random forest. Re-running reproduces the reported figures exactly,
with one caveat: step 9 depends on live UniProt content, so an annotation update there could
change that table.

**A note on a defect found during final verification.** The step-6 outputs on disk had been
overwritten by a stale background process using 300 trees, while the committed script specifies
100. This was detected by re-running and comparing against the reports. The script was re-run
and all downstream artefacts regenerated. If you re-run step 5, confirm no other Python process
is writing to `ouput/analysis/step6/` at the same time.

## The dashboard

After re-running the analysis, refresh the dashboard's data and rebuild the shareable file:

```bash
python ddls_claude/app/build_data.py
python ddls_claude/app/build_standalone.py
```

Then either serve it:

```bash
python -m http.server 8765 --directory ddls_claude/app
```

…and open <http://localhost:8765>, or just open `ddls_claude/app/findings_standalone.html`
directly — it is one self-contained file needing no server and no internet.

## Layout

```
ouput/analysis/      analysis scripts and their generated CSV/PNG outputs
ouput/md/            analysis reports, feature definitions, owner questions
ddls_claude/analysis/  later analyses: cross-assay, RBS features, UniProt check
ddls_claude/md/      literature review, meeting walkthrough, prompt packs
ddls_claude/app/     the interactive dashboard
ddls_claude/handin/  this package: report, AI disclosure, transcripts
```

Note the folder `ouput` is spelled that way in the original project; it is kept for
compatibility with the existing scripts.
