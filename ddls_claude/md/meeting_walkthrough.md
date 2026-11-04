# Meeting briefing: walking the data owner through the analysis

Companion to `ddls_claude/app/findings_standalone.html`. Section 5 is the walkthrough script;
sections 1–4 are what you need in your head before you start.

---

## 1. What was done, in one paragraph

We took the 32-peptide screen and asked a single question: does anything about the signal
peptide sequence predict how much collagen was secreted? We computed 34 sequence descriptors
for all 32 peptides, tested each one against secretion **within each blot separately**,
calibrated the result against what random chance produces, measured how reliable the
measurements themselves are, and then fitted four model families under honest
cross-validation. The answer is that no feature predicts secretion beyond chance, and no model
predicts held-out peptides better than guessing — but one hypothesis taken from the literature
does hold up, and several things about how the library was built explain why the rest didn't.

---

## 2. How it was done — the four rules that make the answer credible

These are worth stating early, because they are the reasons he should believe a negative
result rather than suspect sloppy analysis. Three of the four come from his own cautions.

1. **The three blots were never pooled.** Each was normalised to its own gel mean, so they sit
   on incomparable scales. Every test was run within a blot; where effects are combined, it is
   the three *effect estimates* that are combined, never the values.
2. **Replicates were collapsed to one value per peptide before anything was fitted.** A peptide
   with three replicates is one observation. Treating replicate rows as independent would have
   tripled the apparent sample size — a common and invisible error.
3. **All 32 candidates were analysed, never only the top performers.** This was his specific
   warning, and it is exactly what the Fu et al. paper did not do.
4. **Model splitting was at peptide level**, with scaling fitted inside training folds only, so
   no peptide appears in both training and test.

---

## 3. The results, as numbers to quote

| Finding | Number |
|---|---|
| Best feature–secretion correlation across 34 descriptors | **ρ = 0.37** |
| What the same screen produces on *shuffled* data (median) | **ρ = 0.44** |
| Family-wise p-value | **0.81** |
| Measurement reliability ceiling | **0.86** |
| Random forest, fitted and scored on the same 32 peptides | **ρ = 0.96** |
| Same model, predicting each held-out peptide | **ρ = −0.19** |
| Peptides matching their native UniProt sequence exactly | **8 of 32** |
| Supplied peptides ending A-S-A | **32 of 32** (native: 13 different motifs) |
| RBS-aware initiation-region folding energy | **ρ = +0.51**, p = 0.004 |

---

## 4. Why it did not work — four reasons, in order

Give them in this order. The first is the cause; the rest explain why it could not be rescued.

**a. There was no signal to learn.** The best of 34 descriptors correlated at 0.37, while
shuffling the outcome and re-running the entire screen produces 0.44 on average. A model's job
is to combine features that individually carry information. If none does, there is nothing to
combine, and no algorithm fixes that.

**b. The effective sample size is 8, 13 and 11 — not 32.** Because the blots cannot be pooled,
any model is learning from three very small datasets. With 34 features against 32 observations
there are more parameters than data points, so a model can reproduce the training set exactly
while learning nothing transferable. That is not a hypothetical: random forest scores 0.96
in-sample and −0.19 out-of-fold.

**c. It is not a noise problem — and this is the part that makes the negative credible.**
Inter-replicate agreement gives a reliability of 0.68–0.81, so a feature that perfectly
predicted true secretion could still have correlated at about 0.86. There was ample room to
detect a real effect. None appeared.

**d. The library itself was built in a way that suppresses variation.** All 32 peptides end
A-S-A, though their native endings span 13 different motifs — so the cleavage region was
standardised and cannot explain differences. All 32 are fused to the same collagen, so the
first residues of the mature protein are constant too. And hydrophobicity is range-restricted:
GRAVY median 1.01, with 26 of 32 peptides between 0.6 and 1.4, sitting right on the optimum
published by the ETH group. Several of the feature families that should matter biologically
were held fixed by the design.

