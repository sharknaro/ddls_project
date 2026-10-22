# Data inspection findings and proposed analysis plan

## Scope
This document initially recorded a descriptive inspection of `data/Information_for_Baris.xlsx` against `AGENTS.md`, `spec.md`, and the data-owner interview. Following the user's request, analysis-plan steps 2–8 have now been carried out as exploratory/descriptive analyses on `data/Information_for_Baris_corrected.xlsx`; details and outputs are documented in `ouput/analysis_steps_2_8_report.md` and `ouput/analysis/`. No model was fitted, and no cross-blot calibration was performed.

## OBSERVED IN DATA

### File and workbook structure

- **File:** `data/Information_for_Baris.xlsx`
- **Format:** Excel `.xlsx` workbook; three visible sheets, no hidden sheets observed.
- Used worksheet ranges:
  - `Information for feeding`: **36 × 4**
  - `Results`: **29 × 14**
  - `SP and other collagen proteins`: **18 × 8**
- Dimensions include headers, spacer rows, and blanks; they are not observation counts.
- No formulas or cell comments were observed in these sheets.

### `Information for feeding`

There are **32 distinct signal-peptide IDs** (`SP1`–`SP32`), each with an origin label, amino-acid sequence, and nucleotide sequence. There is also a single `Bacola110` protein entry.

| Entry type | Columns | Meaning visible from labels |
|---|---|---|
| Protein construct | Protein name, origin, AA Sequence, Nt Sequence | One `Bacola110` entry, origin listed as “Bovine collagen a1[I]” |
| Signal peptides | SP Name, SP origin, AA Sequence, Nt Sequence | 32 rows of named peptides |

- Signal-peptide amino-acid sequences are **21–42 residues** long; nucleotide sequences are **63–126 bases** long.
- For all 32 peptide rows, nucleotide length is three times amino-acid sequence length, and observed characters are consistent with standard amino-acid letters and A/C/G/T bases.
- The `Bacola110` entry has a 108-character amino-acid sequence and a 327-base nucleotide sequence. The nucleotide length is not exactly three times the AA length; the entry includes a terminal sequence not represented as amino acids. The workbook does not annotate sequence boundaries or the meaning of this difference.
- No duplicate peptide IDs are present in this sheet.
- **Units:** sequence lengths are counts of characters/residues/bases, not assay units. The workbook does not state a unit for the sequences.
- **Missingness:** the listed sequence and origin cells for these entries are populated; blank rows serve as separators.
- The spreadsheet labels nucleotide sequences “Nt Sequence”; whether every sequence is codon-optimized is not encoded in the cells.

### `Results`

The sheet contains four separate blocks of replicated numeric values arranged with peptide identifiers as columns and replicate labels as rows:

| Block | Peptides | Replicate rows | Numeric entries | Observed range |
|---|---:|---:|---:|---:|
| `Blot 1 ranked (Fold-changes of each replication)` | 8 | 3 | 24 | 0.153055111–3.159090481 |
| `Blot 2 ranked (Fold-changes of each replication)` | 13 | 3 | 39 | 0–6.230062842 |
| `Blot 3 ranked (Fold-changes of each replication)` | 11 | 3 | 33 | 0.000441299–3.417239713 |
| `Validation blot ranked (Fold-changes of each replication)` | 7 | 4 | 28 | 0.119086156–2.476547553 |

- The first three blocks contain **32 distinct peptides total**, with no peptide appearing in more than one of those blocks.
- All seven validation-blot peptides also appear in the first three blocks: `SP2`, `SP3`, `SP32`, `SP26`, `SP5`, `SP19`, `SP4`.
- All 32 measured IDs match IDs in `Information for feeding`.
- One value is exactly **0** (`SP9`, Blot 2, replicate 1); all other reported numeric values are positive. The workbook does not explain whether zero means a measured zero, below detection, or a coded value.
- Blank cells are primarily unused cells at the edges of blocks; Blot 1 and Blot 3 have 15 and 6 blank slots respectively in their rectangular numeric regions. No replicate value is blank for a peptide inside the populated block boundaries.
- Numeric values are stored as numbers. Replicate labels are text (`Repli. 1` etc.).
- **Units:** not specified. Titles call the values “Fold-changes,” but do not specify denominator, calculation, assay units, or whether values are per-replicate normalization.
- The block titles say “ranked,” while peptide order differs from a straightforward ordering of the displayed values. The meaning of “ranked” is not further explained.

