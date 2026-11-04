# Step-by-step prompts to get the PI agent to the hand-in

Your agent's status summary already matches the analysis conclusions, so these prompts are
mostly about **verification and producing deliverables**, not redoing the science.

Give **one step at a time**. Wait for the named output file before moving on. If the agent
produces something thin, say so and ask it to redo that step rather than continuing.

---

## Part 0 — Before you start

Two things make or break this:

1. **Your agent must be working in the same project folder**, so it can read `ouput/analysis/`,
   `ddls_claude/` and `data/`. If it cannot, nothing below works.
2. **Paste the canonical facts block (Part A) into every prompt that writes prose.** A smaller
   model asked to "write the report" will invent plausible-looking numbers. Giving it the real
   ones removes the opportunity.

---

## Part A — Canonical facts block

Paste this verbatim into steps 2, 3 and 5. Every value was regenerated and verified on
2026-11-04 from the analysis outputs.

```
CANONICAL NUMBERS — use these exactly; do not recompute from memory, do not round differently,
do not invent any number that is not here. If something you need is missing, read it from the
CSV and say which file you read it from.

DATASET
- 32 signal peptides, one collagen construct, B. subtilis
- Three main blots, separately normalised to their own gel mean: n = 8, 13, 11
- Validation blot: 7 peptides, treated as a separate experiment
- Other-protein table: 4 peptides x 7 constructs, categorical, no stated thresholds

FEATURE SCREEN (34 robust descriptors, tested within each blot)
- Best observed combined |rho| = 0.3687  (feature: h_core9_mean_kd)
- Permutation null, 5,000 within-blot shuffles of the whole screen:
    median best-of-panel = 0.4406 ; 95th percentile = 0.5978
- Family-wise p-value = 0.8078
- Interpretation: the best real feature is WEAKER than the median result on shuffled data

MEASUREMENT RELIABILITY
- Mean inter-replicate Spearman per blot: 0.418 to 0.581
- Spearman-Brown reliability of a 3-replicate mean: 0.68 to 0.81
- Attenuation ceiling (max detectable correlation): 0.855, 0.898, 0.827 -> mean 0.86

MODELLING (scikit-learn; target = within-blot percentile rank; 34 features; peptide-level splits)
- Models: DummyRegressor(mean); Ridge(alpha=10); Ridge(alpha=100);
  RandomForestRegressor(n_estimators=100, min_samples_leaf=2, random_state=0);
  KNeighborsRegressor(n_neighbors=5). Scaling inside training folds via Pipeline.
- CV schemes: LeaveOneOut (32 folds) and LeaveOneGroupOut with blot as group (3 folds)
- Out-of-fold mean within-blot Spearman, leave-one-peptide-out:
    Ridge(10) -0.130 ; Ridge(100) -0.126 ; RandomForest -0.187 ; kNN -0.119
- Out-of-fold, leave-one-blot-out:
    Ridge(10) -0.078 ; Ridge(100) -0.044 ; RandomForest -0.146 ; kNN -0.070
- In-sample (fitted and scored on the same 32 peptides):
    Ridge(10) 0.729 ; Ridge(100) 0.673 ; RandomForest 0.964 ; kNN 0.289
- Every out-of-fold score is negative under both schemes
- Note: the leave-one-peptide-out baseline reads -1.00; this is an ARTEFACT of a constant
  predictor under LOO, not a result. The meaningful baseline is leave-one-blot-out = 0.00.

THE ONE POSITIVE LEAD (pre-specified from Fu et al. 2018)
- Feature: RBS-aware mRNA folding free energy, shared 5'UTR + first 48 nt of the SP CDS
- Per-blot Spearman: Blot 1 +0.262 ; Blot 2 +0.632 ; Blot 3 +0.491
- Combined rho = +0.5145 ; positive in all three blots
- One-sided permutation p (20,000 shuffles): 0.0042 as a single pre-specified hypothesis;
  0.0118 corrected for the family of three window sizes (30/48/60 nt)
- Leave-one-peptide-out range +0.466 to +0.594, zero sign flips
- Not a GC or length proxy: GC alone gives -0.02, length alone +0.25
- MANDATORY CAVEAT: a coding-sequence-only version of this feature family was already in the
  34-feature exploratory screen, so this is a refinement of an examined family, NOT clean
  out-of-sample confirmation. The true transcription start site is unknown, so the window is
  approximate. No mechanism is established.

SEQUENCE QC / LIBRARY DESIGN
- SP31: listed amino-acid sequence starts V, its own nucleotide sequence starts ATG (= M);
  residues 2-30 agree. Only AA/NT disagreement in the sheet. NOT corrected; owner must confirm.
- All 32 supplied peptides end A-S-A
- Native UniProt C-termini span 13 distinct motifs (ASA 12, AHA 3, AKA 3, AEA 2, ADA 2,
  and one each of AQA, AGA, ANA, VQA, AYA, AFA, VFA, LAG)
- Only 8 of 32 supplied peptides match their native signal peptide exactly
- 18 of 30 annotated peptides differ from native at the C-terminus
- Conclusion: the cleavage region was ENGINEERED/standardised, not inherited
- Consequence: the A-x-A motif Fu et al. associate with good performers is a design CONSTANT
  here, so it cannot explain any difference between these peptides

CANDIDATE-LEVEL RESULTS (within their own blots only; there is no cross-blot ranking)
- SP5 (Blot 1, CV 0.14) and SP26 (Blot 3, CV 0.21): high AND reproducible
- SP4 leads Blot 1 by mean but falls to 5th by median; it is also the peptide with the
  recurring secondary band reported in the thesis
- SP23 moves 3rd -> 9th between mean and median; replicates approx 0.00, 0.07, 3.42
- 8 of 32 peptides move >= 2 ranks depending on the summary used
- 6 peptides have CV > 1: SP21, SP9, SP23, SP30, SP31, SP25
- SP9 recorded zero retained as numeric zero; owner's tentative reading is "no secretion"

LITERATURE CONTEXT
- Fu et al. 2018 analysed 16 peptides (their 15 best + wild-type), reported NO correlation
  coefficient and NO p-value anywhere, and found no correlation for SignalP D-score or pI.
  Their sequence logos use selected positives with no negative set. They conclude in-silico
  prediction of the optimal signal peptide is not currently feasible.
- Grasso et al. 2023 (ACS Synth Biol 12:390) needed ~4,400 informative peptides to fit their
  random forest; their data are on Zenodo under CC BY.
- Five of these 32 peptides overlap Fu et al.'s top 15. Rank agreement with collagen secretion
  is rho = -0.20 (n=5), but the sequences are NOT identical because of the C-terminal
  modification, so this is suggestive only.
```

