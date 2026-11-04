# Data and workbook guide

## Purpose and source boundaries

This guide describes the supplied workbook `data/Information_for_Baris.xlsx` (original, unchanged) and the context relevant to the collagen-secretion project. The workbook is an observed source; the interview transcript `data/20261020_pi_transcript.txt` is the authoritative source for what the data owner says about the experiment. The supplied PhD thesis chapter provides project-specific scientific context, while the supplied paper provides context from a different *Bacillus subtilis* signal-peptide study. These sources should not be conflated.

The owner describes screening about 32 signal peptides for secretion of recombinant collagen in *B. subtilis* and quantifying Western-blot bands by densitometry. The owner says measurements in the three original gels were normalized to each gel's mean, and therefore warns against direct pooling across those gels. The workbook itself labels values “Fold-changes,” but does not specify units or calculation. Keep each blot as a separate measurement group unless a documented calibration is justified. The fourth/validation blot is a separate experiment, not interchangeable with the original gels.

This document explains workbook layout and terminology; it does not perform feature–secretion association analysis.

## Workbook sheet guide

### 1. `Information for feeding`

**Role:** Sequence inventory for the main screen: one collagen construct and the 32 candidate signal peptides. It links peptide identifiers (`SP1`–`SP32`) with source labels and amino-acid/nucleotide sequence strings. This is essential for identifying the tested candidates and, later, for mapping any pre-specified sequence feature to its measured peptide. The sheet alone does not say which peptide performed better.

**Columns observed:**
- `Protein for coupling with secretion signal peptides`: the sheet includes `Bacola110`.
- `Origin`: source annotation as written in the workbook.
- `AA Sequence`: amino-acid sequence string.
- `Nt Sequence`: nucleotide sequence string (`Nt` means nucleotide).
- `SP Name`, `SP origin`, `AA Sequence`, `Nt Sequence`: signal-peptide identifiers, origin annotations, and sequences.

The sequence strings and labels are workbook observations, not independent verification of sequence provenance, construct boundaries, codon optimization, or amino-acid translation. In particular, the workbook does not explicitly document every sequence boundary or whether the listed nucleotide sequence includes extra cloning/tag residues.

### 2. `Results`

**Role:** Replicate-level numeric band-intensity-derived values for the 32 main candidates, grouped into `Blot 1`, `Blot 2`, and `Blot 3`, plus a separate `Validation blot` block. It is the workbook's outcome sheet and is the only sheet giving replicate numeric values for the main signal-peptide screen.

**Structure observed:** The first three blocks contain 8, 13, and 11 peptides respectively, each with three replicate rows. The separate validation block includes seven peptides shared with the main blocks and four replicate rows. The workbook does not report raw band intensity, a defined denominator, units, assay conditions, or an explicit biological/technical replicate distinction. The owner states that original blot values were normalized against each gel's mean; that statement cannot be independently verified from the workbook alone.

**Interpretation safeguard:** Values labeled “Fold-changes” are not absolute secretion yields. Preserve the original blot grouping. Do not pool or compare separately normalized main-gel values as one common scale. Treat the validation blot as a distinct experiment. One observed value is exactly zero for SP9 in Blot 2; the workbook does not say if it represents true zero, below-detection measurement, or a code. Preserve as recorded unless the owner/source records clarify it.

### 3. `SP and other collagen proteins`

**Role:** A small categorical table describing four secretion-tag labels across seven other protein constructs, followed by amino-acid and nucleotide sequences for those constructs. It supplies context about whether chosen tags appeared to behave similarly with other collagen constructs/lengths. It is not a second replicate-level quantitative version of the main screen.

**Categorical columns observed:** `Bacola225`; `Alpha1 with C propeptide`; `Alpha2 with C propeptide`; `Alpha1 w/o C propeptide`; `Alpha2 w/o C propeptide`; `Tropocollagen`; and `Procollagen (It is like Procollagen wIth N,C propeptides)`. Values are categorical (`High`, `Medium`, `Low`, `No`), not numeric measurements. The workbook does not define category thresholds or explain what `No` means. Treat these as uncalibrated labels until their provenance and meaning are confirmed.

