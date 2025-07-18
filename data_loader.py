import pandas as pd
from pathlib import Path


def load_gtn_excel(path):
    """
    Load GTN Excel file and return as DataFrame.
    Assumes pay elements start at column index 4 (i.e., column E).
    """
    df = pd.read_excel(path, engine='openpyxl')
    df.columns = df.columns.str.strip()
    return df


def load_payrun_excel(path):
    """
    Load Payrun Excel file and return as DataFrame.
    Assumes pay elements start at column index 25 (i.e., column Z).
    """
    df = pd.read_excel(path, engine='openpyxl')
    df.columns = df.columns.str.strip()
    return df


def extract_employee_ids(df, col_name):
    """
    Extracts employee IDs from given column.
    """
    return df[col_name].dropna().astype(str).unique().tolist()


def get_gtn_elements(df):
    return df.columns[4:].tolist()  # from column E


def get_payrun_elements_from_row_2(filepath: str):  # from column Z2
    df = pd.read_excel(filepath, sheet_name="Payrun file", header=1)
    df.columns = df.columns.str.strip()

    all_cols = df.columns.tolist()
    valid_cols = [col for col in all_cols[25:] if not col.startswith("Unnamed")]

    return valid_cols


if __name__ == "__main__":
    gtn_path = Path("data/GTN.xlsx")
    payrun_path = Path("data/Payrun.xlsx")
    payrun_path_str = "data/Payrun.xlsx"

    gtn_df = load_gtn_excel(gtn_path)
    payrun_df = load_payrun_excel(payrun_path)

    gtn_employee_ids = extract_employee_ids(gtn_df, 'employee_id')
    payrun_employee_ids = extract_employee_ids(payrun_df, 'Employee ID')

    print(f"GTN count: {len(gtn_employee_ids)} \n employee_ids: ", gtn_employee_ids)
    print(f"Payrun count: {len(payrun_employee_ids)} \n employee_ids: ", payrun_employee_ids)

    print("\nGTN elements:", get_gtn_elements(gtn_df))
    print("Payrun elements from row 2:", get_payrun_elements_from_row_2(payrun_path_str))
