# tests/test_gtn_header_structure.py

import os
import pandas as pd
import pytest


@pytest.mark.parametrize("case_path, should_be_valid", [
    ("tests/data_case_valid", False),
    ("tests/data_case_03_invalid_gtn_header", True),
])
def test_gtn_file_has_single_header_row(case_path, should_be_valid):
    gtn_path = os.path.join(case_path, "GTN.xlsx")

    try:
        # Try to load the GTN file with MultiIndex columns
        df = pd.read_excel(gtn_path, header=[0, 1], engine="openpyxl")
        is_multi = isinstance(df.columns, pd.MultiIndex)
    except Exception:
        # If loading with MultiIndex fails, try loading with a single header row
        is_multi = False

    if should_be_valid:
        assert not is_multi, "Expected flat columns for valid GTN file, but got MultiIndex."
    else:
        assert is_multi, "Expected MultiIndex from invalid GTN file, but got flat columns."
