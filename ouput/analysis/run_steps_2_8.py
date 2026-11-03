#!/usr/bin/env python3
"""Reproducible descriptive analyses for analysis_plan.md steps 2–8.

Uses the corrected workbook. No cross-blot pooling is used for the primary
associations. Generated files are written beneath ouput/analysis/.
"""
from pathlib import Path
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr, kendalltau, wilcoxon

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'data' / 'Information_for_Baris_corrected.xlsx'
OUT = ROOT / 'ouput' / 'analysis'
OUT.mkdir(parents=True, exist_ok=True)

# Read all source cells without treating zeros as missing.
wb = pd.ExcelFile(INPUT)
feeding = pd.read_excel(INPUT, sheet_name='Information for feeding', header=None)
results = pd.read_excel(INPUT, sheet_name='Results', header=None)
third = pd.read_excel(INPUT, sheet_name='SP and other collagen proteins', header=None)

blocks = [
    ('Blot 1', 1, 1, 2, 5),
    ('Blot 2', 6, 7, 8, 11),
    ('Blot 3', 12, 13, 14, 17),
    ('Validation blot', 20, 21, 22, 26),
]
# tuple: display name, zero-based title row, zero-based peptide-header row,
# zero-based replicate start, zero-based replicate end-exclusive

# Sequence inventory, with source Excel row references.
seq = {}
for ridx in range(4, 36):
    pid = feeding.iat[ridx, 0]
    if pd.notna(pid):
        aa = str(feeding.iat[ridx, 2]).strip()
        nt = str(feeding.iat[ridx, 3]).strip().upper()
        seq[pid] = dict(sequence_sheet_row=ridx + 1, aa=aa, nt=nt)

# Long replicate observations and per-peptide/block summaries.
long = []
summary = []
replicate_ranks = []
for name, title_idx, hidx, start, end in blocks:
    peptide_cols = [c for c in range(1, results.shape[1]) if pd.notna(results.iat[hidx, c])]
    for c in peptide_cols:
        pid = str(results.iat[hidx, c]).strip()
        vals = []
        for rr in range(start, end):
            value = results.iat[rr, c]
            if pd.notna(value):
                rep = str(results.iat[rr, 0]).strip()
                vals.append(float(value))
                long.append(dict(block=name, peptide_id=pid, replicate=rep, value=float(value),
                                 source_cell=f'Results!{chr(65+c)}{rr+1}'))
        arr = np.asarray(vals, dtype=float)
        summary.append(dict(block=name, peptide_id=pid, n=len(arr), mean=arr.mean(), median=np.median(arr),
                            sd=arr.std(ddof=1) if len(arr)>1 else np.nan,
                            min=arr.min(), max=arr.max(), cv=(arr.std(ddof=1)/arr.mean() if len(arr)>1 and arr.mean()!=0 else np.nan)))
        for rep, value in zip([str(results.iat[rr,0]).strip() for rr in range(start,end) if pd.notna(results.iat[rr,c])], arr):
            replicate_ranks.append(dict(block=name, peptide_id=pid, replicate=rep, value=value,
                                        within_replicate_rank=np.nan))

long_df = pd.DataFrame(long)
sum_df = pd.DataFrame(summary)
# Rank by mean outcome within each block; average ranks for ties. Larger value = stronger relative outcome.
sum_df['within_block_mean_rank_desc'] = sum_df.groupby('block')['mean'].rank(ascending=False, method='average')
for block, grp in long_df.groupby('block'):
    for rep, inds in grp.groupby('replicate').groups.items():
        ranks = grp.loc[inds, 'value'].rank(ascending=False, method='average')
        long_df.loc[inds, 'within_replicate_rank_desc'] = ranks

sum_df.sort_values(['block','within_block_mean_rank_desc']).to_csv(OUT/'replicate_summary_by_peptide.csv', index=False)
long_df.to_csv(OUT/'replicate_values_long.csv', index=False)

# Within-block replicate rank concordance (exploratory reliability description, not independent n).
rank_rows=[]
for name, title_idx, hidx, start, end in blocks:
    reps = [str(results.iat[rr,0]).strip() for rr in range(start,end)]
    pids = [str(results.iat[hidx,c]).strip() for c in range(1,results.shape[1]) if pd.notna(results.iat[hidx,c])]
    vals = {rep:[] for rep in reps}
    for c in range(1,results.shape[1]):
        if pd.isna(results.iat[hidx,c]): continue
        for rr,rep in zip(range(start,end), reps):
            v=results.iat[rr,c]
            if pd.notna(v): vals[rep].append(float(v))
    for i in range(len(reps)):
        for j in range(i+1,len(reps)):
            if not vals[reps[j]]:
                continue
            rho,p=spearmanr(vals[reps[i]], vals[reps[j]])
            tau=kendalltau(vals[reps[i]], vals[reps[j]]).statistic
            rank_rows.append(dict(block=name,replicate_a=reps[i],replicate_b=reps[j],n=len(vals[reps[i]]),spearman_rho=rho,kendall_tau=tau,p_value=p))
