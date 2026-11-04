/* Build the project presentation as a structured .pptx.
   Theme + layouts + sections; charts are the slide-grade PNGs from make_figures.py. */
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(path.join(
  "C:", "Users", "bakar", "AppData", "Local", "Claude-Data", "claude_pzs8sxrjxfjjc",
  "local-agent-mode-sessions", "skills-plugin",
  "9606e98c-890a-47ed-a81b-9fcc22f2c2e8", "1d413830-1073-4ef7-b093-812cdfddf559",
  "skills", "pptx", "scripts", "apply_theme.js"));

const HERE = __dirname;
const FIG = (n) => path.join(HERE, "fig", n);
const OUT = path.join(HERE, "..", "package", "slides.pptx");

const THEME = {
  name: "Signal peptide analysis",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "16202A", lt1: "FFFFFF", dk2: "1B3A5C", lt2: "F2F4F6",
    accent1: "2A78D6", accent2: "1BAF7A", accent3: "EB6834",
    accent4: "EDA100", accent5: "52514E", accent6: "8A8882",
    hlink: "2A78D6", folHlink: "1B3A5C",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.3 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Baris Akar";
pres.title = "Signal peptides and collagen secretion in Bacillus subtilis";
const C = pres.SchemeColor;

const W = 13.3, H = 7.5, M = 0.72;
const INK = C.text1, MUT = "8A8882", SEC = "52514E";
const BLUE = C.accent1, TEAL = C.accent2, ORANGE = C.accent3, GOLD = C.accent4;

/* ---------------------------------------------------------------- layouts */
pres.defineSlideMaster({
  title: "COVER", background: { color: "16202A" },
  objects: [
    { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 1.55, w: 10, h: 0.34,
        fontSize: 12, bold: true, charSpacing: 2.4, color: "1BAF7A" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.0, w: 11.4, h: 2.2,
        fontSize: 40, bold: true, color: "FFFFFF", valign: "top", align: "left" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.3, w: 8.6, h: 1.0,
        fontSize: 17, color: "C9D3DC", valign: "top" }, text: " " } },
    { placeholder: { options: { name: "meta", type: "body", x: M, y: 6.25, w: 8.6, h: 0.8,
        fontSize: 12.5, color: "8FA0AE", valign: "top" }, text: " " } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENT", background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.46, w: 10, h: 0.3,
        fontSize: 11.5, bold: true, charSpacing: 2.2, color: "1BAF7A" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.78, w: 11.9, h: 0.72,
        fontSize: 30, bold: true, color: "16202A", valign: "top", align: "left" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 1.7, w: 11.9, h: 4.6,
        fontSize: 15, color: "52514E", valign: "top" }, text: " " } },
    { placeholder: { options: { name: "note", type: "body", x: M, y: 6.62, w: 11.9, h: 0.6,
        fontSize: 11.5, color: "8A8882", valign: "top" }, text: " " } },
    { text: { text: "Signal peptides & collagen secretion", options: { x: 10.6, y: 6.98,
        w: 2.4, h: 0.3, fontSize: 9.5, color: "A9A8A2", align: "right", isTextBox: true } } },
    { placeholder: { options: { name: "slideNumber", type: "sldNum", x: 0.42, y: 6.98,
        w: 0.6, h: 0.3, fontSize: 9.5, color: "A9A8A2" } } },
  ],
});

pres.defineSlideMaster({
  title: "CLOSE", background: { color: "1B3A5C" },
  objects: [
    { placeholder: { options: { name: "eyebrow", type: "body", x: M, y: 0.46, w: 10, h: 0.3,
        fontSize: 11.5, bold: true, charSpacing: 2.2, color: "7FD9B6" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.78, w: 11.9, h: 0.8,
        fontSize: 30, bold: true, color: "FFFFFF", valign: "top", align: "left" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 2.1, w: 11.9, h: 4.4,
        fontSize: 15, color: "D5DFE8", valign: "top" }, text: " " } },
  ],
});

