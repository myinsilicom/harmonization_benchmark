# This file contains utility functions for processing metadata and calculating mas score.


import json
import pandas as pd
from typing import Dict, List, Tuple, Set
from IPython.display import display

def json_to_dataframe(json_path: str) -> pd.DataFrame:
    """
    Convert a JSON file containing sample data into a pandas DataFrame.
    
    The function expects a JSON structure where the top level keys are sample IDs,
    and each sample contains key-value pairs where values are dictionaries with a "val" key.
    
    Parameters:
    -----------
    json_path : str
        Path to the JSON file to be processed
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with samples as rows and attributes as columns
        
    Raises:
    -------
    FileNotFoundError: If the JSON file doesn't exist
    ValueError: If the JSON structure is not as expected
    """
    try:
        # Load the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise ValueError("JSON file must contain a dictionary at the top level")
            
        # Process the JSON data
        processed_data = {}
        
        for sample_id, details in data.items():
            if not isinstance(details, dict):
                print(f"Warning: Sample {sample_id} doesn't have a dictionary structure. Skipping.")
                continue
                
            try:
                sample_data = {}
                for key, value in details.items():
                    if isinstance(value, dict) and "val" in value:
                        sample_data[key] = value["val"]
                    else:
                        print(f"Warning: Field '{key}' in sample {sample_id} doesn't have expected structure. Using raw value.")
                        sample_data[key] = value
                        
                processed_data[sample_id] = sample_data
            except Exception as e:
                print(f"Error processing sample {sample_id}: {str(e)}. Skipping this sample.")
                
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(processed_data, orient="index")
        
        if df.empty:
            print("Warning: Resulting DataFrame is empty. Check the JSON structure.")
            
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {json_path}")
    except Exception as e:
        raise Exception(f"Error processing JSON file: {str(e)}")


def filter_gdc_metadata(gdc_meta: Dict, gdc_required_var: List) -> Dict:

    """
    Filter metadata based on required variables and update special keys.
    """

    filtered = {key: value for key, value in gdc_meta.items() if key in gdc_required_var}
    
    if 'diagnosis_is_primary_disease' in filtered:
        filtered['diagnosis_is_primary_disease']['value_names'] = [True, False]
    else:
        raise KeyError("'diagnosis_is_primary_disease' key is missing in metadata")
    return filtered


def process_input_dataframe(df_raw: pd.DataFrame, filtered_meta: Dict) -> pd.DataFrame:

    """
    Fill NaN with 'unknown', cast to string, clean gene_symbol, and filter columns using metadata keys.
    """

    df = df_raw.fillna("unknown").astype(str)


    # Needs to handle gene_symbol separately.
    if 'gene_symbol' in df.columns:

        # Remove quotes first to normalize the input
        df['gene_symbol'] = df['gene_symbol'].str.replace("'", "", regex=False)

        # Remove square brackets first
        df['gene_symbol'] = df['gene_symbol'].str.replace(r'[\[\]]', '', regex=True)

        # Replace separators and annotations with ''
        df['gene_symbol'] = df['gene_symbol'].str.replace(r'[:_-][^,]*(?=,)', '', regex=True)

        df['gene_symbol'] = df['gene_symbol'].str.replace(r'[:_-][^,]*$', '', regex=True)

    valid_columns = set(df.columns) & set(filtered_meta.keys())

    # Ensure valid_columns is not empty
    if not valid_columns:
        raise ValueError("No valid columns found after filtering with metadata keys.")

    return df[list(valid_columns)]


def precompute_gdcmeta_values(filtered_meta: Dict, columns: Set) -> Dict:
    """
    Precompute lowercase meta values for the given columns.
    """

    meta_values = {}

    for col in columns:
        if col in filtered_meta and 'value_names' in filtered_meta[col]:
            meta_values[col] = {str(val).lower() for val in filtered_meta[col]['value_names']}
        else:
            meta_values[col] = set()

    return meta_values


def compute_matches(df: pd.DataFrame, meta_values: Dict, numeric_cols: Set[str]) -> Dict:

    """
    Compute counts for numeric and non-numeric columns.
    """

    counts = {}

    for col in df.columns:

        if col in numeric_cols:
            counts[col] = pd.to_numeric(df[col], errors="coerce").notna().sum()

        else:
            # Exclude "unknown" values from being counted as matches
            matches = (df[col].str.lower().isin(meta_values.get(col, set())) & 
                      (df[col].str.lower() != "unknown"))
            counts[col] = matches.sum()
    
    return counts


def calculate_mas_score(counts: Dict, total_required: int, num_rows: int) -> float:

    """
    Calculate the mas score.
    """

    total_count = sum(counts.values())
    total_cells = total_required * num_rows
    return total_count / total_cells if total_cells > 0 else 0.0


def assess_data_mas(input_path: str, 
                         meta_path: str,
                         file_type: str = "csv") -> Tuple[pd.DataFrame, float]:
    """
    Main function that processes metadata and returns a counts DataFrame and mas score.
    
    Parameters:
    -----------
    input_path : str
        Path to the input file (either a CSV file or a JSON file)
    meta_path : str
        Path to the metadata JSON file
    file_type : str, optional
        Type of input file, either "csv" or "json" (default is "csv")
        
    Returns:
    --------
    Tuple[pd.DataFrame, float]
        - DataFrame with counts of matched variables
        - mas score (float between 0 and 1)
        
    Raises:
    -------
    ValueError: If file_type is not "csv" or "json"
    FileNotFoundError: If input_path or meta_path doesn't exist
    """
    # Validate file_type parameter
    if file_type not in ["csv", "json"]:
        raise ValueError("file_type must be either 'csv' or 'json'")
    
    # Load input data based on file_type
    if file_type == "csv":
        # Load CSV file with first column as index
        df_raw = pd.read_csv(input_path, index_col=0)
    else:  # file_type == "json"
        # Use json_to_dataframe function to convert JSON to DataFrame
        df_raw = json_to_dataframe(input_path)
    
    # Load the Standard vocabularies
    with open(meta_path, 'r') as f:
        gdc_meta = json.load(f)
    
    gdc_required_var = gdc_meta.keys()

    # Process the input dataframe
    filtered_meta = filter_gdc_metadata(gdc_meta, gdc_required_var)
    
    df_processed = process_input_dataframe(df_raw, filtered_meta)
    
    # Compute metadata values and mas score
    meta_values = precompute_gdcmeta_values(filtered_meta, set(df_processed.columns))
    numeric_cols = {"age_at_diagnosis", "days_to_follow_up"}
    counts = compute_matches(df_processed, meta_values, numeric_cols)
    
    # Create counts DataFrame
    counts_df = pd.DataFrame(list(counts.items()), columns=['Variable', 'Matched counts'])
    counts_df['Total counts'] = counts_df['Variable'].map(lambda col: df_processed[col].notna().sum())
    counts_df = counts_df.sort_values(by="Variable")

    # Calculate mas score
    mas_score = calculate_mas_score(counts, len(gdc_required_var), df_raw.shape[0])
    
    return counts_df, mas_score
