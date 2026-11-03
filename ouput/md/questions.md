# Questions for the data owner

These questions target information that is not established by the supplied workbook or analysis notes. Clarifying them would help interpret the measurements, the `other_protein_categories_heatmap.png`, and any follow-up analysis. The questions are grouped by priority; where possible, source protocols, raw files, or construct maps would be especially helpful.

## 1. Numeric results and assay interpretation

1. **What exactly is each “Fold-change” value?** Please provide the formula, numerator and denominator, and clarify whether the value is normalized per replicate, per blot, or in another way. The interview describes division by the mean intensity of the gel; is that precisely how these workbook values were calculated?
2. **What does a larger value mean biologically?** Is it a relative Western-blot band intensity for extracellular collagen, and can it be interpreted as more secreted protein? Could differences in expression, cell lysis, degradation, processing, loading, transfer, or antibody detection also affect it?
3. **Can the raw densitometry measurements and processing details be shared?** This includes original blot/image files if available, background subtraction, band-selection rules, exposure/saturation checks, loading or normalization controls, and any excluded measurements.
4. **What is the origin of the exact zero for SP9 in Blot 2?** In meeting 2, you said it likely represents no secretion but were unsure of its origin. Can raw densitometry or assay records establish whether it is a measured zero, no detectable band/below detection, or another encoding, and how should it be handled?
5. **What exactly are the replicate units and independence structure?** In meeting 2, you described them as biological (and “in a way, both”). What does each replicate label correspond to—independent cultures, technical repeats, or a combination—and were any measurements repeated from the same sample?
6. **What experimental conditions were held constant or varied** across peptides and blots (strain, culture, induction, sample volume, collection time, gel/blot protocol, antibody, exposure, and batch)? Were controls included, and where are they recorded?
7. **Can you confirm the ordering clarification?** In meeting 2, you said peptide columns run left-to-right in ascending mean replicate fold-change, mainly for presentation aesthetics. Does that apply to all four blocks, and are there any exceptions?

## 2. Validation blot and cross-blot comparability

8. **How was the validation blot designed?** Were its seven peptides selected in advance, and were they run alongside any shared reference or control samples?
9. **Is the validation blot normalized in the same way as the three original blots?** Does it have a common calibrator or other basis for comparing values between blots? What was meant by the suggestion of a weighted/cross-gel ranking?
10. **Should the validation measurements be treated as a separate replication of the same assay or a distinct experiment?** Are there conditions or protocol changes that could explain the observed shifts relative to the original blot?

## 3. Other-protein category table and heatmap

11. **What do the labels `High`, `Medium`, `Low`, and `No` mean?** Are they visual judgments, thresholds on densitometry, relative rankings, or another classification? Please provide the definitions/cutoffs and the underlying numeric measurements, if available.
12. **Can you confirm whether `No` means the product was not produced for every construct/category entry?** Meeting 2 clarified that it means not produced rather than missing or untested; the heatmap retains it as a categorical label, not a numeric zero.
13. **What is the provenance of the table?** Were these categories measured experimentally with the same assay as the main screen, inferred from another source, or assigned by another method? How many replicates and what controls support each cell?
14. ~~Can you confirm `S19` → `SP19`?~~ **Resolved in meeting 2:** the owner confirmed that `S19` refers to `SP19`.
15. **Partly resolved in meeting 2:** the owner confirmed `Np` was intended as `No`. The corrected workbook also changes Greek-eta `Ηigh` to `High`; please verify this correction against source records if possible.
16. **Can you confirm the exact identity and composition of each protein construct/column?** In particular, what are the sequence boundaries and meaning of “Procollagen (It is like Procollagen wIth N,C propeptides),” and how do the `Alpha1`/`Alpha2`, C-propeptide, tropocollagen, `Bacola225`, and `Bacola110` constructs differ?
17. **Were the four signal peptides chosen for this table selected in any particular way?** Are they intended as representative examples, top performers, or a convenience subset? This affects whether the table can support any general claim about transfer across proteins.

## 4. Sequence and construct definitions

