# Signal-peptide features and collagen secretion: association and modelling report

**Scope.** This report covers analysis-plan steps 3–7: sequence QC and feature derivation,
feature–outcome association testing within each blot, the validation blot and other-protein
table as separate context, and the decision on whether predictive modelling is defensible.
Steps 1–2 (data inventory, outcome description) are in `analysis_plan.md`,
`analysis_steps_2_8_report.md` and `final_analysis_part1.md`.

**One-line answer to the data owner's question.** Across 32 peptides and 34 documented
sequence descriptors, **no feature showed an association with secretion that survives honest
accounting for how many features were screened**, and **no model predicted held-out peptides
better than chance**. This is a negative result, not a failed analysis, and it is reported as
the owner said a well-supported negative result would be acceptable.

---

## 1. How to read this report

Three rules were enforced throughout, all of them from the owner's own cautions:

1. **The three main blots are analysed separately.** Blot-normalised values are never pooled
   onto a shared numeric scale. Where effects are combined, it is the per-blot *effect
   estimates* that are combined by meta-analysis, never the values themselves.
2. **Replicates are collapsed to one value per peptide before any test or model.** A peptide
   with three replicates is one observation, not three.
3. **All candidates are analysed, never only the top performers.** This is the selection bias
   the owner specifically warned about, and it is the reason the conclusions here differ from
   a published analysis that examined only its 15 best peptides.

Sample sizes are small and are stated everywhere: Blot 1 n=8, Blot 2 n=13, Blot 3 n=11,
validation blot n=7, other-protein table 4 peptides × 7 constructs.

---

## 2. Sequence QC: two findings that need the owner

Full detail in [`feature_definitions.md`](feature_definitions.md). All 32 peptides passed
alphabet, length, reading-frame and duplicate checks. Two things need confirmation.

### 2.1 SP31 begins with V in the protein column but ATG in the nucleotide column

`SP31`'s listed amino-acid sequence starts `VRKSLITLGLASV…`; its own nucleotide sequence
starts `ATG`, which translates to **M**. Residues 2–30 agree exactly. This is the only
amino-acid/nucleotide disagreement in the sheet, every other peptide begins with M, and `ATG`
is the initiator codon.

It has **not** been corrected. The feature table uses the sequence exactly as supplied and
flags the row. This is the same class of issue as `S19`, `Np` and the Greek `Η` resolved in
meeting 2, and it should be resolved the same way — by the owner, not by assumption.

### 2.2 The cleavage motif is a library-wide constant

**All 32 peptides end in A-S-A.** Positions −3, −2 and −1 are identical across the entire
library.

This changes how one published observation applies here. Fu et al. (2018) report an A-x-A-like
C-region motif among their top-performing peptides. In this library that motif is present in
32 of 32 peptides — it is a **design constant, not a variable**, and a constant cannot explain
why some of these peptides secrete better than others. The feature is excluded from association
testing for exactly that reason, and the search for explanatory variation is confined to the
n-region, the hydrophobic core, overall length and composition, and nucleotide properties.

---

## 3. Features: what was computed, and one that could not be

34 descriptors were computed for all 32 peptides **before any outcome was consulted**, so
feature choice cannot have been steered by the results. Definitions, scales, software versions
and settings are in [`feature_definitions.md`](feature_definitions.md).

### 3.1 Region boundaries are only half-reproducible

No SignalP or trained predictor was available offline, so n/h/c regions come from a transparent
maximum-subarray search on Kyte–Doolittle hydropathy, repeated under four settings
(three thresholds plus the Eisenberg scale) to test stability. The result matters:

| Quantity | Range across settings (median) | Verdict |
|---|---|---|
| h-region **start** | 0 residues | **stable** |
| h-region **length** | 4 residues (max 18) | **unstable** |

Spearman correlation of h-region length between thresholds is only 0.30, 0.45 and −0.02.
**Where the hydrophobic stretch begins is reproducible; where it ends is not.**

Rather than build on an unstable boundary, every region feature was recomputed from a fixed
9-residue maximal-hydropathy window, whose only free quantity is its position. Features are
labelled `robust` or `fragile` in `step3/feature_stability_classification.csv`. **Only the
robust set is tested; the fragile set is reported as sensitivity.** This is a real limitation:
without experimental cleavage data or a signal-peptide-specific predictor, h-region length and
c-region length cannot be defined reliably enough to test.

### 3.2 The mRNA folding feature is an approximation, and says so

