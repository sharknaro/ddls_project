# Data analysis part 1: final results (analysis-plan steps 2–10)

**Analysis dataset:** `data/Information_for_Baris_corrected.xlsx`. The deliverables below cover descriptive outcome review, sequence QC, limited within-blot feature exploration, context categories, and the decision about prediction feasibility. This is not a causal analysis or a validated prediction study.

## Executive conclusion

The workbook supports descriptive rankings **within** Blot 1, Blot 2, and Blot 3 and a separate descriptive comparison of seven shared peptides in the validation blot. Replicate rank agreement varies, the shared-peptide validation comparison is imperfect, and the four simple sequence features examined do not show a consistent relationship with relative outcome across the three original blots. Third-sheet categories are uncalibrated labels for four tags across different constructs. Accordingly, **reliable prediction, candidate extrapolation, and new sequence design are not supported by the current data**. No model was fit and no cross-blot calibration was attempted.

This is a “no clear association / inconclusive” result for the limited exploratory features tested, not evidence that no biological relationship exists. The small candidate counts, assay uncertainties, and missing feature-boundary/provenance information limit inference.

## Data decisions carried forward

- The corrected workbook's category values `SP19`, `High`, and `No` were accepted as strings as provided. This does not independently confirm category meaning or origin.
- SP9/Blot 2/replicate 1 value `0` remains numeric zero; whether it denotes no detection is unknown.
- Results are summarized by arithmetic mean **within each block**, with medians and spread included. Main blot values are not pooled; validation is separate.
- Peptide column order was treated under the requested assumption as right-to-left descending mean fold-change; calculated summaries are traceable in CSVs rather than silently inferred from position.

## Steps 2–8: findings

### Outcome and replicate behavior

There are 32 main peptides with 3 replicate values each and 7 validation peptides with 4 each. Per-block mean leaders (lowest candidates in parentheses) are SP4 (SP8) in Blot 1, SP19 (SP9) in Blot 2, SP26 (SP25) in Blot 3, and SP4 (SP2) in validation. These are local ranks only. Replicate-to-replicate Spearman rank concordance ranges from 0.262–0.595, 0.571–0.593, 0.145–0.682, and −0.071–0.750 for Blots 1, 2, 3, and validation respectively, indicating uneven replicate rank stability.

The seven shared peptides have imperfect original-to-validation correspondence (mean-based Spearman ρ=0.679, n=7; rank correspondence ρ=0.692). Six validation means are lower than their main-blot means, but the observations span three original blots and a separate experiment. This is not sufficient to estimate a general conversion/calibration; none was fit.

### Sequence QC and feature exploration

All 32 AA sequences use standard amino-acid letters; all Nt sequences use A/C/G/T. There are no exact duplicate AA or Nt strings. Nt length is three times AA length and translation matches the listed AA sequence for all 32. This checks internal consistency only—not sequence provenance, codon optimization, or construct boundaries.

Exploratory features were defined over the full listed sequence: AA length; fraction of `AVILMFWY` residues; `(K+R-D-E)/length` as a simple charge proxy; and first-nine-nucleotide GC fraction (especially exploratory because the initiation region is not verified). Spearman correlations were modest/variable and did not reproduce direction consistently across blots. The largest trend was positive length in Blot 3 (ρ=0.560, n=11, nominal p=0.073), but length trends were near zero in Blots 1 and 2. No clear, consistent feature–outcome relationship emerged. These small-sample p-values are unadjusted and not confirmatory.

### Other-protein categorical context

The third sheet has four peptide labels (SP3, SP5, SP19, SP26) and seven protein constructs, with `High`, `Medium`, `Low`, `No` strings only. Thresholds, assay provenance, category meaning, and replicate details are undocumented. These data remain descriptive and cannot serve as a quantitative endpoint, retraining dataset, or independent validation set.

Full tables/figures are in `ouput/analysis/`; the methods and more detailed step 2–8 narrative are in `ouput/analysis_steps_2_8_report.md`.

## Step 9: prediction and extrapolation decision

