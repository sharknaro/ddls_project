# Can external literature improve prediction performance?

Review of the two supplied papers plus a literature search on *B. subtilis* signal-peptide
research, assessed specifically against two questions:

1. Can the Western-blot densitometry assay be compared or calibrated against published assays?
2. Can anything in the literature improve prediction performance beyond the null result found
   on the 32-peptide dataset?

Analysis outputs for this review are in `ddls_claude/analysis/`.

---

## Headline

**The single most valuable thing found is not a model or a dataset — it is that the 32 peptides
are identified.** The thesis chapter's plasmid and primer tables name every one of them as a
specific native *B. subtilis* 168 signal peptide. They are not anonymous sequences.

That changes what is possible: the library can now be joined to published screens of the same
peptides. The first time that join is made, it produces a result that **argues against**
borrowing published models — see §3.

A second concrete find: the thesis states that every construct carries an **identical RBS and
5′UTR** immediately upstream of the start codon (`AGGAGGAATATAC` + `ATG`). That answers one of
the open questions in `questions.md` and makes a properly defined translation-initiation
folding energy computable — **and when computed, it produces the first positive association in
this project.** See §0.

---

## 0. The one positive result: mRNA accessibility at the translation-initiation region

Fu et al. propose that a **less negative** folding free energy near the translation-initiation
region leaves the ribosome-binding site and start codon accessible, favouring secretion. That
is a directional hypothesis stated in the literature, not one invented here. It was previously
untestable because the 5′ context was unknown; the thesis supplies it.

Recomputing the folding energy over the **shared 5′ context plus the first 48 bases of each
signal peptide's coding sequence** gives:

| | Blot 1 | Blot 2 | Blot 3 | Combined |
|---|---:|---:|---:|---:|
| `dg_rbs_plus48` | **+0.26** | **+0.63** | **+0.49** | **+0.51** |
| previous coding-sequence-only version | −0.44 | +0.19 | +0.35 | +0.11 |

**Positive in all three independently normalised blots, in the direction the literature
predicts.** Permutation test (20,000 within-blot permutations, one-sided):

- **p = 0.0042** treating it as a single pre-specified hypothesis
- **p = 0.012** correcting for the family of three window sizes (30/48/60 nt)

Robustness (`rbs_hypothesis_test.csv` and checks):

| Check | Combined ρ |
|---|---:|
| Headline | +0.515 |
| Median instead of mean outcome | +0.449 |
| Excluding SP9 (the recorded zero) | +0.484 |
| Excluding SP23 (unstable replicates) | +0.501 |
| Excluding SP4 (secondary band) | +0.594 |
| Leave-one-peptide-out range | +0.466 to +0.594, **no sign flips** |

**Not simply a proxy for something else.** The feature correlates moderately with GC content
(ρ = −0.39), length (+0.39) and GRAVY (−0.39), but those descriptors tested on their own give
combined ρ of **−0.02** (GC) and **+0.25** (length). The association does not survive as a GC
or length effect.

### How much weight this deserves

More than anything else in the project, but not yet a finding to build on:

- It is **one hypothesis with a direction specified in advance by the literature**, which is why
  it is tested against a single-hypothesis null rather than the best-of-34 screen null (0.60)
  that governs §4 of the main report. Judging it by the screen null would be the wrong test;
  treating it as confirmed would be the wrong conclusion.
- **It is not fully independent of the earlier exploratory work.** A coding-sequence-only
  version of this feature family was in the 34-feature screen and ranked second. This is a
  refinement of a family already examined, not a clean out-of-sample confirmation, and that
  should be stated plainly in any write-up.
- **The window is still approximate.** The true transcription start site of the P3P promoter is
  not stated, so the real initiation region is longer than the window used. Fu et al. used
  170 nt from the transcription start site.
- **No mechanism is established.** Folding energy is a computed quantity, and an association in
  32 peptides across three blots is not evidence that mRNA structure causes the difference.
- n is still 32, and the measurement reliability ceiling is about 0.86, so ρ ≈ 0.5 is a moderate
  effect against that ceiling, not a strong one.

**What would settle it:** the actual transcript start site and full 5′UTR from the owner, so
the window matches the published definition; and ideally a prospective test — design or select
peptides that differ in predicted initiation-region accessibility while holding composition
roughly constant, and measure them on one gel.

---