pd.DataFrame(rank_rows).to_csv(OUT/'replicate_rank_concordance.csv',index=False)

# Figure: replicate observations per peptide, faceted by distinct blot, with each block on its own scale.
sns.set_theme(style='whitegrid')
fig, axes = plt.subplots(2,2,figsize=(16,11))
for ax,(name,grp) in zip(axes.flat,long_df.groupby('block',sort=False)):
    order=(sum_df[sum_df.block==name].sort_values('mean')['peptide_id'].tolist())
    sns.stripplot(data=grp,x='peptide_id',y='value',order=order,hue='replicate',dodge=True,jitter=.16,size=5,ax=ax)
    ax.set_title(f'{name}: replicate values (ordered by mean)')
    ax.set_xlabel('Peptide ID (low → high mean)')
    ax.set_ylabel('Reported fold-change')
    ax.tick_params(axis='x',rotation=55)
    ax.legend(title='Replicate',fontsize=8)
fig.tight_layout()
fig.savefig(OUT/'replicate_values_by_blot.png',dpi=180)
plt.close(fig)

# Step 3: shared peptides, main-blot and validation are kept as separate observations.
val = sum_df[sum_df.block=='Validation blot'].set_index('peptide_id')
main = sum_df[sum_df.block!='Validation blot'].set_index('peptide_id')
paired=[]
for pid,row in val.iterrows():
    m=main.loc[pid]
    # Store names as strings, but treat first-column cells as replicate labels only in data rows.
    paired.append(dict(peptide_id=pid,main_block=m.block,main_mean=m['mean'],main_median=m['median'],main_sd=m.sd,
                       validation_mean=row['mean'],validation_median=row['median'],validation_sd=row.sd,
                       mean_difference_validation_minus_main=row['mean']-m['mean'],
                       main_mean_rank_desc=m.within_block_mean_rank_desc,
                       validation_mean_rank_desc=row.within_block_mean_rank_desc))
pair_df=pd.DataFrame(paired)
pair_df.to_csv(OUT/'validation_paired_shared_peptides.csv',index=False)
rho,p=spearmanr(pair_df.main_mean,pair_df.validation_mean)
pearson,pp=pearsonr(pair_df.main_mean,pair_df.validation_mean)
rankrho,rankp=spearmanr(pair_df.main_mean_rank_desc,pair_df.validation_mean_rank_desc)
try:
    wx=wilcoxon(pair_df.validation_mean,pair_df.main_mean,alternative='two-sided')
    wstat,wp=float(wx.statistic),float(wx.pvalue)
except ValueError:
    wstat,wp=np.nan,np.nan
pd.DataFrame([dict(n=len(pair_df),spearman_rho=rho,spearman_p=p,pearson_r=pearson,pearson_p=pp,
                   rank_spearman_rho=rankrho,rank_spearman_p=rankp,paired_wilcoxon_stat=wstat,paired_wilcoxon_p=wp,
                   mean_validation_minus_main=pair_df.mean_difference_validation_minus_main.mean(),
                   median_validation_minus_main=pair_df.mean_difference_validation_minus_main.median())]).to_csv(OUT/'validation_comparison_stats.csv',index=False)
fig,ax=plt.subplots(figsize=(7,6))
for _,row in pair_df.iterrows():
    ax.scatter(row.main_mean,row.validation_mean,s=50)
    ax.annotate(row.peptide_id,(row.main_mean,row.validation_mean),xytext=(4,4),textcoords='offset points',fontsize=9)
ax.set_xlabel('Original blot mean (within its own blot)')
ax.set_ylabel('Validation blot mean (separate experiment)')
ax.set_title('Shared peptides: separate blot summaries (n=7)')
fig.tight_layout();fig.savefig(OUT/'validation_shared_peptides.png',dpi=180);plt.close(fig)

