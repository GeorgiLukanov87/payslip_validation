# tests/test_file_type.py

import os
import pytest
import pandas as pd


def is_excel_file(filepath):
    return filepath.endswith('.xlsx')


def can_open_excel(filepath):
    try:
        pd.read_excel(filepath, engine='openpyxl')
        return True
    except Exception:
        return False


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_01_invalid_filetype"
])
def test_file_types(case_path):
    gtn_path = os.path.join(case_path, "GTN.xlsx")  # assume default expected name
    payrun_path = os.path.join(case_path, "Payrun.xlsx")

    errors = []

    if not is_excel_file(gtn_path):
        errors.append("GTN file is not .xlsx")
    elif not can_open_excel(gtn_path):
        errors.append("GTN file cannot be opened as Excel")

    if not is_excel_file(payrun_path):
        errors.append("Payrun file is not .xlsx")
    elif not can_open_excel(payrun_path):
        errors.append("Payrun file cannot be opened as Excel")

    assert not errors, f"File validation errors: {errors}"
