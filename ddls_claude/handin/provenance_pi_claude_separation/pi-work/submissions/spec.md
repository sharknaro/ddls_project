# Scientific specification: signal peptides and recombinant-collagen secretion

## Source and attribution policy
The interview transcript `data/20261020_pi_transcript.txt` is the authoritative raw source for the data owner's statements. The transcript is an automatically generated transcript and contains apparent recognition errors (for example, “Western blood,” “baseless subtleties,” and “fault change”); do not silently treat those spellings as verified technical terms. Where context strongly suggests a term such as Western blot or fold change, that interpretation is contextual, not a substitute for checking the underlying workbook or asking the owner.

This specification separates:
- **Owner-stated:** information explicitly described or affirmed by the owner in the interview.
- **UNKNOWN / TO VERIFY:** information not established by that interview or not verified against the files.
- **Analysis proposal:** a cautious way to answer the question, not a fact about the supplied data or a commitment from the owner.

No dataset analysis has been performed in drafting this specification.

## 1. Owner's scientific question

**Owner-stated:** The owner explored secretion of recombinant collagen in *Bacillus subtilis* using a library of approximately 32 signal peptides. They want to know whether secretion efficiency is associated with signal-peptide features, including amino-acid sequence, codon-optimized nucleic-acid sequence, possible mRNA/translation-initiation features, structure, hydrophobicity, and other calculable properties (the owner mentions pI and folding Gibbs energy as examples). They would like to understand why some peptides performed better and, if evidence permits, use the findings to suggest new synthetic signal peptides.

The owner confirmed the broad deliverables as (1) analyze associations/correlations among candidate features and secretion, (2) develop a model if feasible, and (3) optionally extrapolate to novel designs. In discussion, the owner clarified that structure is one possible feature, not necessarily the answer; position-specific sequence features or hydrophobic/hydrophilic character may be relevant too.

**Decision that depends on the answer (owner-stated):** Whether there are useful, defensible signal-peptide features or candidate designs worth further consideration, with high-secretion candidates of greatest practical interest. The owner notes possible future publication value and that collaborators might experimentally test one or two candidates if circumstances allow. No immediate experimental validation commitment is established.

## 2. Project scope and owner expectations

- **Owner-stated:** The biological system is recombinant collagen secretion in *Bacillus subtilis*. The library contains around 32 signal peptides. The owner wants the analysis to include good and poor performers, rather than selecting only the best.
- **Owner-stated:** Secretion is of interest as high / medium / low, rather than necessarily requiring an absolute numeric threshold. No rule for those categories was specified.
- **Owner-stated:** The owner is most interested in the best candidates if scope forces prioritization, but sees value in examining all categories.
- **Owner-stated:** The owner would accept a well-supported negative result (no clear correlation) as informative.
- **Owner-stated:** The owner is cautious about prediction confidence and does not specify an acceptable numerical confidence threshold.
- **UNKNOWN / TO VERIFY:** Whether the project should produce a quantitative predictive model, a descriptive feature/correlation report only, a candidate ranking, or all of these. The transcript expresses interest in all, while feasibility and validation are unresolved.

## 3. Data and files known to be present

Observed directory inventory (filenames only; contents have not been scientifically analyzed):

| File | What is known from interview / inventory | Status |
|---|---|---|
| `data/20261020_pi_transcript.txt` | Transcript of the data-owner interview; authoritative source for stated project requirements. | Read for this specification. |
| `data/20261016_ddls_project_meeting1.mp3` | Interview audio recording. | Present; not analyzed here. |
| `data/Information_for_Baris.xlsx` | Workbook supplied with the project. Owner described an intended three-sheet organization (details below). | Present; sheet names, exact schema, values, and contents remain UNKNOWN / TO VERIFY. |
| `data/Paper_for_IDEAS.pdf` | A paper the owner says they can share and refers to when discussing prior work; the transcript does not identify its bibliographic details or exact findings. | Present; not reviewed for this specification. |
| `data/PhD_Thesis_Final_Chapter2_CollagenProduction_HOJBERG.pdf` | Thesis document supplied with the project. | Present; contents and relationship to the data remain UNKNOWN / TO VERIFY. |

The directory also contains `.env` and `.gitignore`, which are not scientific source data and should not be read or exposed as part of scientific analysis.

### Owner-described expected workbook layout (not yet verified)
The owner said the data would be in a CSV-like format but then described a workbook with three sheets. This must be reconciled by inspecting the actual file; do not call it a CSV unless it is actually a CSV.

