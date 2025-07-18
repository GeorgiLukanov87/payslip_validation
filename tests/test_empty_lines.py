# tests/test_empty_lines.py

import os
import pytest
import pandas as pd


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_02_gtn_with_empty_rows"
])
def test_gtn_file_has_no_empty_rows(case_path):
    gtn_path = os.path.join(case_path, "GTN.xlsx")

    df = pd.read_excel(gtn_path, engine='openpyxl')
    empty_rows = df[df.isna().all(axis=1)]

    assert empty_rows.empty, f"GTN file contains empty rows at indices: {empty_rows.index.tolist()}"