Fu et al. computed folding free energy around the *translation initiation site*, which includes
the 5′UTR and ribosome-binding site. The owner offered that context in meeting 2 but **it has
not been received.** The energies here (ViennaRNA 2.7.2, first 30/48/60 bases) begin at the
signal peptide's own start codon and contain no upstream sequence. They are therefore **not the
same quantity** and cannot confirm or refute that paper's observation. Obtaining the RBS/5′UTR
context is the single most useful piece of missing data for this specific question.

### 3.3 Not computed

SignalP D-score (no offline installation — not approximated), codon adaptation index (would
need a *B. subtilis* reference set; computing it against this library's own 32 sequences would
be circular), and any predicted 3-D structure (see §7).

### 3.4 These descriptors are not independent tests

22 feature pairs reach |ρ| ≥ 0.8 (`step3/feature_redundant_pairs.csv`). Length, hydrophobic
fraction, GRAVY and core hydropathy all measure overlapping properties of the same short
sequence; so do pI, net charge and K/R count. Counting "how many features correlate" would
badly overstate the evidence, and this drives the multiplicity handling in §4.

---

## 4. Association testing: the result

Per-blot Spearman correlations between each robust feature and the per-peptide replicate mean,
combined across blots by inverse-variance Fisher-z meta-analysis of the *effects*.
Full table: `step4/associations_robust_mean.csv`. Figure: `step4/association_forest.png`.

### 4.1 The strongest associations

| Feature | Blot 1 | Blot 2 | Blot 3 | Combined ρ | 95% CI | Same direction? |
|---|---:|---:|---:|---:|---|:--:|
| `h_core9_mean_kd` | −0.08 | −0.45 | −0.42 | **−0.37** | −0.66 to 0.02 | yes |
| `mrna_dg_first30nt` | −0.12 | 0.24 | 0.68 | 0.35 | −0.04 to 0.65 | **no** |
| `c_prox6_frac_polar_STNQ` | — | −0.13 | −0.55 | −0.33 | −0.67 to 0.12 | yes |
| `h_core9_frac_hydrophobic` | −0.36 | −0.33 | −0.27 | −0.31 | −0.63 to 0.08 | yes |
| `frac_hydrophobic_AVILMFWY` | −0.43 | −0.09 | −0.39 | −0.27 | −0.60 to 0.13 | yes |
| `aromaticity` | −0.13 | −0.38 | −0.17 | −0.26 | −0.58 to 0.15 | yes |

**Every confidence interval crosses zero.**

### 4.2 The multiplicity test, which is the decisive part

Screening 34 correlated descriptors across three small blots will produce a large-looking
correlation by chance. To calibrate this, the outcome was permuted *within each blot* 5,000
times and the whole screen re-run, recording the largest |combined ρ| each time.

| Quantity | Value |
|---|---:|
| Observed best |combined ρ| (`h_core9_mean_kd`) | **0.37** |
| Null **median** of the best-of-panel | **0.44** |
| Null 95th percentile | 0.60 |
| **Family-wise p-value** | **0.81** |

The best association in this dataset is **weaker than the median result of the same screen run
on randomised outcomes.** There is no feature-level signal to report.

### 4.3 Why the consistent direction is not a counter-argument

Six features point the same way in all three blots, all of them negative, all hydrophobicity-
related: more hydrophobic → lower measured secretion. That looks like a pattern, and it is
worth stating, but three things keep it from being evidence:

- These are **not six findings.** They are one property measured six ways — the features are
  mutually correlated at |ρ| ≥ 0.8.
- With three blots, one feature agrees in direction by chance a quarter of the time. Across a
  correlated panel of 34, several such runs are expected.
- The effect is **inside** the permutation null band, so it is what chance produces here.

Leave-one-peptide-out analysis (`step4/leave_one_peptide_out_stability.csv`) shows no sign
flips for the top features, so the direction is at least not driven by a single peptide. It is
stable *and* indistinguishable from chance — both can be true, and here both are.

`mrna_dg_first30nt`, the feature closest to the published mRNA observation, is **not**
directionally consistent: it is negative in Blot 1, weakly positive in Blot 2, and strongly
positive in Blot 3 (0.68). Its combined estimate is driven almost entirely by one blot. On a
quantity that is in any case an approximation (§3.2), this does not support the Fu et al.
pattern in this dataset.

---

## 5. Is the outcome too noisy to detect anything?

This is the natural objection to a negative result, and it was tested rather than assumed.

Inter-replicate rank agreement within blots averages ρ ≈ 0.42–0.58. Via Spearman–Brown, the
reliability of a 3-replicate mean is 0.68–0.81, giving an **attenuation ceiling of about 0.86**
(`step5/measurement_reliability.csv`). A feature that perfectly predicted true secretion could
correlate with these measurements at roughly 0.86 — not 1.0, but far above the 0.37 observed.

