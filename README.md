# Polaris-ASAP-OpenADMET_Challenge-2025_Final
Datasets and Code for training ADME and Potency models for the [Antiviral Drug Discovery 2025](https://polarishub.io/competitions/asap-discovery/antiviral-drug-discovery-2025) Challenge 

This repository is a summary of our work on the Polaris-ASAP-OpenADMET Antiviral Challenge 2025, including post-competition analysis and enhancements. 
It provides the training scripts for all the five ADME problems posed in the challenge as well as the codebase for experimenting with various models of Potency.
The ADME endpoints considered include:
1. LogD - lipophilicity
2. KSOL - kinetic solutibility
3. HLM - Human liver microsomal clearance
4. MLM - Mouse liver microsomal clearance
5. MDR1-MDCKII permeability

Potency modeling was considered against the SAR-Cov2 and MERS-CoV main protease (Mpro) enzyme.

If you are interested in our original contribution to the challenge, it can be found in this repository and a corresponding discussion here.

Models themselves (for inference) could be found on huggingface.

## Team SystemsCBLab members:
1. Mounika Sri Lakskmi Mallepulla [UG student]
2. Ida Priyadarshini T [PhD Student]
3. Ashok Palaniappan, Ph.D (PI)
