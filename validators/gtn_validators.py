# validators/gtn_validators.py

import pandas as pd
from logger_config import logger


def check_gtn_numeric_elements(gtn_df: pd.DataFrame, mapping: dict) -> list:
    """
    Check that all mapped GTN element columns contain numeric values.
    """
    non_numeric_columns = []
    for vendor_col in mapping['used'].keys():
        if vendor_col in gtn_df.columns:
            non_numeric_rows = gtn_df[~pd.to_numeric(gtn_df[vendor_col], errors='coerce').notna()]
            if not non_numeric_rows.empty:
                logger.warning("Non-numeric values found", extra={
                    "column": vendor_col,
                    "row_count": len(non_numeric_rows)
                })
                non_numeric_columns.append(vendor_col)
    logger.info("GTN numeric validation completed", extra={"non_numeric_columns": non_numeric_columns})
    return non_numeric_columns
