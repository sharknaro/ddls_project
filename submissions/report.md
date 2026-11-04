# Signal-peptide secretion report

## The question

Do sequence features of 32 N-terminal signal peptides predict recombinant collagen secretion in *Bacillus subtilis*, and does the evidence support training a model to design new high-secretion peptides?

## The data & files

The analysis used the corrected workbook (`data/Information_for_Baris_corrected.xlsx`), which contains:

- **Sequences:** 32 signal peptides (`SP1`–`SP32`), 21–42 residues, with matched nucleotide sequences, plus one ~110-aa bovine collagen construct.
- **Results:** replicate "fold-change" values in four blocks — Blot 1 (8 peptides), Blot 2 (13), Blot 3 (11), and a separate validation blot (7).
- **Other proteins:** 4 peptides × 7 constructs, categorical labels only.

Band intensity was normalised per lane by Ponceau total protein, then divided by the mean of normalised intensities **on that same membrane** (owner's account, confirmed against the thesis methods). Each blot is therefore centred on the mean of a *different* peptide subset.

**The three blots do not share a numeric scale. The effective sample size is 8, 13 and 11 — not 32.** Every analysis below respects that boundary; no blot-normalised values were ever pooled.

## The right outcome definition

For a feature–secretion question, the relevant unit is **one value per peptide per blot**, not one value per replicate. Replicates are biological repeats of the same peptide; treating the 96 replicate rows as independent observations would have tripled the apparent sample size and inflated every result. Replicates were therefore collapsed to a per-peptide mean before any test or model, with the median retained as a sensitivity check.

Where effects are combined across blots, it is the three per-blot *effect estimates* that are combined by inverse-variance Fisher-z meta-analysis — never the values themselves.

## Data check

All 32 peptides passed alphabet, reading-frame and duplication checks. Two anomalies were found and **left uncorrected** for the data owner to resolve:

| Finding | Detail |
|---|---|
| `SP31` | Listed amino-acid sequence begins `V`; its own nucleotide sequence begins `ATG` (= `M`). Residues 2–30 agree exactly. The only AA/NT disagreement in the sheet. |
| `SP9` | One replicate recorded as exactly 0, retained as a numeric zero. Owner's tentative reading is "no secretion", origin unverified. |

## The trap and honest truth

### Trap 1: the feature screen looks promising until it is calibrated

34 sequence descriptors were computed for all 32 peptides **before any outcome was consulted**, then correlated with secretion within each blot. The best result was ρ = 0.369.

That number means nothing on its own. Screening 34 correlated descriptors across three small blots will produce a large correlation by chance. To measure how large, the outcome was permuted **within each blot 5,000 times and the entire screen re-run**:

| Quantity | Value |
|---|---:|
| Best observed \|combined ρ\| | 0.369 |
| Permutation null, **median** best-of-panel | **0.441** |
| Permutation null, 95th percentile | 0.598 |
| **Family-wise p-value** | **0.81** |

**The best real feature is weaker than the median result on shuffled data.** Every per-feature confidence interval crosses zero. Six features point the same way in all three blots, but they are mutually correlated at |ρ| ≥ 0.8 — one property measured six ways, sitting inside the chance band.

### Trap 2: a null result is worthless without a detectability check

"No association" and "too noisy to detect one" are different claims. Inter-replicate rank agreement was converted via Spearman–Brown to the reliability of a 3-replicate mean:

| Blot | Mean inter-replicate ρ | Reliability of mean | Max detectable ρ |
|---|---:|---:|---:|
| Blot 1 | 0.476 | 0.732 | 0.855 |
| Blot 2 | 0.581 | 0.806 | 0.898 |
| Blot 3 | 0.418 | 0.683 | 0.827 |

A feature perfectly predicting true secretion could correlate at about **0.86** against these measurements. There was ample room to detect a moderate effect. **The null is informative, not underpowered.**

### Trap 3: in-sample model fit is not performance

Four model families were fitted with splitting at **peptide** level and scaling inside training folds only.

| Model | In-sample ρ | Leave-one-peptide-out | Leave-one-blot-out |
|---|---:|---:|---:|
| Random forest | **0.964** | **−0.187** | −0.146 |
| Ridge (α=10) | 0.729 | −0.130 | −0.078 |
| Ridge (α=100) | 0.673 | −0.126 | −0.044 |
| k-NN (k=5) | 0.289 | −0.119 | −0.070 |

A random forest fitted and scored on the same 32 peptides reproduces their ranking almost perfectly. Trained without each peptide and asked to predict it, it does **worse than guessing**. With 34 features and 32 observations a model memorises the dataset while learning nothing transferable. **Every out-of-fold score is negative under both schemes**, including leave-one-blot-out — the realistic test of predicting peptides from a new experiment.

### Trap 4: the library cannot report on its own cleavage region

Each peptide was compared with its native UniProt sequence (reviewed *B. subtilis* 168, taxid 224308), using the SP→gene mapping recovered from the thesis plasmid tables.

| | Native (UniProt) | Supplied |
|---|---|---|
| Distinct C-terminal motifs | **13** (ASA 12, AHA 3, AKA 3, AEA 2, ADA 2, +8 singletons incl. `LAG`) | **1** (ASA, 32/32) |

Only **8 of 32** peptides match their native signal peptide exactly; **18 of 30** differ at the C-terminus. The cleavage region was **engineered to a uniform A-S-A**, not inherited. This is a defensible design choice — it standardises signal-peptidase processing — but it means the A-x-A motif that Fu et al. associate with good performers is a **constant here, not a variable**. Hydrophobicity is similarly range-restricted (GRAVY median 1.01; 26 of 32 between 0.6 and 1.4, on the optimum reported by Grasso et al.).

Notably, **SP1/AmyE** — the classic *B. subtilis* secretion tag — ranks 7th of 8 in its blot and is among the most heavily modified peptides (native ending `LAG`, not an A-x-A motif, plus six extra residues).

### The one honest positive

Fu et al. (2018) propose that a *less negative* folding free energy near the translation-initiation region leaves the ribosome-binding site accessible, predicting a **positive** correlation. This became computable only once the thesis supplied the shared 5′ context (RBS `AGGAGGAATATAC` + `ATG`, identical across constructs).

| | Blot 1 | Blot 2 | Blot 3 | Combined |
|---|---:|---:|---:|---:|
| RBS-aware ΔG | +0.262 | +0.632 | +0.491 | **+0.515** |
| Previous coding-only version | −0.443 | +0.190 | +0.346 | +0.106 |

One-sided permutation test, 20,000 within-blot shuffles: **p = 0.0042** as a single pre-specified hypothesis; **p = 0.0118** corrected for three window sizes. Leave-one-peptide-out range +0.466 to +0.594 with no sign flips. Not a proxy — GC alone gives −0.02, length alone +0.25.

**Mandatory caveat:** a coding-sequence-only version of this feature family was already in the 34-feature screen and ranked second, so this is a **refinement of an examined family, not clean out-of-sample confirmation**. The true transcription start site is unknown, so the window is approximate. No mechanism is established.

## Answer/recommendation

**No — do not train a predictive model or propose synthetic designs from this dataset.** This was tested across four model families and two validation schemes rather than assumed, and every out-of-fold score was negative.

The owner **can** act on this as:

- a **within-blot prioritisation** of reproducible candidates: **SP5** (Blot 1, CV 0.14) and **SP26** (Blot 3, CV 0.21) are both high and stable;
- a **warning about ranking instability**: 8 of 32 peptides move ≥2 ranks between mean and median, including **SP4**, which leads Blot 1 by mean but falls to 5th by median and carries the unresolved secondary band;
- a **specific, testable hypothesis** about mRNA accessibility at the translation-initiation region.

The owner **cannot** act on this as a cross-blot ranking, a validated feature rule, a predictive model, a mechanism, or evidence that any peptide will perform on a different protein target. Five of these peptides overlap Fu et al.'s best amylase performers and rank agreement with collagen is ρ = −0.20 (n = 5) — consistent with documented target-dependence, though confounded by the C-terminal modification.

**This is a negative result about the dataset's shape, not about the biology or the quality of the experiment.** The screen identified reproducible performers, produced data that could be tested rigorously, and generated a testable lead.

## Caveats & next steps

1. **Put a shared reference lane on every gel.** The single largest structural fix — it converts three incomparable blots into one comparable dataset. Nothing analytical substitutes for it.
2. **Measure more peptides on that common scale.** This matters more than any modelling refinement; Grasso et al. required ~4,400 informative peptides to fit a comparable model.
3. **Supply raw densitometry** to audit the normalisation, resolve the SP9 zero, and assess the SP4 secondary band.
4. **Supply the transcription start site and full 5′UTR** so the one positive lead can be tested against its published definition.
5. **Confirm the two sequence anomalies** — `SP31`'s `V` versus `M`, and whether the uniform A-S-A standardisation was intentional.
6. **Vary the C-region deliberately** in any future library if cleavage effects are of interest.
7. If modelling is attempted later, split at peptide/design level and treat prediction of peptides from a **new experimental batch** as the honest test.

## AI-use disclosure

**Agent A (Data owner)** provided the experimental data, the project goal, the assay account, and the domain constraints — keep the blots separate, include poor performers, treat the validation blot as a separate experiment.

**Agent B (Claude, via Claude Code)** performed essentially all computational work: data inspection and QC, the 34 sequence descriptors, the statistical analyses including the permutation calibration and reliability estimate, the machine-learning evaluation, the literature screening and UniProt retrieval, the interactive dashboard, and the drafting of this report. It did **not** generate, simulate or alter any measurement; the SP9 zero and the SP31 discrepancy were flagged, not patched.

**Person (I)** set the research question, conducted the data-owner interviews, supplied and enforced the domain constraints, challenged AI-proposed interpretations — including requiring that the reliability ceiling be computed before any null result was accepted — re-ran the analysis scripts to verify outputs, and traced every reported number to its source file. That verification caught a real defect: a stale background process had overwritten the modelling outputs with a different random-forest configuration than the committed script specified. It was re-run and is recorded rather than quietly fixed.