1. **Sheet 1 (owner-described):** names and sequences: nucleic-acid sequence (described as codon-optimized), amino-acid sequence of the protein fused to the signal peptide, and signal-peptide sequence. The owner says signal peptides are at the N-terminus and continue directly into the protein sequence. Exact columns, row granularity, sequence orientation, and whether sequences are separate or concatenated are UNKNOWN / TO VERIFY.
2. **Sheet 2 (owner-described):** secretion results as “fold changes” (transcription says “fault chains” in places). The owner explains that for each gel, band intensity was divided by that gel's mean intensity, with values above one indicating above-mean intensity and below one indicating below-mean intensity. Exact column names, whether values are raw or summarized, replicate structure, and the final mapping from band intensity to secretion are UNKNOWN / TO VERIFY.
3. **Sheet 3 (owner-described):** results for other proteins / a validation case. The owner mentions four signal peptides tried with proteins of different length and suggests these can be used as a check for another protein. The owner specifically cautions this is not the same complete set of approximately 32 peptides and is not suitable for ordinary retraining; protein length/context may confound it. Exact number and identity of proteins, peptides, measurements, and role of this sheet are UNKNOWN / TO VERIFY.

### Assay and units
- **Owner-stated:** Performance was assessed using Western blotting and densitometry/band intensity. There were three different gels for the main candidate measurements; within each gel, the owner ranked candidates after comparing band intensity to that gel's mean intensity. The owner says they divided each band's intensity by its gel's mean; values above one are above the gel mean and below one are below it.
- **Owner-stated:** There was a fourth gel described as a validation gel containing signal peptides from different gels. It may be used to make a new weighted ranking or estimate what the rankings across gels might have been, but it must be treated as a separate experiment, not directly combined with the original gel-normalized values.
- **UNKNOWN / TO VERIFY:** Raw densitometry values, exact normalization formula and order of operations, whether “mean” is across all bands or a subset, background subtraction, exposure/saturation handling, loading controls, technical/biological replicates, lane-to-candidate mapping, gel membership, controls, uncertainty, and whether higher normalized band intensity is a validated proxy for higher secreted collagen quantity.
- **Units:** The normalized ratio is described as a band intensity divided by a gel mean, hence likely dimensionless, but actual units and workbook encoding are UNKNOWN / TO VERIFY. Do not assume raw intensity units.
- **Owner-stated:** The owner can provide raw band intensities if needed, but anticipated the analysis would be more complicated. It is UNKNOWN whether those raw values are present in the supplied workbook.

## 4. Hypotheses and expectations

These are questions or expectations, not established findings:

- **Owner-stated question:** Signal-peptide amino-acid or nucleic-acid features may associate with secretion. Examples raised include mRNA folding, translation-initiation features/domains, sequence patterns, hydrophobicity, pI, folding Gibbs energy, and structure.
- **Owner-stated expectation:** Some prior paper reportedly found a small correlation for one feature; the owner is interested in checking whether that is consistent with this dataset. The paper and exact feature/result are UNKNOWN / TO VERIFY.
- **Owner-stated caution:** Prior work described by the owner selected the 15 best performers from a larger library and looked for correlations without including poor performers. The owner believes this selection may limit the conclusions. The referenced library was described as having a different signal-pattern composition; overlap with the present set is UNKNOWN / TO VERIFY.
- **Owner-stated biological concern:** Secretion in *B. subtilis* depends on the signal peptide together with the protein; collagen/protein length differences may affect performance. A relationship for one protein length may not transfer to a longer protein.
- **UNKNOWN / TO VERIFY:** Direction, magnitude, and reproducibility of any feature-secretion relationship; which features can actually be computed reliably for these sequences; whether structure predictions are feasible or informative for short signal peptides; whether any classifier/regressor is identifiable from the sample size.

## 5. What has already been tried

- **Owner-stated:** The owner experimentally screened approximately 32 signal peptides and used Western blot densitometry to rank them within three gels after normalizing band intensity by each gel's mean.
- **Owner-stated:** A fourth/validation gel combined signal peptides from different gels; the owner suggests it could support a separate cross-gel ranking/weighting exercise.
- **Owner-stated:** Four signal peptides were also tried with other proteins / proteins of different length; the owner considers them a possible check but not a sound retraining set.
- **Owner-stated:** The owner has not personally run computational predictions or a machine-learning analysis on this dataset.
- **Owner-stated:** The owner has seen prior literature involving a larger library and selection of the top 15; a small correlation was reportedly found for one factor. Details require verification.
- **NOT DONE:** No dataset analysis, structure calculation, feature calculation, statistical test, model fitting, or interpretation has been conducted for this specification.