A predictive model is **not justified** on this dataset at this stage:

1. Only 32 unique main candidates are available, divided among three separately normalized blots; each has just three reported replicates and replicate independence is unspecified.
2. The feature analyses did not identify a stable, consistently directional signal across blots. Fitting many candidate features would invite overfitting and multiplicity.
3. Seven shared peptides are too few for a general cross-blot calibration; their validation data are a separate experiment and must not be used both to calibrate and validate.
4. The third-sheet categories lack verified quantitative meaning and represent only four selected peptides across different proteins, not suitable model training or external validation.
5. No genuinely independent, sufficiently sized holdout set remains for an honest estimate of generalization.

Therefore no model, held-out performance estimate, or proposed synthetic signal-peptide design is reported. Within-blot means may be used as **descriptive candidate rankings** for the corresponding experimental block only, not as a unified top-candidate ranking across all 32. Any future candidate selection should be explicitly exploratory and confirmed experimentally. This is not a claim that prediction will never be possible; it is a limit of the available evidence.

## Step 10: conclusions, limitations, and next data needs

### Conclusions supported by the current workbook

- Replicate-level fold-change-like values and sequence strings are present for the 32 main candidates; all sequence IDs match measured IDs.
- The block-specific data allow descriptive outcome summaries and rankings, with variable replicate consistency.
- In the small set of features examined, no clear, consistent within-blot association was observed.
- Validation-blot values can be summarized separately for seven shared peptides, but they do not justify general calibration.
- Other-protein information is categorical, limited, and not comparable as a quantitative validation outcome.
- Reliable prediction, causal/mechanistic inference, and transfer to other proteins or lengths are not supported.

### Unresolved limitations

- The workbook does not define fold-change calculation, raw intensity values, background correction, units, exact normalization, assay conditions, controls, or replicate type/independence. The owner describes gel-mean normalization, but this is not independently verified here.
- The meaning of the observed zero is not established.
- Sequence boundaries, cleavage sites, translation-initiation windows, codon optimization status, and protein fusion boundaries require source records/owner confirmation.
- `High`/`Medium`/`Low`/`No` thresholds, provenance, and interpretation are unknown even in the corrected copy.
- Small n, separate blots, noisy replicate ranks, and unadjusted exploratory tests limit statistical certainty.
- Correlation cannot demonstrate causation or mechanism; predicted structural or sequence properties are not direct secretion evidence.

### Recommended follow-up before any predictive analysis

1. Obtain original densitometry values and processing/normalization records, lane maps, controls, assay conditions, and a definition of replicate structure.
2. Confirm whether the zero is true zero, below-detection, or another encoding, and clarify outcome meaning/units with the owner.
3. Verify exact sequence boundaries, fusion constructs, codon optimization, and the start/stop/initiation regions.
4. Confirm provenance and definitions for third-sheet categories and whether `No` is an outcome or a missing/not-tested indicator.
5. If prediction is still desired, prospectively test a pre-specified set of candidates/features under a comparable assay design, with independent replicate structure and a held-out or new-experiment evaluation planned in advance.

## Reproducibility and output index

- Detailed steps 2–8 report: `ouput/analysis_steps_2_8_report.md`
- Analysis script: `ouput/analysis/run_steps_2_8.py`
- Replicate summaries/data/figures: `ouput/analysis/replicate_summary_by_peptide.csv`, `replicate_values_long.csv`, `replicate_rank_concordance.csv`, `replicate_values_by_blot.png`
- Validation comparison: `ouput/analysis/validation_paired_shared_peptides.csv`, `validation_comparison_stats.csv`, `validation_shared_peptides.png`
- Sequence and feature table / associations: `ouput/analysis/sequence_qc_and_features.csv`, `within_blot_feature_associations.csv`, `within_blot_feature_associations.png`
- Other-protein categories: `ouput/analysis/other_protein_categories_matrix.csv`, `other_protein_categories_long.csv`, `other_protein_category_counts.csv`, `other_protein_categories_heatmap.png`
