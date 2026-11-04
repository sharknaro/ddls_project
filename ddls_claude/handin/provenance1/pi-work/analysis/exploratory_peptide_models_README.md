# Exploratory peptide-level model: method and interpretation

Script: `exploratory_peptide_models.py`; run with `python ouput/analysis/exploratory_peptide_models.py` after building features and descriptive outcome summaries. Inputs: `documented_sequence_features.csv`, `replicate_summary_by_peptide.csv`.

## Target and split

Target is the arithmetic mean of the three reported replicates for each candidate in each original blot. Validation-blot observations are excluded from this exercise. There is exactly one row per peptide within its original blot; leave-one-peptide-out (LOO) predictions ensure replicates are never split across folds. No outcome values from another blot are used to train a given blot model. This evaluates interpolation/ranking among these small, observed candidate sets—not transfer to new protein constructs, assays, batches, or sequence space.

## Models/features

The baseline predicts the mean outcome among the training peptides in that blot. The exploratory model is Ridge regression (alpha=10) after training-fold median imputation and feature standardization, using six preselected features: AA length; K/R count in N5; hydrophobic fraction in the heuristic central segment; mean Kyte–Doolittle hydropathy in that segment; whole-sequence K+R−D−E per-residue proxy; and ViennaRNA MFE on first 30 nt of listed SP CDS. These are correlated and the model is not tuned. SP31’s MFE was set missing because its listed Nt does not translate to its listed AA; median imputation occurs within each training fold. The feature panel is small relative to wider sequence-embedding approaches but is still large relative to n, so shrinkage is used and interpretation remains cautious.

## Results

LOO results (`exploratory_model_metrics_by_blot.csv`) show:

| Blot | n peptides | Baseline MAE | Ridge MAE | Baseline RMSE | Ridge RMSE | Ridge Spearman ρ | Ridge LOO R² |
|---|---:|---:|---:|---:|---:|---:|---:|
| Blot 1 | 8 | 0.426 | 0.586 | 0.504 | 0.643 | −0.667 | −1.131 |
| Blot 2 | 13 | 0.761 | 0.722 | 0.995 | 0.979 | 0.049 | −0.136 |
| Blot 3 | 11 | 0.496 | 0.472 | 0.564 | 0.604 | −0.118 | −0.391 |

Ridge has slightly lower MAE in Blots 2 and 3, but worse than baseline in Blot 1. The rank correlations are poor in all three blots. LOO R² is negative throughout (R² relative to the full-sample mean baseline convention), indicating predictions are worse than a simple mean benchmark on squared error. The small MAE differences are not robust evidence of useful predictive signal; n is too small for precise uncertainty estimates and LOO folds share most training data. The unusual baseline rank correlation is a consequence of leave-one-out means and must not be interpreted as an alternative ranking model.

## Conclusion / limitations

This proves a model can be fitted, not that it predicts reliably. The selected six features and Ridge penalty were prespecified for this exploratory demonstration, not optimized. There is no independent test set, model selection uncertainty is not captured, outcomes are normalized within blot, and assay outcome semantics remain incompletely audited. Do not use these predictions to claim a new sequence will improve secretion. Candidate-level predictions in the companion CSV are diagnostic only. A larger prospective screen with replicated designs and a held-out peptide/new-batch test is needed for meaningful predictive evaluation.
