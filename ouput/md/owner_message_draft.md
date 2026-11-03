# Draft message to the data owner

Draft for Baris to send before the next meeting. Adapt the tone as you like — the content is
what matters. Each question is written so it can be answered in one line.

---

Hi Alexiou,

Quick update plus a few questions before we meet, mostly things I'd rather confirm with you
than assume — you'll recognise the pattern from last time.

**1. Another one of those "organic traps" — SP31.**

In the sequence sheet, SP31's amino-acid sequence starts with **V** (`VRKSLITLGLASV…`), but its
own nucleotide sequence starts with **ATG**, which translates to **M**. Residues 2–30 match
perfectly, all 31 other peptides start with M, and ATG is the start codon — so I think the V is
a typo for M. It's the only AA/nucleotide disagreement anywhere in the sheet.

I have **not** changed it, same as before. Can you confirm which letter is correct?

**2. Was the C-terminal A-S-A deliberate?**

All 32 peptides end in **A-S-A** — positions −3, −2, −1 are identical across the whole library.
Was the cleavage region fixed on purpose (to standardise signal-peptidase processing?), or is it
just inherited from the source peptides?

I ask because it changes what we can conclude. The Fu et al. paper highlights an A-x-A cleavage
motif in their best performers — but here it's in 32 out of 32, so it's a constant, not a
variable, and it can't explain why some of your peptides secrete better than others. If the
cleavage region is something you'd want to learn about, a future library would need to vary it
on purpose.

**3. The two things you offered last time — these are now the bottleneck.**

- **Raw band intensities / densitometry.** This would let me audit the normalisation, settle
  whether SP9's zero is a true zero or below detection, and check the replicate structure.
  Several caveats in my report disappear the moment this exists. Even partial or messy is fine.
- **The RBS / 5′UTR and terminator context.** Without the upstream sequence I can only compute
  mRNA folding energy starting from each peptide's own start codon — which is *not* the
  quantity Fu et al. reported (theirs spans the translation-initiation region including the
  RBS). So right now I can't properly test the one published quantitative lead we have. If the
  upstream context really is identical across all constructs, then one copy of it is all I need.

**4. One thing I'd flag on SP4.**

SP4 is top of Blot 1 by mean, but its replicates are 0.67 / 1.00 / 3.16 — so by median it drops
to 5th. It's also the peptide your thesis flags for the recurring secondary band. Before anyone
treats it as the Blot 1 winner, do you remember whether the secondary band was present in these
specific blots? You mentioned you might be able to tell me which peptides showed two bands.

**Where the analysis stands**

The honest headline is a negative result, which you said would be acceptable. I computed 34
sequence features (composition, charge, hydrophobicity by region, pI, GC/codon statistics, mRNA
folding) for all 32 peptides, and tested them within each blot separately — never pooling across
blots, never using only the top performers.

No feature is associated with secretion beyond chance. I checked this properly by shuffling the
outcomes within each blot 5,000 times and re-running the entire screen: the best real
correlation is actually *weaker* than the typical best correlation on randomised data.

Importantly, this isn't because the measurements are too noisy — I checked. Your replicates
agree well enough that a genuinely predictive feature could have shown a correlation of about
0.86. There was room to find something; there just isn't anything there.

So my current recommendation is that training a model on these 32 peptides isn't defensible, and
AlphaFold would add more features to the same 32 outcomes rather than more evidence. I'll bring
the full reasoning and the candidate-by-candidate rankings (within each blot) to the meeting.

Thanks — and genuinely, the SP31 thing was fun to find.

Baris
