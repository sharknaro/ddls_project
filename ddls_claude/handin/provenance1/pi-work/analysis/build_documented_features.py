#!/usr/bin/env python3
"""Build documented, exploratory signal-peptide sequence features.

Inputs are the listed signal-peptide AA and coding sequences in the corrected
workbook. Since cleavage/boundary annotations and full translation-initiation
context are unavailable, AA regions are explicit positional heuristics and
RNA folding is calculated only on the available SP CDS (not a full mRNA/5'UTR).
These are features, not validated secretion predictors.
"""
from pathlib import Path
import math
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
XLSX=ROOT/'data'/'Information_for_Baris_corrected.xlsx'
OUT=ROOT/'ouput'/'analysis'
OUT.mkdir(parents=True,exist_ok=True)

# Region conventions: sequences are 1-indexed in documentation.
# N = residues 1-5; C = last 5 residues; putative core = residues 5 through L-3
# inclusive (Python aa[4:-3]). These are exploratory positional windows only.
HYD='AVILMFWY'
AA='ACDEFGHIKLMNPQRSTVWY'
# Kyte-Doolittle hydropathy, standard scale.
KD={'I':4.5,'V':4.2,'L':3.8,'F':2.8,'C':2.5,'M':1.9,'A':1.8,'G':-0.4,'T':-0.7,'S':-0.8,'W':-0.9,'Y':-1.3,'P':-1.6,'H':-3.2,'E':-3.5,'Q':-3.5,'D':-3.5,'N':-3.5,'K':-3.9,'R':-4.5}
# Approximate integer net charge at neutral pH, side chains only; termini omitted.

wb=pd.ExcelFile(XLSX)
df=pd.read_excel(XLSX,sheet_name='Information for feeding',header=None)
rows=[]
for i in range(4,36):
    pid=df.iat[i,0]
    if pd.isna(pid): continue
    aa=str(df.iat[i,2]).strip().upper()
    nt=str(df.iat[i,3]).strip().upper()
    if not aa or not nt or set(aa)-set(AA) or set(nt)-set('ACGT'):
        raise ValueError(f'Invalid alphabet for {pid}')
    L=len(aa); n5=aa[:5]; core=aa[4:-3]; c5=aa[-5:]
    if not core: raise ValueError(f'Empty core for {pid}')
    translated=''
    try:
        from Bio.Seq import Seq
        translated=str(Seq(nt).translate(to_stop=False))
    except ImportError:
        pass
    x={'peptide_id':str(pid),'source_excel_row':i+1,'aa_sequence':aa,'nt_sequence':nt,
       'aa_length':L,'nt_length':len(nt),'nt_length_is_3x_aa':len(nt)==3*L,
       'translation_matches_aa':translated==aa,
       'region_definition':'N=aa[1:5]; heuristic core=aa[5:L-3] (Python aa[4:-3]); C=last 5 aa (1-indexed notation; endpoints per script)',
       'N5_sequence':n5,'heuristic_core_sequence':core,'C5_sequence':c5,
       'N5_KR_count':sum(n5.count(a) for a in 'KR'),'N5_basic_fraction':sum(n5.count(a) for a in 'KR')/len(n5),
       'core_hydrophobic_AVILMFWY_fraction':sum(core.count(a) for a in HYD)/len(core),
       'core_mean_Kyte_Doolittle':float(np.mean([KD[a] for a in core])),
       'core_GS_fraction':sum(core.count(a) for a in 'GS')/len(core),
       'core_ST_fraction':sum(core.count(a) for a in 'ST')/len(core),
       'C5_AXA_like_motif':int(len(aa)>=3 and aa[-3]=='A' and aa[-1]=='A'),
       'whole_hydrophobic_AVILMFWY_fraction':sum(aa.count(a) for a in HYD)/L,
       'whole_mean_Kyte_Doolittle':float(np.mean([KD[a] for a in aa])),
       'whole_KRDE_net_charge_sidechain_proxy':aa.count('K')+aa.count('R')-aa.count('D')-aa.count('E'),
       'whole_KRDE_net_charge_per_residue':(aa.count('K')+aa.count('R')-aa.count('D')-aa.count('E'))/L,
       'whole_polar_NQST_fraction':sum(aa.count(a) for a in 'NQST')/L,
       'whole_GS_fraction':sum(aa.count(a) for a in 'GS')/L,
       'whole_ST_fraction':sum(aa.count(a) for a in 'ST')/L,
       'whole_proline_fraction':aa.count('P')/L,'whole_cysteine_fraction':aa.count('C')/L,
       'N5_GC_fraction':(nt[:15].count('G')+nt[:15].count('C'))/len(nt[:15]),
       'whole_CDS_GC_fraction':(nt.count('G')+nt.count('C'))/len(nt),
       'first_30nt_GC_fraction':(nt[:30].count('G')+nt[:30].count('C'))/len(nt[:30]),
       'first_30nt_AU_fraction':(nt[:30].count('A')+nt[:30].count('T'))/len(nt[:30]),
       'first_30nt_CpG_dinucleotide_count':sum(nt[j:j+2]=='CG' for j in range(min(29,len(nt)-1))),
       'codon_adaptation_or_RBS_metric':'not computed: host reference/RBS and full transcript context unavailable'}
    rows.append(x)