### `SP and other collagen proteins`

The sheet includes a small categorical table plus sequences for seven protein constructs.

- Categorical table: **4 signal-tag rows × 7 protein columns**.
  - Row labels: `SP3`, `SP5`, `S19`, `SP26`
  - Protein columns: `Bacola225`, `Alpha1 with C propeptide`, `Alpha2 with C propeptide`, `Alpha1 w/o C propeptide`, `Alpha2 w/o C propeptide`, `Tropocollagen`, and `Procollagen (It is like Procollagen wIth N,C propeptides)`.
  - Values include `High`, `Medium`, `Low`, and `No`. In addition, one cell contains `Ηigh` with a Greek capital eta rather than Latin H; another contains `Np`.
  - `Alpha2 with C propeptide` is marked `No` for all four tags.
- Sequence table: protein names and AA/Nt sequences for the seven named proteins. AA sequence lengths range from **221 to 1,448** characters; nucleotide sequence lengths range from **666 to 4,347** bases.
- Protein sequence rows are populated, but the sheet does not identify assay conditions, replicate count, numeric measurements, category thresholds, or how the categorical labels were assigned.
- `S19` does **not** match a named peptide ID in the main sequence or result sheets; `SP19` does exist. Whether `S19` is a typo for `SP19` is **not verified**.
- No observations are explicitly labeled as experimental controls.

### Notable data-quality flags

- `Ηigh` (Greek eta) and `Np` are inconsistent with the other category values and require clarification before recoding.
- `S19` is an identifier mismatch relative to `SP19` in the other sheets.
- The zero for `SP9` is unexplained.
- The `Bacola110` AA/Nt length difference and sequence boundary are unannotated.
- The categorical table uses `No`; its meaning (e.g. not tested, no secretion, unavailable) is unknown. It must not be treated automatically as a secretion category.
- “Ranked” block titles and column order do not define an explicit ranking procedure.
- No raw band intensities, assay units, conditions, loading controls, or uncertainty summaries are provided in the workbook sheets inspected.

## STATED BY DATA OWNER

From the interview, distinct from what is directly encoded in the workbook:

- The project concerns recombinant collagen secretion in *Bacillus subtilis* using approximately 32 signal peptides.
- The owner described Western-blot densitometry and stated that values in the three main gels were divided by the mean intensity of their respective gel; values above one are above that gel mean, below one below it.
- The owner warned that values from the three separate gels cannot be directly compared.
- The owner described a fourth/validation gel containing peptides from different original gels and said it should be treated as a separate experiment; they suggested it might support a weighted or cross-gel ranking.
- The owner described four signal peptides tested with other proteins/different lengths as a possible limited check, not a good retraining set.
- The owner wants the full range of good and poor performers considered, is interested in correlations with peptide features, and would accept a negative result.
- The owner described an intended workbook structure with sequences, fold-change results, and validation/other-protein information, but the actual workbook layout differs in details (see below).

### Differences from the interview/specification

- The workbook does contain 32 peptide sequences and a results sheet, consistent with the broad description.
- The results sheet has four blocks, including a block titled “Validation blot,” which is consistent with the owner’s account. The seven validation peptides are explicitly identifiable.
- The other-protein sheet contains **four tag rows**, but the owner’s account said four peptides; the workbook’s `S19` label makes the exact identity unresolved.
- The workbook’s additional-protein table contains **categorical labels**, not replicate numeric “validation results” as described in the interview.
- The owner described a possible “three-sheet” workbook with a separate sheet for sequences, fold changes, and validation. In the actual file, sequence data and additional protein information are split differently: sequences are in the first sheet, while other-protein categories and protein sequences are in the third.
- The data owner’s stated within-gel mean normalization is **not independently verifiable from this workbook alone** because raw band intensities and normalization details are absent.
- The owner referred to a “fourth gel”; the workbook calls the block “Validation blot.” Treating these as the same event is consistent with the interview but not independently verified by metadata.

## UNKNOWN

These points cannot be established reliably from the workbook or interview alone:

