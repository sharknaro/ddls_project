# Project instructions

## Scientific goal
Determine whether features of the approximately 32 N-terminal signal peptides are associated with measured recombinant-collagen secretion in *Bacillus subtilis*, and whether the available evidence supports cautious prediction of high-secretion candidates.

## Owner's decision / question
The data owner wants to know whether amino-acid sequence, codon-optimized nucleic-acid sequence (including possible mRNA/translation-initiation features), or signal-peptide structure/physicochemical properties relate to secretion efficiency—and, if there is useful evidence, whether the features can help identify or propose candidates with high secretion. The owner is especially interested in the best-secreting candidates. The proposed extrapolation/design work is an optional, exploratory deliverable, not an established capability.

## Source materials and data locations
- Owner interview transcript (authoritative raw source): `data/20261020_pi_transcript.txt`. 
- Interview recording: `data/20261016_ddls_project_meeting1.mp3`.
- Supplied workbook: `data/Information_for_Baris.xlsx`.
- Additional supplied documents: `data/Paper_for_IDEAS.pdf`, `data/PhD_Thesis_Final_Chapter2_CollagenProduction_HOJBERG.pdf`.
- Detailed scientific specification and caveats: `spec.md`.

## Mandatory safeguards (MUST NOT)
- MUST treat the interview as the authoritative source for the owner's stated goals, data-generation account, caveats, and expectations. Distinguish those statements from anything inferred from files or proposed as a future analysis.
- MUST inspect and document the actual workbook sheets, columns, entries, measurement definitions, units, and coding before interpreting results. The interview's expected workbook layout is not verification of its actual contents.
- MUST NOT treat measurements normalized within different Western-blot gels as directly comparable across gels. The owner explicitly warned that three gels were normalized by their own mean intensities and cannot be directly compared.
- MUST NOT silently combine the separate fourth/validation gel with the three original gels. The owner says it must be treated as a separate experiment; any proposed cross-gel ranking/weighting needs explicit method, assumptions, and owner confirmation.
- MUST NOT imply that correlation establishes causation, mechanism, or a generally transferable secretion rule.
- MUST NOT treat predicted structures (including any AlphaFold output) as evidence of secretion performance or as validated biological mechanisms.
- MUST NOT claim reliable machine-learning prediction, generalization to other proteins/protein lengths, or experimentally validated improvement from this small dataset. Any suggested new sequences are hypotheses for testing, not proven high-secretion designs.
- MUST NOT assume an exact secretion threshold, formal high/medium/low labeling rule, statistical significance criterion, validation split, structure-prediction method, or confidence cutoff: these are UNKNOWN / TO VERIFY or require a stated analysis decision.
- MUST NOT use the four observations mentioned for other proteins as an interchangeable validation/training set without documenting their distinct protein context and limitations.
- MUST NOT fill in missing assay details, replicate structure, units, biological meaning, or coding from guesswork. Mark them UNKNOWN / TO VERIFY.
- MUST NOT start interpretation from filenames, transcript transcription artifacts, or presumed biological conventions when the original data definitions are available to check.

## Known ways analysis can mislead
- Within-gel normalization can create apparent cross-gel differences or erase comparability; gel is an experiment/batch boundary.
- Restricting analysis to top candidates can create selection bias and conceal whether a feature distinguishes good from poor secretion. The owner specifically warns against analyzing only the best candidates.
- Different collagen/protein lengths or identities can change secretion behavior and confound apparent signal-peptide associations.
- The four other-protein observations are a limited check, not a robust retraining/validation set; length and protein context may confound comparison.
- Approximately 32 candidates is a small dataset relative to the number of sequence-derived, structural, and physicochemical features that might be explored. Avoid overfitting and overclaiming.
- Structure may be an exploratory feature, but a predicted structural pattern is not automatically interpretable as better secretion.

## Detailed specification
Follow `spec.md` for the source-attributed scientific specification, inventory, explicit unknowns, comparisons, evidence standards, and definition of done. Do not analyze the dataset or write analysis code until separately asked to do so.
