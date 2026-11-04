# AI use disclosure

**Project:** Signal-peptide features and recombinant collagen secretion in *Bacillus subtilis*
**Author:** Baris Akar (bakar@dtu.dk) · **Date:** 4 November 2026

This statement is deliberately explicit. The computational work in this project was done with
heavy AI assistance, and the submission should be read with that in mind.

---

## 1. Tools used

| Tool | Role |
|---|---|
| **Claude (Anthropic), via Claude Code** | Primary analysis and programming assistant. Wrote and executed essentially all of the analysis code; performed the statistical analyses; screened the literature; drafted the reports and built the dashboard. |
| **A smaller local agent ("PI agent")** | Used in the early phase for the initial data inspection, analysis planning and the first descriptive pass. |

Automated speech-to-text was used to transcribe the two data-owner interviews. Those
transcripts contain recognition errors, which are flagged in the project documents and were
never treated as verified technical terms.

---

## 2. What the AI did

Substantially all of the computational work:

- **Data inspection and QC** — workbook structure, sequence alphabet/frame/translation checks,
  identification of the SP31 amino-acid/nucleotide discrepancy.
- **Feature engineering** — all 34 sequence descriptors, the region-segmentation procedure and
  its stability analysis, the mRNA folding calculations.
- **Statistics** — within-blot Spearman correlations, Fisher-z meta-analysis, the permutation
  multiplicity calibration, the Spearman–Brown reliability estimate, the pre-specified
  hypothesis test.
- **Machine learning** — model selection, the cross-validation design including leakage
  controls, and all fitting and evaluation.
- **Literature work** — reading the two supplied papers, searching for and assessing external
  *B. subtilis* signal-peptide resources, retrieving native sequences from UniProt.
- **Writing and visualisation** — the analysis reports, this document, and the interactive
  dashboard.

Most code in `ouput/analysis/` and `ddls_claude/analysis/` was written by Claude. The
`ouput/analysis/run_steps_2_8.py` descriptive pass originated with the smaller agent and was
reviewed and extended afterwards.

---

## 3. What the AI did **not** do

- It did **not** generate, simulate or impute any experimental data. Every measurement comes
  from the data owner's workbook.
- It did **not** alter any measurement. The SP9 zero was retained as a numeric zero and the
  SP31 V/M discrepancy was left uncorrected, both flagged for the owner instead.
- It did **not** conduct the experiments, which were performed by the data owner.
- It did **not** decide the scientific framing alone. The constraints that shape the analysis —
  keep the blots separate, include poor performers, treat the validation blot as a separate
  experiment — come from the data owner's interviews.
- It did **not** have authority over conclusions. Claims were accepted only where traceable to
  a named output file.

---

## 4. Direction and verification by the author

The author set the research question, ran the interviews, supplied the domain constraints,
rejected analyses that overstepped them, and directed every phase of the work.

Verification performed:

- **Scripts were re-run** and outputs compared against the figures quoted in the reports. This
  caught a genuine defect: a stale background process had overwritten the step-6 results using
  a different random-forest configuration than the committed script specified. The script was
  re-run and all downstream artefacts regenerated. It is recorded in §9 of `FINAL_REPORT.md`
  rather than quietly fixed.
- **Numbers were traced to source files.** Every figure in the report and dashboard comes from
  a named CSV in `ouput/analysis/` or `ddls_claude/analysis/`, not from prose.
- **AI-proposed interpretations were challenged**, including requiring that the measurement
  reliability ceiling be computed before any null result was accepted, and that the one positive
  finding carry an explicit caveat about not being clean out-of-sample confirmation.
- **Data anomalies were referred to the data owner** rather than resolved by the AI.

---

## 5. Specific AI-related risks and how they were handled

| Risk | Handling |
|---|---|
| Fabricated or drifted numbers | Every reported figure regenerated from scripts and traced to a CSV before submission. |
| Overstated findings | The single positive result is reported with its caveats in the report, the dashboard and the slides. In-sample model fit is never presented as performance. |
| Plausible-but-wrong code | Analysis scripts are included so the work can be re-run and audited rather than taken on trust. |
| Silent "fixing" of awkward data | SP31, the SP9 zero and the A-S-A standardisation were escalated to the data owner as open questions, not patched. |
| Confirmation bias from a leading prompt | The permutation calibration and the leave-one-blot-out validation were designed to be capable of returning a negative result, and did. |

---

## 6. Transcripts included

The `transcripts/` folder contains:

- `20261020_pi_transcript.txt` — first data-owner interview
- `20261023_ddls_project_meeting2_transcript.txt` — second data-owner interview
- `claude-session-export.zip` — the complete Claude Code session, including the transcripts of
  two subagents used for literature screening

The session export is a verbatim record: every prompt, tool call, script, intermediate result
and correction, including the mistakes and the dead ends.

---

## 7. Summary statement

> The experimental data are the data owner's. The research question, the domain constraints and
> the direction of the work are the author's. The computational analysis, code, statistics,
> literature review and written drafts were produced with substantial assistance from Claude
> (Anthropic). Results were verified by re-running the analysis scripts and tracing every
> reported number to its source file. Full session transcripts are included.