---

## Part B — The six steps

### Step 1 — Sync, re-run, and reconcile

> Before producing anything, get the project into a verified state.
>
> 1. Read every markdown file in `ouput/md/` and `ddls_claude/md/`, including the most recent
>    meeting document, and list anything in them that is not yet reflected in your current
>    understanding of the project.
> 2. Re-run every analysis script in order and confirm it completes:
>    `ouput/analysis/run_steps_2_8.py`, `features_step3.py`, `associations_step4.py`,
>    `context_step5.py`, `modeling_step6.py`, then
>    `ddls_claude/analysis/sp_identity_and_cross_assay.py`, `improved_features_step8.py`,
>    `rbs_hypothesis_test.py`, `uniprot_native_sp_check.py`.
> 3. After re-running, check that the regenerated CSVs still match the figures quoted in the
>    markdown reports and in `ddls_claude/app/data.js`. Report ANY discrepancy with the file
>    name and both values. Do not quietly fix a number — tell me about it.
> 4. Produce `ddls_claude/md/verification_log.md`: what you ran, what matched, what did not,
>    and any script that failed.
>
> Note: `uniprot_native_sp_check.py` needs internet access. If it cannot reach UniProt, say so
> rather than fabricating the comparison.

**Why this step:** script-versus-output drift is a real failure mode — it already happened once
in this project and was only caught by re-running. A grader may re-run your scripts.

