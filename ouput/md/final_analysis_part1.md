# Data analysis part 1: final results (analysis-plan steps 2–10)

**Analysis dataset:** `data/Information_for_Baris_corrected.xlsx`. The deliverables below cover descriptive outcome review, sequence QC, limited within-blot feature exploration, context categories, and the decision about prediction feasibility. This is not a causal analysis or a validated prediction study.

## Executive conclusion

The workbook supports descriptive rankings **within** Blot 1, Blot 2, and Blot 3 and a separate descriptive comparison of seven shared peptides in the validation blot. Replicate rank agreement varies, the shared-peptide validation comparison is imperfect, and the four simple sequence features examined do not show a consistent relationship with relative outcome across the three original blots. Third-sheet categories are uncalibrated labels for four tags across different constructs. Accordingly, **the dataset can support a carefully scoped exploratory machine-learning exercise to predict held-out peptides within the observed data, but not a claim of reliable generalization or a validated new-sequence design rule**. The earlier analysis did not fit a model. Cross-blot calibration was not attempted.

This is a “no clear association / inconclusive” result for the limited exploratory features tested, not evidence that no biological relationship exists. The small candidate counts, assay uncertainties, and missing feature-boundary/provenance information limit inference.

## Data decisions carried forward

- In meeting 2, the owner confirmed that third-sheet `S19` refers to `SP19`, `Np` was intended as `No`, and `No` means the product was not produced (not missing or untested). These remain categorical labels, not numeric zero. The corrected workbook uses `SP19` and `No`; meeting 2 does not independently clarify the `Ηigh` to `High` transcription correction.
- The owner described SP9/Blot 2/replicate 1's zero as likely indicating no secretion, while also saying its origin is uncertain. The recorded zero is retained; it is not independently verified as a measured zero or detection-limit code.
- The owner clarified that peptides were arranged left-to-right by ascending **mean of replicate values**, mainly for presentation aesthetics. Results are summarized by arithmetic mean within each block, with medians and spread included. Main blot values are not pooled; validation is separate.
- The owner described the replicates as biological (and “in a way, both”); the exact experimental unit and independence remain unspecified.

## Steps 2–8: findings

### Outcome and replicate behavior

There are 32 main peptides with 3 replicate values each and 7 validation peptides with 4 each. Per-block mean leaders (lowest candidates in parentheses) are SP4 (SP8) in Blot 1, SP19 (SP9) in Blot 2, SP26 (SP25) in Blot 3, and SP4 (SP2) in validation. These are local ranks only. Replicate-to-replicate Spearman rank concordance ranges from 0.262–0.595, 0.571–0.593, 0.145–0.682, and −0.071–0.750 for Blots 1, 2, 3, and validation respectively, indicating uneven replicate rank stability.

The seven shared peptides have imperfect original-to-validation correspondence (mean-based Spearman ρ=0.679, n=7; rank correspondence ρ=0.692). Six validation means are lower than their main-blot means, but the observations span three original blots and a separate experiment. This is not sufficient to estimate a general conversion/calibration; none was fit.

### Sequence QC and feature exploration

All 32 AA sequences use standard amino-acid letters; all Nt sequences use A/C/G/T. There are no exact duplicate AA or Nt strings. Nt length is three times AA length and translation matches the listed AA sequence for all 32. This checks internal consistency only—not sequence provenance, codon optimization, or construct boundaries.

Exploratory features were defined over the full listed sequence: AA length; fraction of `AVILMFWY` residues; `(K+R-D-E)/length` as a simple charge proxy; and first-nine-nucleotide GC fraction (especially exploratory because the initiation region is not verified). Spearman correlations were modest/variable and did not reproduce direction consistently across blots. The largest trend was positive length in Blot 3 (ρ=0.560, n=11, nominal p=0.073), but length trends were near zero in Blots 1 and 2. No clear, consistent feature–outcome relationship emerged. These small-sample p-values are unadjusted and not confirmatory.

Additional transparent descriptors were calculated without using outcomes: N-terminal-five-residue K/R count, a heuristic internal segment (positions 5 through length−3) hydrophobic fraction, simple residue counts, and a C-terminal AXA-like pattern. The heuristic internal-region hydrophobic fraction ranges from 0.414 to 0.765 (mean 0.597); every listed sequence has an A-x-A-like pattern over its final three residues. This motif therefore does not distinguish candidates in this set. These summaries are descriptive and were not used to fit a model; the positional convention is not a verified signal-peptide domain boundary. Full values: `ouput/analysis/sequence_descriptors_exploratory.csv`.

