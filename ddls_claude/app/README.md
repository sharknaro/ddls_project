# Findings dashboard — local app

An offline, self-contained dashboard illustrating the signal-peptide analysis and its
conclusion. No internet connection, no build step, no npm, no framework.

## Run it

From the repository root:

```bash
python -m http.server 8765 --directory ddls_claude/app
```

Then open <http://localhost:8765>.

It also works by opening `index.html` directly from disk — the data is loaded via a
`<script>` tag rather than `fetch`, so there is no cross-origin restriction. A server is
only needed if you want to share it on your network.

To serve it to other machines on the local network, bind all interfaces:

```bash
python -m http.server 8765 --bind 0.0.0.0 --directory ddls_claude/app
```

## Sharing it with someone else

**A `localhost` link cannot be shared** — it resolves to the recipient's own machine, so they
would get a connection error. Send the standalone build instead:

```bash
python ddls_claude/app/build_standalone.py
```

That inlines the data into **`findings_standalone.html`** — one 93 KB file with no server, no
internet and no accompanying files. Email it, and the recipient opens it by double-clicking.
Rebuild it after any change to `index.html` or `data.js`.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole app — markup, styles, charts. Vanilla JS and inline SVG. |
| `data.js` | `const DATA = {...}`, generated from the analysis outputs. ~50 KB. |
| `findings_standalone.html` | **The shareable one-file build.** Generated; do not edit by hand. |
| `build_data.py` | Regenerates `data.js` from the CSVs in `ouput/analysis/` and `ddls_claude/analysis/`. |
| `build_standalone.py` | Inlines `data.js` into `index.html` to produce the shareable file. |

## Regenerating the data

Every number shown is computed from `data/Information_for_Baris_corrected.xlsx` by the
analysis scripts — nothing in the app is illustrative or hard-coded. After re-running any
analysis script, refresh the app's data with:

```bash
python ddls_claude/app/build_data.py
```

## Sections

1. **Verdict** — the two answers: prediction (no, and it was tested) and biological
   information (yes, one lead).
2. **The measurements** — replicate-level values faceted by blot, each on its own scale;
   plus which rankings are stable under mean versus median.
3. **Feature screen** — the 34-feature association result, the permutation calibration that
   makes it interpretable, and the reliability ceiling that makes the null credible.
4. **The one lead** — the RBS-aware initiation-region folding energy, with its caveats.
5. **Can we model?** — the in-sample versus out-of-fold contrast.
6. **What the sequences are** — the engineered A-S-A cleavage region, the per-peptide UniProt
   comparison, and the cross-assay check against Fu et al.
7. **Limits** — what the analysis cannot say, and what would make the question answerable.

## Notes on the design

- Charts are faceted by blot rather than overlaid, because the three blots share no common
  scale. Overlaying them would imply a comparison the data do not support.
- Colours are the validated default data-viz palette; the categorical slots used were checked
  with the palette validator in both light and dark mode, all-pairs.
- Every chart has hover tooltips, and the tables carry the same numbers for anyone who cannot
  rely on colour.
- Light and dark themes both ship; the toggle is remembered per browser via `localStorage`
  and falls back to the OS setting.

## Caveat for presentation

The headline conclusion is a **negative result with one qualified positive lead**. The
"one lead" section states explicitly that the finding is not clean out-of-sample confirmation,
because a coding-sequence-only version of the same feature family was in the exploratory
screen. Please keep that caveat in place if you present or adapt this.