## 0b. The A-S-A ending is engineered, not inherited

Checked all 32 against their native UniProt sequences
(`ddls_claude/analysis/uniprot_native_sp_comparison.csv`, reviewed *B. subtilis* 168 entries,
taxid 224308). The result is unambiguous.

**Native C-terminal tripeptides are diverse. The supplied ones are not.**

| | Native (UniProt SIGNAL annotation) | Supplied |
|---|---|---|
| ASA | 12 | **32** |
| AHA | 3 | 0 |
| AKA | 3 | 0 |
| AEA, ADA | 2 each | 0 |
| AQA, AGA, ANA, VQA, AYA, AFA, VFA, LAG | 1 each | 0 |

- **Only 8 of 32 supplied peptides match their native signal peptide exactly.**
- **18 of 30 annotated peptides have a C-terminus that differs from native.**
- Six also differ in length: SP1/amyE is 6 residues longer than annotated, SP8/phoA 10 shorter,
  SP14/yncM 5 shorter, SP10/vpr 3 longer, SP16/yocH 2 shorter, SP30/bsn 2 longer.
- SP17/yqxI and SP21/ywtF have no SIGNAL annotation in UniProt, so they cannot be checked.

So the uniform A-S-A is a **deliberate standardisation of the cleavage region across the
library**, not a property inherited from the source genes. That answers question #23 and is a
defensible design choice — it holds signal-peptidase processing constant so that other
differences stand out. It also means the library was never able to report on C-region effects,
by construction.

### Three consequences

**1. These are engineered peptides, not wild-type ones.** Any comparison to published results on
"the pel signal peptide" or "the amyE signal peptide" compares *different molecules*. SP6/Pel
natively ends ANA, not ASA; SP1/AmyE natively ends LAG — not an A-x-A motif at all — and is also
six residues longer here.

**2. The cross-assay result in §3 is weaker than it first appeared.** Its five peptides are not
the same sequences Fu et al. measured. The finding that amylase performance does not predict
collagen performance is therefore confounded with the C-terminal modification, and should be
reported as suggestive at best. It does not change the direction of the conclusion — target
dependence is independently documented — but it removes it as clean evidence.

**3. A new candidate explanation for some of the poor performers.** SP1/AmyE is the classic
*B. subtilis* secretion signal peptide and ranks 7th of 8 in its blot. It is also one of the
most heavily modified peptides in the set: LAG → ASA plus six extra residues. The possibility
that modification, not the native peptide's intrinsic quality, drove its poor showing is worth
putting to the owner. The same applies to SP8/phoA (10 residues shorter than annotated).

**Caveat on the reference.** UniProt SIGNAL annotations are frequently predictions rather than
experimentally determined cleavage sites, so "native" here means "as annotated". Where the
annotation came from a predictor, a length disagreement may reflect the predictor rather than
the construct. The C-terminal composition result does not depend on this: a 32-of-32 uniform
A-S-A against a 13-way-diverse annotated background is not an annotation artefact.

---

## 1. The SP identity map (needs owner confirmation)

From the thesis plasmid aliases pBS008–pBS039 and primer names PRB7–PRB70:

| | | | |
|---|---|---|---|
| SP1 AmyE | SP9 PhoB | SP17 YqxI | SP25 SacC |
| SP2 AprE | SP10 Vpr | SP18 YvgO | SP26 AbnA |
| SP3 Bpr | SP11 XynA | SP19 YwaD | SP27 BglS |
| SP4 Epr | SP12 YbdN | SP20 YweA | SP28 YolA |
| SP5 Mpr | SP13 YlqB | SP21 YwtF | SP29 Csn |
| SP6 Pel | SP14 YncM | SP22 YxaL | SP30 Bsn |
| SP7 PenP | SP15 YoaW | SP23 NprB | SP31 CwlO |
| SP8 PhoA | SP16 YocH | SP24 SacB | SP32 EglS |

Full table with each peptide's standing in its own blot:
`ddls_claude/analysis/sp_gene_identity_and_standing.csv`.

This is read from the thesis, not from the supplied workbook, and the thesis's strain table is
off by one row in the PDF text layer (the mapping above uses the plasmid aliases, which are
self-consistent). **It should be confirmed by the owner before being relied on.** Note that
SP31 = CwlO is also the peptide with the unresolved V/M discrepancy from
`feature_definitions.md` §1.

