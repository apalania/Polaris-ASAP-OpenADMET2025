# Polaris-ASAP-OpenADMET_Challenge-2025_Final
Datasets and Code for training ADME and Potency models for the [Antiviral Drug Discovery 2025](https://polarishub.io/competitions/asap-discovery/antiviral-drug-discovery-2025) Challenge 

This repository is a summary of our work on the Polaris-ASAP-OpenADMET Antiviral Challenge 2025, including post-competition analysis and enhancements. 
It provides all the datasets we used for the Challenge, training scripts for all the five ADME problems posed in the challenge, and a codebase for various model experiments with Potency.
The ADME endpoints considered include:
1. LogD - lipophilicity
2. KSOL - kinetic solutibility
3. HLM - Human liver microsomal clearance
4. MLM - Mouse liver microsomal clearance
5. MDR1-MDCKII permeability

Potency modeling was considered against the SAR-Cov2 and MERS-CoV main protease (Mpro) enzyme.

Our original contribution to the challenge can be found [here](https://github.com/apalania/Polaris_ASAP-Challenge-2025) and a corresponding discussion [here](https://chemrxiv.org/doi/full/10.26434/chemrxiv-2025-1tb2m).

Ms. Mounika Srilakshmi*, Ms. Ida Titus*, Dr. Ashok Palaniappan. Experiments with data-augmented modeling of ADME and potency endpoints in the ASAP-Polaris-OpenADMET Antiviral Challenge. ChemRxiv. 09 September 2025. DOI: https://doi.org/10.26434/chemrxiv-2025-1tb2m

Models themselves (for inference) could be found on huggingface.

## Team SystemsCBLab members:
1. Ida Priyadarshini T [doctoral candidate]
2. Mounika Srilakskmi Mallepulla [UG student]
3. Ashok Palaniappan, Ph.D (PI)