features=pd.DataFrame(rows)
# RNA folding: calculate ViennaRNA MFE for the listed CDS only and explicitly
# label as a truncated-context proxy. Also use fixed windows to avoid length-dependent
# comparisons of full CDS. T is converted to U.
try:
    import RNA
except ImportError:
    RNA=None
for col in ['mfe_CDS_kcal_mol','mfe_first30nt_kcal_mol','mfe_first45nt_kcal_mol','mfe_first60nt_kcal_mol']:
    features[col]=np.nan
features['rna_fold_tool']='not available'
features['rna_fold_scope']='SP CDS only; no RBS, 5UTR, start context beyond SP coding sequence, or downstream fusion sequence'
if RNA is not None:
    features['rna_fold_tool']=f'ViennaRNA Python package {getattr(RNA,"__version__","version unavailable")}; RNA.fold default parameters'
    for ix,row in features.iterrows():
        seq=row.nt_sequence.replace('T','U')
        for name,part in [('mfe_CDS_kcal_mol',seq),('mfe_first30nt_kcal_mol',seq[:30]),('mfe_first45nt_kcal_mol',seq[:45]),('mfe_first60nt_kcal_mol',seq[:60])]:
            _,mfe=RNA.fold(part)
            features.loc[ix,name]=float(mfe)
    features['rna_fold_tool']=f'ViennaRNA Python package {getattr(RNA,"__version__","version unavailable")}; RNA.fold default parameters; T→U'

features.to_csv(OUT/'documented_sequence_features.csv',index=False)
# Concise methods dictionary, one row per feature family / named field.
meta=[
('aa_length','Length of listed amino-acid sequence','count','Exact listed sequence; boundaries unverified'),
('N5_KR_count; N5_basic_fraction','K+R count and proportion in first 5 AA','count; fraction','Positional N5 window, not a validated N-region annotation'),
('core_hydrophobic_AVILMFWY_fraction','Fraction of A,V,I,L,M,F,W,Y in heuristic core aa[4:-3]','fraction','Heuristic core positions 5 through L-3; not verified H-region'),
('core_mean_Kyte_Doolittle; whole_mean_Kyte_Doolittle','Mean residue hydropathy using Kyte-Doolittle scale','scale mean','Standard residue scale; averages depend on positional window'),
('core_GS_fraction; core_ST_fraction; whole_GS_fraction; whole_ST_fraction','Residue fraction in named composition groups','fraction','Transparent composition summaries; groups not mechanistic claims'),
('whole_KRDE_net_charge_sidechain_proxy; whole_KRDE_net_charge_per_residue','K+R-D-E, ignoring termini and pH-dependent partial charges','count; count/residue','Simple charge proxy, not pI or formal charge calculation'),
('whole_polar_NQST_fraction; whole_proline_fraction; whole_cysteine_fraction','Composition fractions','fraction','Full listed sequence'),
('C5_AXA_like_motif','Indicator that final three residues fit A-x-A','binary','Pattern scan only; cleavage motif/site unverified'),
('N5_GC_fraction; first_30nt_GC_fraction; first_30nt_AU_fraction; first_30nt_CpG_dinucleotide_count; whole_CDS_GC_fraction','Nucleotide composition/count metrics','fraction/count','Only listed SP coding sequence; no initiation context or host reference'),
('MFE fields','Minimum free energy from ViennaRNA RNA.fold on CDS or fixed first-nucleotide windows','kcal/mol','T→U; default settings; truncated CDS only, not full mRNA or translation initiation region'),
('codon_adaptation_or_RBS_metric','Not calculated','NA','Requires host codon reference or verified RBS/full transcript context'),
('translation check','Listed nt translated in standard frame and compared to listed AA','boolean','SP31 does not match: nt encodes MRKSL... whereas listed AA begins VRKSL...; retained as supplied and flagged')]
pd.DataFrame(meta,columns=['feature_name','definition','unit','assumption_and_limit']).to_csv(OUT/'documented_feature_dictionary.csv',index=False)
print(f'Wrote {len(features)} features for {len(features.peptide_id.unique())} peptides; ViennaRNA={RNA is not None}')
if not features.nt_length_is_3x_aa.all():
    raise SystemExit('Sequence length QC failed')
if not features.translation_matches_aa.all():
    print('WARNING: listed sequence translation mismatch(s):', ', '.join(features.loc[~features.translation_matches_aa,'peptide_id']))
