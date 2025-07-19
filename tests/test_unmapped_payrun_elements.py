import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapping_loader import load_mapping


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_07_unmapped_payrun_elements"
])
def test_pay_elements_have_mapping(case_path):
    payrun_path = os.path.join(case_path, "Payrun.xlsx")
    mapping_path = os.path.join(case_path, "mapping.json")

    # Read raw first 2 rows (no header) to find position of 'Pay elements'
    raw = pd.read_excel(payrun_path, sheet_name="Payrun file", header=None, nrows=2, engine="openpyxl")
    pay_elements_start_col = None
    for idx, val in enumerate(raw.iloc[0]):
        if isinstance(val, str) and val.strip().lower() == "pay elements":
            pay_elements_start_col = idx + 1
            break

    assert pay_elements_start_col is not None, "Could not detect start of Pay elements block."

    # Now read with proper header row (row 1)
    df = pd.read_excel(payrun_path, sheet_name="Payrun file", header=1, engine="openpyxl")
    mapping = load_mapping(mapping_path)
    mapped_labels = set(mapping['used_reverse'].keys())

    pay_element_columns = df.columns[pay_elements_start_col:]
    print(pay_element_columns)
    unmapped = [col for col in pay_element_columns if col not in mapped_labels]

    assert not unmapped, f"Unmapped Pay elements found in Payrun: {unmapped}"
