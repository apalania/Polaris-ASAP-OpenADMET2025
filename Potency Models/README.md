## Scripts for training Potency models: a combination of classical ML + deep learning  

1. *_Pretrained_GNN-transformer_ChEMBL_random-split.py_*: 
Script for training the baseline model of potency prediction using ligand-protein pairs discovered from ChEMBL - UniProt.

2. *_Fine-tuned_GPFT_T-stratified_random.py_; _Fine-tuned_GPFT_T-stratified_scaffold.py_*:
Scripts for training Gradual partial (progressive) fine-tuning models of the baseline ChEMBL-UniProt model using the Polaris potency train data. GPFT was done with scaffold split or random split.  

4. *_AttFPGNN-transformer_Polaris-only_T-stratified_random.py_; _ATTFPGNN-transformer_Polaris-only_T-stratified_scaffold.py_*:
Script for training _de novo_ AttentiveFingerPrint GNN-transformer architectures for learning the molecule potency against SARS and MERS _M^Pro_ targets. Options to include docking scores in the final model are provided in the script. Both splits are shown - Random & Scaffold.

6. *_Ensembles_Early-Late-Stacking_random.py_; _Ensembles_Early-Late-Stacking_scaffold.py_*:
Implementations for the Ensemble methods for the various model classes, to determine the best pair combination when evaluated on unseen blindset. Three techniques were considered: Early fusion, late fusion, and stacking meta-learner.

8. *_XGBoost-models_25D-55D_docking_random-scaffold.py_*:
Script for training a model classical ML -- XGBoost with 25 or 55 antivirals-specific descriptors. The option to include docking scores is contained in the script. Since there are a few instances whose docking scores could not be computed, a binary flag (_has_docking_) is included in the feature space when docking scores are available in docking-enhanced XGBoost models. Both random and scaffold splits are available in a unified complete script. 
