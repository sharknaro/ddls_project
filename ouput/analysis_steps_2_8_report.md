# Analysis plan steps 2–8: results and caveats

**Data used:** `data/Information_for_Baris_corrected.xlsx`. Analyses are descriptive/exploratory; no model fitting or cross-blot calibration was performed. Replicate independence, precise assay semantics, and category meanings remain unknown. All three original blot analyses are kept separate; validation results are only compared descriptively with their seven matched main-screen peptides.

Reproduce the outputs with `python ouput/analysis/run_steps_2_8.py`. Machine-readable tables and figures are in `ouput/analysis/`; see its README for file descriptions.

## 2. Outcome distributions and replicate consistency

Every main-screen peptide has 3 numeric replicates, and each validation peptide has 4. The reported zero for SP9/Blot 2 replicate 1 is preserved as numeric zero. Per-peptide mean, median, sample SD, min/max, CV, and within-blot mean rank are in `ouput/analysis/replicate_summary_by_peptide.csv`; exact replicate values and source cells are in `replicate_values_long.csv`.

Descriptive within-blot mean leaders and ranges:

| Block | Highest mean | Mean | Lowest mean | Mean | Range of all replicate values |
|---|---|---:|---|---:|---:|
| Blot 1 | SP4 | 1.610 | SP8 | 0.361 | 0.153–3.159 |
| Blot 2 | SP19 | 3.659 | SP9 | 0.047 | 0–6.230 |
| Blot 3 | SP26 | 1.912 | SP25 | 0.073 | 0.00044–3.417 |
| Validation blot | SP4 | 1.735 | SP2 | 0.503 | 0.119–2.477 |

These are **within-block ranks only**, not common-scale comparisons across gels. Replicate-to-replicate Spearman rank concordance varied: Blot 1 0.262–0.595, Blot 2 0.571–0.593, Blot 3 0.145–0.682, validation −0.071–0.750. This suggests consistency is uneven, especially with only three/four replicate rows; these correlations do not establish replicate independence or assay reliability. See `replicate_rank_concordance.csv` and `replicate_values_by_blot.png`.

## 3. Shared-peptide comparison with validation blot

Seven shared peptides were matched by ID to their original-blot summaries (SP2, SP3, SP32, SP26, SP5, SP19, SP4). Across their means, Spearman association between main and validation values is **ρ=0.679** (n=7; nominal p=0.094); Pearson r=0.482 (p=0.273). Rank correspondence is also imperfect (Spearman ρ=0.692). Six of seven validation means are lower than their original-blot means; paired mean difference (validation minus original) is −0.757, median difference −0.544. This pattern could reflect selection/design or experiment/scale differences; it is not evidence for a calibration factor. One small paired test is not a confirmatory comparison.

No calibration/weighting is fitted. The shared candidates come from three original blots and the validation is a separate experiment; their values cannot safely define a general cross-blot conversion. Paired values/IDs are in `validation_paired_shared_peptides.csv`, with plot `validation_shared_peptides.png`.

## 4. Working outcome and grouping

For descriptive ranking only, outcome is the arithmetic mean of the recorded replicate values **within each individual block**. Medians and spread are included so the reader can see sensitivity to skew/outliers; e.g. SP4 in Blot 1 has mean 1.610 but median 1.003, and SP23 in Blot 3 has mean 1.162 but median 0.069 because of a single high replicate. No high/medium/low cutoffs were invented. Values labeled fold-change remain relative assay values, not absolute secretion yields, and the owner’s normalization description cannot be verified from the workbook.

## 5. Sequence inventory and QC

For the 32 peptide sequences, all AA strings use valid standard one-letter amino-acid symbols and all Nt strings use A/C/G/T; no duplicate AA or Nt strings were found. Lengths are 21–42 AA (mean 29.97) and 63–126 nt. Each Nt sequence is exactly 3× its AA length, and translation in the supplied frame matches the listed AA sequence for all 32. This is a sequence consistency check, not provenance verification, proof of codon optimization, or confirmation of fusion boundaries. The file `sequence_qc_and_features.csv` keeps the strings, source row, validation flags, and derived feature columns.

## 6. Limited interpretable features calculated

Given missing cleavage boundaries, only simple, transparent features over each **entire listed peptide string** were calculated:

- AA length;
- fraction of residues in `AVILMFWY` (broad hydrophobic-residue proxy; not a named hydrophobicity scale);
- `(K + R − D − E) / length` (simple charge proxy, not pI);
- exploratory GC fraction in the first 9 nt (initiation context/sequence boundaries are unverified).

No pI, RNA folding, cleavage prediction, hydrophobicity scale score, or structural model is presented. The numeric feature definitions and values are in `sequence_qc_and_features.csv`.

## 7. Within-original-blot feature associations

Spearman correlations of block-specific mean fold-change with each feature (all candidates in each blot; n=8, 13, 11) were:

| Feature | Blot 1 ρ (p) | Blot 2 ρ (p) | Blot 3 ρ (p) |
|---|---:|---:|---:|
| Full listed AA length | −0.095 (0.823) | 0.129 (0.673) | 0.560 (0.073) |
| AVILMFWY fraction | −0.429 (0.289) | −0.088 (0.775) | −0.391 (0.235) |
| Charge proxy per residue | −0.024 (0.955) | −0.462 (0.112) | −0.284 (0.397) |
| First-9-nt GC fraction (exploratory) | 0.150 (0.723) | −0.029 (0.924) | 0.301 (0.368) |

Values are exploratory, p-values unadjusted across features/blots, and samples are small. Effects are not consistent across blots; the moderately positive length trend in Blot 3 is not clear evidence of an association and does not appear in Blots 1 or 2. No feature gives compelling consistent association evidence here. This is **inconclusive/no clear association in these simple checks**, not evidence that no biological relationship exists. Because normalized scales and measurement precision are uncertain, further inferential claims would be premature. Table and faceted scatter plots: `within_blot_feature_associations.csv` and `within_blot_feature_associations.png`.

## 8. Other-protein categories as separate descriptive context

The corrected third sheet supplies 4 peptide rows (SP3, SP5, SP19, SP26) × 7 protein constructs, with categorical labels only. The corrected strings are retained exactly; in particular `No` is treated as the observed category, not numeric zero or a verified absence of secretion. The table has no category thresholds, assay replicates, quantitative measurements, or provenance details. The labels vary by construct and peptide; the `Alpha2 with C propeptide` and `Procollagen` columns are `No` for all four rows in this corrected workbook. The categories cannot be translated into measured numeric outcomes or treated as independent validation. See `other_protein_categories_matrix.csv`, `other_protein_categories_long.csv`, and `other_protein_categories_heatmap.png`.

## Summary and limitations

Steps 2–8 have been carried out descriptively. The workbook supports within-blot summary/ranking, a limited seven-peptide separate validation comparison, sequence consistency checks, and a few simple exploratory correlations. It does **not** establish raw assay units, replicate type/independence, normalization details, objective secretion categories, category provenance, or universal cross-blot calibration. Further sequence-feature work should wait for owner-approved feature definitions and assay/sequence-boundary clarification. No causal mechanism or reliable prediction is supported by these analyses.