### Other-protein categorical context

The third sheet has four peptide labels (SP3, SP5, SP19, SP26) and seven protein constructs, with `High`, `Medium`, `Low`, `No` strings only. Thresholds, assay provenance, category meaning, and replicate details are undocumented. These data remain descriptive and cannot serve as a quantitative endpoint, retraining dataset, or independent validation set.

Full tables/figures are in `ouput/analysis/`; the methods and more detailed step 2–8 narrative are in `ouput/analysis_steps_2_8_report.md`.

## Inserted step 6a: machine-learning feasibility and sequence-guided design

The dataset has enough rows to **run** a small, exploratory model, but not enough to establish a reliable, generalizable secretion predictor. A defensible first analysis would use one summarized outcome per peptide (not replicate rows), keep the three original blots separate or explicitly account for block, and use a very small predeclared feature set. Validation must split at peptide level; any score would be highly uncertain with the resulting small held-out sets. Within-blot ranks are not a common target across gels, and pooling normalized values requires an assumption that has not been verified. Thus a model can test whether simple descriptors carry some within-dataset signal, while performance estimates remain exploratory and should be compared with simple baselines and uncertainty.

**Decision:** A limited peptide-level exploratory model is feasible and may be useful to test, but the prior work did not fit one. There is no basis yet to claim reliable prediction or optimize novel sequences. The seven shared validation peptides and four selected peptides in categorical other-protein data do not provide sufficiently sized independent validation. Any reported result should show per-blot or carefully justified block-aware results, use peptide-level splits/resampling, and make clear that this is a small-sample exploratory exercise. Future reliable design guidance needs a larger prospective screen and a genuinely held-out peptide set or new experimental batch.

## Inserted step 6b: AlphaFold-assisted structural visualization

No AlphaFold structure was generated. The inputs are short signal peptides (21–42 aa), which function in a membrane/translocon context and are cleaved during secretion; an isolated peptide prediction would not model that environment or process. A predicted conformation would not be a measurement of secretion, and confidence scores would not validate a mechanism. No structural images or structure–outcome correlations are presented.

If visualization is later pursued, it should be explicitly illustrative, document the tool/version, input boundaries, templates/MSA/settings and confidence, and not be interpreted as evidence that folding explains secretion. Signal-peptide-specific or membrane-context analyses may be more relevant but remain hypotheses unless independently tested.

## Step 9: prediction and extrapolation decision

A reliable predictive model is **not established** by this dataset. To assess whether the documented feature families add exploratory value, a low-complexity per-blot leave-one-peptide-out Ridge model was run against a training-mean baseline, using one replicate-mean outcome per peptide. Replicate rows were never split and no cross-blot outcome pooling occurred.

The six-feature compact model had Ridge MAE of 0.586, 0.722, and 0.472 for Blots 1–3 (baseline 0.426, 0.761, 0.496). It slightly improved MAE in Blots 2–3 but worsened it in Blot 1; ranking correlations were poor (−0.667, 0.049, −0.118) and LOO R² was negative in all three blots. This does not demonstrate stable predictive signal. Full methods and model results are in `ouput/analysis/exploratory_peptide_models_README.md`.

A broader association screen of 34 robust, nonconstant features likewise found no feature surviving its within-blot maximum-statistic multiplicity test (best family-wise p≈0.81). The feature most consistently directionally associated was the 9-residue maximal-hydropathy core score (negative Spearman direction in all three blots; combined rho≈−0.37), but its uncertainty includes zero and multiplicity-adjusted evidence is weak. First-30-nt MFE had mixed direction and did not replicate consistently. Detailed results are in `ouput/analysis/step4/`.

Only 32 unique candidates are available, divided among three separately normalized blots; replicate stability is uneven, and no independent sufficiently sized holdout remains. The seven shared validation peptides are too few for general calibration, and the other-protein categories are selected and nonquantitative. Thus the model demonstrates that fitting is feasible, not reliable prediction, causal inference, or transfer to novel designs. Within-blot means remain **descriptive local rankings** only; do not treat model LOO predictions as validated candidate winners. Future design guidance requires prospective data and a genuinely held-out peptide set or new experimental batch.

## Step 10: conclusions, limitations, and next data needs

### Conclusions supported by the current workbook

