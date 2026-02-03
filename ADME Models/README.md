Scripts for training XGBoost models (with early stopping) for each endpoint are provided.

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

Ensemble strategy -- common to all endpoints [Ensemble_final.py]
