# Who did what: Pi agent vs Claude

**Project:** Signal-peptide features and recombinant collagen secretion in *Bacillus subtilis*
**Author:** Baris Akar (bakar@dtu.dk) · **Date:** 4 November 2026

This project was carried out with two different AI agents at different stages. This document
separates their contributions so the course owners can see exactly what each produced.

Accompanying bundles:

| File | Contents |
|---|---|
| `pi-work.zip` | 41 files — everything authored by the Pi agent |
| `claude-work.zip` | 67 files — everything authored by Claude |

Together these cover every project file except four deliberate exclusions, listed in §6.

---

## 1. Summary

| | Pi agent | Claude |
|---|---|---|
| **Phase** | Project setup and first analysis pass | Second pass: feature engineering through delivery |
| **Framing docs** | `AGENTS.md`, `spec.md`, `data.md`, `literature.md`, `analysis_plan.md` | — |
| **Analysis scripts** | 3 (`run_steps_2_8`, `build_documented_features`, `exploratory_peptide_models`) | 8 |
| **Reports** | `analysis_steps_2_8_report.md`, `final_analysis_part1.md` | `final_analysis_part2.md`, `feature_definitions.md`, final `report.md` |
| **Modelling** | Ridge + LOO, per blot | 4 model families × 2 CV schemes + permutation nulls |
| **Deliverables** | — | Dashboard, slides, submission package |

**Both agents independently reached the same conclusion** — see §4, which is the most useful
part of this document for assessment purposes.

---

## 2. Pi agent — what it produced

### Project framing (before any analysis)

`AGENTS.md` and `spec.md` are **Pi's work and were never modified**. They are the backbone of
the project: `spec.md` separates owner-stated facts from UNKNOWN / TO VERIFY items, and
`AGENTS.md` encodes the mandatory safeguards — don't pool blots, don't analyse only top
performers, don't claim mechanism. Every constraint Claude later worked under came from these
two documents.

`data.md`, `literature.md`, `row_level_data_inventory.md` and `analysis_plan.md` complete the
setup. The numbered 10-step analysis plan in `analysis_plan.md` is Pi's, and the later work
follows its structure.

### First analysis pass

- `run_steps_2_8.py` — descriptive analysis: replicate summaries, rank concordance, validation
  blot comparison, other-protein categories, and a first set of simple sequence features.
- `build_documented_features.py` — an independent feature set with a documented data dictionary
  (`documented_feature_dictionary.csv`), including explicit statements of which positional
  windows are heuristics rather than verified regions.
- `exploratory_peptide_models.py` — ridge regression against a mean baseline, leave-one-peptide-out
  within each blot separately.

Reported in `analysis_steps_2_8_report.md` and `final_analysis_part1.md`.

### Session logs

`analysis-transcript-1.md` (commit session, 3 Nov) and `analysis-transcript-2.md` (status and
file-collection session, 4 Nov). Note these are **short** — they cover only the final two Pi
sessions, not the earlier analysis work.

---

## 3. Claude — what it produced

### Feature engineering and statistics

- `features_step3.py` — 34 documented descriptors; region segmentation with a **stability test**
  that demoted h/c-boundary features to sensitivity-only after showing the boundary was not
  reproducible; zero-variance features identified and excluded.
- `associations_step4.py` — within-blot associations, Fisher-z meta-analysis of per-blot effects,
  and the **5,000-permutation family-wise calibration** that produced the key negative result.
- `context_step5.py` — the **measurement reliability ceiling** (Spearman–Brown), which is what
  makes the null interpretable rather than merely underpowered.
- `modeling_step6.py` — four model families, leave-one-peptide-out *and* leave-one-blot-out, plus
  the in-sample / out-of-fold contrast.

### Later analyses

- `sp_identity_and_cross_assay.py` — recovered the SP→gene mapping from the thesis and compared
  five shared peptides against Fu et al.
- `improved_features_step8.py` and `rbs_hypothesis_test.py` — the RBS-aware mRNA folding feature
  and its pre-specified one-sided permutation test.
- `uniprot_native_sp_check.py` — compared all 32 peptides against their native UniProt sequences,
  which established that the A-S-A cleavage region was **engineered, not inherited**.

### Findings that originated in this phase

1. **The permutation calibration** — the best feature (ρ = 0.369) is weaker than the median
   result on shuffled data (0.441); family-wise p = 0.81.