The thesis gives **no stated criterion** for why these 32 of roughly 170 *B. subtilis* signal
peptides were chosen — not hydrophobicity, length, charge, native secretion level, or Sec/Tat
class. That is worth asking about, because a selection rule would bear directly on why the
library might span a narrow feature range.

---

## 2. What the two supplied papers actually offer

### Fu et al. (2018) — weaker evidence than it appears

Re-screened in full. The important finding is methodological: **their feature analysis is less
rigorous than the one already done here, and its headline is a visual impression.**

- Their feature analysis uses **n = 16** — the 15 selected best performers plus the wild-type
  signal peptide. The 173-member library was never used for feature analysis; features were
  never computed for poor performers.
- **No correlation coefficient and no p-value appears anywhere in the paper.** The "rising
  pattern" between mRNA folding energy and secretion is a scatter plot read by eye.
- Their sequence logos are built from 15 selected positives with **no negative set**, which is
  exactly the selection bias the data owner warned against.
- They explicitly report **no correlation** between secretion and SignalP D-score, and none
  with pI.
- Their own conclusion is that *in silico* prediction of the optimal signal peptide for a given
  target is not currently feasible, and that library screening is the practical route.

So this paper **corroborates the null result rather than contradicting it.** Their one
positive-looking trend is loose even within their own 15: yobB has the most negative ΔG
(−40.2 kcal/mol) yet mid-range activity.

**Assay comparability: not possible.** They use enzyme activity (starch–iodine microplate, and
DNS for the fermenter), never a Western blot. No specific activity (U/mg) is reported, so
activity cannot be converted to protein mass. The only shared currency with a densitometry
measurement is *fold-change relative to a reference construct*.

Usable: 15 peptides with U/mL values, plus their Table 2 features (N/H/C domain strings,
SignalP 4.1 D-score, ExPASy pI, mfold ΔG).

### The thesis chapter — the missing assay metadata, and what it confirms

The protocol is now documented: Bio-Rad 4–20% gradient gels, iBlot 2 transfer, **Ponceau S
total-protein staining as the only loading control** (no housekeeping protein), anti-His mouse
monoclonal (Merck 05-949) 1:1000, anti-mouse HRP (Cytiva GENA9310) 1:15000, ECL Prime, GE
AI600 CCD imager, quantified in **ImageLab (Bio-Rad)**.

The normalisation matches the owner's meeting-2 account exactly: per-lane Ponceau total protein
→ normalisation factor applied to chemiluminescence → divide by the mean of normalised
intensities **on that same membrane**.

What it confirms about cross-blot comparison — and this is the important part:

- The calibrator is **the gel's own mean, not a physical reference lane**. There is no shared
  calibrator sample, no reference strain, and no dilution series on the screen gels.
- **Nothing in the method permits cross-gel comparison.** A fold-change of 1 means a different
  absolute level on each gel.
- **Which peptides were on which gel is nowhere stated**, and no grouping rationale is given.
- Not documented anywhere: exposure time, background-subtraction method, saturation or
  linearity checks, sample volumes for the screen, statistical test, or n per group.
- Replicates are full independent production runs (inoculation → blot), repeated at least three
  times — genuinely biological. Plotted as mean ± **standard error**.

Two specific items that affect candidate interpretation:

- **SP4 (Epr)** is the only peptide named as consistently producing a secondary band, and the
  thesis excluded it from all later work despite its highest secretion. **Whether the
  quantification summed or excluded that secondary band is not stated** — so SP4's value is of
  uncertain meaning, which compounds the mean-vs-median instability already found for it.
- The validation gel contents are confirmed as SP2, SP3, SP4, SP5, SP19, SP26, SP32, with
  **SP2 (AprE) deliberately included as a mid-level internal control**. That matches the
  workbook exactly. Note the thesis then carries forward SP19, SP5, SP26, SP3 — SP32 is dropped
  without explanation.
- **The High/Medium/Low categories for other proteins are not documented in the thesis at all.**
  Their derivation remains unknown, so the caution in the main report stands.

---

## 3. The cross-assay test, and why it matters most

Five of the 32 peptides are also among Fu et al.'s 15 best performers for α-amylase. This
permits a direct, if small, test of whether performance transfers between target proteins.

