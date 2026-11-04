# Do signal-peptide sequence features predict recombinant collagen secretion in *Bacillus subtilis*?

**Author:** Baris Akar (bakar@dtu.dk) · **Date:** 4 November 2026
**Course:** DDLS — Data-Driven Life Science project
**Data owner:** Alexiou et al. (PhD thesis chapter 2, collagen production in *B. subtilis*)

---

## 1. Summary

A library of 32 N-terminal signal peptides was screened experimentally for secretion of a
recombinant bovine collagen fragment in *Bacillus subtilis*, measured by Western-blot
densitometry across three separately normalised blots. This project asked whether features of
those peptides — amino-acid composition, physicochemical properties, region structure, or
nucleotide/mRNA properties — are associated with the measured secretion, and whether the
evidence supports predicting or designing high-secretion candidates.

**The headline is a negative result with one qualified positive lead.**

Across 34 documented sequence descriptors tested within each blot, **no feature showed an
association that survives honest accounting for how many features were screened**. The best
observed correlation (ρ = 0.369) is *weaker* than the median result obtained by shuffling the
outcome and re-running the entire screen (ρ = 0.441); the family-wise p-value is 0.81. Four
model families under peptide-level cross-validation **all produced negative out-of-fold
performance** under both leave-one-peptide-out and leave-one-blot-out validation.

Critically, this is not a noise artefact. Inter-replicate agreement gives a measurement
reliability ceiling of approximately **0.86**, so an effect of moderate size would have been
detectable. The null is informative rather than merely underpowered.

One hypothesis taken from the published literature does hold up: the folding free energy of the
mRNA translation-initiation region, computed with the construct's actual ribosome-binding site,
is positively associated with secretion in **all three blots** (combined ρ = +0.51, one-sided
permutation p = 0.0042). This is reported as a lead for experimental follow-up, not as a
validated predictor, and with the explicit caveat that it refines a feature family already
present in the exploratory screen.

Two findings about the library itself explain much of the negative result: the cleavage region
was **engineered to a uniform A-S-A** across all 32 peptides (native endings span 13 distinct
motifs), and hydrophobicity is range-restricted around the optimum reported in the literature.
Several feature families that should matter biologically were held fixed by the experimental
design and therefore could not vary.

**Recommendation:** do not train a predictive model or propose synthetic designs from this
dataset. The binding constraint is the number of peptides measured on a common scale, which a
shared reference lane on every gel would fix.

---

## 2. Background and question

Secretion of heterologous protein in *B. subtilis* depends on the N-terminal signal peptide that
directs the nascent chain to the Sec translocon. Because the optimal peptide is known to be
target-protein-specific, the field relies on empirical library screening rather than prediction.

The data owner screened approximately 32 signal peptides for secretion of a ~110-aa bovine
collagen fragment and wished to know:

1. whether amino-acid sequence, codon-optimised nucleotide sequence, mRNA/translation-initiation
   features, structure or physicochemical properties relate to secretion efficiency;
2. whether, if so, those features could identify or propose high-secretion candidates;
3. whether it is worth training a machine-learning model, and subsequently using predicted
   structure to explain secretion.

The owner stated explicitly in interview that a well-supported negative result would be
informative and acceptable, and cautioned against analysing only the best performers.

---

## 3. Data

**Source:** `data/Information_for_Baris_corrected.xlsx`, three sheets.

| Component | Content |
|---|---|
| Sequences | 32 signal peptides (`SP1`–`SP32`), amino-acid 21–42 residues, nucleotide 63–126 bases; one collagen construct |
| Results | Four blocks of replicate "fold-change" values: Blot 1 (8 peptides), Blot 2 (13), Blot 3 (11), validation blot (7) |
| Other proteins | 4 peptides × 7 constructs, categorical labels (`High`/`Medium`/`Low`/`No`) |

**Outcome definition.** Band intensity was normalised per lane by Ponceau-stained total protein,
then divided by the mean of normalised intensities **on that same membrane** (owner's account,
confirmed against the thesis methods). The three main blots are therefore each centred on the
mean of a *different* subset of peptides and **do not share a numeric scale**.

