#!/usr/bin/env python3
"""Build slides.html — a self-contained light-theme deck.

No slide framework and no CDN: a CSS-grid layout per slide guarantees the header, body and
footer zones never overlap, and every chart is native inline SVG drawn from data.js.
Navigation is arrow keys / space / scroll-snap. Prints to landscape PDF, one slide per page.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_JS = ROOT / 'ddls_claude' / 'app' / 'data.js'
OUT = ROOT / 'ddls_claude' / 'handin' / 'package' / 'slides.html'

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signal peptides &amp; collagen secretion</title>
<style>
:root{
  --paper:#fcfcfb; --raise:#f4f4f0; --rule:#e4e3dc;
  --ink:#0b0b0b; --ink2:#52514e; --muted:#8a8882;
  --grid:#e8e7e0; --axis:#c3c2b7;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100;
  --good:#0ca30c; --bad:#d03b3b;
  --pad-x:clamp(28px,6.5vw,110px);
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--paper); color:var(--ink);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:clamp(14px,1.18vw,19px); line-height:1.55;
  height:100vh; overflow:hidden; -webkit-font-smoothing:antialiased;
}
.slide{
  display:none; height:100vh; grid-template-rows:auto minmax(0,1fr) auto;
  gap:clamp(14px,2.2vh,30px);
  padding:clamp(34px,7vh,78px) var(--pad-x) clamp(26px,4.5vh,54px);
  position:relative; animation:fade .22s ease both;
}
.slide.on{display:grid}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.eyebrow{
  font-size:clamp(10px,.78vw,13px); letter-spacing:.17em; text-transform:uppercase;
  font-weight:650; color:var(--s3); margin-bottom:.55em;
}
h1{font-size:clamp(32px,4.4vw,60px); line-height:1.08; letter-spacing:-.033em; font-weight:660}
h2{font-size:clamp(22px,2.75vw,40px); line-height:1.14; letter-spacing:-.026em; font-weight:650}
h3{font-size:clamp(14px,1.25vw,20px); font-weight:650; letter-spacing:-.012em}
.lede{color:var(--ink2); font-size:1.02em; max-width:58ch; margin-top:.5em}
.body{display:flex; flex-direction:column; justify-content:center; min-height:0}
footer{color:var(--muted); font-size:.82em; line-height:1.5; max-width:92ch;
  display:flex; justify-content:space-between; align-items:flex-end; gap:24px}
em{font-style:italic} strong{font-weight:640; color:var(--ink)}
code{font-family:ui-monospace,Menlo,monospace; background:var(--raise); padding:1px 6px;
  border-radius:4px; font-size:.92em}
.two{display:grid; grid-template-columns:1fr 1fr; gap:clamp(18px,2.4vw,40px); align-items:center}
.wide{display:grid; grid-template-columns:1.55fr 1fr; gap:clamp(18px,2.4vw,40px); align-items:center}
.card{background:var(--raise); border:1px solid var(--rule); border-radius:14px;
  padding:clamp(14px,1.5vw,24px) clamp(16px,1.7vw,28px)}
.card.ac{border-left:3px solid var(--c)}
.tile{background:var(--raise); border:1px solid var(--rule); border-radius:13px;
  padding:clamp(12px,1.3vw,20px)}
.tile .v{font-size:clamp(22px,2.4vw,38px); font-weight:680; letter-spacing:-.03em; line-height:1.05}
.tile .l{font-size:.8em; color:var(--ink2); margin-top:.45em; line-height:1.42}
.blue{color:var(--s1)} .orange{color:var(--s2)} .teal{color:var(--s3)}
.ok{color:var(--good)} .bad{color:var(--bad)}
ol,ul{padding-left:1.35em; font-size:1.02em} li{margin-bottom:.62em}
li::marker{color:var(--muted); font-weight:600}
ol.big{list-style:none; padding:0; display:grid; gap:clamp(10px,1.3vh,18px); counter-reset:n}
ol.big li{counter-increment:n; display:grid; grid-template-columns:auto 1fr; gap:16px;
  align-items:start; margin:0}
ol.big li::before{content:counter(n); font-size:.86em; font-weight:700; color:var(--s1);
  background:var(--raise); border:1px solid var(--rule); border-radius:50%;
  width:2.05em; height:2.05em; display:grid; place-items:center; line-height:1}
table{border-collapse:collapse; width:100%; font-size:.9em}
th,td{padding:.52em .7em; border-bottom:1px solid var(--rule); text-align:left}
th{font-size:.84em; color:var(--muted); font-weight:650}
td.n,th.n{text-align:right; font-variant-numeric:tabular-nums}
.legend{display:flex; flex-wrap:wrap; gap:clamp(12px,1.5vw,26px); align-items:center;
  font-size:.84em; color:var(--ink2); margin-bottom:clamp(8px,1.2vh,16px)}
.legend i{width:11px; height:11px; border-radius:3px; display:inline-block; margin-right:7px;
  vertical-align:-1px}
.legend i.dash{width:16px;height:0;border-top:2px dashed var(--axis);border-radius:0}
svg{display:block; width:100%; height:auto; overflow:visible}
.ax{font-size:13px; fill:var(--muted)} .axl{font-size:14px; fill:var(--ink2)}
.ft{font-size:15px; fill:var(--ink); font-weight:650}
.vl{font-size:13px; font-weight:600}
#bar{position:fixed; top:0; left:0; height:3px; background:var(--s1); width:0; z-index:9;
  transition:width .18s ease}
#cnt{position:fixed; right:clamp(14px,2vw,26px); bottom:clamp(12px,2vh,22px); z-index:9;
  font-size:.78em; color:var(--muted); font-variant-numeric:tabular-nums;
  background:rgba(252,252,251,.92); padding:4px 11px; border-radius:20px;
  border:1px solid var(--rule)}
@media (max-width:820px){
  .two,.wide{grid-template-columns:1fr}
  .slide{height:auto; min-height:100vh; padding-top:48px; padding-bottom:48px}
}
@media print{
  @page{size:landscape; margin:12mm}
  body{height:auto;overflow:visible}
  .slide{display:grid!important; height:auto; page-break-after:always; border:0;
    padding:0 0 18mm; animation:none}
  #bar,#cnt{display:none}
}
</style>
</head>
<body>
<div id="bar"></div><div id="cnt"></div>

<section class="slide">
  <header>
    <div class="eyebrow">DDLS project &middot; data-driven life science</div>
    <h1>Do signal-peptide features predict<br>collagen secretion in <em>B.&nbsp;subtilis</em>?</h1>
  </header>
  <div class="body">
    <p class="lede" style="font-size:1.18em;max-width:46ch">32 peptides, three Western blots,
    one collagen construct &mdash; and the question of whether any of it supports a predictive
    model.</p>
  </div>
  <footer><div>Baris Akar &middot; bakar@dtu.dk &middot; 4 November 2026<br>
    Data owner: Alexiou et al., thesis chapter 2</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">The question</div>
    <h2>Three questions from the data owner</h2></header>
  <div class="body">
    <ol class="big" style="max-width:62ch">
      <li><div>Do sequence, nucleotide or physicochemical features relate to secretion?</div></li>
      <li><div>If so, can they identify or design high-secretion candidates?</div></li>
      <li><div><strong>Is it worth training a model?</strong></div></li>
    </ol>
    <div class="card ac" style="--c:var(--s3);margin-top:clamp(16px,2.4vh,30px);max-width:72ch">
      The owner stated that a well-supported negative result would be informative, and cautioned
      against analysing only the best performers &mdash; the exact flaw they had seen in the
      published literature.
    </div>
  </div>
  <footer><div></div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">The data</div>
    <h2>Effective n is 8, 13 and 11 &mdash; not 32</h2></header>
  <div class="body">
    <div class="legend">
      <span><i style="background:var(--s1)"></i>Blot 1</span>
      <span><i style="background:var(--s2)"></i>Blot 2</span>
      <span><i style="background:var(--s3)"></i>Blot 3</span>
      <span><i style="background:var(--ink);height:4px;border-radius:1px"></i>peptide mean</span>
      <span><i class="dash"></i>that gel's own mean</span>
    </div>
    <div id="c-reps"></div>
  </div>
  <footer><div>Each blot was divided by the mean of a <em>different</em> peptide subset, so the
    three panels share no numeric scale and cannot be compared across.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Method</div>
    <h2>Four rules &mdash; three of them the owner's own cautions</h2></header>
  <div class="body">
    <div class="two" style="align-items:stretch">
      <div class="card"><h3 class="blue">Never pool the blots</h3>
        <p style="margin-top:.4em;color:var(--ink2)">Combine the three per-blot <em>effect
        estimates</em> by meta-analysis &mdash; never the blot-normalised values themselves.</p></div>
      <div class="card"><h3 class="blue">One value per peptide</h3>
        <p style="margin-top:.4em;color:var(--ink2)">96 replicate rows collapsed to 32
        observations before any test. Otherwise the sample size triples on paper.</p></div>
      <div class="card"><h3 class="blue">All 32 candidates</h3>
        <p style="margin-top:.4em;color:var(--ink2)">Never only the top performers &mdash; the
        selection bias the owner specifically warned about.</p></div>
      <div class="card"><h3 class="blue">Split at peptide level</h3>
        <p style="margin-top:.4em;color:var(--ink2)">Scaling fitted inside training folds only,
        so no peptide informs its own prediction.</p></div>
    </div>
  </div>
  <footer><div>34 descriptors were computed <em>before</em> any outcome was consulted, so feature
    choice could not be steered by results.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Result 1</div>
    <h2>No feature survives the screen</h2></header>
  <div class="body">
    <div class="legend">
      <span><i style="background:var(--s1)"></i>Blot 1</span>
      <span><i style="background:var(--s2)"></i>Blot 2</span>
      <span><i style="background:var(--s3)"></i>Blot 3</span>
      <span><i style="background:var(--ink);transform:rotate(45deg)"></i>combined, 95% CI</span>
      <span><i style="background:var(--grid)"></i>inside the chance band</span>
    </div>
    <div id="c-forest"></div>
  </div>
  <footer><div>Top 10 of 34 descriptors, each tested within each blot separately. Every
    confidence interval crosses zero.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">The trap</div>
    <h2>0.37 looks fine &mdash; until you calibrate it</h2></header>
  <div class="body">
    <div class="wide">
      <div id="c-null"></div>
      <div style="display:grid;gap:clamp(10px,1.3vw,16px)">
        <div class="tile"><div class="v orange">0.369</div>
          <div class="l">best real feature, of 34 screened</div></div>
        <div class="tile"><div class="v blue">0.441</div>
          <div class="l">median best-of-panel on <em>shuffled</em> outcomes</div></div>
        <div class="tile"><div class="v">p = 0.81</div>
          <div class="l">family-wise, 5,000 permutations</div></div>
      </div>
    </div>
  </div>
  <footer><div>The outcome was permuted within each blot and the whole 34-feature screen re-run
    each time. <strong>The best real feature is weaker than chance.</strong></div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Result 2</div>
    <h2>The null is informative, not underpowered</h2></header>
  <div class="body">
    <div class="wide">
      <div id="c-ceiling"></div>
      <div>
        <table>
          <tr><th>Blot</th><th class="n">Inter-replicate &rho;</th>
              <th class="n">Max detectable &rho;</th></tr>
          <tr><td>Blot 1</td><td class="n">0.476</td><td class="n">0.855</td></tr>
          <tr><td>Blot 2</td><td class="n">0.581</td><td class="n">0.898</td></tr>
          <tr><td>Blot 3</td><td class="n">0.418</td><td class="n">0.827</td></tr>
        </table>
        <p style="margin-top:1em;color:var(--ink2);font-size:.95em">Spearman&ndash;Brown
        reliability of a 3-replicate mean. A feature perfectly predicting true secretion could
        still only correlate at about <strong>0.86</strong> against these measurements.</p>
      </div>
    </div>
  </div>
  <footer><div>There was room to detect a moderate effect. None appeared &mdash; so this is a
    genuine negative, not a noisy assay.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Result 3</div>
    <h2>In-sample fit is not performance</h2></header>
  <div class="body">
    <div class="legend">
      <span><i style="background:var(--s4)"></i>In-sample &mdash; fitted and scored on the same
        peptides</span>
      <span><i style="background:var(--s1)"></i>Out-of-fold &mdash; predicting held-out
        peptides</span>
    </div>
    <div id="c-models"></div>
  </div>
  <footer><div>34 features against 32 observations: the model memorises the set and learns
    nothing transferable. <strong>Every out-of-fold score is negative under both validation
    schemes</strong>, including leave-one-blot-out.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Why it could not work</div>
    <h2>The library suppresses its own variation</h2></header>
  <div class="body">
    <div class="wide">
      <div id="c-motif"></div>
      <div style="display:grid;gap:clamp(10px,1.3vw,16px)">
        <div class="card"><h3>Engineered, not inherited</h3>
          <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">Native C-termini span
          <strong>13 motifs</strong>. All 32 supplied peptides end
          <strong class="orange">A-S-A</strong>. Only <strong>8 of 32</strong> match their native
          sequence exactly.</p></div>
        <div class="card"><h3>So the motif explains nothing</h3>
          <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">The A-x-A motif Fu et al.
          link to good performers is a <em>constant</em> here, not a variable.</p></div>
      </div>
    </div>
  </div>
  <footer><div>Hydrophobicity is range-restricted too: GRAVY median 1.01, 26 of 32 between 0.6
    and 1.4 &mdash; on the optimum published by Grasso et al. <strong>SP1/AmyE</strong>, the
    classic secretion tag, ranks 7th of 8 and is among the most modified peptides.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Why it could not work</div>
    <h2>Four reasons, in order</h2></header>
  <div class="body">
    <ol class="big" style="max-width:76ch">
      <li><div><strong>No signal to learn.</strong> Best feature 0.369; shuffled data gives 0.441.
        Nothing for a model to combine.</div></li>
      <li><div><strong>Effective n is 8 / 13 / 11</strong> against 34 features &mdash;
        memorisation, not learning.</div></li>
      <li><div><strong>Not a noise problem.</strong> The reliability ceiling is 0.86, so there was
        room to see an effect.</div></li>
      <li><div><strong>Design holds key features fixed.</strong> Constant cleavage region,
        constant mature-protein start, restricted hydrophobicity range.</div></li>
    </ol>
  </div>
  <footer><div>A negative result about <em>this dataset's shape</em> &mdash; not about the
    biology, and not a criticism of the experiment.</div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">The one honest positive</div>
    <h2>mRNA accessibility at the initiation region</h2></header>
  <div class="body">
    <div id="c-rbs"></div>
    <div class="two" style="margin-top:clamp(12px,1.8vh,22px)">
      <div class="card ac" style="--c:var(--s3)"><h3 class="teal">What was found</h3>
        <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">Positive in
        <strong>all three blots</strong>, in the direction Fu et al. predicted. Combined
        &rho; = <strong>+0.515</strong>, one-sided permutation p = <strong>0.0042</strong>.
        Computable only because the thesis supplied the shared RBS.</p></div>
      <div class="card ac" style="--c:var(--s2)"><h3 class="orange">What it is not</h3>
        <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">A coding-only version of this
        family was already in the 34-feature screen &mdash; a refinement, <strong>not clean
        out-of-sample confirmation</strong>. Transcription start site unknown. No mechanism
        established.</p></div>
    </div>
  </div>
  <footer><div></div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Recommendation</div>
    <h2>What the owner can and cannot act on</h2></header>
  <div class="body">
    <div class="two" style="align-items:stretch">
      <div class="card ac" style="--c:var(--good)">
        <h3 class="ok">Can</h3>
        <ul style="margin-top:.6em;font-size:.95em;color:var(--ink2)">
          <li>Prioritise <strong>SP5</strong> (CV 0.14) and <strong>SP26</strong> (CV 0.21)
            &mdash; high and reproducible within their own blots</li>
          <li>Treat <strong>SP4</strong> with caution &mdash; 1st by mean, 5th by median, plus the
            unresolved secondary band</li>
          <li>Test the mRNA-accessibility hypothesis</li>
        </ul>
      </div>
      <div class="card ac" style="--c:var(--bad)">
        <h3 class="bad">Cannot</h3>
        <ul style="margin-top:.6em;font-size:.95em;color:var(--ink2)">
          <li>Build a cross-blot ranking</li>
          <li>Train a predictive model or propose synthetic designs</li>
          <li>Claim a mechanism</li>
          <li>Assume transfer to another protein target &mdash; five peptides shared with
            Fu et al. give &rho; = &minus;0.20</li>
        </ul>
      </div>
    </div>
  </div>
  <footer><div></div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">Next steps</div>
    <h2>What would make the question answerable</h2></header>
  <div class="body">
    <ol class="big" style="max-width:78ch">
      <li><div><strong>A shared reference lane on every gel.</strong> The single largest fix
        &mdash; it turns three incomparable blots into one dataset. Nothing analytical
        substitutes for it.</div></li>
      <li><div><strong>More peptides on that common scale.</strong> Grasso et al. needed about
        4,400 informative peptides to fit a comparable model.</div></li>
      <li><div><strong>Raw densitometry</strong> &mdash; to audit the normalisation, resolve the
        SP9 zero and assess SP4's secondary band.</div></li>
      <li><div><strong>Transcription start site and 5&prime;UTR</strong> &mdash; to test the one
        lead against its published definition.</div></li>
      <li><div><strong>Confirm two anomalies:</strong> SP31's <code>V</code> versus <code>M</code>,
        and whether the uniform A-S-A was intentional.</div></li>
    </ol>
  </div>
  <footer><div></div></footer>
</section>

<section class="slide">
  <header><div class="eyebrow">AI-use disclosure</div>
    <h2>Who did what</h2></header>
  <div class="body">
    <div class="two" style="align-items:stretch">
      <div class="card"><h3>Agent A &mdash; data owner</h3>
        <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">Experimental data, project
        goal, assay account, and the domain constraints the whole analysis runs under.</p></div>
      <div class="card"><h3>Agent B &mdash; Claude</h3>
        <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">Essentially all computational
        work: QC, features, statistics, machine learning, literature, dashboard, drafting.
        Generated and altered <em>no</em> measurement; flagged anomalies rather than patching
        them.</p></div>
    </div>
    <div class="card ac" style="--c:var(--s1);margin-top:clamp(12px,1.8vh,22px)">
      <h3>Person &mdash; me</h3>
      <p style="margin-top:.4em;color:var(--ink2);font-size:.95em">Research question, interviews,
      constraints, challenging AI interpretations, and verification &mdash; re-running every
      script and tracing each number to its source file. That caught a real defect: a stale
      background process had overwritten the modelling outputs with a different random-forest
      configuration than the committed script specified. Re-run, and recorded rather than quietly
      fixed.</p>
    </div>
  </div>
  <footer><div>A Pi agent independently built its own feature set and ridge/LOO models and
    reached the same negative conclusion.</div></footer>
</section>

<script>
__DATA__
</script>
<script>
const NS="http://www.w3.org/2000/svg", BLOTS=["Blot 1","Blot 2","Blot 3"];
const CB={"Blot 1":"var(--s1)","Blot 2":"var(--s2)","Blot 3":"var(--s3)"};
const LBL={h_core9_mean_kd:"Hydrophobic core · mean hydropathy",
 mrna_dg_first30nt:"mRNA ΔG · first 30 nt",
 c_prox6_frac_polar_STNQ:"C-terminal 6 · polar fraction",
 h_core9_frac_hydrophobic:"Hydrophobic core · hydrophobic fraction",
 frac_hydrophobic_AVILMFWY:"Whole peptide · hydrophobic fraction", aromaticity:"Aromaticity",
 aa_length:"Peptide length", isoelectric_point:"Isoelectric point",
 frac_leucine:"Leucine fraction", n_prox_net_charge_ph7:"N-region · net charge (pH 7)",
 n_prox_frac_basic_KR:"N-region · basic fraction", net_charge_ph7:"Net charge (pH 7)",
 frac_glycine:"Glycine fraction", mrna_dg_first60nt:"mRNA ΔG · first 60 nt",
 n_prox_kr_count:"N-region · K+R count", kr_minus_de:"(K+R) − (D+E)",
 n_prox_length:"N-region length", h_core9_start_1based:"Hydrophobic core · start position"};
const nm=k=>LBL[k]||k;
function el(t,a,p){const n=document.createElementNS(NS,t);for(const k in a)n.setAttribute(k,a[k]);
  if(p)p.appendChild(n);return n;}
function mk(w,h){const s=document.createElementNS(NS,"svg");
  s.setAttribute("viewBox","0 0 "+w+" "+h);s.setAttribute("role","img");return s;}
const sg=v=>(v>=0?"+":"−")+Math.abs(v).toFixed(2);

function reps(){
  const W=1240,H=430,PT=34,PB=76,gx=30,FW=(W-gx*2)/3,PL=44;
  const s=mk(W,H);
  BLOTS.forEach((b,bi)=>{
    const rows=DATA.summary.filter(d=>d.block===b).sort((a,c)=>a.mean-c.mean);
    const rep=DATA.replicates.filter(d=>d.block===b);
    const x0=bi*(FW+gx), ih=H-PT-PB, iw=FW-PL;
    const mx=Math.max.apply(null,rep.map(d=>d.value))*1.1;
    const X=i=>x0+PL+iw*((i+0.5)/rows.length), Y=v=>PT+ih-(v/mx)*ih;
    const g=el("g",{},s);
    el("text",{x:x0+PL,y:16,class:"ft"},g).textContent=b;
    el("text",{x:x0+PL+iw,y:16,class:"ax","text-anchor":"end"},g)
      .textContent=rows.length+" peptides";
    for(let t=0;t<=Math.ceil(mx);t++){
      el("line",{x1:x0+PL,x2:x0+PL+iw,y1:Y(t),y2:Y(t),stroke:"var(--grid)","stroke-width":1},g);
      el("text",{x:x0+PL-9,y:Y(t)+5,class:"ax","text-anchor":"end"},g).textContent=t;}
    el("line",{x1:x0+PL,x2:x0+PL+iw,y1:Y(1),y2:Y(1),stroke:"var(--axis)","stroke-width":1.6,
      "stroke-dasharray":"5 4"},g);
    rows.forEach((r,i)=>{
      const x=X(i);
      rep.filter(d=>d.peptide_id===r.peptide_id).forEach((d,k)=>{
        el("circle",{cx:x+(k-1)*4,cy:Y(d.value),r:3.6,fill:CB[b],opacity:.82,
          stroke:"var(--paper)","stroke-width":1.3},g);});
      el("rect",{x:x-8.5,y:Y(r.mean)-1.6,width:17,height:3.2,rx:1.6,fill:"var(--ink)"},g);
      el("text",{x:x,y:PT+ih+15,class:"ax","text-anchor":"end",
        transform:"rotate(-55 "+x+" "+(PT+ih+15)+")"},g).textContent=r.peptide_id;});
    el("line",{x1:x0+PL,x2:x0+PL+iw,y1:PT+ih,y2:PT+ih,stroke:"var(--axis)","stroke-width":1.2},g);
    if(bi===0)el("text",{x:4,y:PT+ih/2,class:"axl","text-anchor":"middle",
      transform:"rotate(-90 4 "+(PT+ih/2)+")"},g).textContent="fold-change";});
  return s;
}

function forest(){
  const rows=DATA.associations.slice(0,10), rh=37, PL=330, PR=40, PT=10, W=1240;
  const H=PT+rows.length*rh+52, s=mk(W,H), iw=W-PL-PR;
  const X=v=>PL+iw*((v+1)/2), p95=DATA.permutation.null_p95;
  el("rect",{x:X(-p95),y:PT-2,width:X(p95)-X(-p95),height:rows.length*rh,
    fill:"var(--grid)",opacity:.75,rx:4},s);
  [-1,-.5,0,.5,1].forEach(t=>{
    el("line",{x1:X(t),x2:X(t),y1:PT-2,y2:PT+rows.length*rh,
      stroke:t===0?"var(--axis)":"var(--grid)","stroke-width":t===0?1.6:1},s);
    el("text",{x:X(t),y:PT+rows.length*rh+24,class:"ax","text-anchor":"middle"},s)
      .textContent=t;});
  el("text",{x:PL+iw/2,y:PT+rows.length*rh+46,class:"axl","text-anchor":"middle"},s)
    .textContent="Spearman ρ with secretion — combined across blots";
  rows.forEach((r,i)=>{
    const y=PT+i*rh+rh/2;
    if(i%2===0)el("rect",{x:PL,y:y-rh/2,width:iw,height:rh,fill:"var(--ink)",opacity:.022},s);
    el("text",{x:PL-14,y:y+5,class:"ax","text-anchor":"end"},s).textContent=nm(r.feature);
    if(r.combined_lo95!==null)
      el("line",{x1:X(r.combined_lo95),x2:X(r.combined_hi95),y1:y,y2:y,
        stroke:"var(--axis)","stroke-width":1.6,"stroke-linecap":"round"},s);
    [["rho_blot1","var(--s1)"],["rho_blot2","var(--s2)"],["rho_blot3","var(--s3)"]].forEach(p=>{
      if(r[p[0]]!==null)el("circle",{cx:X(r[p[0]]),cy:y,r:4.4,fill:p[1],opacity:.9,
        stroke:"var(--paper)","stroke-width":1.4},s);});
    el("rect",{x:X(r.combined_rho)-4.6,y:y-4.6,width:9.2,height:9.2,fill:"var(--ink)",
      transform:"rotate(45 "+X(r.combined_rho)+" "+y+")"},s);});
  return s;
}

function nullc(){
  const P=DATA.permutation,W=720,H=430,PL=56,PR=30,PT=56,PB=66,s=mk(W,H);
  const iw=W-PL-PR,ih=H-PT-PB,lo=0,hi=.9,X=v=>PL+iw*((v-lo)/(hi-lo));
  const sd=(P.null_p95-P.null_median)/1.645;let d="";
  for(let v=lo;v<=hi;v+=.003){
    const y=PT+ih-Math.exp(-.5*Math.pow((v-P.null_median)/sd,2))*ih*.86;
    d+=(d?"L":"M")+X(v).toFixed(1)+","+y.toFixed(1);}
  el("path",{d:d+"L"+X(hi)+","+(PT+ih)+"L"+X(lo)+","+(PT+ih)+"Z",fill:"var(--s1)",opacity:.14},s);
  el("path",{d:d,fill:"none",stroke:"var(--s1)","stroke-width":2.4},s);
  [[P.observed,"var(--s2)","observed  0.37",-1,0],
   [P.null_median,"var(--s1)","chance  0.44",1,1]].forEach(a=>{
    el("line",{x1:X(a[0]),x2:X(a[0]),y1:PT-8,y2:PT+ih,stroke:a[1],"stroke-width":2.6},s);
    el("text",{x:X(a[0])+a[3]*10,y:PT-16-a[4]*22,class:"vl",
      "text-anchor":a[3]>0?"start":"end",fill:a[1]},s).textContent=a[2];});
  el("line",{x1:PL,x2:W-PR,y1:PT+ih,y2:PT+ih,stroke:"var(--axis)","stroke-width":1.2},s);
  [0,.2,.4,.6,.8].forEach(t=>el("text",{x:X(t),y:PT+ih+24,class:"ax","text-anchor":"middle"},s)
    .textContent=t.toFixed(1));
  el("text",{x:PL+iw/2,y:H-14,class:"axl","text-anchor":"middle"},s)
    .textContent="largest |ρ| found when the outcome is shuffled";
  return s;
}

function ceiling(){
  const W=720,H=430,PL=56,PR=30,PT=56,PB=66,s=mk(W,H);
  const iw=W-PL-PR,ih=H-PT-PB,X=v=>PL+iw*v;
  const obs=DATA.associations.map(a=>Math.abs(a.combined_rho)).filter(v=>v!==null);
  const bins=new Array(20).fill(0);obs.forEach(v=>bins[Math.min(19,Math.floor(v*20))]++);
  const mx=Math.max.apply(null,bins);
  bins.forEach((n,i)=>{if(!n)return;const h=(n/mx)*ih*.78;
    el("rect",{x:X(i/20)+1.5,y:PT+ih-h,width:iw/20-3,height:h,rx:2.5,fill:"var(--s1)",
      opacity:.72},s);});
  [[DATA.permutation.observed,"var(--s2)","observed  0.37",-1,0],
   [0.86,"var(--s3)","reliability ceiling  0.86",-1,1]].forEach(a=>{
    el("line",{x1:X(a[0]),x2:X(a[0]),y1:PT-8,y2:PT+ih,stroke:a[1],"stroke-width":2.6},s);
    el("text",{x:X(a[0])+a[3]*10,y:PT-16-a[4]*22,class:"vl","text-anchor":"end",fill:a[1]},s)
      .textContent=a[2];});
  el("line",{x1:PL,x2:W-PR,y1:PT+ih,y2:PT+ih,stroke:"var(--axis)","stroke-width":1.2},s);
  [0,.2,.4,.6,.8,1].forEach(t=>el("text",{x:X(t),y:PT+ih+24,class:"ax","text-anchor":"middle"},s)
    .textContent=t.toFixed(1));
  el("text",{x:PL+iw/2,y:H-14,class:"axl","text-anchor":"middle"},s)
    .textContent="|combined ρ| for each of the 34 features";
  return s;
}

function models(){
  const rows=DATA.insample.filter(m=>m.model.indexOf("Baseline")!==0);
  const W=1240,PL=260,PR=96,PT=16,rh=86,H=PT+rows.length*rh+54,s=mk(W,H);
  const iw=W-PL-PR,X=v=>PL+iw*((v+1)/2);
  [-1,-.5,0,.5,1].forEach(t=>{
    el("line",{x1:X(t),x2:X(t),y1:PT-4,y2:PT+rows.length*rh-18,
      stroke:t===0?"var(--axis)":"var(--grid)","stroke-width":t===0?1.6:1},s);
    el("text",{x:X(t),y:PT+rows.length*rh+2,class:"ax","text-anchor":"middle"},s).textContent=t;});
  el("text",{x:PL+iw/2,y:PT+rows.length*rh+26,class:"axl","text-anchor":"middle"},s)
    .textContent="Spearman ρ between predicted and actual ranking";
  rows.forEach((r,i)=>{
    const yb=PT+i*rh, hero=r.model.indexOf("forest")>=0;
    el("text",{x:PL-16,y:yb+26,class:"ax","text-anchor":"end",
      "font-weight":hero?"700":"400",fill:hero?"var(--ink)":"var(--muted)"},s)
      .textContent=r.model;
    [["in_sample_spearman","var(--s4)"],["honest_out_of_fold_spearman","var(--s1)"]]
      .forEach((p,j)=>{
      const v=r[p[0]],y=yb+2+j*26,x1=X(0),x2=X(v);
      el("rect",{x:Math.min(x1,x2),y:y,width:Math.max(3,Math.abs(x2-x1)),height:20,rx:4,
        fill:p[1]},s);
      el("text",{x:x2+(v>=0?9:-9),y:y+15,class:"vl","text-anchor":v>=0?"start":"end",
        fill:"var(--ink2)"},s).textContent=sg(v);});});
  return s;
}

function motif(){
  const rows=DATA.native_motifs.slice().sort((a,b)=>b.n-a.n);
  const W=720,PL=74,PR=120,PT=34,rh=23,H=PT+(rows.length+2.4)*rh+16,s=mk(W,H);
  const iw=W-PL-PR,X=v=>PL+(v/32)*iw;
  el("text",{x:PL,y:16,class:"ax"},s).textContent="native C-terminus (UniProt annotation)";
  rows.forEach((r,i)=>{
    const y=PT+i*rh;
    el("text",{x:PL-10,y:y+13,class:"ax","text-anchor":"end"},s).textContent=r.motif;
    el("rect",{x:PL,y:y+2,width:Math.max(3,X(r.n)-PL),height:14,rx:3,
      fill:r.motif==="ASA"?"var(--s1)":"var(--axis)",opacity:r.motif==="ASA"?.9:.55},s);
    el("text",{x:X(r.n)+8,y:y+13,class:"ax"},s).textContent=r.n;});
  const y=PT+rows.length*rh+14;
  el("line",{x1:PL-50,x2:W-PR,y1:y-5,y2:y-5,stroke:"var(--rule)","stroke-width":1},s);
  el("text",{x:PL-10,y:y+15,class:"vl","text-anchor":"end",fill:"var(--ink)"},s).textContent="ASA";
  el("rect",{x:PL,y:y+4,width:X(32)-PL,height:14,rx:3,fill:"var(--s2)"},s);
  el("text",{x:X(32)+8,y:y+15,class:"vl",fill:"var(--s2)"},s).textContent="32 — supplied";
  return s;
}

function rbs(){
  const W=1240,H=340,PT=30,PB=62,gx=28,FW=(W-gx*2)/3,PL=48,s=mk(W,H);
  BLOTS.forEach((b,bi)=>{
    const pts=DATA.scatter.filter(d=>d.block===b),x0=bi*(FW+gx);
    const xs=pts.map(p=>p.dg_rbs_plus48),ys=pts.map(p=>p.mean);
    const xmin=Math.min.apply(null,xs)-1,xmax=Math.max.apply(null,xs)+1;
    const ymax=Math.max.apply(null,ys)*1.14,ih=H-PT-PB,iw=FW-PL;
    const X=v=>x0+PL+(v-xmin)/(xmax-xmin)*iw,Y=v=>PT+ih-(v/ymax)*ih;
    const g=el("g",{},s);
    el("text",{x:x0+PL,y:14,class:"ft"},g).textContent=b;
    el("text",{x:x0+PL+iw,y:14,class:"vl","text-anchor":"end",fill:"var(--s3)"},g)
      .textContent="ρ = "+sg(DATA.rbs["blot"+(bi+1)]);
    for(let t=0;t<=Math.ceil(ymax);t++){
      el("line",{x1:x0+PL,x2:x0+PL+iw,y1:Y(t),y2:Y(t),stroke:"var(--grid)","stroke-width":1},g);
      el("text",{x:x0+PL-9,y:Y(t)+5,class:"ax","text-anchor":"end"},g).textContent=t;}
    pts.forEach(p=>el("circle",{cx:X(p.dg_rbs_plus48),cy:Y(p.mean),r:4.6,fill:CB[b],opacity:.85,
      stroke:"var(--paper)","stroke-width":1.4},g));
    el("line",{x1:x0+PL,x2:x0+PL+iw,y1:PT+ih,y2:PT+ih,stroke:"var(--axis)","stroke-width":1.2},g);
    const st=Math.ceil((xmax-xmin)/4);
    for(let t=Math.ceil(xmin/st)*st;t<=xmax;t+=st)
      el("text",{x:X(t),y:PT+ih+22,class:"ax","text-anchor":"middle"},g).textContent=t;
    el("text",{x:x0+PL+iw/2,y:H-12,class:"axl","text-anchor":"middle"},g)
      .textContent="ΔG (kcal/mol)  →  less structured";
    if(bi===0)el("text",{x:4,y:PT+ih/2,class:"axl","text-anchor":"middle",
      transform:"rotate(-90 4 "+(PT+ih/2)+")"},g).textContent="fold-change";});
  return s;
}

const C={"c-reps":reps,"c-forest":forest,"c-null":nullc,"c-ceiling":ceiling,
  "c-models":models,"c-motif":motif,"c-rbs":rbs};
for(const id in C){const h=document.getElementById(id); if(h)h.appendChild(C[id]());}

const S=[].slice.call(document.querySelectorAll(".slide"));
const bar=document.getElementById("bar"), cnt=document.getElementById("cnt");
let i=0;
function show(n){
  i=Math.max(0,Math.min(S.length-1,n));
  S.forEach((s,k)=>s.classList.toggle("on",k===i));
  bar.style.width=((i+1)/S.length*100)+"%";
  cnt.textContent=(i+1)+" / "+S.length;
  if(location.hash!=="#"+(i+1))history.replaceState(null,"","#"+(i+1));
}
addEventListener("keydown",e=>{
  if(["ArrowRight","ArrowDown","PageDown"," "].indexOf(e.key)>=0){e.preventDefault();show(i+1);}
  else if(["ArrowLeft","ArrowUp","PageUp","Backspace"].indexOf(e.key)>=0){e.preventDefault();show(i-1);}
  else if(e.key==="Home"){e.preventDefault();show(0);}
  else if(e.key==="End"){e.preventDefault();show(S.length-1);}
});
addEventListener("click",e=>{
  if(e.target.closest("a"))return;
  show(e.clientX < innerWidth*0.3 ? i-1 : i+1);
});
addEventListener("wheel",e=>{
  if(Math.abs(e.deltaY)<18)return;
  const t=Date.now(); if(t-(window._w||0)<420)return; window._w=t;
  show(i+(e.deltaY>0?1:-1));
},{passive:true});
show(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));
</script>
</body>
</html>
"""

html = TEMPLATE.replace('__DATA__', DATA_JS.read_text(encoding='utf-8'))
OUT.write_text(html, encoding='utf-8')
print(f'Wrote {OUT}  ({len(html)/1024:.0f} KB, {html.count("<section")} slides, '
      f'7 native SVG charts, light theme, no framework, no CDN)')