**The honest framing:** this is a negative result about *this dataset's shape*, not about the
biology, and not about his experiment, which was a perfectly reasonable screen. The constraint
is the number of peptides measured on a common scale.

---

## 5. The walkthrough — suggested order and what to say

The app's tabs are clickable in any order. **Do not walk them left to right.** The order below
builds the argument; the tab order does not.

Roughly 25 minutes. Times are a guide.

### Opening (before the app) — 1 min

Say what you set out to do and that the answer is a qualified no, so he is not waiting for a
reveal. Something like: *"I tested whether sequence features predict secretion. They don't —
and I want to show you why I believe that rather than just assert it. There is one thing that
did hold up, and a couple of things about the library I need to ask you about."*

### Tab 1 — **Verdict** · 2 min

Set the frame. Two questions with different answers: prediction (no, and it was tested) and
biological information (yes, one lead). Read the four tiles. Then move on quickly — this tab is
a promise, the rest of the walkthrough is paying it off.

### Tab 2 — **The measurements** · 4 min

Establish what the data are before claiming anything about them.

- Point at the **three separate panels** and say the y-axes are not comparable — this is his own
  warning, implemented. The dashed line is each gel's mean.
- Then the **rank-stability table**: eight peptides move two or more places depending on whether
  you rank by mean or median. **SP23** goes from 3rd to 9th; its replicates are roughly 0.00,
  0.07 and 3.42. **SP4** leads Blot 1 by mean but falls to 5th by median — and it is the peptide
  with the secondary band.
- End on the useful part: **SP5 and SP26** are both high and reproducible. That is actionable
  for him regardless of everything else.

> This tab buys credibility. It shows you engaged with the measurement before reaching for
> models.

### Tab 3 — **Feature screen** · 5 min

The core test.

- The forest plot: 34 descriptors, each tested **within each blot**, every confidence interval
  crossing zero. Note the shaded band is what chance produces.
- Then the decisive number: shuffle the outcome within each blot 5,000 times, re-run the whole
  screen, and the best result on *random* data is 0.44 — larger than the 0.37 we actually found.
- **Pre-empt the obvious objection yourself** by scrolling to the reliability table: the
  measurements reproduce well enough that a real effect could have correlated at 0.86. So the
  null is not "the assay is too noisy", it is "there is nothing there to find".

> If he pushes back anywhere, it will be here. The reliability ceiling is your answer.

### Tab 4 — **Can we model?** · 4 min

The single most persuasive image in the whole thing.

- Point at the random forest row: **0.96 in-sample, −0.19 out-of-fold**, same model, same data.
- Say plainly: with 34 features and 32 observations, a model memorises the dataset. Any
  impressive-looking figure of this kind is measuring memorisation, not prediction.
- Then the table below: every model, both validation schemes, all negative — including
  leave-one-blot-out, which is the realistic test of predicting peptides from a new experiment.

> This is where "should we train a model?" gets answered with evidence instead of opinion.

### Tab 5 — **What the sequences are** · 5 min

Now explain *why* the screen was always going to struggle — and ask him your questions.

- The motif chart: native C-termini span 13 motifs; all 32 supplied peptides end A-S-A. **Ask
  him directly whether that standardisation was deliberate and why A-S-A.** It is a reasonable
  design choice, but it means the library could never report on cleavage-region effects.
- Only **8 of 32** match their native sequence exactly; six also differ in length.
- **SP1/AmyE** — the classic *B. subtilis* secretion tag — ranks 7th of 8, and is one of the most
  modified peptides in the set. Ask whether the modification rather than the peptide might
  explain that.
- Mention **SP31**: its amino-acid sequence starts with V but its own nucleotide sequence starts
  ATG. One-character disagreement, uncorrected, needs his call. He enjoyed the `S19` / `Np` /
  Greek-`Η` finds last time; this is the same kind.