**Effective sample size is 8, 13 and 11 — not 32.**

**Replicates** are biological, repeated end-to-end from production to blot, three per peptide.

### Known unknowns carried through, not patched

- **SP31**: the listed amino-acid sequence begins `V`, but its own nucleotide sequence begins
  `ATG`, which translates to `M`; residues 2–30 agree exactly. This is the only amino-acid /
  nucleotide disagreement in the sheet. **Not corrected** — the owner must confirm.
- **SP9**: one recorded replicate is exactly 0. Retained as a numeric zero. The owner's
  tentative reading is "no secretion", but its origin is unverified.
- **SP4**: reported in the thesis as consistently producing a secondary band; whether the
  quantification summed or excluded it is not stated.
- **High/Medium/Low** thresholds for the other-protein table are undocumented, so those labels
  were never converted to numbers or used as an outcome.
- Raw densitometry, exposure settings, background-subtraction method and saturation checks are
  not available.

---

## 4. Methods

### 4.1 Design rules enforced throughout

Three derive from the data owner's own cautions; the fourth is standard leakage control.

1. **Blots were never pooled.** Every test ran within a blot. Where effects are combined, it is
   the three per-blot *effect estimates* that are combined by inverse-variance Fisher-z
   meta-analysis — never the blot-normalised values.
2. **Replicates were collapsed to one value per peptide** before any test or model. Treating
   replicate rows as independent would have tripled the apparent sample size.
3. **All 32 candidates were analysed**, never only the top performers.
4. **Model splitting at peptide level**, with scaling fitted inside training folds only.

### 4.2 Sequence QC and feature derivation

All 32 peptides were checked for alphabet validity, reading frame, translation consistency and
duplication. 34 descriptors were then computed **before any outcome was consulted**, so feature
choice could not be steered by results.

- **Physicochemical:** GRAVY (Kyte–Doolittle), aromaticity, instability index, isoelectric point
  and net charge at pH 7 (Biopython 1.88 `ProteinAnalysis` / `IsoelectricPoint`), composition
  fractions.
- **Region-based:** no SignalP installation was available, so regions were derived by a
  transparent maximum-subarray search on Kyte–Doolittle hydropathy. **This segmentation was
  tested for stability** under four settings (three thresholds plus the Eisenberg scale). The
  h-region *start* is stable (median range 0 residues) but its *end* is not (median range 4;
  between-threshold correlation 0.30, 0.45, −0.02). Features were therefore recomputed from a
  fixed-width 9-residue maximal-hydropathy window and labelled `robust`; boundary-dependent
  features were labelled `fragile` and reported only as sensitivity.
- **Nucleotide/transcript:** GC fraction, GC3, and minimum free energy of 5′ windows
  (ViennaRNA 2.7.2).
- **Excluded:** zero-variance features. `axa_like_motif` is constant across all 32 peptides and
  cannot explain any between-peptide difference.
- **Not computed:** SignalP D-score (no offline installation; not approximated), codon
  adaptation index (no non-circular reference set), predicted 3-D structure.

22 feature pairs reach |ρ| ≥ 0.8. The descriptors are **not independent tests**, which governs
the multiplicity handling below.

### 4.3 Association testing and multiplicity calibration

Per-feature Spearman correlation with the per-peptide replicate mean, within each blot, combined
by Fisher-z meta-analysis. Because screening 34 correlated descriptors across three small blots
will produce a large correlation by chance, the outcome was **permuted within each blot 5,000
times and the entire screen re-run**, recording the largest |combined ρ| each time. This yields
a family-wise p-value for the best-of-panel result.

### 4.4 Measurement reliability

Inter-replicate rank agreement within each blot was converted via Spearman–Brown to the
reliability of a 3-replicate mean; its square root is the largest correlation any feature could
show against these measurements. This is required to distinguish "no effect" from "too noisy to
see one".

### 4.5 Modelling

scikit-learn 1.9.0. Target: within-blot percentile rank of the per-peptide mean, which lets all
32 peptides share one target without pooling incomparable values. Predictors: the 34 robust
descriptors.

