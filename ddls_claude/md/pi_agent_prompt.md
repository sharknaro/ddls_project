# Prompt for directing an agent to reproduce this analysis

Copy everything below the line. It specifies method, not conclusions: it tells the agent which
checks to run and what standards to hold, but never what the answers are. Findings reported
back are therefore independent corroboration rather than an echo.

If the agent is a smaller model, give it one numbered section at a time rather than the whole
prompt at once, and ask for the output file of each section before moving on.

---

## Task

You are analysing an experimental screen of 32 N-terminal signal peptides tested for
recombinant collagen secretion in *Bacillus subtilis*. Secretion was measured by Western blot
densitometry. Determine whether any sequence-derived feature of the peptides is associated with
measured secretion, and whether the evidence supports predicting or designing high-secretion
candidates.

A well-supported negative result is a valid and acceptable outcome. Do not manufacture a
positive finding, and do not soften a negative one.

## Data

- `data/Information_for_Baris_corrected.xlsx` — three sheets: peptide sequences (amino acid and
  nucleotide), a `Results` sheet with four blocks of replicate fold-change values, and a
  categorical table for other protein constructs.
- `data/20261020_pi_transcript.txt` and `data/20261023_ddls_project_meeting2_transcript.txt` —
  interviews with the data owner. These are the authoritative source for what the measurements
  mean. Read them before interpreting any number.
- `data/Paper_for_IDEAS.pdf` — Fu et al. 2018, a signal-peptide screen in the same organism.
- `data/PhD_Thesis_Final_Chapter2_CollagenProduction_HOJBERG.pdf` — the thesis chapter
  describing the experiment that produced this data. Read it in full; it contains the assay
  protocol and construct details the spreadsheet omits.

## Hard constraints — violating any of these invalidates the result

1. **The three main blots are separate experiments.** Each was normalised to its own gel mean,
   so values from different blots are not on a common scale. Never pool them into one numeric
   outcome. If you combine evidence, combine per-blot *effect estimates* (e.g. Fisher-z
   meta-analysis of per-blot correlations), never the values themselves.
2. **Collapse replicates to one value per peptide before any test or model.** A peptide with
   three replicates is one observation. Treating replicate rows as independent samples is
   leakage and inflates n by 3x.
3. **Analyse all candidates, never only the top performers.** The data owner explicitly warned
   about this. A feature common to good performers tells you nothing unless you also show poor
   performers lack it.
4. **The validation blot is a separate experiment.** Describe it on its own. Do not fit a
   conversion between blots.
5. **Split at peptide level** for any model. Scale and fit inside training folds only.
6. **Do not silently fix data anomalies.** Flag them for the owner and carry the data as
   supplied.
7. Correlation is not causation, and a predicted structure is not evidence of secretion.

## Method

### 1. Sequence QC — before anything else

For all 32 peptides check: amino-acid and nucleotide alphabets; whether nucleotide length is
exactly 3x amino-acid length; **whether each nucleotide sequence actually translates to its
listed amino-acid sequence**; whether each begins with an initiator methionine; duplicates.
Report every mismatch individually with the peptide ID. Do not correct any of them.

Then examine the **C-terminal three residues of every peptide** and tabulate them. Also
tabulate the first two residues. Report the distribution, not just examples.

### 2. Establish what the peptides actually are

The thesis plasmid table (pBS008–pBS039) and primer names map each SP number to a source gene.
Extract that mapping. Then, for each gene, retrieve the native sequence and its annotated
SIGNAL feature from UniProt (reviewed *B. subtilis* 168, taxid 224308, REST API) and compare
it residue-by-residue with the supplied sequence. Report: how many match exactly, how many
differ at the C-terminus, how many differ in length. Tabulate native versus supplied C-terminal
tripeptides side by side.

State clearly what this implies about whether the library is wild-type or engineered, and what
follows for comparisons to published work on those same named peptides.

### 3. Describe the outcome and measure its reliability

Per peptide per blot: mean, median, SD, CV, min, max, and within-blot rank. Plot replicate-level
values faceted by blot, each on its own scale.

Then do two things that are easy to skip:

- **Compare ranking by mean against ranking by median.** Report every peptide whose rank moves
  by two or more places, and every peptide whose CV exceeds 1.
- **Estimate the reliability ceiling.** Compute inter-replicate rank agreement within each blot,
  convert to the reliability of a k-replicate mean (Spearman–Brown), and take the square root.
  This is the largest correlation any feature could show against these measurements. You need it
  to interpret a null result: without it you cannot distinguish "no effect" from "too noisy to
  see one".

### 4. Derive features — all of them, before looking at any outcome