- Replicate-level fold-change-like values and sequence strings are present for the 32 main candidates; all sequence IDs match measured IDs.
- The block-specific data allow descriptive outcome summaries and rankings, with variable replicate consistency.
- The expanded 34-feature association screen did not identify a feature surviving multiplicity correction; directional patterns (for example, core hydropathy) remain exploratory.
- Validation-blot values can be summarized separately for seven shared peptides, but they do not justify general calibration.
- Other-protein information is categorical, limited, and not comparable as a quantitative validation outcome.
- The small peptide-level model did not show stable predictive performance; reliable prediction, causal/mechanistic inference, and transfer to other proteins or lengths are not supported.

### Unresolved limitations

- The workbook does not contain raw band intensities, background correction, units, assay conditions, controls, or replicate identifiers. In meeting 2, the owner described two-stage normalization: band intensity normalized by total lane protein, then each lane-normalized band divided by the mean lane-normalized intensity across the gel. This account has not been independently audited against source values or processing files.
- The owner interprets the SP9 zero as likely no secretion but is uncertain about its origin; it remains an observed numeric zero in the analysis.
- Sequence boundaries, cleavage sites, translation-initiation windows, and protein fusion boundaries require source records/owner confirmation. The owner said the signal-peptide nucleotide sequences have the same codon optimization as in the first sheet and could potentially supply RBS/start/stop/terminator context; those records have not yet been provided.
- The owner clarified `No` as product not produced. Thresholds and provenance for `High`/`Medium`/`Low` remain unknown.
- Small n, separate blots, noisy replicate ranks, and unadjusted exploratory tests limit statistical certainty.
- Correlation cannot demonstrate causation or mechanism; predicted structural or sequence properties are not direct secretion evidence.

### Recommended follow-up before any predictive analysis

1. Ask the owner for available band-intensity/densitometry files and processing/normalization records (including total-lane protein values), lane maps, controls, assay conditions, and replicate identifiers so the stated two-stage normalization can be audited.
2. Clarify the origin of SP9's zero and identify any secondary-band cases; the owner recalled a possible secondary band but did not identify the peptide in this meeting.
3. If nucleotide initiation features are pursued, obtain the stated RBS/start/stop/terminator context and verify exact sequence boundaries and construct maps.
4. Record the owner's `No` definition as not produced; seek category thresholds/provenance for `High`/`Medium`/`Low` if those labels will be analyzed.
5. If prediction is still desired, prospectively test a pre-specified set of candidates/features under a comparable assay design, with independent replicate structure and a held-out or new-experiment evaluation planned in advance.

## Reproducibility and output index

- Detailed steps 2–8 report: `ouput/analysis_steps_2_8_report.md`
- Analysis script: `ouput/analysis/run_steps_2_8.py`
- Replicate summaries/data/figures: `ouput/analysis/replicate_summary_by_peptide.csv`, `replicate_values_long.csv`, `replicate_rank_concordance.csv`, `replicate_values_by_blot.png`
- Validation comparison: `ouput/analysis/validation_paired_shared_peptides.csv`, `validation_comparison_stats.csv`, `validation_shared_peptides.png`
- Sequence and feature table / associations: `ouput/analysis/sequence_qc_and_features.csv`, `within_blot_feature_associations.csv`, `within_blot_feature_associations.png`
- Documented exploratory features: `ouput/analysis/build_documented_features.py`, `documented_sequence_features.csv`, `documented_feature_dictionary.csv`, `documented_sequence_features_README.md`
- Expanded AA/nucleotide feature engineering: `ouput/analysis/features_step3.py`, methods in `ouput/md/feature_definitions.md`, tables/plots in `ouput/analysis/step3/`
- Expanded blot-aware association screen: `ouput/analysis/associations_step4.py`, tables/plots in `ouput/analysis/step4/`
- Exploratory peptide-level modeling: `ouput/analysis/exploratory_peptide_models.py`, `exploratory_model_metrics_by_blot.csv`, `exploratory_model_loo_predictions.csv`, `exploratory_peptide_models_README.md`
- Additional descriptive sequence features: `ouput/analysis/sequence_descriptors_exploratory.csv`
- Documented feature build: `ouput/analysis/build_documented_features.py`; feature definitions/settings: `ouput/analysis/documented_feature_dictionary.csv` and `ouput/analysis/documented_sequence_features_README.md`; values: `ouput/analysis/documented_sequence_features.csv`
- Other-protein categories: `ouput/analysis/other_protein_categories_matrix.csv`, `other_protein_categories_long.csv`, `other_protein_category_counts.csv`, `other_protein_categories_heatmap.png`
