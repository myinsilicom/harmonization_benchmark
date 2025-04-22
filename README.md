# INSILICOM-BDF Benchmark Dataset and FAIRness score

## Introduction to INSILICOM-BDF Use Case Exercise Materials

This repository contains;

1. An example to run the Insilicom data harmonization API.
2. Calculate the FAIRness score for the input, API output and the manually curated metadata.

The definition of the **FAIRness score**:

The FAIRness score quantifies the alignment of input metadata with the Genomic Data Commons (GDC) standard. It is calculated as the ratio of harmonized data cells to the total expected cells across sixteen GDC-required variables. The score ranges from 0 to 1, with higher values indicating better compliance and metadata quality.

## Dataset Description

The dataset includes:

1. `geo_input_20.json`: The 20 lung cancer-related GEO samples** metadata provided in **JSON format**.
2. `gold_standard_20.json`: The same 20 GEO metadata manually curated by us.
3. `gdc_meta.json`: The Genomic Data Commons (GDC) standard.

## Running API

Following the [`01_metadata_API_calling.ipynb`](./src/01_metadata_API_calling.ipynb) notebook.

## Calculating FAIRness score

Following the [`02_fairness_score_calculation.ipynb`](./src/02_fairness_score_calculation.ipynb) notebook.

## Important Notice

This benchmark dataset is developed by **Insilicom** and **for ARPA-H BDF program use only**. It is subject to limited release.


## Contact Information

For questions, please contact:

- **Jinfeng Zhang** – [jinfeng@insilicom.com](mailto:jinfeng@insilicom.com)
- **Sheldon Pang** – [xpang@insilicom.com](mailto:xpang@insilicom.com)

---

2025 **Insilicom LLC**. All Rights Reserved.
Limited external release for **ARPA-H BDF program** use only.