Compute a documented set covering: length; composition; hydrophobicity (name the scale); charge
and pI (name the method); region-based features for the n-region, hydrophobic core and
cleavage-proximal region; and nucleotide features including GC, GC3 and mRNA folding free energy
(name the software and version).

Two requirements specific to this step:

- **Test the stability of your region segmentation.** Whatever rule you use to find the
  hydrophobic region, repeat it under at least three settings (different thresholds, a second
  hydrophobicity scale) and report how much the region start and the region end move. Classify
  every region-derived feature as robust or fragile on that basis, and test only the robust ones.
- **Drop zero-variance features and say which they were.** A feature constant across all 32
  peptides cannot explain any difference between them. Report it as a finding about the library
  rather than discarding it silently.

Also report pairwise correlations among your features and list the pairs above |rho| 0.8. These
descriptors are not independent tests.

### 5. Test associations within blot, with honest multiplicity

For each feature, compute Spearman correlation with the per-peptide summary **within each blot
separately**. Report all three per-blot values, a combined estimate with a confidence interval,
and whether the direction is consistent across blots.

Then calibrate for the size of the screen: **permute the outcome within each blot several
thousand times, re-run the entire feature screen each time, and record the largest absolute
combined correlation.** Compare your observed best against that null distribution. This tells
you how large the best-looking association gets by chance when many correlated descriptors are
tried. Report the family-wise p-value.

Also run leave-one-peptide-out on your top features and report whether any correlation changes
sign.

### 6. Test one pre-specified hypothesis separately from the screen

Fu et al. propose that a **less negative** folding free energy near the translation-initiation
region leaves the ribosome-binding site and start codon accessible, favouring secretion —
predicting a positive correlation. Their feature spans the transcript from the transcription
start site, so it requires the 5′ context, not just the peptide coding sequence.

Find the shared upstream sequence in the thesis (look at the forward-primer overhangs used for
cloning, which carry the RBS and start codon). Recompute folding energy over that context plus
the first 30/48/60 bases of each peptide's coding sequence, and test it.

Because this is a single directional hypothesis specified in the literature rather than one of
many screened descriptors, test it against a **single-hypothesis permutation null**, one-sided,
with the family limited to the window-size choice. Explain in your report why that null differs
from the one in step 5 and why using the step 5 null here would be the wrong test.

If it is significant, check it is not a proxy: report what it correlates with among your other
features, and test those confounders on their own. Then state plainly that this feature is a
refinement of a family already examined in the screen, so it is not clean out-of-sample
confirmation.

### 7. Decide on modelling by testing it, not by asserting it

Fit at least: a baseline that predicts the training mean, a regularised linear model, a tree
ensemble, and a nearest-neighbour model. Outcome: within-blot percentile rank. Use **both**
leave-one-peptide-out and **leave-one-blot-out** cross-validation. Leave-one-blot-out is the
realistic test, because the practical question is predicting peptides measured in a new batch.

Report out-of-fold performance for every model. Then fit each model on all 32 peptides and
report its **in-sample** performance in the same table, side by side with the honest out-of-fold
number. Explain what the gap between the two columns means.

Only compute a permutation null for a model that actually scored above chance; say so if none
did.

### 8. Context, kept separate

Describe the seven shared peptides in the validation blot without fitting a conversion: rank
agreement with their original blots, and the direction of any scale shift.

Summarise the four-peptide other-protein table on its own terms. `No` means product not produced
(owner, meeting 2). `Low`/`Medium`/`High` have no stated thresholds — do not convert them to
numbers or use them as an outcome.

If any of the 32 peptides appear in published screens with quantitative values, compare their
standing across assays — but first check whether the sequences are actually identical (see
step 2), and caveat accordingly if they are not.

## Output

Produce a reproducible report containing: methods and feature definitions with software
versions; the QC findings; plots and tables; the association results with their multiplicity
calibration; the modelling assessment; candidate-level findings **within their original blots
only**; and explicit limitations.

Also produce a list of questions for the data owner, covering every anomaly you flagged and
every piece of missing metadata that limited the analysis.

## Standards

- State sample sizes everywhere. Effective n here is 8, 13 and 11, not 32.
- Report uncertainty, not just point estimates.
- Distinguish what the owner stated, what the files show, and what you inferred.
- If a result is null, say so directly and show the evidence that the measurements were good
  enough to have detected an effect.
- Never present in-sample fit as performance.
- Any proposed new sequence or "high performer" is a hypothesis for experimental testing.
- If anything you find contradicts what this prompt implies you should look for, report that
  instead. The method matters; the expected answer does not.
