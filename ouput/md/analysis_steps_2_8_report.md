# Analysis plan steps 2–8: results and caveats

**Data used:** `data/Information_for_Baris_corrected.xlsx`. Analyses are descriptive/exploratory; no model fitting or cross-blot calibration was performed. Meeting 2 adds owner-reported clarifications: replicates are described as biological (exact unit/independence unclear); values were ranked left-to-right by ascending replicate mean for presentation; normalization was described as lane-total-protein normalization followed by division by the gel-wide mean of those normalized band intensities; and `No` means product not produced. These details are not independently audited against raw assay records. All three original blot analyses are kept separate; validation results are only compared descriptively with their seven matched main-screen peptides.

Reproduce the outputs with `python ouput/analysis/run_steps_2_8.py`. Machine-readable tables and figures are in `ouput/analysis/`; see its README for file descriptions.

## 2. Outcome distributions and replicate consistency

Every main-screen peptide has 3 numeric replicates, and each validation peptide has 4. The owner described these as biological replicates (also saying “in a way, both”); exact unit and independence are still unspecified. The reported zero for SP9/Blot 2 replicate 1 is preserved as numeric zero. The owner interprets it as likely no secretion but is unsure of its origin, so this is not treated as verified measurement semantics. Per-peptide mean, median, sample SD, min/max, CV, and within-blot mean rank are in `ouput/analysis/replicate_summary_by_peptide.csv`; exact replicate values and source cells are in `replicate_values_long.csv`.

Descriptive within-blot mean leaders and ranges:

| Block | Highest mean | Mean | Lowest mean | Mean | Range of all replicate values |
|---|---|---:|---|---:|---:|
| Blot 1 | SP4 | 1.610 | SP8 | 0.361 | 0.153–3.159 |
| Blot 2 | SP19 | 3.659 | SP9 | 0.047 | 0–6.230 |
| Blot 3 | SP26 | 1.912 | SP25 | 0.073 | 0.00044–3.417 |
| Validation blot | SP4 | 1.735 | SP2 | 0.503 | 0.119–2.477 |

These are **within-block ranks only**, not common-scale comparisons across gels. The owner clarified that workbook peptide order is ascending by mean replicate value from left to right, mainly for aesthetics. Replicate-to-replicate Spearman rank concordance varied: Blot 1 0.262–0.595, Blot 2 0.571–0.593, Blot 3 0.145–0.682, validation −0.071–0.750. This suggests consistency is uneven, especially with only three/four replicate rows; these correlations do not establish replicate independence or assay reliability. See `replicate_rank_concordance.csv` and `replicate_values_by_blot.png`.

## 3. Shared-peptide comparison with validation blot

Seven shared peptides were matched by ID to their original-blot summaries (SP2, SP3, SP32, SP26, SP5, SP19, SP4). Across their means, Spearman association between main and validation values is **ρ=0.679** (n=7; nominal p=0.094); Pearson r=0.482 (p=0.273). Rank correspondence is also imperfect (Spearman ρ=0.692). Six of seven validation means are lower than their original-blot means; paired mean difference (validation minus original) is −0.757, median difference −0.544. This pattern could reflect selection/design or experiment/scale differences; it is not evidence for a calibration factor. One small paired test is not a confirmatory comparison.

No calibration/weighting is fitted. The shared candidates come from three original blots and the validation is a separate experiment; their values cannot safely define a general cross-blot conversion. Paired values/IDs are in `validation_paired_shared_peptides.csv`, with plot `validation_shared_peptides.png`.

## 4. Working outcome and grouping

For descriptive ranking only, outcome is the arithmetic mean of the recorded replicate values **within each individual block**, matching the owner's clarification of the workbook's ascending left-to-right ordering. Medians and spread are included so the reader can see sensitivity to skew/outliers; e.g. SP4 in Blot 1 has mean 1.610 but median 1.003, and SP23 in Blot 3 has mean 1.162 but median 0.069 because of a single high replicate. No high/medium/low cutoffs were invented. Values labeled fold-change remain relative assay values, not absolute secretion yields. In meeting 2, the owner described normalization as first dividing band intensity by total lane protein, then dividing each lane-normalized band by the gel-wide mean of these normalized intensities. This process has not been audited against raw data.

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

The corrected third sheet supplies 4 peptide rows (SP3, SP5, SP19, SP26) × 7 protein constructs, with categorical labels only. In meeting 2, the owner confirmed `S19` refers to `SP19`, `Np` was intended as `No`, and `No` means the product was not produced, rather than missing or untested. `No` remains categorical and is not recoded as a numeric zero. The corrected strings are retained exactly. The table has no category thresholds, quantitative measurements, or documented replicate/provenance details. The labels vary by construct and peptide; the `Alpha2 with C propeptide` and `Procollagen` columns are `No` for all four rows in this corrected workbook. They cannot be treated as a quantitative endpoint or independent validation. See `other_protein_categories_matrix.csv`, `other_protein_categories_long.csv`, and `other_protein_categories_heatmap.png`.

## Summary and limitations

Steps 2–8 have been carried out descriptively. The workbook supports within-blot summary/ranking, a limited seven-peptide separate validation comparison, sequence consistency checks, and a few simple exploratory correlations. The owner has now described replicate type as biological (exact unit/independence unclear) and the two-stage normalization process, but raw assay data and records needed to verify these remain unavailable. `No` is owner-defined as product not produced; category thresholds and provenance are still unknown. Further sequence-feature work should wait for owner-approved feature definitions and assay/sequence-boundary clarification. No causal mechanism or reliable prediction is supported by these analyses.

## Meeting 2 data-owner clarifications and remaining follow-up

These are owner statements captured in an auto-transcribed meeting, not independently verified against experimental records:

- **Ranking:** peptide columns are ordered left-to-right by ascending replicate mean, mainly for presentation aesthetics.
- **Replicates:** described as biological (“in a way, both”); precise units and independence remain unclear.
- **Zero:** SP9's zero was interpreted as likely no secretion, but the owner was unsure of its origin. The numerical zero remains unchanged.
- **Normalization:** first normalize band intensity by total lane protein, then divide each lane-normalized band by the gel-wide mean of normalized band intensities. Raw band intensities and processing records are needed to audit this.
- **Categories:** `S19` was confirmed as `SP19`; `Np` as `No`; and `No` means product not produced, not missing or untested. `No` remains a category, not a numeric zero. `Ηigh` → `High` is in the corrected workbook but was not clearly confirmed in this meeting.
- **Sequence/gel context:** owner says nucleotide sequences share the codon optimization used in the first sheet and may be able to provide RBS/start/stop/terminator context. A possible secondary band was recalled, but no peptide was identified.

Next useful inputs are the available band-intensity and normalization records, replicate identifiers/unit details, the SP9 zero provenance, any identified secondary-band cases, and source confirmation of category thresholds/provenance. No new quantitative analyses were run from this transcript.