---

### Step 2 — The written report

> Write the main project report to `ddls_claude/md/FINAL_REPORT.md`.
>
> [PASTE THE CANONICAL FACTS BLOCK HERE]
>
> Structure:
> 1. **Summary** (<= 400 words) — the question, what was done, the answer. State plainly that the
>    headline is a negative result with one qualified positive lead.
> 2. **Background and question** — recombinant collagen secretion in *B. subtilis*; the data
>    owner's actual question; why it matters.
> 3. **Data** — the workbook, the three separately normalised blots, the validation blot, the
>    other-protein table, and the known unknowns.
> 4. **Methods** — sequence QC, feature derivation with software and versions, the within-blot
>    association design, the permutation calibration, the reliability estimate, and the
>    modelling with its cross-validation and leakage controls. Name scales, software and
>    parameters.
> 5. **Results** — in this order: QC findings; outcome description and candidate stability;
>    the feature screen and its permutation calibration; the reliability ceiling; the modelling
>    result including the in-sample versus out-of-fold contrast; the sequence/UniProt finding;
>    the one positive lead.
> 6. **Discussion — why no predictor was obtained**, as four ordered reasons: (a) no signal to
>    learn; (b) effective n is 8/13/11 with 34 features; (c) it is not a noise problem, because
>    the reliability ceiling is 0.86; (d) the library design suppresses variation.
> 7. **Limitations.**
> 8. **Conclusions and recommended next steps.**
> 9. **Reproducibility** — scripts, inputs, outputs, seeds, dependencies.
> 10. **AI use statement** and **References.**
>
> Rules: every number must come from the block above or from a named CSV. Distinguish what the
> data owner stated, what the files show, and what was inferred. Never present in-sample fit as
> performance. Describe any proposed sequence as a hypothesis for experimental testing. Do not
> claim mechanism. Keep the mandatory caveat on the positive lead.

Then, as a follow-up in the same step:

> Now convert `FINAL_REPORT.md` to PDF, keeping the tables readable. If no converter is
> available, say so and leave the markdown — do not produce a degraded version silently.

---

### Step 3 — The runnable code package

> Prepare the code deliverable so someone else can reproduce the analysis from scratch.
>
> 1. Write `ddls_claude/REPRODUCE.md`: prerequisites, exact install commands, the scripts to run
>    in order, expected runtime, and what each one writes. Note that the UniProt step needs
>    internet and the modelling step takes a few minutes.
> 2. Write `ddls_claude/requirements.txt` with pinned versions actually installed here
>    (pandas, numpy, scipy, scikit-learn, matplotlib, seaborn, openpyxl, biopython, ViennaRNA).
>    Get the versions by running `pip freeze`, not from memory.
> 3. Write `ddls_claude/run_all.py` that executes every analysis script in dependency order,
>    stops on the first failure, and prints a clear per-step status.
> 4. Confirm `ddls_claude/app/` runs: `python -m http.server 8765 --directory ddls_claude/app`,
>    and that `findings_standalone.html` opens with no server.
> 5. Create the zip for upload at `ddls_claude/handin/code_and_app.zip` containing the analysis
>    scripts, the app folder, `REPRODUCE.md`, `requirements.txt` and `run_all.py`.
>    **Do not include anything from `data/`** — that is the owner's unpublished data. State in
>    `REPRODUCE.md` that the input workbook is not redistributed and must be supplied.
>
> Report the zip's size and file count.

---

### Step 4 — Transcripts and AI disclosure