The source workbook contains three apparent anomalies: `S19` as a row identifier (the other sheets contain `SP19`); `Ηigh` with Greek capital eta rather than Latin H; and `Np`. The requested corrected copy changes these to `SP19`, `High`, and `No`, respectively. Those are editorial corrections requested by the project owner, not independently verified reinterpretations. The unchanged source is retained as `data/Information_for_Baris.xlsx`; corrected copy is `data/Information_for_Baris_corrected.xlsx`. Do not regard the correction itself as evidence for the meaning of the category system.

## Glossary and abbreviations

| Term / abbreviation | Meaning in this project |
|---|---|
| `AA` | Amino acid; `AA Sequence` is a protein sequence written using one-letter amino-acid codes. |
| `Nt` | Nucleotide; `Nt Sequence` is a DNA/RNA sequence written as nucleotide bases. In the workbook the sequences appear DNA-like (A/C/G/T), but column label is simply `Nt`. |
| `SP` | Signal peptide / secretion tag. Workbook IDs such as SP1–SP32 identify candidate N-terminal signal sequences. The thesis sometimes uses “secretion tag” for the signal sequence. |
| `SP1`–`SP32` | Candidate peptide identifiers. The number is an ID, not a performance score or rank. |
| `B. subtilis` | *Bacillus subtilis*, the bacterial host used in the project described by the owner and thesis. |
| `B. stearothermophilus` | *Bacillus stearothermophilus*, source species of AmyS in the supplied 2018 paper. |
| `Bacola110` | Workbook name for the short collagen construct used with the main signal-peptide screen. The thesis calls the original 110-amino-acid construct `BsbColv2`; the workbook's `Bacola110` and thesis name should not be silently treated as identical without confirming naming/boundaries. |
| `Bacola225` | Name used in the thesis and workbook for an extended collagen construct of about 225 amino acids (thesis). |
| `BsbColv2` | Thesis name for the initial bovine type I alpha I collagen-derived construct; described in the thesis as 110 aa / approximately 10 kDa. |
| `Alpha1`, `α1`, `a1[I]` | Alpha-1 chain of type I collagen (the thesis uses alpha I / α1[I] notation). `Alpha2`/`α2` means the alpha-2 chain. The `[I]` denotes collagen type I, not a mathematical index. |
| `C-propeptide` | C-terminal propeptide region of procollagen. In native collagen biology, propeptides participate in chain association/folding and are removed during maturation. In the thesis, constructs with and without C-propeptide were tested. |
| `N-` / `C-terminal` | At the amino (N) or carboxyl (C) end of a protein sequence. Signal peptides are N-terminal; propeptides can occur at termini. |
| `w/o` | “Without.” Thus `Alpha1 w/o C propeptide` means the alpha-1 construct without its C-propeptide. `w/` means “with.” These abbreviations describe construct composition, not assay outcomes. |
| `Tropocollagen` | Mature, full-length collagen molecule after removal of procollagen propeptides. The supplied thesis describes a type I alpha I tropocollagen construct and distinguishes it from procollagen. |
| `Procollagen` | Collagen precursor containing N- and C-terminal propeptides. It is not synonymous with tropocollagen. The workbook's parenthetical description is retained as written and is not a precise construct definition. |
| `Collagen type I` | Fibrillar collagen built physiologically from two α1(I) chains and one α2(I) chain; the thesis describes this 2:1 composition. A single alpha chain construct is not the complete native heterotrimer. |
| `Triple helix` | The characteristic collagen structure formed by three collagen chains winding together. The thesis reports circular-dichroism evidence for triple-helical structures in its constructs; this does not establish a secretion mechanism for a signal peptide. |
| `Hydroxyproline` / hydroxylation | Proline modified by addition of a hydroxyl group. The thesis discusses prolyl-4-hydroxylase (P4H) and collagen hydroxylation; this post-translational modification is distinct from signal-peptide secretion. |
| `Codon-optimized` | A DNA coding sequence whose synonymous codons have been adapted to a host's preferences while retaining the encoded amino-acid sequence. This is stated for constructs in the thesis; the workbook does not itself consistently mark sequence optimization status. |
| `Fold-change` | A ratio-like relative quantity. Workbook heading uses this label; owner says band intensity divided by the mean intensity of its gel. Exact calculation and units remain undocumented in workbook. Do not interpret as absolute titer. |
| `Replicate` / `Repli.` | Repeated measurement label in Results. Biological versus technical replicate status is not specified by workbook. |
| `Blot` | Western blot experiment/gel grouping as labeled in Results. A blot-specific normalization means numerical values across blots may not share a common scale. |
| `Validation blot` | Workbook label for the separate block with seven shared peptides and four replicate values. Owner describes a fourth validation gel as a separate experiment; calibration/comparability details are not supplied. |
| `Western blot` | Antibody-based method to detect a protein separated by gel electrophoresis and transferred to a membrane. Band intensity is used here as a relative proxy; absolute secretion interpretation requires assay validation. |
| `Densitometry` | Quantifying signal intensity of image bands. Owner says this was used to compare secretion candidates. Raw values and image-processing details are not in workbook. |
| `MW` / `kDa` | Molecular weight / kilodalton (a unit of molecular mass). Apparent gel mobility can differ from predicted mass, especially for collagenous proteins, as discussed in the thesis. |
| `POI` | Protein of interest; the target protein fused downstream of a signal peptide. |
| `Sec-type` / `Sec pathway` | Protein secretion route involving the Sec translocation machinery. The 2018 paper concerns Sec-type signal peptides; this is literature context, not a pathway assignment independently demonstrated for each workbook construct. |
| `N-domain`, `H-domain`, `C-domain` | Conventional signal-peptide regions: N-terminal positively charged region, hydrophobic core, and C-terminal region around the cleavage site. Boundaries are predictions/conventions and are not annotated for the workbook peptides. |
| `Cleavage site` | Position where signal peptidase removes the signal peptide from the mature protein. The workbook does not report cleavage measurements. |
| `mRNA` | Messenger RNA, the transcript translated into protein. Predicted RNA structure near translation initiation can affect expression, but no such feature has been measured in this workbook. |
| `RBS` / `Shine–Dalgarno (SD)` | Ribosome-binding site / bacterial sequence motif that helps position the ribosome for translation initiation. The 2018 paper proposes that RNA structure around this region can affect translation; this is a paper-specific interpretation. |
| `TIS` | Translation initiation site. Used in the 2018 paper's predicted mRNA folding analysis. |
| `pI` | Isoelectric point: pH at which a protein has zero net electrical charge. |
| `Gibbs free energy` (`ΔG`) | Thermodynamic quantity used by the paper's software to estimate RNA folding stability; more negative predicted values generally indicate more stable predicted folding under specified model conditions. Not a direct secretion measurement. |
| `D-score` | SignalP prediction score used in the supplied paper as a signal-peptide-related predictor. It is a tool output, not a direct experimental secretion result. |
| `AlphaFold` | Protein-structure prediction system. A predicted structure is not an observed structure and does not by itself establish secretion or mechanism. The project interview mentions AlphaFold as an expected possible tool; this workbook guide makes no structure predictions. |
| `High`, `Medium`, `Low`, `No` | Categorical strings in the third workbook sheet. Their thresholds and provenance are undocumented in the workbook; `No` must not automatically be interpreted as zero secretion or not tested. |
| `His tag` | Histidine-rich affinity/detection tag often used for protein purification or antibody detection. The thesis sequences include His-tag residues; exact boundaries need construct records. |
| `KO7S` | Strain label appearing in the thesis as a negative-control source; the acronym expansion is not defined in the supplied material, so no expansion is assumed. |
| `glmS` | Genomic locus targeted for construct integration, as described in the thesis. |
| `GRAS` | “Generally recognized as safe,” regulatory/industrial terminology used in the thesis to describe *B. subtilis* as a production host. |
| `P4H` | Prolyl-4-hydroxylase, enzyme that catalyzes proline hydroxylation. Thesis names BaP4H (from *Bacillus anthracis*) and MimiP4H (from Giant Mimivirus). |
| `CD` | Circular dichroism, spectroscopy used in the thesis to assess collagen triple-helix formation. |
| `SDS-PAGE` | Sodium dodecyl sulfate polyacrylamide gel electrophoresis, a method for separating proteins by apparent size. |
| `AmyS` | Alpha-amylase from *Geobacillus stearothermophilus* used as the reporter target in the supplied Fu et al. study; not the collagen target of the workbook. |
| `HTP` | High-throughput; the 2018 study describes high-throughput screening of a signal-peptide library. |
| `USER cloning` | Uracil-specific excision reagent cloning, a DNA assembly approach mentioned in the thesis. |
| `BaP4H` | *Bacillus anthracis* prolyl-4-hydroxylase, as named in the thesis. |
| `MimiP4H` | Prolyl-4-hydroxylase from Giant Mimivirus, as named in the thesis. |
| `OD600` | Optical density measured at 600 nm, used as an estimate of culture turbidity/biomass in the supplied paper. |
| `U/mL` | Enzyme activity units per millilitre, used for the amylase assay in Fu et al.; not a unit used for the workbook collagen fold-change values. |
| `A-X-A` | Amino-acid motif pattern (any residue X between alanines) discussed in the paper as a potential signal-peptide cleavage motif. |
| `MUSCLE` | Multiple-sequence alignment software used in Fu et al. to align signal-peptide regions. |
| `mfold` | RNA secondary-structure prediction software/web server used in Fu et al. |
| `MEGA` | Molecular Evolutionary Genetics Analysis software, used in the paper's sequence-analysis workflow. |
| `USER` | Uracil-specific excision reagent; appears in the thesis as a cloning method. |
| `Gibson assembly` | DNA assembly method named in the thesis for extending collagen constructs. |
| `cDNA` | Complementary DNA made from RNA; the thesis reports amplifying bovine collagen sequences from bovine skin cDNA. |
| `KO` | Knockout, in the thesis strain/control label `KO7S`; the exact strain-label expansion is not confirmed here. |
| `TBS-T` | Tris-buffered saline with Tween detergent, a buffer name present in the thesis methods. |
| `IPTG` | Isopropyl β-D-1-thiogalactopyranoside, an inducer of the pgrac100 expression system discussed in the thesis. |
| `PrsA` | Bacillus foldase/protein quality-control factor mentioned in the supplied paper's background/references; not a workbook variable. |
| `HTP` | High-throughput; the 2018 study describes high-throughput screening of a signal-peptide library. |

## Terminology cautions

- **Signal peptide vs secretion tag:** Used somewhat interchangeably in project materials. The signal peptide is the N-terminal sequence that directs export and is commonly cleaved; “tag” may refer more broadly to the construct component. Confirm exact fusion boundaries before sequence-level analysis.
- **Secretion vs production/expression:** A Western-blot band in culture supernatant is evidence of detected extracellular protein, but production, release, degradation, processing, and detection can all affect signal. The workbook values should not automatically be called absolute secretion rates.
- **Alpha and tropocollagen:** “Alpha” names collagen polypeptide chains (α1(I), α2(I)); tropocollagen is mature collagen after propeptide removal. Neither term is a synonym for a signal peptide.
- **Ranked:** “Ranked” appears in Results block titles, but the workbook does not state ranking method, and columns are not a straightforward sorted ordering of all replicate values. Do not infer rank from column position.
- **Correction vs verification:** The corrected workbook applies exactly the requested string substitutions. The original remains available. Correction does not resolve scientific uncertainty about what categories mean.