| Model | Specification |
|---|---|
| Baseline | `DummyRegressor(strategy='mean')` |
| Ridge | `StandardScaler` → `Ridge(alpha=10)` |
| Ridge | `StandardScaler` → `Ridge(alpha=100)` |
| Random forest | `RandomForestRegressor(n_estimators=100, min_samples_leaf=2, random_state=0)` |
| k-NN | `StandardScaler` → `KNeighborsRegressor(n_neighbors=5)` |

Two cross-validation schemes: `LeaveOneOut` (32 folds) and `LeaveOneGroupOut` with blot as the
group (3 folds). The second is the realistic test — can a model trained on two blots rank
peptides measured in a third, separate experiment?

Each model was additionally fitted and scored on all 32 peptides to quantify the in-sample /
out-of-fold gap.

---

## 5. Results

### 5.1 Sequence QC

All 32 peptides passed alphabet, frame and duplication checks. Two findings required the owner:
the **SP31** V/M discrepancy (§3), and that **all 32 peptides end A-S-A** — positions −3, −2, −1
are identical library-wide.

### 5.2 Outcome description and candidate stability

Ranking by replicate mean and by median disagree for **8 of 32 peptides by two or more places**,
because single extreme replicates dominate the mean.

| Peptide | Blot | Mean | Median | CV | Rank by mean | Rank by median |
|---|---|---:|---:|---:|---:|---:|
| SP23 | 3 | 1.16 | 0.07 | 1.68 | 3rd | **9th** |
| SP4 | 1 | 1.61 | 1.00 | 0.84 | **1st** | **5th** |
| SP21 | 2 | 0.85 | 0.26 | 1.40 | 8th | **12th** |

Six peptides have a standard deviation exceeding their own mean (SP21, SP9, SP23, SP30, SP31,
SP25). **SP4 is the most consequential case:** it leads Blot 1 by mean but falls to fifth by
median, and it is the peptide flagged in the thesis for a recurring secondary band.

**Candidates that are both high and reproducible, within their own blots only:** SP5 (Blot 1,
CV 0.14) and SP26 (Blot 3, CV 0.21). SP19 leads Blot 2 by a wide margin but with CV 0.63.
There is no cross-blot ranking, because the data do not support one.

### 5.3 Feature screen: nothing above chance

| Quantity | Value |
|---|---:|
| Best observed \|combined ρ\| (`h_core9_mean_kd`) | **0.369** |
| Permutation null, **median** best-of-panel | **0.441** |
| Permutation null, 95th percentile | 0.598 |
| **Family-wise p-value** | **0.81** |

Every per-feature confidence interval crosses zero. **The best association in this dataset is
weaker than the median result of the same screen run on randomised outcomes.**

Six features point the same way in all three blots, all hydrophobicity-related. This is not six
findings: those features are mutually correlated at |ρ| ≥ 0.8, so it is one property measured
six ways, and it sits inside the chance band. Leave-one-peptide-out produced no sign flips, so
the direction is stable *and* indistinguishable from chance — both are true.

### 5.4 The null is credible, not underpowered

| Blot | Mean inter-replicate ρ | Reliability of mean | Max detectable ρ |
|---|---:|---:|---:|
| Blot 1 | 0.476 | 0.732 | 0.855 |
| Blot 2 | 0.581 | 0.806 | 0.898 |
| Blot 3 | 0.418 | 0.683 | 0.827 |

A feature perfectly predicting true secretion could correlate with these measurements at about
**0.86**, far above the 0.37 observed. There was room to detect a moderate-to-strong effect.

### 5.5 Modelling: no model beats chance

**Out-of-fold mean within-blot Spearman:**

| Model | Leave-one-peptide-out | Leave-one-blot-out |
|---|---:|---:|
| Ridge (α=10) | −0.130 | −0.078 |
| Ridge (α=100) | −0.126 | −0.044 |
| Random forest | −0.187 | −0.146 |
| k-NN (k=5) | −0.119 | −0.070 |

**Every score is negative under both schemes** — the expected signature of fitting noise and
carrying it to held-out data.

**In-sample versus out-of-fold:**

