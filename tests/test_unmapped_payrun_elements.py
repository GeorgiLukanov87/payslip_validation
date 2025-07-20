# tests/test_unmapped_payrun_elements.py

import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapping_loader import load_mapping

IGNORE_LIST = {
    'BIK Company Car', 'Enhanced AL', 'Holiday Pay / Holiday pay',
    'Commission', 'Statutory Redundancy', 'PILON', 'Add pay (Stay Overs)',
    'Enhanced Annual Leave', 'Regular Overtime', 'Advance', 'National Insurance ER',
    'BIK Health Deduction / BIK Health', 'BIK Voucher Deduction',
    'Post Tax Pension EE', 'National Insurance EE', 'Student Loan',
    'Notes', 'Department', 'Currency', 'Cost Center', 'Payroll',
    'Unnamed'  # wildcard to match any unnamed columns
}


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_07_unmapped_payrun_elements"
])
def test_pay_elements_have_mapping(case_path):
    payrun_path = os.path.join(case_path, "Payrun.xlsx")
    mapping_path = os.path.join(case_path, "mapping.json")

    # Step 1: Detect "Pay elements" header position
    raw = pd.read_excel(payrun_path, sheet_name="Payrun file", header=None, nrows=2, engine="openpyxl")
    pay_elements_start_col = None
    for idx, val in enumerate(raw.iloc[0]):
        if isinstance(val, str) and val.strip().lower() == "pay elements":
            pay_elements_start_col = idx + 1
            break

    assert pay_elements_start_col is not None, "Could not detect start of Pay elements block."

    # Step 2: Load columns and mapping
    df = pd.read_excel(payrun_path, sheet_name="Payrun file", header=1, engine="openpyxl")
    mapping = load_mapping(mapping_path)
    mapped_labels = set(mapping['used_reverse'].keys())

    # Step 3: Validate all pay element columns
    pay_element_columns = df.columns[pay_elements_start_col:]
    unmapped = []
    for col in pay_element_columns:
        if col in mapped_labels:
            continue
        if any(col.startswith(prefix) for prefix in IGNORE_LIST):
            continue
        if col.startswith("Unnamed:"):
            continue
        unmapped.append(col)

    assert not unmapped, f"Unmapped Pay elements found in Payrun: {unmapped}"