**So noise is not the explanation.** There is enough measurement reliability here to detect a
moderate-to-strong feature effect. None was found. `step5/reliability_vs_observed.png` shows
all observed associations sitting below both the chance threshold and the reliability ceiling.

What the modest replicate agreement *does* mean is that individual peptide rankings within a
blot are soft — adjacent ranks should not be read as meaningful differences.

---

## 6. The validation blot and the other-protein table, as separate context

### 6.1 Seven shared peptides

No cross-blot conversion was fitted, in line with the owner's warning. Descriptively
(`step5/shared_peptide_reproducibility.csv`): the rank order of the seven shared peptides is
broadly preserved between their original blot and the validation blot (ρ = 0.68, p = 0.09),
while **6 of 7 shift downward** in absolute value (median shift −0.54).

That combination — order roughly kept, scale moved — is precisely why blot-normalised values
from different blots must not be pooled, and it supports the owner's instinct. SP4 is the one
peptide that does not shift down, and it ranks first in both; the thesis notes SP4's recurring
secondary band, which the owner also raised in meeting 2 and which remains unresolved.

As an informal direction check, 17 of 33 robust features point the same way in the validation
blot as in the main-blot combined estimate. That is 52% — exactly chance. With n=7 this check
has almost no power either way, and it is reported for completeness, not as evidence.

### 6.2 Four peptides, seven other constructs

Counts per peptide (`step5/other_protein_counts_by_peptide.csv`), kept categorical:

| Peptide | No | Low | Medium | High | Rank in its own main blot |
|---|---:|---:|---:|---:|---|
| SP3 | 3 | 1 | 1 | 2 | 2nd of 8 (Blot 1) |
| SP5 | 2 | 2 | 1 | 2 | 3rd of 8 (Blot 1) |
| SP19 | 2 | 3 | 2 | 0 | **1st of 13 (Blot 2)** |
| SP26 | 2 | 2 | 0 | 3 | **1st of 11 (Blot 3)** |

`No` means product not produced (owner, meeting 2). `Low`/`Medium`/`High` have **no stated
thresholds** and are not calibrated to the fold-change scale, so they were not converted to
numbers and are not used as an outcome anywhere.

One observation worth the owner's attention, offered as a question rather than a finding:
**SP19 ranks first in its own blot but receives no `High` rating on any other construct**,
while SP26 — also first in its blot — receives three. If the categories are comparable to each
other, that is consistent with the thesis's and Fu et al.'s shared warning that signal-peptide
performance is target-dependent and does not automatically transfer across protein length or
identity. It rests on four peptides and undefined labels, so it cannot carry more weight than
that.

---

## 7. Candidate-level findings: which rankings are solid and which are not

This is the part most directly useful to the owner, and it does not depend on any feature or
model. Rankings are reported **within each blot only** — there is no unified cross-blot
ranking, because the data do not support one.

### 7.1 Eight of 32 peptides change rank by two or more places depending on the summary used

Ranking by replicate mean and by replicate median disagree substantially for several
candidates, because single extreme replicates dominate the mean:

| Peptide | Blot | Mean | Median | CV | Rank by mean | Rank by median |
|---|---|---:|---:|---:|---:|---:|
| **SP23** | 3 | 1.16 | 0.07 | 1.68 | 3rd | **9th** |
| **SP4** | 1 | 1.61 | 1.00 | 0.84 | **1st** | **5th** |
| **SP21** | 2 | 0.85 | 0.26 | 1.40 | 8th | **12th** |
| SP16 | 2 | 0.70 | 0.68 | 0.87 | 10th | 7th |
| SP28 | 3 | 0.40 | 0.38 | 0.55 | 10th | 7th |

SP23's three replicates are approximately 0.00, 0.07 and 3.42 — the mean places it third in its
blot, the median places it ninth. **SP4 is the most consequential case**: it leads Blot 1 by
mean but falls to fifth by median, and it is also the peptide the thesis flags for a recurring
secondary band, which the owner raised again in meeting 2 and which is still unresolved. Any
decision to carry SP4 forward as the Blot 1 leader should wait on that.

Six peptides have a standard deviation exceeding their own mean (CV > 1): SP21, SP9, SP23,
SP30, SP31, SP25.

### 7.2 Candidates whose standing is stable

By contrast, these rank highly on both summaries with low replicate spread, and are the most
defensible candidates to carry forward **within their own blot**:

- **Blot 1:** SP3 (mean 1.43, median 1.35, CV 0.24) and SP5 (mean 1.42, median 1.43, CV 0.14).
  SP5 is the most reproducible candidate in the whole dataset.