| Model | In-sample ρ | Out-of-fold ρ |
|---|---:|---:|
| Random forest | **0.964** | **−0.187** |
| Ridge (α=10) | 0.729 | −0.130 |
| Ridge (α=100) | 0.673 | −0.126 |
| k-NN (k=5) | 0.289 | −0.119 |

A random forest fitted and scored on the same 32 peptides reproduces their ranking almost
perfectly. The same model, trained without each peptide and asked to predict it, does **worse
than guessing**. With 34 features and 32 observations a model memorises the dataset completely
while learning nothing transferable.

*Note:* the leave-one-peptide-out baseline reads −1.00. This is an artefact — a constant
predictor's fold-to-fold mean moves inversely to the held-out value. The meaningful baseline is
leave-one-blot-out, which is 0.00.

### 5.6 The library was built in a way that suppresses variation

Each peptide was compared with its native sequence in UniProt (reviewed *B. subtilis* 168,
taxid 224308), using the SP→gene mapping recovered from the thesis plasmid and primer tables.

| | Native (UniProt) | Supplied |
|---|---|---|
| Distinct C-terminal motifs | **13** (ASA 12, AHA 3, AKA 3, AEA 2, ADA 2, and one each of AQA, AGA, ANA, VQA, AYA, AFA, VFA, LAG) | **1** (ASA, 32/32) |

- **Only 8 of 32** supplied peptides match their native signal peptide exactly.
- **18 of 30** annotated peptides differ from native at the C-terminus.
- Six also differ in length (SP1/amyE +6 residues, SP8/phoA −10, SP14/yncM −5).

The cleavage region was therefore **standardised by design, not inherited**. This is a
defensible choice — it holds signal-peptidase processing constant — but it means the A-x-A motif
that Fu et al. associate with good performers is a **constant here, not a variable**, and the
library could never report on C-region effects.

Hydrophobicity is similarly range-restricted: GRAVY median 1.01, with 26 of 32 peptides between
0.6 and 1.4 — sitting on the optimum reported by Grasso et al. (2023).

A consequence worth noting: **SP1/AmyE**, the classic *B. subtilis* secretion tag, ranks 7th of 8
in its blot and is among the most heavily modified peptides in the set (native ending `LAG`, not
an A-x-A motif at all, plus six extra residues).

### 5.7 The one positive lead

Fu et al. (2018) propose that a **less negative** folding free energy near the
translation-initiation region leaves the ribosome-binding site and start codon accessible,
favouring secretion — predicting a *positive* correlation. This was previously untestable
because the 5′ context was unknown; the thesis supplies it in the cloning primer overhangs
(shared RBS `AGGAGGAATATAC` + `ATG`, identical across all constructs).

Recomputing folding energy over the real 5′ context plus the first 48 bases of coding sequence:

| | Blot 1 | Blot 2 | Blot 3 | Combined |
|---|---:|---:|---:|---:|
| RBS-aware ΔG | **+0.262** | **+0.632** | **+0.491** | **+0.515** |
| Previous coding-only version | −0.443 | +0.190 | +0.346 | +0.106 |

One-sided permutation test, 20,000 within-blot shuffles: **p = 0.0042** as a single
pre-specified hypothesis, **p = 0.0118** corrected for the family of three window sizes.
Leave-one-peptide-out range +0.466 to +0.594 with **no sign flips**. Not a proxy: GC alone gives
ρ = −0.02 and length alone +0.25.

**Why a different test from §5.3:** this is a single directional hypothesis specified in the
literature, not the best of 34 screened descriptors. Judging it against the screen's
best-of-34 null (0.598) would be the wrong test.

**Mandatory caveats.** A coding-sequence-only version of this feature family was already in the
34-feature screen and ranked second, so this is a **refinement of an examined family, not clean
out-of-sample confirmation**. The true transcription start site is unknown, so the window
remains approximate. No mechanism is established. Against a reliability ceiling of 0.86, ρ ≈ 0.5
is a moderate effect.

### 5.8 Separate context: validation blot and other proteins

