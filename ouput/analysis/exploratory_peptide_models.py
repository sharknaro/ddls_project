#!/usr/bin/env python3
"""Small-n exploratory modeling using one outcome row per peptide.

No cross-blot outcome pooling. For each original blot separately, compare a
median-only baseline to ridge regression on a compact, predefined feature set.
Leave-one-peptide-out cross-validation is used; no replicate rows are split.
Performance is descriptive and not an external validation estimate.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'ouput'/'analysis'
features=pd.read_csv(OUT/'documented_sequence_features.csv')
outcomes=pd.read_csv(OUT/'replicate_summary_by_peptide.csv')
# Small predeclared continuous feature panel; exclude near-duplicate composition measures
# and unreliable sequence-derived features for SP31 (nt/translation inconsistency).
FEATURES=['aa_length','N5_KR_count','core_hydrophobic_AVILMFWY_fraction',
          'core_mean_Kyte_Doolittle','whole_KRDE_net_charge_per_residue',
          'mfe_first30nt_kcal_mol']
joined=outcomes[outcomes.block!='Validation blot'].merge(features,on='peptide_id',validate='many_to_one')
# Do not use SP31's nucleotide-derived MFE because listed Nt/AA disagree. Impute within
# training fold by pipeline, so this candidate's RNA feature is missing rather than trusted.
j=joined.copy()
j.loc[j.peptide_id=='SP31','mfe_first30nt_kcal_mol']=np.nan
rows=[]; preds=[]
for block,g in j.groupby('block',sort=False):
    X=g[FEATURES].replace([np.inf,-np.inf],np.nan)
    y=g['mean'].to_numpy(float)
    n=len(g)
    loo=LeaveOneOut()
    # Baseline: training-fold mean, implemented directly to avoid leakage.
    baseline=[]; modelpred=[]
    for train,test in loo.split(X):
        baseline.append(float(np.mean(y[train])))
        pipe=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),Ridge(alpha=10.0))
        pipe.fit(X.iloc[train],y[train])
        modelpred.append(float(pipe.predict(X.iloc[test])[0]))
    for pid,obs,bp,mp in zip(g.peptide_id,y,baseline,modelpred):
        preds.append(dict(block=block,peptide_id=pid,observed_mean=obs,loo_baseline_prediction=bp,loo_ridge_prediction=mp,
                          residual_model=obs-mp,residual_baseline=obs-bp))
    for name,p in [('mean-baseline',baseline),('ridge-alpha-10',modelpred)]:
        p=np.asarray(p)
        rows.append(dict(block=block,n=n,model=name,features=(';'.join(FEATURES) if name!='mean-baseline' else 'none'),
             MAE=mean_absolute_error(y,p),RMSE=mean_squared_error(y,p)**0.5,
             Spearman_rho=spearmanr(y,p).statistic,LOO_R2=r2_score(y,p),
             note='LOO at peptide level; exploratory only; not an external validation estimate'))
# Secondary ranking target: within-blot outcome ranks; similarly exploratory, report Spearman above.
pd.DataFrame(rows).to_csv(OUT/'exploratory_model_metrics_by_blot.csv',index=False)
pd.DataFrame(preds).to_csv(OUT/'exploratory_model_loo_predictions.csv',index=False)
# Compact pooled display of metrics only; do not pool observations/scales.
print(pd.DataFrame(rows).to_string(index=False))