- **Blot 2:** SP19 is first by a wide margin (mean 3.66) but with CV 0.63; SP15 is far more
  consistent (mean 1.47, CV 0.055) though lower. SP17 and SP14 sit between.
- **Blot 3:** SP26 (mean 1.91, median 1.87, CV 0.21) is both the leader and reproducible —
  the clearest single candidate in that blot.

**SP5 and SP26 are the two candidates that combine a high within-blot position with stable
replicates.** That is a descriptive observation about measurement quality, not a prediction
that they will outperform elsewhere, and SP19's higher raw value in a different blot cannot be
compared with either of them.

### 7.3 SP9's zero

SP9 (Blot 2) has replicates 0.000, 0.012 and 0.130 — the lowest in the dataset. The recorded
zero is retained as a numeric zero. The owner's tentative reading in meeting 2 was "no
secretion at all," but they were unsure of its origin, so it is not recoded and the
interpretation stays tentative pending the raw densitometry records.

---

## 8. Structure prediction (AlphaFold): still not the next step

The owner's longer-term interest is to predict structures for the 32 peptides and ask whether
folding explains secretion. The position taken in `analysis_plan.md` §6b is unchanged, and this
analysis adds a concrete reason to hold off.

A predicted structure would be a new, high-dimensional feature family. The present result is
that 34 documented descriptors produced nothing above chance on 32 peptides, and the
multiplicity test in §4.2 shows exactly why: with this sample size, adding feature families
mostly adds opportunities for chance patterns. Adding structural descriptors to the same 32
outcomes would face the same arithmetic, with the extra problems that isolated signal peptides
have no well-defined solution structure (their relevant conformation is in a membrane and
translocon, and they are cleaved during secretion), and that model confidence is not evidence
about secretion.

Structure work becomes worthwhile when there are more measured peptides, not more features on
the same 32.

---

## 9. Does a model add defensible value? Tested, not asserted

Rather than decline to model, models were fitted under honest validation. Outcome: within-blot
percentile rank. Predictors: the 34 robust features. Splitting at **peptide level**, with
scaling fitted inside each training fold. Two schemes: leave-one-peptide-out, and
**leave-one-blot-out**, which is the realistic case — predicting peptides measured in a new
experimental batch. Full results: `step6/model_cv_performance.csv`.

### Out-of-fold performance

| Model | Leave-one-peptide-out | Leave-one-blot-out |
|---|---:|---:|
| Ridge (α=10) | −0.130 | −0.078 |
| Ridge (α=100) | −0.126 | −0.044 |
| Random forest (100 trees) | −0.187 | −0.146 |
| k-NN (k=5) | −0.119 | −0.070 |

**Every model has a negative out-of-fold rank correlation under both schemes.** Not merely "no
better than chance" — slightly worse, which is the expected signature of fitting noise and
carrying it to held-out data. No permutation null is needed to interpret a score at or below
zero, so none was computed for these (the rule was fixed in advance at 0.10; the permutation
machinery is in the script and would have run had any model cleared it).

*Note on the baseline row in the CSV:* the leave-one-peptide-out baseline shows −1.00. That is
an artefact, not a result — a constant predictor's fold-to-fold mean moves inversely to the
held-out value, forcing ρ = −1. The meaningful reference is the leave-one-blot-out baseline,
which is 0.00.

### Why in-sample fit must never be reported

| Model | In-sample ρ | Honest out-of-fold ρ |
|---|---:|---:|
| Random forest | **0.964** | **−0.187** |
| Ridge (α=10) | 0.729 | −0.130 |
| Ridge (α=100) | 0.673 | −0.126 |
| k-NN (k=5) | 0.289 | −0.119 |

A random forest fitted and scored on the same 32 peptides reproduces their ranking almost
perfectly — ρ = 0.96. The same model, trained without each peptide and asked to predict it,
does **worse than guessing**. With 34 features and 32 observations a model can memorise the
dataset completely while learning nothing transferable.

This is the single most useful exhibit for the question "is it worth training a model?". Any
figure resembling the left-hand column — and such figures are easy to produce — is measuring
memorisation, not prediction.

### Decision

**On this dataset, no. A predictive model is not defensible, and no synthetic sequence should be
proposed from one.** The constraint is not the algorithm; it is 32 peptides split across three
non-comparable blots, with 34 correlated descriptors. Section 5 shows the measurements are
reliable enough that a real effect could have been detected, so this is a genuine negative.