The seven shared peptides broadly preserve rank order between their original blot and the
validation blot (ρ = 0.68, p = 0.09) while **6 of 7 shift downward** in absolute value (median
−0.54). Order roughly kept, scale moved — precisely why pooling is not permissible. No
conversion between blots was fitted.

The four-peptide other-protein table was summarised categorically and never used as an outcome.
Notably **SP19 ranks first in its own blot but receives no `High` rating on any other
construct**, while SP26 receives three — consistent with the documented target-dependence of
signal-peptide performance.

Five of the 32 peptides also appear among Fu et al.'s 15 best amylase performers; rank agreement
with collagen secretion is ρ = −0.20 (n = 5). This is confounded with the C-terminal
modification (§5.6), since the sequences are not identical, and is suggestive only.

---

## 6. Discussion: why no predictor was obtained

**(a) There was no signal to learn.** The best of 34 descriptors correlated at 0.369, while
shuffling the outcome and re-running the entire screen produces 0.441 on average. A model's job
is to combine features that individually carry information. If none does, there is nothing to
combine, and no algorithm fixes that.

**(b) The effective sample size is 8, 13 and 11.** Because the blots cannot be pooled, any model
learns from three very small datasets. With 34 features against 32 observations there are more
parameters than data points, so a model can reproduce the training set exactly while learning
nothing — demonstrated directly by the 0.964 / −0.187 gap.

**(c) It is not a noise problem.** The reliability ceiling of 0.86 means a real effect of
moderate size would have been visible. This is what makes the null informative rather than
merely underpowered, and it is the single most important check in the analysis.

**(d) The library design suppresses variation.** The cleavage region is constant by engineering;
the first residues of the mature protein are constant because all peptides are fused to the same
collagen; and hydrophobicity is range-restricted around the published optimum. Several feature
families that should matter biologically were held fixed and therefore could not explain
anything.

**Higher-capacity models were deliberately not attempted.** Ridge suits p > n with a weak linear
signal; random forest captures non-linearity and interactions; k-NN captures local structure. If
those find nothing under two validation schemes, adding capacity fits the 32 points harder and
generalises worse. For comparison, Grasso et al. required ~4,400 informative peptides to fit a
random forest for this task.

**Predicted structure (AlphaFold) was not pursued**, and should not be: it would add a
high-dimensional feature family to the same 32 outcomes, which the multiplicity result shows
mostly adds opportunities for chance patterns. Isolated signal peptides also have no
well-defined solution structure — their relevant conformation is in the membrane and translocon,
and they are cleaved during secretion.

**This is a negative result about this dataset's shape, not about the biology, and not a
criticism of the experiment.** The screen identified reproducible high performers, produced data
that could be tested rigorously, and generated a specific testable lead.

---

## 7. Limitations

- Association is not causation; nothing here establishes mechanism. A null on association is
  also not evidence that signal-peptide sequence is biologically irrelevant.
- Region boundaries are computed, not observed. The h/c boundary is demonstrably unstable and
  those features were reported only as sensitivity.
- The folding energies are not initiation-region energies in the published sense, because the
  true transcription start site is unknown.
- No cross-blot scale exists; all rankings are within-blot.
- The other-protein table has four peptides and undefined thresholds. It is context, not
  validation.
- SP31 and the SP9 zero remain unresolved and were carried through rather than patched.
- The SP→gene mapping is read from the thesis, not the workbook, and needs owner confirmation.
- UniProt SIGNAL annotations are frequently predictions, so length disagreements may reflect the
  predictor. The C-terminal composition result does not depend on this.
- Results apply to this collagen construct, host, assay and conditions.

---

## 8. Conclusions and next steps

1. **No sequence feature predicts secretion in this dataset beyond chance**, and the measurement
   quality was sufficient that a moderate effect would have been detected.
2. **A predictive model is not defensible**, and no synthetic sequence should be proposed from
   one. This was tested across four model families and two validation schemes, not assumed.
3. **One lead is worth pursuing:** mRNA accessibility at the translation-initiation region.
4. **Usable now:** SP5 and SP26 are high and reproducible within their own blots.

**What would make the question answerable, in priority order:**

