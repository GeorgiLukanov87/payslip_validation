# validators/gtn_validators.py

import pandas as pd


def check_gtn_numeric_elements(gtn_df: pd.DataFrame, mapping: dict) -> list:
    """
    Check that all mapped GTN element columns contain numeric values.
    Returns a list of element names that contain non-numeric values.
    """
    non_numeric_columns = []
    for vendor_col in mapping['used'].keys():
        if vendor_col in gtn_df.columns:
            if not pd.to_numeric(gtn_df[vendor_col], errors='coerce').notna().all():
                non_numeric_columns.append(vendor_col)
    return non_numeric_columns
