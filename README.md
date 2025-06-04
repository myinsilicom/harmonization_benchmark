# INSILICOM Benchmark Dataset and Model Alignment Score (MAS)

## Introduction to INSILICOM Use Case Exercise Materials

This repository contains;

1. An example to run the Insilicom data harmonization API.
2. Calculate the MAS score for the input, API output and the manually curated metadata.

The definition of the **MAS score**:

The MAS score quantifies the alignment of input metadata with a given data model, such as GDC standard. It is calculated as the ratio of harmonized data cells to the total expected cells across all required variables (16 for GDC). The score ranges from 0 to 1,with higher values indicating better compliance and metadata quality.

## Dataset Description

The dataset includes:

1. [`geo_input_20.json`](./data/geo_input_20.json): The 20 lung cancer-related GEO samples** metadata provided in **JSON format**.
2. [`gold_standard_20.json`](./data/gold_standard_20.json): The same 20 GEO metadata manually curated by us.
3. [`gdc_meta.json`](./data/gdc_meta.json): The Genomic Data Commons (GDC) standard.


## Cancer Harmonization Benchmark

- **Benchmark Name**: Cancer Harmonization Benchmark
- **Version**: 1.0
- **File name**: [`gold_standard_20.json`](./data/gold_standard_20.json)
- **Data Type**: metadata
- **Data Model Source**: GDC
- **Data Model Target**: GDC
- **Includes Variable Mappings**: true
- **Includes Value Mappings**: true
- **Has Hidden Data**: true
- **Hidden Data Proportion**: 20%
- **Annotation Method**: Manual by 2 experts
- **Number of Variables**: 23
- **Number of Values**: 460
- **API Submission Supported**: true
- **Container Submission Supported**: false
- **License**: CC BY 4.0
- **Number of Cases**: 20


## Running API

Following the [`01_metadata_API_calling.ipynb`](./src/01_metadata_API_calling.ipynb) notebook.

## Calculating FAIRness score

Following the [`02_fairness_score_calculation.ipynb`](./src/02_fairness_score_calculation_simple.ipynb) notebook.

## Important Notice

This benchmark dataset is developed by **Insilicom**. It is subject to limited release.


## Contact Information

For questions, please contact:

- **Jinfeng Zhang** – [jinfeng@insilicom.com](mailto:jinfeng@insilicom.com)
- **Sheldon Pang** – [xpang@insilicom.com](mailto:xpang@insilicom.com)

---

2025 **Insilicom LLC**. All Rights Reserved.
Limited external release.