| SP | Gene | Blot | Collagen rank | Within-blot pct | AmyS activity (U/mL) | vs native SP |
|---|---|---|---|---|---:|---:|
| SP6 | Pel | 1 | **6th of 8** | 0.38 | 1487.85 | **1.69× (their best)** |
| SP17 | YqxI | 2 | 2nd of 13 | 0.92 | 1394.15 | 1.58× |
| SP27 | BglS | 3 | 8th of 11 | 0.36 | 1379.55 | 1.56× |
| SP24 | SacB | 3 | 6th of 11 | 0.55 | 1019.10 | 1.15× |
| SP15 | YoaW | 2 | 4th of 13 | 0.77 | 871.00 | 0.99× (their weakest) |

**Spearman ρ = −0.20 (p = 0.75, n = 5).** There is no positive agreement. Fu et al.'s single
best amylase peptide, `pel`, sits in the bottom half for collagen; their weakest of the 15,
`yoaW`, sits in the top third.

The same point from a different angle — the classic, heavily used *B. subtilis* secretion
signal peptides, as they performed for collagen:

| SP | Gene | Blot | Rank |
|---|---|---|---|
| SP1 | **AmyE** | 1 | **7th of 8** |
| SP2 | AprE | 1 | 5th of 8 |
| SP6 | Pel | 1 | 6th of 8 |
| SP11 | XynA | 2 | 5th of 13 |
| SP24 | SacB | 3 | 6th of 11 |
| SP27 | BglS | 3 | 8th of 11 |

AmyE — the best-known secretion signal peptide in this organism — is second from bottom in its
blot. The top performers here are instead YwaD (SP19), AbnA (SP26), Mpr (SP5) and Bpr (SP3).

**Caveats, which are serious.** n = 5; the five peptides span three blots with no common scale,
so even their relative standing is approximate; the reporter protein, host background
(PrsA-overexpressing, protease-deficient vs KO7S), promoter and assay chemistry all differ. This
is descriptive, and a p-value of 0.75 means it is also entirely consistent with chance.

What it is *not* consistent with is a strong, transferable rule. And it matches what three
independent sources already say: Fu et al. report no correlation between cutinase and esterase
performance; SPSED reports the same; the thesis says secretion depends on the signal-peptide ×
protein-of-interest interplay.

---

## 4. External resources found, and whether they would help

### The ETH high-throughput dataset — the only one at useful scale

Grasso et al., *Signal Peptide Efficiency: From High-Throughput Data to Prediction and
Explanation*, ACS Synth Biol 2023;12(2):390. 11,643 designed signal peptide variants built from
134 wild-type *B. subtilis* templates, secretion measured by nanoliter-reactor flow cytometry,
**4,421 informative peptides** used for modelling. Random Forest on 156 physicochemical
features with TreeSHAP explanation.

Data are on **Zenodo (DOI 10.5281/zenodo.6448806) under CC BY 4.0** — supplementary tables, the
training/test data, the fitted model and the SHAP explainer. Raw reads at SRA PRJNA825264.

Their reported feature effects are directly comparable with the features already computed here:

| Their finding | Direction | Bearing on this dataset |
|---|---|---|
| GRAVY (whole SP) | optimum around **1.0**; strongly negative is bad | **non-monotonic** — a Spearman correlation cannot detect an interior optimum |
| Charge (whole SP) | below **+2** better, slightly negative best | this library's net charge at pH 7 is mean 2.49, median 2.50 — mostly *above* their optimum |
| Boman index, H-region | lower (more hydrophobic) better | same direction as the weak trend seen here |
| Glycine in H-region | high is unfavourable | computed here as `h_core9_frac_helix_breaker_GPS` |
| Pro/turn in C-region, −1 and −3 Ala | known cleavage effects, quantified | **constant in this library** (all 32 end A-S-A) |

Two of these are genuinely actionable. First, **GRAVY has an interior optimum**, which every
rank-correlation test run so far would miss by construction. Second, their region scheme
includes an **"after-cleavage" region** (first 3 residues of the mature protein) — which in this
dataset is identical for all 32 peptides, since all are fused to the same collagen. Another
constant, and another reason variation is scarce here.

**Performance caveat:** their model reports MSE of 1.22 on a 1–10 scale, with **no R² or
correlation coefficient given**. Of 15 externally tested designs, 11 fell within ±1 unit. It is
a useful model, not a solved problem, and it is validated on one protein (AmyQ) in one host.

