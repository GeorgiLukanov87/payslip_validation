import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from comparator import compare_employees


def extract_employee_ids(df: pd.DataFrame, col_name: str):
    if col_name not in df.columns:
        raise KeyError(f"Missing column '{col_name}' in file. Available columns: {list(df.columns)}")
    return df[col_name].dropna().astype(str).unique().tolist()


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_05_missing_in_payrun"
])
def test_employees_in_gtn_exist_in_payrun(case_path):
    gtn_path = os.path.join(case_path, "GTN.xlsx")
    payrun_path = os.path.join(case_path, "Payrun.xlsx")

    gtn_df = pd.read_excel(gtn_path, engine='openpyxl')
    payrun_df = pd.read_excel(payrun_path, sheet_name="Payrun file", header=0, engine='openpyxl')

    gtn_ids = extract_employee_ids(gtn_df, "employee_id")
    payrun_ids = extract_employee_ids(payrun_df, "Employee ID")

    _, missing_in_payrun = compare_employees(gtn_ids, payrun_ids)

    assert not missing_in_payrun, f"The following Employee IDs are in GTN but missing in Payrun: {missing_in_payrun}"