/* ---------------------------------------------------------------- helpers */
function card(s, { x, y, w, h, fill = "F2F4F6", accent = null, name }) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.07, fill: { color: fill },
    line: { color: "E4E6E9", width: 1 }, objectName: name,
  });
  if (accent) {
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.26, y: y + 0.26, w: 0.17, h: 0.17,
      fill: { color: accent }, line: { color: accent, width: 0 },
      objectName: name + "-dot",
    });
  }
}
function stat(s, { x, y, w, h = 1.3, value, label, color = INK, size = 27 }) {
  card(s, { x, y, w, h, name: "stat-" + label.slice(0, 12) });
  s.addText(value, { x: x + 0.26, y: y + 0.13, w: w - 0.5, h: 0.56, fontSize: size,
    bold: true, color, isTextBox: true, margin: 0, valign: "top" });
  s.addText(label, { x: x + 0.26, y: y + 0.72, w: w - 0.5, h: h - 0.8, fontSize: 11.5,
    color: SEC, isTextBox: true, margin: 0, valign: "top" });
}
function numbered(s, items, { x, y, w, gap = 0.9, size = 15 }) {
  items.forEach((t, i) => {
    const yy = y + i * gap;
    s.addShape(pres.ShapeType.ellipse, { x, y: yy, w: 0.44, h: 0.44,
      fill: { color: "F2F4F6" }, line: { color: "2A78D6", width: 1.25 },
      objectName: "num" + i });
    s.addText(String(i + 1), { x, y: yy, w: 0.44, h: 0.44, fontSize: 13.5, bold: true,
      color: BLUE, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    s.addText(t, { x: x + 0.66, y: yy - 0.03, w: w - 0.66, h: 0.72, fontSize: size,
      color: SEC, isTextBox: true, margin: 0, valign: "top" });
  });
}

/* ================================================================ 1. cover */
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "COVER", sectionTitle: "Opening" });
s.addText("DDLS project  ·  data-driven life science", { placeholder: "eyebrow" });
s.addText([
  { text: "Do signal-peptide features predict\n", options: {} },
  { text: "collagen secretion in ", options: {} },
  { text: "B. subtilis", options: { italic: true } },
  { text: "?", options: {} },
], { placeholder: "title" });
s.addText("32 peptides, three Western blots, one collagen construct — and the question of "
  + "whether any of it supports a predictive model.", { placeholder: "body" });
s.addText("Baris Akar  ·  bakar@dtu.dk  ·  4 November 2026\n"
  + "Data owner: Alexiou et al., thesis chapter 2", { placeholder: "meta" });
s.addNotes("Headline: a negative result with one qualified positive lead. Say so up front so "
  + "the audience is not waiting for a reveal.");

