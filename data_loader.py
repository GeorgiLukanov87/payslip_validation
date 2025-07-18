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


def get_payrun_elements(df):
    return df.columns[25:].tolist()  # from column Z


if __name__ == "__main__":
    gtn_path = Path("data/GTN.xlsx")
    payrun_path = Path("data/Payrun.xlsx")

    gtn_df = load_gtn_excel(gtn_path)
    payrun_df = load_payrun_excel(payrun_path)

    print("GTN employee_ids:", extract_employee_ids(gtn_df, "employee_id"))
    print("Payrun employee_ids:", extract_employee_ids(payrun_df, "Employee_ID"))

    print("GTN elements:", get_gtn_elements(gtn_df))
    print("Payrun elements:", get_payrun_elements(payrun_df))
