# Hand-in checklist

Verified 4 November 2026. All figures regenerated from the committed scripts and cross-checked
against source CSVs.

## Upload slots

| # | Slot | File to upload | Status |
|---|---|---|---|
| 1 | Written report | `ddls_claude/handin/FINAL_REPORT.md` | ready |
| 2 | Runnable app or code | `ddls_claude/handin/code_and_app.zip` (81 files, 2.7 MB) | ready |
| 3 | Interview + analysis transcripts | the three files in `ddls_claude/handin/transcripts/` **plus** `AI_DISCLOSURE.md` | ready |
| 4 | Presentation slides | — | **not produced** (optional for PhD per the form) |
| 5 | Anything else (optional) | `ddls_claude/app/findings_standalone.html` | ready |

## Verification performed

| Check | Result |
|---|---|
| 12 key figures in the report match their source CSVs | pass |
| Leave-one-blot-out random forest figure matches | pass (−0.146) |
| UniProt counts match (8/32 exact, 18/30 differ, 13 motifs) | pass |
| Mandatory caveat on the positive lead present in report | pass |
| Zip contains no owner data (`data/`, .xlsx, .mp3, .pdf) | pass |
| Zip contains all 14 analysis scripts and the full app | pass |
| Step-6 outputs regenerated from the committed script | pass |
| Dashboard data consistent with CSVs | pass |

## Contents of `transcripts/`

- `20261020_pi_transcript.txt` — first data-owner interview
- `20261023_ddls_project_meeting2_transcript.txt` — second data-owner interview
- `claude-session-export.zip` (8.9 MB) — complete Claude Code session including two
  literature-screening subagent transcripts

## Notes

- The report is markdown. If the course requires PDF, convert before upload; no converter was
  available in this environment.
- The input workbook is intentionally excluded from the zip as the data owner's unpublished
  data. `REPRODUCE.md` states this and explains how to supply it.
- Slides were not produced. The upload form marks them for the oral presentation and for
  Master's students; add them if you are presenting.