/* ================================================================ 2. question */
pres.addSection({ title: "Question and data" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Question and data" });
s.addText("The question", { placeholder: "eyebrow" });
s.addText("Three questions from the data owner", { placeholder: "title" });
numbered(s, [
  "Do sequence, nucleotide or physicochemical features relate to secretion?",
  "If so, can they identify or design high-secretion candidates?",
  "Is it worth training a model?",
], { x: M, y: 1.95, w: 7.6, gap: 0.92, size: 16 });
card(s, { x: 8.7, y: 1.95, w: 3.9, h: 2.9, accent: TEAL, name: "owner-quote" });
s.addText("What the owner asked for", { x: 9.32, y: 2.18, w: 3.2, h: 0.32, fontSize: 13,
  bold: true, color: INK, isTextBox: true, margin: 0 });
s.addText("A well-supported negative result would be informative — and do not analyse only "
  + "the best performers. That was the exact flaw they had seen in the published literature.",
  { x: 9.32, y: 2.62, w: 3.0, h: 2.0, fontSize: 12.5, color: SEC, isTextBox: true,
    margin: 0, valign: "top" });
s.addText("Both cautions are built into every analysis that follows.", { placeholder: "note" });

/* ================================================================ 3. data */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Question and data" });
s.addText("The data", { placeholder: "eyebrow" });
s.addText("Effective n is 8, 13 and 11 — not 32", { placeholder: "title" });
s.addImage({ path: FIG("replicates.png"), x: M, y: 1.6, w: 11.9, h: 3.56 });
[["8 / 13 / 11", "peptides per blot", INK],
 ["3", "separately normalised blots", INK],
 ["96 → 32", "replicate rows collapsed", INK]].forEach((t, i) =>
  stat(s, { x: M + i * 4.1, y: 5.3, w: 3.7, value: t[0], label: t[1], color: t[2] }));
s.addText("Each blot was divided by the mean of a different peptide subset, so the three "
  + "panels share no numeric scale.", { placeholder: "note" });
s.addNotes("Point at the three separate y-axes. This is the owner's own warning, implemented.");

/* ================================================================ 4. method */
pres.addSection({ title: "Method" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
s.addText("Method", { placeholder: "eyebrow" });
s.addText("Four rules — three of them the owner's own cautions", { placeholder: "title" });
const rules = [
  ["Never pool the blots", "Combine the three per-blot effect estimates by meta-analysis — "
    + "never the blot-normalised values themselves."],
  ["One value per peptide", "96 replicate rows collapsed to 32 observations before any test. "
    + "Otherwise the sample size triples on paper."],
  ["All 32 candidates", "Never only the top performers — the selection bias the owner "
    + "specifically warned about."],
  ["Split at peptide level", "Scaling fitted inside training folds only, so no peptide "
    + "informs its own prediction."],
];
rules.forEach((r, i) => {
  const x = M + (i % 2) * 6.1, y = 1.92 + Math.floor(i / 2) * 2.16;
  card(s, { x, y, w: 5.8, h: 1.92, accent: BLUE, name: "rule" + i });
  s.addText(r[0], { x: x + 0.62, y: y + 0.2, w: 5.0, h: 0.34, fontSize: 15.5, bold: true,
    color: INK, isTextBox: true, margin: 0 });
  s.addText(r[1], { x: x + 0.62, y: y + 0.66, w: 4.96, h: 1.1, fontSize: 13, color: SEC,
    isTextBox: true, margin: 0, valign: "top" });
});
s.addText("34 descriptors were computed before any outcome was consulted, so feature choice "
  + "could not be steered by results.", { placeholder: "note" });

/* ================================================================ 5. forest */
pres.addSection({ title: "Results" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
s.addText("Result 1", { placeholder: "eyebrow" });
s.addText("No feature survives the screen", { placeholder: "title" });
s.addImage({ path: FIG("forest.png"), x: 1.05, y: 1.62, w: 11.2, h: 4.78 });
s.addText("Top 10 of 34 descriptors, each tested within each blot separately. Every confidence "
  + "interval crosses zero; the grey band is what chance alone produces.",
  { placeholder: "note" });

/* ================================================================ 6. trap */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
s.addText("The trap", { placeholder: "eyebrow" });
s.addText("0.37 looks fine — until you calibrate it", { placeholder: "title" });
s.addImage({ path: FIG("null.png"), x: M, y: 1.78, w: 7.5, h: 4.38 });
[["0.369", "best real feature, of 34 screened", ORANGE],
 ["0.441", "median best-of-panel on shuffled outcomes", BLUE],
 ["p = 0.81", "family-wise, 5,000 permutations", INK]].forEach((t, i) =>
  stat(s, { x: 8.55, y: 1.86 + i * 1.52, w: 4.05, h: 1.36, value: t[0], label: t[1], color: t[2] }));
s.addText("The outcome was permuted within each blot and the whole 34-feature screen re-run "
  + "each time. The best real feature is weaker than chance.", { placeholder: "note" });
s.addNotes("This is the decisive slide for the negative result. If they push back anywhere, "
  + "it is here — the reliability ceiling on the next slide is the answer.");

/* ================================================================ 7. ceiling */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
s.addText("Result 2", { placeholder: "eyebrow" });
s.addText("The null is informative, not underpowered", { placeholder: "title" });
s.addImage({ path: FIG("ceiling.png"), x: M, y: 1.78, w: 7.5, h: 4.38 });
card(s, { x: 8.55, y: 1.92, w: 4.05, h: 4.1, name: "reliability" });
s.addText("Measurement reliability", { x: 8.9, y: 2.14, w: 3.4, h: 0.34, fontSize: 14,
  bold: true, color: INK, isTextBox: true, margin: 0 });
s.addTable([
  [{ text: "Blot", options: { bold: true, color: MUT, fontSize: 11 } },
   { text: "Inter-rep ρ", options: { bold: true, color: MUT, fontSize: 11, align: "right" } },
   { text: "Max ρ", options: { bold: true, color: MUT, fontSize: 11, align: "right" } }],
  ["Blot 1", { text: "0.476", options: { align: "right" } }, { text: "0.855", options: { align: "right" } }],
  ["Blot 2", { text: "0.581", options: { align: "right" } }, { text: "0.898", options: { align: "right" } }],
  ["Blot 3", { text: "0.418", options: { align: "right" } }, { text: "0.827", options: { align: "right" } }],
], { x: 8.9, y: 2.62, w: 3.4, colW: [1.1, 1.2, 1.1], fontSize: 12, color: SEC,
     border: { type: "solid", color: "E4E6E9", pt: 0.5 }, rowH: 0.3 });
s.addText("A feature perfectly predicting true secretion could still only correlate at about "
  + "0.86 against these measurements.", { x: 8.9, y: 4.28, w: 3.4, h: 1.5, fontSize: 12.5,
    color: SEC, isTextBox: true, margin: 0, valign: "top" });
s.addText("There was room to detect a moderate effect. None appeared — so this is a genuine "
  + "negative, not a noisy assay.", { placeholder: "note" });

/* ================================================================ 8. models */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Results" });
s.addText("Result 3", { placeholder: "eyebrow" });
s.addText("In-sample fit is not performance", { placeholder: "title" });
s.addImage({ path: FIG("models.png"), x: 0.82, y: 1.62, w: 11.7, h: 4.35 });
s.addText("34 features against 32 observations: the model memorises the set and learns nothing "
  + "transferable. Every out-of-fold score is negative under both validation schemes, "
  + "including leave-one-blot-out.", { placeholder: "note" });
s.addNotes("The single most persuasive exhibit. Random forest: 0.96 in-sample, −0.19 "
  + "out-of-fold. Same model, same data, two ways of scoring it.");

/* ================================================================ 9. motif */
pres.addSection({ title: "Why it could not work" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Why it could not work" });
s.addText("Why it could not work", { placeholder: "eyebrow" });
s.addText("The library suppresses its own variation", { placeholder: "title" });
s.addImage({ path: FIG("motif.png"), x: M, y: 1.68, w: 7.3, h: 4.68 });
card(s, { x: 8.42, y: 1.9, w: 4.18, h: 2.1, accent: ORANGE, name: "engineered" });
s.addText("Engineered, not inherited", { x: 9.04, y: 2.12, w: 3.26, h: 0.32, fontSize: 14,
  bold: true, color: INK, isTextBox: true, margin: 0 });
s.addText("Native C-termini span 13 motifs. All 32 supplied peptides end A-S-A. Only 8 of 32 "
  + "match their native sequence exactly.", { x: 9.04, y: 2.54, w: 3.22, h: 1.3,
    fontSize: 12.5, color: SEC, isTextBox: true, margin: 0, valign: "top" });
card(s, { x: 8.42, y: 4.2, w: 4.18, h: 2.1, accent: BLUE, name: "constant" });
s.addText("So the motif explains nothing", { x: 9.04, y: 4.42, w: 3.26, h: 0.32, fontSize: 14,
  bold: true, color: INK, isTextBox: true, margin: 0 });
s.addText("The A-x-A motif Fu et al. link to good performers is a constant here, not a "
  + "variable — it could never explain a difference.", { x: 9.04, y: 4.84, w: 3.22, h: 1.3,
    fontSize: 12.5, color: SEC, isTextBox: true, margin: 0, valign: "top" });
s.addText("SP1/AmyE, the classic B. subtilis secretion tag, ranks 7th of 8 — and is among the "
  + "most heavily modified peptides in the set.", { placeholder: "note" });

/* ================================================================ 10. reasons */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Why it could not work" });
s.addText("Why it could not work", { placeholder: "eyebrow" });
s.addText("Four reasons, in order", { placeholder: "title" });
numbered(s, [
  "No signal to learn.  Best feature 0.369; shuffled data gives 0.441. Nothing for a model to combine.",
  "Effective n is 8 / 13 / 11 against 34 features — memorisation, not learning.",
  "Not a noise problem.  The reliability ceiling is 0.86, so there was room to see an effect.",
  "Design holds key features fixed.  Constant cleavage region, constant mature-protein start, restricted hydrophobicity range.",
], { x: M, y: 2.0, w: 11.4, gap: 1.06, size: 15.5 });
s.addText("A negative result about this dataset's shape — not about the biology, and not a "
  + "criticism of the experiment.", { placeholder: "note" });

/* ================================================================ 11. lead */
pres.addSection({ title: "The lead and what next" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The lead and what next" });
s.addText("The one honest positive", { placeholder: "eyebrow" });
s.addText("mRNA accessibility at the initiation region", { placeholder: "title" });
s.addImage({ path: FIG("rbs.png"), x: M, y: 1.6, w: 11.9, h: 3.68 });
card(s, { x: M, y: 5.44, w: 5.8, h: 1.5, accent: TEAL, name: "found" });
s.addText("What was found", { x: M + 0.62, y: 5.62, w: 4.9, h: 0.3, fontSize: 13.5,
  bold: true, color: INK, isTextBox: true, margin: 0 });
s.addText("Positive in all three blots, in the direction Fu et al. predicted. Combined "
  + "ρ = +0.515, one-sided permutation p = 0.0042.", { x: M + 0.62, y: 5.96, w: 4.9, h: 0.9,
    fontSize: 12, color: SEC, isTextBox: true, margin: 0, valign: "top" });
card(s, { x: 6.8, y: 5.44, w: 5.8, h: 1.5, accent: ORANGE, name: "notconf" });
s.addText("What it is not", { x: 7.42, y: 5.62, w: 4.9, h: 0.3, fontSize: 13.5, bold: true,
  color: INK, isTextBox: true, margin: 0 });
s.addText("A coding-only version of this family was already in the 34-feature screen — a "
  + "refinement, not clean out-of-sample confirmation. No mechanism established.",
  { x: 7.42, y: 5.96, w: 4.9, h: 0.9, fontSize: 12, color: SEC, isTextBox: true,
    margin: 0, valign: "top" });
s.addNotes("State the caveats yourself before they are asked for. If this lead later fails to "
  + "replicate, how it was described now is what will matter.");

/* ================================================================ 12. can/cannot */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The lead and what next" });
s.addText("Recommendation", { placeholder: "eyebrow" });
s.addText("What the owner can and cannot act on", { placeholder: "title" });
card(s, { x: M, y: 1.9, w: 5.8, h: 3.3, fill: "EFF8F3", name: "can" });
s.addText("Can", { x: M + 0.42, y: 2.12, w: 4.8, h: 0.4, fontSize: 19, bold: true,
  color: "0E7A52", isTextBox: true, margin: 0 });
s.addText([
  { text: "Prioritise SP5 (CV 0.14) and SP26 (CV 0.21) — high and reproducible within their own blots", options: { bullet: true, breakLine: true } },
  { text: "Treat SP4 with caution — 1st by mean, 5th by median, plus the unresolved secondary band", options: { bullet: true, breakLine: true } },
  { text: "Test the mRNA-accessibility hypothesis", options: { bullet: true } },
], { x: M + 0.42, y: 2.64, w: 4.92, h: 2.4, fontSize: 13.5, color: SEC, isTextBox: true,
     margin: 0, valign: "top", paraSpaceAfter: 9 });
card(s, { x: 6.8, y: 1.9, w: 5.8, h: 3.3, fill: "FDF1EC", name: "cannot" });
s.addText("Cannot", { x: 7.22, y: 2.12, w: 4.8, h: 0.4, fontSize: 19, bold: true,
  color: "B33D16", isTextBox: true, margin: 0 });
s.addText([
  { text: "Build a cross-blot ranking", options: { bullet: true, breakLine: true } },
  { text: "Train a predictive model or propose synthetic designs", options: { bullet: true, breakLine: true } },
  { text: "Claim a mechanism", options: { bullet: true, breakLine: true } },
  { text: "Assume transfer to another protein target — five peptides shared with Fu et al. give ρ = −0.20", options: { bullet: true } },
], { x: 7.22, y: 2.64, w: 4.92, h: 2.4, fontSize: 13.5, color: SEC, isTextBox: true,
     margin: 0, valign: "top", paraSpaceAfter: 9 });
s.addText("This is a negative result about the dataset's shape — not about the biology, and "
  + "not a criticism of the experiment. The screen produced reproducible candidates, data that "
  + "could be tested rigorously, and one testable lead.",
  { x: M, y: 5.46, w: 11.9, h: 0.8, fontSize: 13.5, color: SEC, isTextBox: true,
    margin: 0, valign: "top", italic: true });

/* ================================================================ 13. next */
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The lead and what next" });
s.addText("Next steps", { placeholder: "eyebrow" });
s.addText("What would make the question answerable", { placeholder: "title" });
numbered(s, [
  "A shared reference lane on every gel.  The single largest fix — it turns three incomparable blots into one dataset.",
  "More peptides on that common scale.  Grasso et al. needed about 4,400 informative peptides.",
  "Raw densitometry — to audit the normalisation, resolve the SP9 zero and assess SP4's secondary band.",
  "Transcription start site and 5′UTR — to test the one lead against its published definition.",
  "Confirm two anomalies: SP31's V versus M, and whether the uniform A-S-A was intentional.",
], { x: M, y: 1.92, w: 11.4, gap: 0.92, size: 14.5 });
s.addText("Nothing analytical substitutes for the first item.", { placeholder: "note" });

/* ================================================================ 14. close */
pres.addSection({ title: "Disclosure" });
s = pres.addSlide({ masterName: "CLOSE", sectionTitle: "Disclosure" });
s.addText("AI-use disclosure", { placeholder: "eyebrow" });
s.addText("Who did what", { placeholder: "title" });
const who = [
  ["Agent A — data owner", "Experimental data, project goal, assay account, and the domain "
    + "constraints the whole analysis runs under."],
  ["Agent B — Claude", "Essentially all computational work: QC, features, statistics, machine "
    + "learning, literature, dashboard, drafting. Generated and altered no measurement; "
    + "flagged anomalies rather than patching them."],
  ["Person — me", "Research question, interviews, constraints, challenging AI interpretations, "
    + "and verification — re-running every script and tracing each number to its source."],
];
who.forEach((r, i) => {
  const x = M + i * 4.1;
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.2, w: 3.7, h: 2.35, rectRadius: 0.07,
    fill: { color: "234A72" }, line: { color: "2F5C8A", width: 1 },
    objectName: "who" + i });
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.3, y: 2.46, w: 0.17, h: 0.17,
    fill: { color: "7FD9B6" }, line: { color: "7FD9B6", width: 0 },
    objectName: "whodot" + i });
  s.addText(r[0], { x: x + 0.62, y: 2.4, w: 2.9, h: 0.5, fontSize: 14, bold: true,
    color: "FFFFFF", isTextBox: true, margin: 0, valign: "top" });
  s.addText(r[1], { x: x + 0.3, y: 2.95, w: 3.1, h: 1.5, fontSize: 12, color: "C9D9E6",
    isTextBox: true, margin: 0, valign: "top" });
});
s.addText("Verification caught a real defect: a stale background process had overwritten the "
  + "modelling outputs with a different random-forest configuration than the committed script "
  + "specified. Re-run, and recorded rather than quietly fixed. A Pi agent independently built "
  + "its own feature set and models, and reached the same negative conclusion.",
  { x: M, y: 4.95, w: 11.9, h: 1.2, fontSize: 12.5, color: "9FB4C7", isTextBox: true,
    margin: 0, valign: "top" });

/* ---------------------------------------------------------------- write */
pres.writeFile({ fileName: OUT }).then(async () => {
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT, (fs.statSync(OUT).size / 1024).toFixed(0) + " KB");
});