- The cross-assay table: five peptides overlap Fu et al.'s best amylase performers, and rank
  agreement is −0.20. Caveat it honestly — those are not the same sequences, because of the
  C-terminal modification.

> This tab turns the negative from "we found nothing" into "here is structurally why, and here
> are three things only you can answer."

### Tab 6 — **The one lead** · 3 min

End the evidence on something forward-looking.

- mRNA accessibility at the translation-initiation region: **ρ = +0.51, positive in all three
  blots, p = 0.004**, in the direction Fu et al. predicted.
- Say why it only became computable now: **his own thesis** supplied the shared RBS/5′UTR in the
  primer overhangs.
- Then state the caveats before he does: it is a refinement of a feature family that was already
  in the exploratory screen, so it is not clean out-of-sample confirmation; the true
  transcription start site is still unknown; and ρ ≈ 0.5 against a 0.86 ceiling is moderate.

> Stating the caveats yourself is what makes the finding credible. If he has to extract them
> from you, it reads as overselling.

### Tab 7 — **Limits** · 3 min, then the ask

Close on what would make the question answerable, and turn it into requests:

1. **A shared reference lane on every gel.** This is the single biggest structural fix — it
   turns three incomparable blots into one comparable dataset.
2. **More peptides measured on that common scale.** Matters more than any analytical refinement.
3. **Raw densitometry** — would let the normalisation be audited, the SP9 zero resolved, and the
   SP4 secondary band assessed.
4. **The transcription start site and full 5′UTR** — needed to test the one positive lead against
   its published definition.

---

## 6. Questions he is likely to ask, and how to answer

**"Could you not just combine the three blots?"**
Not without a shared calibrator. Each is centred on the mean of a *different* subset of
peptides, so a fold-change of 1 means a different absolute amount on each gel. Combining them
would inject a gel-specific offset of unknown size and manufacture signal that isn't there.
This is also what his own thesis figure caption says.

**"Isn't 32 enough? People publish on less."**
It is three sets of 8, 13 and 11, against 34 features. And the comparison is instructive: the
ETH group needed about 4,400 informative peptides to fit their model.

**"Maybe the features were the wrong ones."**
Possible, and worth saying honestly. But the ones tested cover what the literature points at —
hydrophobicity on two scales, charge, pI, region composition, length, GC, codon position and
mRNA folding. And the strongest published feature, the A-x-A cleavage motif, is a constant here
by construction.

**"The paper found a correlation though."**
Fu et al. analysed **16 peptides — their 15 best plus wild-type** — with no correlation
coefficient and no p-value anywhere in the paper. Their sequence logos use selected positives
with no negative set. They also report *no* correlation for SignalP D-score or pI, and conclude
that in-silico prediction is not currently feasible. Their paper supports this result rather
than contradicting it.

**"So the experiment was a waste?"**
No — and do not let this one pass. It identified reproducible high performers (SP5, SP26, SP19),
it produced a dataset that could be tested rigorously, and it generated a specific, testable
lead about mRNA accessibility. What it cannot do is support a predictive model, which is a
statement about sample size and scale, not about the quality of his work.

**"What about AlphaFold?"**
It would add more features to the same 32 outcomes. The multiplicity test shows that adding
feature families to this sample size mostly adds chances for a spurious result. Also, isolated
signal peptides have no well-defined solution structure — their relevant conformation is in the
membrane and translocon, and they are cleaved during secretion.

---

## 7. Three things to be careful about

- **Do not call it a failed analysis.** It is a negative result with a quantified bound, which
  he said in the first interview he would accept.
- **Do not present the RBS finding as a discovery.** It is a lead with stated caveats. If it
  later fails to replicate, how you described it now is what will matter.
- **The SP→gene mapping and the UniProt comparison are read from his thesis and a public
  database, not from the workbook.** Ask him to confirm the mapping before either of you builds
  on it.