- Exact meaning and calculation of the numeric “Fold-changes,” and whether they are already normalized values for each replicate.
- Whether zero is a true zero or a detection-limit/missing-value code.
- What `No` and `Np` mean; whether `Np` is a typo; whether `Ηigh` means `High`.
- Whether `S19` means `SP19`.
- Biological versus technical replicate structure, independence of replicate rows, experimental conditions, assay controls, band quantification and background correction.
- Whether higher fold-change corresponds directly to more absolute secreted collagen.
- Exact sequence boundaries/construct composition, particularly whether signal peptides or tags are included in any stored full protein sequences.
- Category definitions/thresholds for High/Medium/Low.
- Why results are described as “ranked,” despite the displayed ordering not being self-explanatory.
- Whether the listed nucleotide sequences are all codon-optimized, and what construct region they encode.
- Whether the four validation-gel replicates are directly comparable among themselves and how the owner intended any weighting/calibration.
- Whether the other-protein categorical ratings are experimental results from the same assay, predictions, or another source.

# Numbered analysis plan

Steps 2–8 below were performed descriptively/exploratorily; see `ouput/analysis_steps_2_8_report.md` for results and caveats. Steps 9–10 remain proposed. The corrected workbook was used, zero retained as numeric zero, and block-specific summaries were kept separate. Remaining assay/category ambiguities limit interpretation.

## 1. Resolve data dictionary, identifiers, and measurement provenance

1. **Calculate/check:** Create a row-level data inventory linking peptide IDs, sequences, result blocks, replicate rows, and third-sheet category rows. Verify `S19`, `Ηigh`, `Np`, zero, “ranked,” and sequence boundaries with the owner or source records.
2. **Why:** Prevents identifier errors and category misinterpretation from contaminating all downstream comparisons.
3. **Output:** Data dictionary, ID crosswalk, and explicit issue/decision log.
4. **Validation/control:** Reconcile 32 sequence IDs against all main result IDs (they match); ask owner to confirm anomalies and consult original assay records if available. Do not “fix” values silently.

## 2. Describe outcome distributions and replicate consistency within each blot

1. **Calculate:** For each peptide and blot, summarize replicate values (e.g. replicate-level points plus mean/median and spread), distributions, range, and within-peptide variability. Keep Blot 1, 2, 3 and validation separate.
2. **Why:** Shows what the response measurements represent and whether rankings are stable across replicates before relating them to sequence features.
3. **Output:** Faceted replicate dot plots by blot, per-peptide summary table, distribution plots, and replicate variability summaries.
4. **Validation/control:** Check summaries against the source cells and confirm values are numeric and mapped to the correct peptide and replicate; preserve zero as observed pending owner clarification. Do not treat replicates as independent peptide-level samples.

## 3. Assess cross-blot calibration only using the validation set, if justified

1. **Calculate:** Compare the seven shared peptides’ within-blot summaries from their original blot with their validation-blot summaries; evaluate rank consistency and any systematic shifts. Only test a calibration/weighting approach if the experimental design supports it and the owner confirms the intended interpretation.
2. **Why:** This addresses the owner’s concern that main-gel normalized values cannot be directly compared, while using the separate validation blot as a possible bridge.
3. **Output:** Paired plot of original-blot versus validation values for shared peptides, rank comparison, and an explicit calibration decision/report.
4. **Validation/control:** Ensure the pairs are correctly ID-matched, and report uncertainty with only seven shared peptides. Do not infer a general calibration from this small selected overlap or use the calibration data as independent validation after fitting to it.

## 4. Define a defensible primary secretion outcome and candidate grouping

1. **Calculate:** Based on owner-confirmed assay meaning, define per-peptide outcome summaries within each blot; optionally define exploratory within-blot high/medium/low categories only if a transparent rule is agreed.
2. **Why:** Gives a consistent target for the owner’s feature question without assuming common scale across gels or inventing categories.
3. **Output:** Outcome definition table and per-blot candidate ranking/category visualization.
4. **Validation/control:** Have the owner confirm the interpretation and category cutoffs; compare replicate-level plots to summarized groupings and test sensitivity to reasonable alternative summaries.

## 5. Describe available sequence data before feature engineering

1. **Calculate:** Report peptide sequence lengths, AA/nucleotide completeness, sequence identity/duplicates, and sequence-level summaries; map signal-peptide and protein fields only where boundaries are verified.
2. **Why:** Confirms that features requested by the owner can be calculated from the actual sequences and that sequences align to measured IDs.
3. **Output:** Sequence inventory and length/ID quality-control table.
4. **Validation/control:** Verify alphabet, lengths, translation/frame and boundaries with biological owner or provided records. Do not infer cleavage sites, signal peptide boundaries, or codon optimization solely from sequence appearance.

## 6. Explore a small, pre-specified set of interpretable features