1. **A shared reference lane on every gel.** The single largest structural fix — it converts
   three incomparable blots into one comparable dataset.
2. **More peptides measured on that common scale.** This matters more than any analytical
   refinement.
3. **Raw densitometry**, to audit the normalisation, resolve the SP9 zero and assess the SP4
   secondary band.
4. **The transcription start site and full 5′UTR**, to test the positive lead against its
   published definition.
5. **Deliberate variation in the C-region**, if cleavage effects are of interest.

If modelling is attempted later, split at peptide/design level, treat prediction of peptides
from a **new experimental batch** as the honest test, and set a held-out set aside before
modelling begins.

---

## 9. Reproducibility

Input: `data/Information_for_Baris_corrected.xlsx` (not redistributed — owner's unpublished
data). Run from the repository root in this order:

```
python ouput/analysis/run_steps_2_8.py
python ouput/analysis/features_step3.py
python ouput/analysis/associations_step4.py
python ouput/analysis/context_step5.py
python ouput/analysis/modeling_step6.py
python ddls_claude/analysis/sp_identity_and_cross_assay.py
python ddls_claude/analysis/improved_features_step8.py
python ddls_claude/analysis/rbs_hypothesis_test.py
python ddls_claude/analysis/uniprot_native_sp_check.py   # needs internet
```

Random seeds fixed at 20261103 in the permutation and modelling scripts. Environment:
Python 3.14.6; pandas 3.0.3, numpy 2.5.0, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0,
seaborn 0.13.2, openpyxl 3.1.5, biopython 1.88, ViennaRNA 2.7.2. See `REPRODUCE.md`.

An interactive dashboard of all results is included as `findings_standalone.html` — a single
self-contained file requiring no server or internet.

**Note on a corrected reproducibility defect.** During final verification the step-6 outputs on
disk were found to have been overwritten by a stale background run using 300 trees, while the
committed script specifies 100. The script was re-run and all downstream artefacts regenerated;
figures reported here match the committed code. Conclusions were unaffected (all out-of-fold
scores were negative under both configurations).

---

## 10. AI use statement

The computational analysis, code and figures in this project were produced with substantial
assistance from Claude (Anthropic), used as an analysis and programming assistant. Full
disclosure, including which work was AI-assisted, what was verified independently, and what the
AI did not do, is in `AI_DISCLOSURE.md`. Complete session transcripts are included with this
submission.

---

## 11. References

1. Fu, G.; Liu, J.; Li, J.; Zhu, B.; Zhang, D. (2018). Systematic Screening of Optimal Signal
   Peptides for Secretory Production of Heterologous Proteins in *Bacillus subtilis*.
   *J Agric Food Chem* 66, 13141–13151. DOI 10.1021/acs.jafc.8b04183
2. Alexiou, A.; Jensen, S. I.; Jers, C.; Abdollahi, M.; Mijakovic, I.; Yang, L. Production &
   secretion of hydroxylated bovine collagen and other polymeric proteins in *Bacillus
   subtilis*. PhD thesis, chapter 2 (supplied).
3. Grasso, S. *et al.* (2023). Signal Peptide Efficiency: From High-Throughput Data to
   Prediction and Explanation. *ACS Synth Biol* 12, 390. Data: Zenodo 10.5281/zenodo.6448806
4. Sun, H. *et al.* (2026). A Deep-Learning-Based Server SecEff-Pred. *J Agric Food Chem*
   74, 6960. DOI 10.1021/acs.jafc.5c14547
5. Peng, C. *et al.* (2022). SPSED: A Signal Peptide Secretion Efficiency Database.
   *Front Bioeng Biotechnol*.
6. Kyte, J.; Doolittle, R. F. (1982). A simple method for displaying the hydropathic character
   of a protein. *J Mol Biol* 157, 105–132.
7. Lorenz, R. *et al.* (2011). ViennaRNA Package 2.0. *Algorithms Mol Biol* 6, 26.
8. Cock, P. J. A. *et al.* (2009). Biopython. *Bioinformatics* 25, 1422–1423.
9. Pedregosa, F. *et al.* (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12, 2825.