18. **Can you provide verified construct maps or sequence records** for each signal-peptide fusion and target protein, showing start/end boundaries, linker/tag residues, cleavage-site annotation (if known), and the exact sequence used experimentally?
19. **What does the 327-nt `Bacola110` nucleotide sequence encode?** Its length is not three times the listed 108-aa sequence. Does it include a stop codon, cloning sequence, tag, or other untranslated/additional bases?
20. **Are the nucleotide sequences codon-optimized, and for which host?** Do they represent the complete expressed coding region or only a peptide/protein segment? Are the listed amino-acid and nucleotide sequences confirmed to correspond to the constructs used in the assay?
21. **Are the signal peptide boundaries experimentally defined or predicted?** If predicted, which method/version and cleavage-site assumptions should be used for sequence-feature analysis?
22. **NEW — Does `SP31` begin with M rather than V?** The listed amino-acid sequence for `SP31` starts `VRKSLITLGLASV…`, but its own nucleotide sequence starts `ATG`, which translates to **M**. Residues 2–30 agree exactly, all 31 other peptides begin with M, and `ATG` is the initiator codon. This is the only amino-acid/nucleotide disagreement in the entire sequence sheet. It looks like the same kind of transcription slip as `S19`, `Np` and the Greek `Η`, but it has **not** been corrected — please confirm which letter is right. See `feature_definitions.md` §1.
23. **NEW — The C-terminal A-S-A is engineered; please confirm and explain the design.** All 32 peptides end in **A-S-A**. Checking each against its native UniProt sequence (reviewed *B. subtilis* 168) shows the native endings are diverse — ASA 12, AHA 3, AKA 3, AEA 2, ADA 2, and one each of AQA, AGA, ANA, VQA, AYA, AFA, VFA and LAG. **Only 8 of 32 supplied peptides match their native signal peptide exactly, and 18 of 30 annotated ones differ at the C-terminus.** So the cleavage region was deliberately standardised rather than inherited. Was that the intent, and was A-S-A chosen for a particular reason? See `ddls_claude/analysis/uniprot_native_sp_comparison.csv`.
23a. **Were some peptides also changed in length?** Six differ from the annotated native signal peptide: SP1/amyE is 6 residues longer, SP8/phoA 10 shorter, SP14/yncM 5 shorter, SP10/vpr 3 longer, SP16/yocH 2 shorter, SP30/bsn 2 longer. Were these deliberate boundary choices, or does the construct include extra residues? (UniProt SIGNAL annotations are often predictions, so part of this may be annotation disagreement rather than construct design.)
23b. **Could modification explain some poor performers?** SP1/AmyE — the classic *B. subtilis* secretion tag — ranks 7th of 8 in its blot, and is among the most-modified peptides in the set (native ending LAG, not an A-x-A motif at all, plus six extra residues). Is it possible that the modification rather than the native peptide drove the poor result? The same question applies to SP8/phoA.
24. **NEW — Can the RBS / 5′UTR and terminator context now be supplied?** You offered this in meeting 2. Without the upstream sequence, the mRNA folding energies computed here start at the signal peptide's own start codon and are therefore **not** the translation-initiation-region folding energy that Fu et al. reported. Supplying the shared upstream context would let that specific published observation be checked properly rather than approximated.

## 5. Data provenance and recommended next steps

22. **Can the workbook’s corrected labels be checked against the original notebook/source records?** Please indicate whether the corrected workbook is the authoritative version and whether any other cell values or IDs need correction.
23. **Are there additional assay records or metadata** (sample sheets, culture-level identifiers, batch/date, gel maps, raw values, protocol versions) that should accompany the workbook for reproducible analysis?
24. **What is the primary scientific question and intended decision?** Is the goal to describe within-blot patterns, identify promising candidates for repeat testing, test sequence-feature associations, or predict performance in new protein constructs?
25. **What evidence would you consider sufficient to compare candidates across blots or across protein constructs?** For example, would a shared reference sample, repeated candidates across batches, quantitative standards, or a larger independent validation set be feasible?

## Meeting 2 updates and remaining priorities

Meeting 2 clarified the owner-reported two-stage normalization (total lane-protein normalization, then division by the gel-wide mean of normalized band intensities), replicate description (biological, exact unit/independence unclear), left-to-right ascending mean ordering, `S19` → `SP19`, `Np` → `No`, and `No` meaning product not produced. The owner interprets the SP9 zero as likely no secretion but is unsure of its origin. The owner may be able to provide band-intensity files (possibly normalized and/or raw), and recalled a possible secondary band but did not identify the peptide.

Priority follow-up: **(1)** obtain intensity/normalization records to audit the method and zero; **(2)** clarify replicate units/independence and any secondary-band identities; **(3)** resolve `High`/`Medium`/`Low` category definitions/provenance and verify `Ηigh` → `High`; **(4)** confirm validation-blot design/comparability. The transcript also indicates that RBS/start/stop/terminator context may be available if nucleotide initiation features are pursued.