The qualification is §4 of `ddls_claude/md/literature_and_prediction_improvement.md`: one
literature-derived feature, the RBS-aware initiation-region folding energy, *does* show a
consistent association (ρ = +0.51, positive in all three blots, p = 0.004 as a single
pre-specified hypothesis). That is a lead to pursue, not a model — one feature with a plausible
published mechanism is a reason to design the next experiment, not to fit a predictor to 32
points.

---

## 10. What would make this question answerable

The owner's underlying goal — capture what makes a signal peptide secrete well, then design new
ones — is a good goal and is not refuted by this analysis. What this analysis shows is that the
current dataset cannot support it. The gap is specific and addressable:

**1. More peptides, measured comparably.** This is the binding constraint. 32 peptides split
across three separately normalised blots gives effective sample sizes of 8, 13 and 11. A
screen that measures substantially more peptides **in one comparable batch**, or with a shared
calibrator on every blot, would change what is possible more than any analytical refinement.

**2. A shared reference sample on every blot.** One or two identical control lanes per blot
would let values be placed on a common scale with a stated, auditable method. At present the
blot boundary is an impassable wall, and it is the single largest structural limitation here.

**3. Raw densitometry.** Offered in meeting 2, not yet received. This would allow the
normalisation to be audited, the SP9 zero resolved, the secondary-band issue (SP4) assessed,
and replicate structure checked. Several caveats in this report collapse once it exists.

**4. The RBS / 5′UTR context.** Also offered in meeting 2. Without it the mRNA-folding feature
cannot be computed as Fu et al. defined it (§3.2), so the one published quantitative lead
available cannot be properly tested.

**5. Variation in the C-region.** Because all 32 peptides end in A-S-A (§2.2), this library
cannot say anything about cleavage-region effects. If that region is of interest, future
designs need to vary it deliberately.

**6. Replicate definition.** "Biological, in a way both" leaves the independence structure
unclear, which affects every uncertainty estimate in this report.

### On training a model later

Model splitting must be at **peptide/design level**, never at replicate-row level, and the
honest test is prediction of peptides from a **new experimental batch** — the leave-one-blot-out
scheme used in §9, not leave-one-peptide-out. A held-out set should be set aside before
modelling begins, as the owner themselves proposed in meeting 2. With a larger screen this
becomes a reasonable thing to attempt; with 32 peptides it does not.

---

## 11. Reproducing this analysis

Run in order from the repository root:

```bash
python ouput/analysis/run_steps_2_8.py
```

```bash
python ouput/analysis/features_step3.py
```

```bash
python ouput/analysis/associations_step4.py
```

```bash
python ouput/analysis/context_step5.py
```

```bash
python ouput/analysis/modeling_step6.py
```

Input: `data/Information_for_Baris_corrected.xlsx`. Outputs: `ouput/analysis/step3/`,
`step4/`, `step5/`, `step6/`. Random seeds are fixed (20261103) in the permutation and
modelling scripts. Dependencies: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn,
biopython 1.88, ViennaRNA 2.7.2, openpyxl.

Supporting documents: [`feature_definitions.md`](feature_definitions.md) (feature methods and
QC), [`analysis_plan.md`](analysis_plan.md) (plan and owner clarifications),
[`questions.md`](questions.md) (open questions for the owner, including the new SP31, A-S-A and
RBS items), [`literature.md`](literature.md) (Fu et al. and thesis context).

---

## 12. Limitations

- **Association and causation.** Nothing here establishes mechanism. A negative result on
  association is also not evidence that signal-peptide sequence is biologically irrelevant to
  secretion — only that these descriptors do not track these measurements at this sample size.
- **Region boundaries are computed, not observed.** No SignalP, no experimental cleavage data.
  The h/c boundary is demonstrably unstable (§3.1) and those features are reported as
  sensitivity only.
- **mRNA folding energies are not initiation-region energies** (§3.2). In addition, 9 of 32
  peptides have ΔG = 0 for the 30-nucleotide window, so that particular feature is heavily
  tied and its rank correlation is correspondingly coarse; the 48- and 60-base windows are
  better behaved.
- **No cross-blot scale exists.** All rankings are within-blot. There is no unified ranking in
  this report because the data do not support one.
- **The other-protein table** has four peptides, undefined category thresholds, and different
  protein constructs. It is context, not validation.
- **SP31 and the SP9 zero** are unresolved data questions carried through rather than patched.
- **Multiplicity.** Even the per-feature p-values that appear in the CSVs are exploratory. The
  family-wise permutation test in §4.2 is the one that should be read.
- **Generalisation.** Results apply to this collagen construct, host, assay and conditions.
  The thesis and Fu et al. both report that signal-peptide performance is target-dependent.

---
