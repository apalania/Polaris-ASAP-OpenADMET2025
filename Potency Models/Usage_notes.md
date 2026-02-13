## BaseModel: AttFPGNN-Transformer on ChEMBL+UniProt

### Inputs 

| File Name | Required Columns | Description |
|-----------|------------------|-------------|
| protein_ligand.csv | protein_sequence, canonical_smiles, IC50 | ChEMBL data with protein sequences, ligand SMILES, and binding affinity values |

### Outputs

| File Name | Description |
|-----------|-------------|
| potency_enhanced_features_best_model.pt | Saved model checkpoint |
| vocab_enhanced_features.pkl | Vocabulary mapping for protein sequences |
| tokenizer_enhanced_features.pkl | Tokenizer for processing protein sequences |

## GPFT: Progressive Fine-tuning models (Random & Scaffold split)

### Inputs 

| File Name | Required Columns | Description |
|-----------|------------------|-------------|
| potency_enhanced_features_best_model.pt | N/A | Pre-trained model weights from base model |
| vocab_enhanced_features.pkl | N/A | Vocabulary for tokenization |
| tokenizer_enhanced_features.pkl | N/A | Tokenizer object |
| polaris_train.csv | ligand_smiles OR SMILES OR canonical_smiles, protein_sequence OR PROTEIN_SEQ, pIC50 OR logIC50 OR IC50 | Training data |
| polaris_unblinded_test.csv | ligand_smiles OR SMILES OR canonical_smiles, protein_sequence OR PROTEIN_SEQ, pIC50 OR logIC50 OR IC50 | Test data |

### Outputs

| File Name | Columns | Description |
|-----------|---------|-------------|
| target_specific_random_p1-20_tuned_predictions.csv | Actual values, Predicted values, Residuals | Fine-tuned model predictions |
| scaffold_split_indices.json (scaffold split only) | N/A | Split indices for use in other models |

## Domain-specific AttFPGNN-Transformer training from scratch (Random & Scaffold split)

### Inputs 

| File Name | Required Columns | Description |
|-----------|------------------|-------------|
| polaris_train.csv | canonical_smiles OR SMILES, protein_sequence OR protein_seq, pIC50 OR pic50 OR p_ic50 | Training data |
| polaris_unblinded_test.csv | Same as training (pIC50 optional) | Test data |
| scaffold_split_indices.json (scaffold split only) | N/A | Pre-computed split indices from GPFT |

### Outputs

| File Name | Columns | Description |
|-----------|---------|-------------|
| test_predictions.csv | Actual values, Predictions, Errors | Test set predictions with metrics |
| enhanced_Target_Random_best_model.pt | N/A | Best trained model checkpoint |
| vocab_enhanced_Target_Random.pkl | N/A | Protein sequence vocabulary |
| tokenizer_enhanced_Target_Random.pkl | N/A | Protein tokenizer |

## XGBoost models, with optional Docking scores in input

### Inputs 

| File Name | Columns | Description |
|-----------|------------------|-------------|
| train.csv | SMILES OR canonical_smiles OR ligand_smiles, PROTEIN_SEQ OR PROTEIN OR TARGET OR protein_sequence, IC50 OR logIC50 OR pIC50 | Training data pool |
| test.csv | Same as train.csv | External test set |
| train_docking_scores.csv  | Docking scores (optional)| Docking scores for training data |
| test_docking_scores.csv  | Docking scores (optional) | Docking scores for test data |
| descriptors_55.txt | N/A | List of 55 molecular descriptor names (one per line) |
| descriptors_25.txt | N/A | List of 25 molecular descriptor names (one per line) |
| enhanced_scaffold_split_indices.json | N/A | Pre-computed train/val split indices |

### Outputs

| File Name | Columns | Description |
|-----------|---------|-------------|
| predictions_xgb_{strategy}\_{desc}desc_{dock}_test.csv | Predictions and actual values | Test predictions for each configuration |
| xgb_{strategy}\_{desc}desc_{dock}.json | N/A | XGBoost model (JSON format) |
| scaler_xgb_{strategy}\_{desc}desc_{dock}.pkl | N/A | StandardScaler for features |

## Stacking ensemble (Domain-specific AttFPGNN-Transformer + XGB)

### Inputs 

| File Name | Location | Required Columns | Description |
|-----------|----------|------------------|-------------|
| enhanced_scaffold_best_model.pt | Enhanced_GNN_Scaffold/ | N/A | Trained GNN model |
| vocab_enhanced_scaffold.pkl | Enhanced_GNN_Scaffold/ | N/A | Vocabulary |
| tokenizer_enhanced_scaffold.pkl | Enhanced_GNN_Scaffold/ | N/A | Tokenizer |
| xgb_target_specific_scaffold_55desc_dock.json | XGB_Scaffold_Potency/ | N/A | XGBoost model |
| scaler_xgb_target_specific_scaffold_55desc_dock.pkl | XGB_Scaffold_Potency/ | N/A | Feature scaler |
| enhanced_scaffold_split_indices.json | Enhanced_GNN_Scaffold/ | N/A | Split indices |
| enhanced_Target_Random_best_model.pt | Enhanced_GNN_Random/ | N/A | Trained GNN model |
| polaris_train.csv | Current directory | SMILES OR canonical_smiles OR ligand_smiles, PROTEIN_SEQ OR PROTEIN OR TARGET OR protein_sequence, IC50 OR logIC50 OR pIC50 | Training dataset |
| polaris_unblinded_test.csv | Current directory | Same as train | Test dataset |
| descriptors_25.txt | Current directory | N/A | Molecular descriptor names |
| train_docking_scores.csv (optional) | Current directory | Docking scores | Docking scores for holdout |
| test_docking_scores.csv (optional) | Current directory | Docking scores | Docking scores for test |

### Outputs

| File Name | Columns | Description |
|-----------|---------|-------------|
| final_test_predictions.csv | SMILES, protein_sequence, True values (pIC50, IC50 nM), GNN predictions, XGBoost predictions, Stacked predictions, Absolute errors | Comprehensive predictions with all model outputs |
| stacking_ridge_model.pth | N/A | Saved stacking model |

