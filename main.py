# main.py

from pathlib import Path
from mapping_loader import load_mapping
from data_loader import (
    load_gtn_excel,
    load_payrun_excel,
    extract_employee_ids,
    get_gtn_elements,
    get_combined_payrun_elements,
    get_final_payrun_target_columns
)
from comparator import compare_employees, compare_elements
from validators.gtn_validators import check_gtn_numeric_elements


def main():
    gtn_path = Path("data/GTN.xlsx")
    payrun_path = Path("data/Payrun.xlsx")
    mapping_path = Path("data/mapping.json")

    mapping = load_mapping(mapping_path)
    gtn_df = load_gtn_excel(gtn_path)
    payrun_df = load_payrun_excel(str(payrun_path))

    gtn_ids = extract_employee_ids(gtn_df, "employee_id")
    payrun_ids = extract_employee_ids(payrun_df, "Employee ID")

    missing_in_gtn, missing_in_payrun = compare_employees(gtn_ids, payrun_ids)
    print("\n--- Employee ID Comparison ---")
    print("Missing in GTN:", missing_in_gtn)
    print("Missing in Payrun:", missing_in_payrun)

    gtn_elements = get_gtn_elements(gtn_df)
    payrun_elements = get_combined_payrun_elements(str(payrun_path))

    missing_gtn_elements, missing_payrun_elements = compare_elements(
        gtn_elements, payrun_elements, mapping
    )
    print("\n--- Pay Element Comparison ---")
    print("Missing mapped GTN elements:", missing_gtn_elements)
    print("Missing mapped Payrun elements:", missing_payrun_elements)

    target_columns_df = get_final_payrun_target_columns(str(payrun_path), mapping)
    print("\n--- Mapped Payrun Data (target columns) ---")
    print(target_columns_df.columns)
    print(target_columns_df.head())

    non_numeric = check_gtn_numeric_elements(gtn_df, mapping)
    print("\n--- GTN Numeric Value Check ---")
    if non_numeric:
        print("Non-numeric values found in columns:", non_numeric)
    else:
        print("All mapped GTN element columns are numeric.")


if __name__ == "__main__":
    main()