# Step 5: sequence QC and transparent simple features. All features describe the full listed sequence;
# no cleavage-site/domain boundary is asserted. A proxy charge is K+R-D-E per residue.
valid_aa=set('ACDEFGHIKLMNPQRSTVWY')
sequence_rows=[]
for pid,item in seq.items():
    aa=item['aa']; nt=item['nt'];
    valid_frame=(len(nt)==3*len(aa))
    genetic_code={
        'TTT':'F','TTC':'F','TTA':'L','TTG':'L','TCT':'S','TCC':'S','TCA':'S','TCG':'S','TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','TGT':'C','TGC':'C','TGA':'*','TGG':'W',
        'CTT':'L','CTC':'L','CTA':'L','CTG':'L','CCT':'P','CCC':'P','CCA':'P','CCG':'P','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','CGT':'R','CGC':'R','CGA':'R','CGG':'R',
        'ATT':'I','ATC':'I','ATA':'I','ATG':'M','ACT':'T','ACC':'T','ACA':'T','ACG':'T','AAT':'N','AAC':'N','AAA':'K','AAG':'K','AGT':'S','AGC':'S','AGA':'R','AGG':'R',
        'GTT':'V','GTC':'V','GTA':'V','GTG':'V','GCT':'A','GCC':'A','GCA':'A','GCG':'A','GAT':'D','GAC':'D','GAA':'E','GAG':'E','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}
    trans=''.join(genetic_code.get(nt[i:i+3],'?') for i in range(0,len(nt)-2,3)) if valid_frame else ''
    hydrophobic_fraction=sum(aa.count(x) for x in 'AVILMFWY')/len(aa)
    hydrophobic_core_fraction=sum(aa.count(x) for x in 'FILMVWY')/len(aa)
    net_charge_proxy=aa.count('K')+aa.count('R')-aa.count('D')-aa.count('E')
    gc_first_9=(nt[:9].count('G')+nt[:9].count('C'))/len(nt[:9]) if len(nt)>=9 else np.nan
    sequence_rows.append(dict(peptide_id=pid,source_row=f'Information for feeding!A{item["sequence_sheet_row"]}',
        aa_length=len(aa),nt_length=len(nt),aa_alphabet_valid=not (set(aa)-valid_aa),nt_alphabet_valid=not (set(nt)-set('ACGT')),
        nt_is_3x_aa_length=valid_frame,translated_nt_matches_aa=(trans==aa),aa_sequence=aa,nt_sequence=nt,
        hydrophobic_residue_fraction_AVILMFWY=hydrophobic_fraction,hydrophobic_core_proxy_fraction_FILMVWY=hydrophobic_core_fraction,
        basic_minus_acidic_count_per_residue=net_charge_proxy/len(aa),basic_minus_acidic_count=net_charge_proxy,
        nt_gc_fraction_first_9_bases=gc_first_9))
seq_df=pd.DataFrame(sequence_rows)
seq_df.to_csv(OUT/'sequence_qc_and_features.csv',index=False)

# Step 6/7: descriptive association analyses within each original blot.
# Primary sequence features prespecified here: full sequence length, AVILMFWY fraction,
# and basic-minus-acidic count/residue. Also show one exploratory first-9-nt GC proxy.
feature_cols={
    'AA length (full listed sequence)':'aa_length',
    'AVILMFWY fraction (full sequence; broad hydrophobic proxy)':'hydrophobic_residue_fraction_AVILMFWY',
    'K+R-D-E per residue (simple charge proxy)':'basic_minus_acidic_count_per_residue',
    'GC fraction in first 9 nt (exploratory; initiation context unverified)':'nt_gc_fraction_first_9_bases',
}
assoc=[]
main_summ=sum_df[sum_df.block!='Validation blot']
joined=main_summ.merge(seq_df,on='peptide_id',validate='many_to_one')
for block,grp in joined.groupby('block',sort=False):
    for label,col in feature_cols.items():
        rho,rp=spearmanr(grp[col],grp['mean'])
        pr,pp=pearsonr(grp[col],grp['mean'])
        assoc.append(dict(block=block,n=len(grp),feature=label,spearman_rho=rho,spearman_p=rp,pearson_r=pr,pearson_p=pp))
assoc_df=pd.DataFrame(assoc)
assoc_df.to_csv(OUT/'within_blot_feature_associations.csv',index=False)
# Show within-blot means and all candidates, no pooled association.
fig,axes=plt.subplots(4,3,figsize=(14,16))
for row,(label,col) in enumerate(feature_cols.items()):
    for colidx,block in enumerate(['Blot 1','Blot 2','Blot 3']):
        grp=joined[joined.block==block]
        ax=axes[row,colidx]
        sns.regplot(data=grp,x=col,y='mean',lowess=False,ci=None,scatter_kws={'s':38},line_kws={'color':'#aa3333'},ax=ax)
        for _,rr in grp.iterrows(): ax.annotate(rr.peptide_id,(rr[col],rr['mean']),xytext=(3,3),textcoords='offset points',fontsize=7)
        stat=assoc_df[(assoc_df.block==block)&(assoc_df.feature==label)].iloc[0]
        ax.set_title(f'{block}: Spearman ρ={stat.spearman_rho:.2f}, n={len(grp)}')
        ax.set_xlabel(label)
        if colidx==0: ax.set_ylabel('Mean reported fold-change')
fig.tight_layout();fig.savefig(OUT/'within_blot_feature_associations.png',dpi=180);plt.close(fig)

# Step 8: category values are retained verbatim in the corrected workbook and summarized as counts.
category_header=third.iloc[1]
cat_rows=[]
for ridx in range(2,6):
    pid=third.iat[ridx,0]
    if pd.isna(pid): continue
    for c in range(1,8):
        cat_rows.append(dict(peptide_id=str(pid),category_sheet_row=ridx+1,protein_construct=str(category_header[c]),category=str(third.iat[ridx,c])))
cat_df=pd.DataFrame(cat_rows)
cat_df.to_csv(OUT/'other_protein_categories_long.csv',index=False)
cat_df.pivot(index='peptide_id',columns='protein_construct',values='category').to_csv(OUT/'other_protein_categories_matrix.csv')
counts=cat_df.groupby(['protein_construct','category']).size().rename('n').reset_index()
counts.to_csv(OUT/'other_protein_category_counts.csv',index=False)
order=['No','Low','Medium','High']
mat=cat_df.pivot(index='peptide_id',columns='protein_construct',values='category')
code={v:i for i,v in enumerate(order)}
num=mat.apply(lambda col:col.map(code))
# Give each construct column enough horizontal space for its full workbook name.
# Rotate labels slightly and anchor them right so long names stay legible in the image.
fig,ax=plt.subplots(figsize=(20,7))
sns.heatmap(num,annot=mat,fmt='',cmap=sns.color_palette(['#d9d9d9','#ef9a9a','#ffe082','#81c784'],as_cmap=True),cbar=False,linewidths=.5,ax=ax)
ax.set_title('Corrected third-sheet category labels (not quantitative or threshold-verified)')
ax.set_xlabel('Protein construct');ax.set_ylabel('Signal peptide')
ax.tick_params(axis='x',labelsize=10,pad=8)
plt.setp(ax.get_xticklabels(),rotation=25,ha='right',rotation_mode='anchor')
fig.tight_layout();fig.savefig(OUT/'other_protein_categories_heatmap.png',dpi=180,bbox_inches='tight');plt.close(fig)

# Summary metadata for exact reproduction and explicit lack of assumptions.
(OUT/'README.md').write_text('''# Analysis outputs (steps 2–8)\n\nGenerated by `run_steps_2_8.py` from `data/Information_for_Baris_corrected.xlsx`. Python dependencies: pandas, numpy, scipy, matplotlib, seaborn, openpyxl.\n\n- `replicate_summary_by_peptide.csv`: per peptide/block mean, median, sample SD, min/max, CV, within-block mean rank.\n- `replicate_values_long.csv`: source cell and numeric replicate-level values.\n- `replicate_rank_concordance.csv`: pairwise replicate Spearman/Kendall rank consistency within each block.\n- `replicate_values_by_blot.png`: replicate values faceted by blot; each has its own axis/scale.\n- `validation_paired_shared_peptides.csv`, `validation_comparison_stats.csv`, `validation_shared_peptides.png`: descriptive paired comparison for seven shared candidates. No calibration was fitted.\n- `sequence_qc_and_features.csv`: sequence alphabet/length/translation QC and transparent full-listed-sequence features. No cleavage boundaries are assumed.\n- `within_blot_feature_associations.csv`, `within_blot_feature_associations.png`: descriptive associations within each original blot; no combined cross-blot outcome is used. P-values are exploratory and unadjusted.\n- `other_protein_categories_long.csv`, `other_protein_categories_matrix.csv`, `other_protein_category_counts.csv`, `other_protein_categories_heatmap.png`: corrected categorical labels kept categorical.\n\nMeeting 2 added owner-reported clarifications: replicates are described as biological (exact unit/independence unclear); values are ordered left-to-right by ascending replicate mean for presentation; normalization is described as lane-total-protein normalization followed by division by the gel-wide mean of normalized band intensities; and category `No` means product not produced. The owner interprets SP9's recorded zero as likely no secretion but is unsure of its origin. These statements have not been audited against raw assay records; `No` remains categorical and the zero remains numeric. The first-nine-nucleotide GC proxy is exploratory only because translation-initiation sequence boundaries are unknown.\n''',encoding='utf-8')
print(f'Wrote analysis outputs to {OUT}')
