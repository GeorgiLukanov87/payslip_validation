# tests/test_unmapped_gtn_elements.py

import os
import sys
import pytest
import pandas as pd
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapping_loader import load_mapping


def get_gtn_elements(df: pd.DataFrame):
    return df.columns[4:].tolist()  # pay elements start from column E (index 4)


@pytest.mark.parametrize("case_path", [
    "tests/data_case_valid",
    "tests/data_case_06_unmapped_gtn_elements"
])
def test_gtn_elements_mapped_to_payrun(case_path):
    gtn_path = os.path.join(case_path, "GTN.xlsx")
    mapping_path = os.path.join(case_path, "mapping.json")

    gtn_df = pd.read_excel(gtn_path, engine='openpyxl')
    mapping = load_mapping(mapping_path)

    gtn_elements = get_gtn_elements(gtn_df)
    mapped_gtn_vendors = set(mapping['used'].keys())
    ignored_vendors = set(mapping['not_used'])

    # Elements that exist in GTN but are not mapped and not ignored
    unmapped = [el for el in gtn_elements if el not in mapped_gtn_vendors and el not in ignored_vendors]

    assert not unmapped, f"GTN contains unmapped elements that are not declared in mapping.json: {unmapped}"
