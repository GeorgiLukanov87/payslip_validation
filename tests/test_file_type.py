import os
import pytest
import pandas as pd
import json


def is_excel_file(filepath):
    return filepath.endswith('.xlsx')


def is_json_file(filepath):
    return filepath.endswith('.json')


def can_open_excel(filepath):
    try:
        pd.read_excel(filepath, engine='openpyxl')
        return True
    except Exception:
        return False


def can_open_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
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
    mapping_path = os.path.join(case_path, "mapping.json")

    errors = []

    if not is_excel_file(gtn_path):
        errors.append("GTN file is not .xlsx")
    elif not can_open_excel(gtn_path):
        errors.append("GTN file cannot be opened as Excel")

    if not is_excel_file(payrun_path):
        errors.append("Payrun file is not .xlsx")
    elif not can_open_excel(payrun_path):
        errors.append("Payrun file cannot be opened as Excel")

    if not is_json_file(mapping_path):
        errors.append("Mapping file is not .json")
    elif not can_open_json(mapping_path):
        errors.append("Mapping file cannot be parsed as JSON")

    assert not errors, f"File validation errors: {errors}"