#### What the Zenodo download actually contained

Downloaded to `ddls_claude/external/zenodo_6448806/` (CC BY 4.0). Note the record resolves to
versioned ID **6448807**; the published DOI's direct file links 404, and the API endpoint
`https://zenodo.org/api/records/6448807/files/<name>/content` is what works.

The two small tables are the **design and validation subset, not the 4,421-peptide training
set.** That set is inside the 735 MB archive, which was not downloaded.

- `Supplementary_Table_5-new.xlsx` — 99 rows of picked-clone plate assay readings.
- `Supplementary_Table_6-new.xlsx` — three sheets. `PRE_edit_SPs_info` is the useful one:
  **60 signal peptides with measured secretion (`WA`, 1 = best to 10 = worst) and 241 feature
  columns**, including Uniprot ID and gene name.

**Overlap with this library is too small to use: 4 genes** (bglS, epr, vpr, yweA), and **zero
exact sequence matches**, because the ETH entries are themselves designed variants rather than
wild-type peptides. A second cross-assay comparison is therefore not possible from these files.

**But the comparison yielded something better — independent confirmation of the cleavage
boundary.** For bglS, the ETH sequence is *exactly* this library's SP27 plus three residues:

```
SP27 (this library):  MPYLKRVLLLLVTGLFMSLFAVTATASA
ETH bglS entry:       MPYLKRVLLLLVTGLFMSLFAVTATASA QTG
```

Their `SP_aa` field is signal peptide **plus the first three residues of the mature protein**
(their "Ac" region). The exact prefix match independently confirms that the supplied sequences
end precisely at the signal-peptidase cleavage site — the assumption underpinning every
C-region feature in `feature_definitions.md`, previously unverified.

For epr, vpr and yweA the C-regions differ (e.g. SP4 ends `…GPLASA` where the ETH epr entry has
`…GPLAHA`). Since the ETH entries are designed variants, it cannot be told from this which side
departs from wild-type. **Worth checking the four against UniProt**, because if the owner's
peptides were engineered to a uniform A-S-A C-terminus rather than inheriting it, that is both
the answer to question #23 and a design decision that may itself have affected secretion.

**The feature schema is the real prize.** Their 241 columns include several things not currently
computed here and computable without new data:

- `CAI_HEG` and `CAI_RSCU` — codon adaptation indices against *B. subtilis* highly expressed
  genes. This supplies the reference set whose absence made CAI uncomputable (§3.3 of the main
  report).
- `mfe_N`, `mfe_H`, `mfe_C`, `mfe_Ac` — RNA folding energy **per region** rather than per window.
- Eight hydrophobicity scales (argos, eisenberg, janin, kyte-doolittle, hopp-woods, ez,
  bulkiness, tm_tend), plus Boman index, aliphatic index, flexibility, polarity, and
  helix/turn/sheet propensities — all per region.

### SecEff-Pred — recent, but amylase-centric

Sun et al., *J Agric Food Chem* 2026;74(8):6960 (DOI 10.1021/acs.jafc.5c14547). ESM-2 protein
language model with multitask learning and simulated data. Reported accuracy 85.6% (α-amylase),
81.6% (alkaline xylanase), 74.7% (cutinase), and 72% on external validation with phospholipase
D. Classification (efficient/inefficient), not regression. **The web server URL is not given in
the PubMed record** and would need to be obtained from the full text.

Applying it to the 32 peptides is cheap and would be a genuinely external prediction. But note
what §3 implies: every reporter it was trained on is a compact, globular, enzymatically assayed
protein. Collagen is a repetitive, Gly/Pro-rich, triple-helix-forming polymer. Expecting
transfer is optimistic, and the cross-assay result above is the first direct evidence against it.

### SPSED — small, useful as a lookup

Peng et al., *Front Bioeng Biotechnol* 2022. 1,025 signal-peptide/target-protein records from 20
experiments, at http://www.spsed.com/, batch-downloadable. Efficiency is expressed as a ratio to
the best peptide **within each source study**, so values are not comparable across studies —
the same limitation as this project's per-gel normalisation, at literature scale. It already
stores Kyte–Doolittle hydrophobicity (whole and h-region) and charge (whole and n-region). Its
own stated caveat is that the best peptide is protein-specific.

### Brockmeier et al. (2006)