## 6. Required comparisons and controls

The following are minimum comparisons implied by the owner's question; exact implementation depends on workbook verification and should be documented before analysis.

1. **Include the full main set:** Examine all available candidates, including poor, intermediate, and strong performers. Do not filter to top candidates before testing associations.
2. **Respect gel boundaries:** Show/compare data within each original gel, retaining gel identity. Do not pool three gel-normalized scales as if they were a common absolute scale.
3. **Treat validation gel separately:** Describe its measurements as a separate experiment. Any cross-gel calibration or weighted ranking must specify which shared peptides anchor it, the calculation, assumptions, and uncertainty; confirm the intended approach with the owner where possible.
4. **Relate candidate features to outcome cautiously:** Explore owner-requested sequence/nucleic-acid/structure/physicochemical feature families only after identifying actual measured outcome, independent units, and sample size. Report effect direction and uncertainty, not just a binary correlation label.
5. **Use the other-protein observations as a distinct contextual check:** Do not treat the four observations as an independent, representative validation set or pool them blindly with main collagen data. Report differences in protein identity/length and assay context if documented.
6. **Controls:** The existence, identity, and placement of biological/technical controls are UNKNOWN / TO VERIFY. Do not invent controls or claim a controlled comparison until confirmed from data/protocol/owner.
7. **High/medium/low groups:** The owner finds coarse categories useful, but category thresholds/rules are UNKNOWN / TO VERIFY. If categories are used, define them transparently from measured data and distinguish exploratory bins from owner-provided labels.
8. **Validation:** The owner raises validation as important but provides no formal split or external dataset. Any internal validation plan must account for small n, gel grouping, and leakage; the four other-protein cases are only a limited check according to the owner.

## 7. Potential confounders and limits

- **Gel/batch:** Three separate gels with gel-specific mean normalization. Gel can confound comparisons; normalized values may not share a common scale.
- **Validation-gel design:** The fourth gel is a separate experiment and needs explicit calibration; shared candidates and measurement procedure must be verified.
- **Protein identity and length:** Different collagen lengths/proteins can alter secretion and interact with signal peptide effects. The four additional cases may not be directly comparable.
- **Outcome construction:** Gel-normalized intensity is a relative measurement. Its relationship to absolute secretion is UNKNOWN / TO VERIFY.
- **Small sample size:** Approximately 32 main signal peptides and four other-protein cases are owner-reported counts, not yet checked against workbook rows. Many candidate features could lead to multiple testing and overfitting.
- **Feature dependence:** Sequence-derived properties may be correlated with one another; feature definitions and computational methods can affect conclusions. This is a methodological risk, not a verified property of this dataset.
- **Selection bias:** Analysis of only top performers could make features appear common without showing that they distinguish high from low secretion.
- **Structural inference:** A predicted signal-peptide structure is uncertain and does not itself establish secretion function or mechanism.
- **External transfer:** Results may be specific to the tested collagen construct, host, assay, and conditions. Generalization is UNKNOWN / TO VERIFY.
- **Transcript uncertainty:** Automated transcription may have misheard scientific terms; resolve from workbook, protocol, or owner rather than converting uncertain words into facts.

## 8. Known missing information (must label UNKNOWN / TO VERIFY until resolved)

- Actual workbook sheet names, full schema, row counts, identifiers, missing-value conventions, and sequence formats.
- Which of the approximately 32 signal peptides map to which gels and which are shared across gels / present on the fourth gel.
- Exact candidate names and sequence provenance; sequence lengths; whether nucleic-acid sequence includes only signal peptide or full fusion construct; exact boundary between signal peptide and collagen.
- Exact collagen construct(s), protein sequences, lengths, and whether all main-set measurements use the same protein construct.
- Exact normalization and densitometry protocol; background correction; raw values; replicates and uncertainty; units; assay controls; experimental conditions.
- Whether the “fourth validation gel” is represented in the workbook and what “weighting” method the owner intended.
- Exact identities/number of the other proteins, their lengths, which four signal peptides were used, and their role as validation/training data.
- The referenced paper's identity and which feature reportedly showed a small correlation; overlap with the owner’s peptides.
- Definitions/methods for proposed features (mRNA folding window/conditions, translation initiation metric, hydrophobicity scale, pI, Gibbs free energy, structure prediction, etc.).
- Pre-specified statistical criterion, multiple-testing approach, high/medium/low thresholds, acceptable prediction confidence, and validation strategy.
- Whether experimental follow-up is possible and who would conduct it.