2. **The reliability ceiling of 0.86** — proving the null is informative, not noise.
3. **The in-sample / out-of-fold gap** — random forest 0.964 vs −0.187.
4. **SP31** — amino-acid sequence begins `V`, its own nucleotide sequence begins `ATG`.
5. **The engineered A-S-A cleavage region** — 13 native motifs collapsed to 1; only 8 of 32
   peptides match their native sequence exactly.
6. **The RBS-aware mRNA lead** — ρ = +0.515, positive in all three blots, p = 0.0042.

### Deliverables

The interactive dashboard, the reveal.js slide deck, the final `report.md`, `AI_DISCLOSURE.md`,
`REPRODUCE.md`, and the submission package.

---

## 4. Independent convergence — the most useful check

The two agents built **separate feature sets and separate modelling pipelines** and reached the
same conclusion. Pi's ridge/LOO results (`exploratory_model_metrics_by_blot.csv`):

| Blot | n | Model | Spearman ρ | LOO R² |
|---|---:|---|---:|---:|
| Blot 1 | 8 | ridge α=10 | −0.667 | −1.131 |
| Blot 2 | 13 | ridge α=10 | +0.049 | −0.136 |
| Blot 3 | 11 | ridge α=10 | −0.118 | −0.391 |

Claude's results (`ouput/analysis/step6/model_cv_performance.csv`):

| Model | Leave-one-peptide-out | Leave-one-blot-out |
|---|---:|---:|
| Ridge (α=10) | −0.130 | −0.078 |
| Random forest | −0.187 | −0.146 |
| k-NN (k=5) | −0.119 | −0.070 |

**Every LOO R² is negative in Pi's run; every out-of-fold Spearman is negative in Claude's.**
Different feature definitions, different code, different validation designs, same answer: the
features do not predict held-out peptides.

This is not two runs of one pipeline. Pi used a compact six-feature panel with its own
positional heuristics; Claude used 34 descriptors with a stability-tested segmentation. The
agreement is therefore meaningful corroboration of the negative result.

---

## 5. Shared and overlapping files

| File | Status |
|---|---|
| `ouput/md/questions.md` | **Shared.** Pi authored questions 1–21; Claude appended 22–24 (SP31, the engineered A-S-A, and the RBS/5′UTR request). Included in both bundles. |
| `submissions/report.md` | Claude-authored, copied into `submissions/` by Pi. |
| `submissions/AGENTS.md`, `submissions/spec.md` | Pi-authored, copied unchanged. |
| `ouput/analysis/replicate_summary_by_peptide.csv` | Produced by Pi's `run_steps_2_8.py`; **consumed by every Claude script**. The single biggest hand-off between the two phases. |

---

## 6. How the classification was made

1. **Direct record.** Files created or edited during the Claude session are known exactly from
   that session's transcript, which is included in the submission.
2. **Everything else** pre-existed that session or was written by Pi afterwards.
3. **File timestamps corroborate** this split but were not treated as proof — a copy or a git
   operation can rewrite them.

Two caveats worth stating plainly:

- The Pi session logs cover only the final two sessions. Pi's earlier analysis work is evidenced
  by its output files and reports rather than by transcripts.
- `ouput/anlaysis/` (note the spelling) is an empty legacy directory and is in neither bundle.

### Deliberate exclusions

A coverage check confirmed that every project file falls into one bundle or the other, except:

| Excluded | Reason |
|---|---|
| `ouput/txt/ideas_extracted.txt` | Full text extraction of a **copyrighted published paper** (Fu et al. 2018). Not redistributed. |
| `ouput/txt/thesis_extracted.txt` | Full text extraction of the data owner's **unpublished thesis chapter**. Not redistributed. |
| `ddls_claude/app/findings_standalone.html` | Already shipped in `app.zip` in the main submission. |
| `submissions/report.md`, `AGENTS.md`, `spec.md` | Duplicate copies; the originals are in their authoring agent's bundle. |

Neither bundle contains the input workbook `data/Information_for_Baris_corrected.xlsx`, which
is the data owner's unpublished experimental data.

---

## 7. Suggested reading order for assessment

1. `pi-work.zip` → `ouput/md/spec.md` — the project framing and its explicit unknowns.
2. `pi-work.zip` → `ouput/md/analysis_plan.md` — the 10-step plan the work follows.
3. `claude-work.zip` → `ddls_claude/handin/package/report.md` — the final report.
4. `exploratory_model_metrics_by_blot.csv` vs `step6/model_cv_performance.csv` — the independent
   convergence in §4.
5. `claude-work.zip` → `ddls_claude/app/findings_standalone.html` — the interactive dashboard
   (single file, no server or internet needed).