*Systematic Screening of All Signal Peptides from Bacillus subtilis*, J Mol Biol 362:393 — the
acknowledged model for the thesis's approach. Worth retrieving for whether it reports
per-peptide quantitative values for these same named peptides, which would enlarge the overlap
in §3 well beyond five.

---

## 5. What would actually improve prediction, ranked

**1. Recompute the mRNA folding feature properly — now possible, and cheap.**
The thesis gives the shared upstream context: `GGCGAU` + RBS `AGGAGGAATATAC` + `ATG` + the SP
coding sequence, with the same P3P promoter and USER overhang for every construct. Fu et al.
define their feature as ΔG of a 170-nt window from the transcription initiation site. That can
now be approximated far better than the coding-sequence-only windows currently used, by
prepending the real 5′UTR before folding. The upstream sequence is shared, so it will not create
differences by itself — but it changes the folding landscape, because the RBS can pair with SP
coding sequence. This is the one feature improvement available without new data.

**2. Test GRAVY and charge for an interior optimum rather than a monotonic trend.**
The ETH result says the relationship is non-monotonic with an optimum near GRAVY 1.0 and charge
below +2. Every test run so far was rank-based and therefore blind to that shape. Worth checking
whether this library even spans the informative range — if all 32 peptides cluster near the
optimum, restricted range would be a genuine, reportable explanation for the null result, and a
more satisfying one than "no signal".

**3. Apply an externally trained model as a true external test.**
Download the ETH model (CC BY 4.0) or run SecEff-Pred, predict the 32 peptides, and correlate
predictions against measured fold-change *within each blot*. This is leakage-free by
construction — the model never saw this data. It is the cleanest available answer to "can
prediction be improved", and it is informative either way: agreement would be a real finding,
and disagreement would quantify the target-dependence that §3 already hints at.

**4. Extend the cross-assay overlap.**
Brockmeier et al. (2006) screened all *B. subtilis* signal peptides, so the overlap with these
32 named peptides may be far larger than the five available from Fu et al. A larger overlap
would turn §3 from a suggestive n=5 into something defensible.

**5. What will not help.**
Training a model on the 32 peptides themselves; adding AlphaFold structures to the same 32
outcomes; or pooling the blots. The constraint is the number of independently measured
peptides on a common scale, and no amount of external literature changes that.

---

## 6. What the literature says about assay comparability

Nothing found permits converting Western-blot densitometry into published activity units. No
specific activity is reported in either supplied paper, and the large screens are all
activity- or fluorescence-based.

The transferable lesson is about design rather than conversion: Fu et al. normalise every plate
to a **single benchmark construct** (AmyS with its native signal peptide), and the thesis used
SP2/AprE as a mid-level internal control on the validation gel only. Putting one or two
identical reference lanes on **every** gel is what would make future blots comparable, and it is
the same recommendation already in the main report — now with the observation that this project
has already done it once, on one gel, and could simply extend the practice.

---

## Sources

- [Fu et al. 2018, J Agric Food Chem 66:13141](https://pubs.acs.org/doi/10.1021/acs.jafc.8b04183) ([PubMed](https://pubmed.ncbi.nlm.nih.gov/30463403/)) — supplied as `data/Paper_for_IDEAS.pdf`
- Alexiou et al., PhD thesis chapter 2 — supplied as `data/PhD_Thesis_Final_Chapter2_CollagenProduction_HOJBERG.pdf`
- [Grasso et al. 2023, ACS Synth Biol 12:390](https://pubs.acs.org/doi/10.1021/acssynbio.2c00328) ([preprint](https://www.biorxiv.org/content/10.1101/2022.05.13.489517v1.full), [Zenodo data](https://zenodo.org/records/6448806))
- [Sun et al. 2026, J Agric Food Chem 74:6960 — SecEff-Pred](https://pubmed.ncbi.nlm.nih.gov/41709814/)
- [Peng et al. 2022, Front Bioeng Biotechnol — SPSED](https://pmc.ncbi.nlm.nih.gov/articles/PMC8804277/)
- [Brockmeier et al. 2006, J Mol Biol 362:393](https://journals.asm.org/doi/10.1128/aem.01146-10) (related protease screen)
- [Signal peptides for recombinant protein secretion in bacterial expression systems](https://microbialcellfactories.biomedcentral.com/articles/10.1186/s12934-018-0901-3)