> Assemble the transparency deliverable in `ddls_claude/handin/transcripts/`.
>
> 1. Copy the two data-owner interview transcripts from `data/` into that folder.
> 2. Collect the AI session transcripts I will place in that folder, and list them.
> 3. Write `ddls_claude/handin/AI_DISCLOSURE.md` covering: which AI tools and models were used;
>    what each was used for (analysis planning, code generation, literature screening, report
>    drafting, dashboard build); what I verified myself; what the AI did NOT do — it did not
>    generate data, did not alter measurements, and did not correct the SP31 or SP9 anomalies;
>    and how AI-produced claims were checked, namely by re-running scripts and tracing every
>    number to a CSV.
>
> Be specific and factual. Do not overstate or understate the AI's role.

---

### Step 5 — Presentation slides

> Produce a slide deck at `ddls_claude/handin/presentation.pptx`, about 12 slides.
>
> [PASTE THE CANONICAL FACTS BLOCK HERE]
>
> Suggested arc, one idea per slide:
> 1. Title — question, host, construct, your name and affiliation
> 2. The question and why it matters
> 3. The data: 32 peptides, three separately normalised blots, n = 8/13/11
> 4. Method and the four safeguards (no pooling; replicates collapsed; all candidates; peptide-level splits)
> 5. What was measured — the faceted replicate figure
> 6. Candidate stability — mean versus median ranking
> 7. The feature screen — the forest figure
> 8. The decisive test — observed 0.37 against a chance median of 0.44
> 9. Why the null is credible — the 0.86 reliability ceiling
> 10. Can we model? — in-sample 0.96 against out-of-fold −0.19
> 11. Why it did not work — the four ordered reasons
> 12. The one lead, with its caveats, and what is needed next
>
> Reuse the figures from `ouput/analysis/` and `ddls_claude/analysis/` rather than redrawing.
> Keep text short — these are speaking slides, not a document.

If your agent cannot write .pptx, ask it for the slide content as markdown and build the deck
yourself; do not accept a silently degraded output.

---

### Step 6 — Final cross-check

> Final QC before submission. Do not write anything new; verify.
>
> 1. Extract every numeric claim from `FINAL_REPORT.md`, the slides and `AI_DISCLOSURE.md`, and
>    confirm each against the CSV it comes from. Report any that do not match.
> 2. Confirm the report, the slides and the dashboard tell the same story with the same numbers.
> 3. Confirm the zip contains no files from `data/`.
> 4. Confirm the mandatory caveat on the positive lead appears in the report AND the slides.
> 5. Confirm no deliverable presents in-sample fit as predictive performance.
> 6. Produce `ddls_claude/handin/CHECKLIST.md` with one line per hand-in item, its file path,
>    and pass/fail.

---

## Part C — Mapping to the four upload slots

| Upload slot | File | Produced by |
|---|---|---|
| 1. Written report | `ddls_claude/md/FINAL_REPORT.md` (+ PDF) | Step 2 |
| 2. Runnable app or code | `ddls_claude/handin/code_and_app.zip` | Step 3 |
| 3. Interview + analysis transcripts | `ddls_claude/handin/transcripts/` + `AI_DISCLOSURE.md` | Step 4 |
| 4. Presentation slides | `ddls_claude/handin/presentation.pptx` | Step 5 |
| Anything else (optional) | `findings_standalone.html` — the interactive dashboard | already built |

The standalone dashboard is worth uploading in the optional slot. It is the thing that most
clearly distinguishes this submission, and it needs no server.

---

## Part D — Two cautions

**On the negative result.** Make sure the report frames it as a negative result with a
quantified bound, not as a failed project. The reliability ceiling is what turns "we found
nothing" into "we established that nothing of moderate size is there". If your agent writes an
apologetic report, send it back.

**On the positive lead.** The caveat that it is not clean out-of-sample confirmation must
survive into every deliverable. It is the first thing a summarising agent drops, and the first
thing a careful examiner would catch.
