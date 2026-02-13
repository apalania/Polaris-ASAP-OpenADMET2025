## ADME Training scripts

### Scripts for training XGBoost models (with early stopping) for each ADME endpoint 

- feature generation from input SMILES dataset;
- k-fold cross-validation for hyperparameter optimization;
- evaluation on holdout test set; and
- retraining on full dataset for evaluation on Challenge Blind test set.

In addition, the script to prepare the ensemble models for each endpoint is provided. Three ensemble combinations are considered and implemented in this script (please see our manuscript for more details).

Endpoint training scripts:

1. LogD [LogD_final.py]
2. KSOL [KSOL_final.py]
3. HLM  [HLM_final.py]
4. MLM  [MLM_final.py]
5. MDR1-MDCKII [LMDR1_final.py]

### Ensemble script
The ensemble strategy is common to all endpoints and a unified script was used for this purpose [Ensemble_final.py].
Please refer to our manuscript for details.

Please consult the (Usage_notes.md)[https://github.com/apalania/Polaris-ASAP-OpenADMET2025/blob/main/ADME%20Models/Usage_notes.md] for using the scripts.
