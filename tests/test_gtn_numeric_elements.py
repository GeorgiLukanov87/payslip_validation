import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapping_loader import load_mapping
from validators.gtn_validators import check_gtn_numeric_elements


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_08_non_numeric_gtn_values"
])
def test_gtn_elements_are_numeric(case_path):
    gtn_path = os.path.join(case_path, "GTN.xlsx")
    mapping_path = os.path.join(case_path, "mapping.json")

    gtn_df = pd.read_excel(gtn_path, engine="openpyxl")
    mapping = load_mapping(mapping_path)

    non_numeric_columns = check_gtn_numeric_elements(gtn_df, mapping)

    assert not non_numeric_columns, f"GTN columns with non-numeric values: {non_numeric_columns}"