## 9. Evidence that would support or contradict the owner's hypothesis

The hypothesis is that some sequence/nucleic-acid/structural/physicochemical features relate to secretion performance.

**Evidence that would support an association (not causation):** A feature-outcome relationship that is visible across the full candidate set (not just the top subset), is directionally coherent within gel or under a justified cross-gel calibration, has uncertainty reported, is not driven solely by one candidate/gel, and is robust to reasonable feature/normalization choices. Similarity with an independently described prior result could add context only after identifying the paper and comparing methods. For prediction, performance must be evaluated without leakage and with validation appropriate to the actual experimental grouping; any external or other-protein check must be labeled as limited and context-dependent.

**Evidence that would contradict or fail to support it:** No consistent trend, substantial within-group scatter, effect changing across gels, association disappearing when all candidates are included, dependence on one outlier, or failure to predict held-out data. Such a result is informative and acceptable to the owner. Failure to find an association in this small dataset does not prove that no biological relationship exists.

**Important distinction:** A visually plausible structure, a computed feature difference, or a fitted model on the same observations is not by itself evidence that the feature causes secretion or that a new design will work.

## 10. What would make results believable to the owner

**Owner-stated expectations:** Calculate relevant factors; provide graphs that show correlations when present and also make absence of clear correlation visible; consider structures for all approximately 32 signal peptides; classify/describe secretion roughly as high, medium, or low rather than requiring an absolute number; prioritize the strongest candidates if necessary; be cautious about predicted structures and prediction confidence. A negative finding is acceptable.

**Operational credibility requirements (analysis proposal, not owner-stated thresholds):** Trace every outcome to its sheet/row and assay definition; preserve gel identity; show all candidates and exclusions; document feature calculation methods and assumptions; show uncertainty and sample size; avoid overfitting; distinguish exploratory findings from validated prediction; explicitly state what did and did not replicate across gels or protein contexts. Agree category cutoffs and any model/validation plan with the owner before treating them as decision rules.

## 11. Definition of done

A first-pass project deliverable is done when it:

1. Verifies and documents the actual workbook structure, sequence fields, outcome fields, coding, units (or states UNKNOWN), gel assignments, and replicate/control information; resolves or flags interview ambiguities.
2. Describes/calculates a documented set of relevant sequence/nucleic-acid/physicochemical features, and clearly labels which requested analyses (including structure prediction) were feasible, not feasible, or uncertain.
3. Presents transparent plots/tables of relationships between these features and secretion outcome using all eligible main-set candidates, with poor and strong performers included and gel context retained.
4. Treats the fourth gel as a separate experiment and explains any cross-gel calibration/ranking method rather than silently pooling normalized values.
5. Separately describes the four other-protein cases and their limitations; does not present them as a robust independent validation or retraining dataset.
6. Gives a cautious conclusion: evidence for an association, no clear association, or inconclusive; reports uncertainty and avoids claims beyond the data. If a model or candidate suggestions are attempted, labels them exploratory and reports a defensible validation result or explains why validation is not possible.
7. Provides the owner with graphs/tables and, where justified, a transparent coarse high/medium/low interpretation; no arbitrary threshold is presented as owner-approved.

No minimum correlation coefficient, p-value, prediction score, structure confidence, or accuracy threshold was specified by the owner. These remain UNKNOWN / TO VERIFY; do not manufacture a numerical pass criterion.

## 12. Claims this dataset must not support

Do not claim, based on this dataset alone, that:
- a feature causes increased secretion or explains the mechanism;
- predicted structure determines secretion performance;
- a fitted model is reliable/generalizable or can design successful sequences;
- a proposed synthetic signal peptide will be high-secreting without experimental validation;
- results transfer to different proteins, collagen lengths, hosts, conditions, or industrial settings;
- gel-normalized values from separate gels are directly comparable absolute secretion measurements;
- the four other-protein observations establish external validation;
- no relationship exists biologically merely because this limited dataset fails to show one.
