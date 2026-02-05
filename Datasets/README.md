## Consolidated datasets:

Final datasets for each ADME endpoint and Potency after merging from external sources and standardization.
Please refer Table 1 in our manuscript for the sources specific to each endpoint. The Challenge datasets were augmented with external data and studied.

### ADME Datasets
1. LogD_consolidated.csv
2. KSOL_consolidated.csv
3. HLM_consolidated.csv
4. MLM_consolidated.csv
5. MDR1_MDCK_consolidated.csv

For each instance the SMILES string and the respective endpoint value are provided. These are provided as input files to the respective training scripts shared in this same repository.

### Potency Dataset:

The fine-tuning dataset and the domain-specific dataset for training from scratch were just the Challenge datasets including SARS and MERS. The dataset is reproduced here for the sake of completeness (polaris-potency_train.tsv)

In addition, a dataset of 30,220 protein-ligand pairs curated from ChEMBL by searching for ligands with IC50 values and retrieving sequences of the corresponding target proteins from UniProt, is also shared. This dataset was compiled using the scripts provided in Supplementary File S4 (with our manuscript) and is used for pre-training a protein-ligand AttFPGNN-transformer baseline model. (Potency-ChEMBL-UniProt_Protein-Ligand_Dataset.csv)