1. **Calculate:** After methods are agreed, compute a limited feature set relevant to the owner: length, position-specific composition or motifs, chosen hydrophobicity measure, and selected nucleotide/mRNA initiation-region features only if region and biological assumptions are verified. Other features such as pI, folding energy, and predicted structure should be separately labeled exploratory and use documented tools/settings.
2. **Why:** Directly addresses whether candidate features relate to secretion while limiting overfitting on only 32 peptides.
3. **Output:** Feature table with definitions and calculation settings; feature-distribution plots.
4. **Validation/control:** Independently spot-check feature calculations against documented methods/software; test sequence inputs and boundary choices; record multiple comparisons and avoid choosing features based on outcome after the fact.

## 7. Test feature–outcome associations using all main candidates while preserving blot

1. **Calculate:** For pre-specified features, show their relationships with secretion outcome within original blots; estimate effect direction and uncertainty. Consider pooled/rank analyses only if a valid normalization strategy has been confirmed. Include all eligible candidates, not only top performers.
2. **Why:** Directly tests the owner’s association hypothesis while respecting gel boundaries and the selection-bias concern.
3. **Output:** Faceted scatter/dot plots or rank plots by blot, effect/uncertainty table, and a clear “association / no clear association / inconclusive” summary.
4. **Validation/control:** Sensitivity to outliers, replicate summaries, and alternative reasonable outcome definitions; control multiplicity or clearly label exploratory tests. Check consistency across blots rather than relying on a pooled correlation.

## 8. Treat other-protein data as a separate, descriptive context check

1. **Calculate:** Once `S19`, `No`, `Np`, and `Ηigh` are resolved, summarize the categorical pattern by peptide and protein construct. Only relate it to main-set results where peptide identity and category semantics are verified.
2. **Why:** Addresses owner interest in transfer across protein lengths while acknowledging different protein contexts.
3. **Output:** Peptide-by-protein category heatmap/table and a caveat on comparability.
4. **Validation/control:** Confirm category origin, meaning, and ID mapping with owner; do not treat the four rows as quantitative, independent validation without supporting provenance.

## 9. Decide whether prediction or candidate extrapolation is supportable

1. **Calculate:** Only if prior steps show a defensible, stable signal, evaluate a very limited model or exploratory candidate ranking using validation that respects blot/group structure; do not create new sequence designs as “predictions” absent a justified model.
2. **Why:** Addresses the optional prediction/design interest without overstating what 32 observations can support.
3. **Output:** If feasible, an explicitly exploratory model report with held-out performance and uncertainty; otherwise a documented conclusion that reliable prediction is not supported.
4. **Validation/control:** Prevent leakage between replicates of the same peptide and avoid using validation-blot observations both to calibrate and validate. Other-protein cases are not assumed to be an adequate external validation set.

## 10. Report conclusions and limitations

1. **Calculate:** No additional statistical calculation; synthesize verified measurements, associations, uncertainty, and unresolved assumptions.
2. **Why:** Delivers an answer that the owner can use without confusing association, prediction, and mechanism.
3. **Output:** Report with methods, data dictionary, plots/tables, limitations, and cautiously ranked candidates only if justified.
4. **Validation/control:** Trace every conclusion to workbook rows and analysis outputs; owner review of unresolved assay/label interpretations; explicitly distinguish confirmed facts from assumptions.

## Completion status: steps 9–10

Steps 9–10 were completed after the descriptive analyses in steps 2–8. No model or candidate extrapolation was fit because the available data do not provide a stable feature association or independent validation design. The integrated data-analysis part 1 report is `final_analysis_part1.md`; detailed results for steps 2–8 are in `../analysis_steps_2_8_report.md`, with reproducible outputs in `../analysis/`. Conclusions and follow-up data needs are summarized in the final report. The cautions below still apply.

# Two most likely misleading parts

1. **Cross-blot normalization/calibration.** The owner says the original blot values are normalized separately and not directly comparable, while the workbook lacks raw intensities and assay details. A calibration using just seven shared peptides could produce an apparently coherent common scale that is unstable or specific to those peptides. Treating it as validated would be especially risky.

2. **Interpreting “Results” and the other-protein categories as secretion outcomes.** The workbook does not define fold-change calculations, replicate independence, or category coding; `S19`, `Ηigh`, `Np`, and `No` are unresolved. If these are silently corrected or assigned meanings, any correlations or apparent protein-length transfer could be artifacts.
