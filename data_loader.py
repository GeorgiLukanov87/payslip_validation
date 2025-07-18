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


def get_payrun_data_from_row_2(filepath: str):
    df = pd.read_excel(filepath, sheet_name="Payrun file", header=1)
    df.columns = df.columns.str.strip()

    valid_cols = get_payrun_elements_from_row_2(filepath)
    df = df[valid_cols]

    return df


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

    payrun_data = get_payrun_data_from_row_2(payrun_path_str)
    print("\nSample payrun data:")
    print(payrun_data.head())
    print(payrun_data.info())

"""
GTN count: 36 
employee_ids:  
    [
    '1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', 
    '1010', '1011', '1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023', 
    '1024', '1025', '1026', '1027', '1028', '1029', '1030', '1031', '1032', '1033', '1034', '1035'
    ] # type is str!

Payrun count: 36 
employee_ids:  
    [
    '1000.0', '1001.0', '1002.0', '1003.0', '1004.0', '1005.0', '1006.0', '1007.0', '1008.0', '1009.0', 
    '1010.0', '1011.0', '1012.0', '1013.0', '1014.0', '1015.0', '1016.0', '1017.0', '1018.0', '1019.0', '1020.0', 
    '1021.0', '1022.0', '1023.0', '1024.0', '1025.0', '1026.0', '1027.0', '1028.0', '1029.0', '1030.0', '1031.0', 
    '1032.0', '1033.0', '1034.0', '1035.0'
    ] # type is float!

GTN elements: 
[
    'salary', 'element1', 'element2', 'element3', 'element4', 'element5', 'element6', 'element7', 
    'element8', 'element9', 'element10'] Payrun elements from row 2: ['Basic Pay / SalaryUK', 'BIK Health', 'BIK Company 
    Car', 'Bonus', 'Enhanced AL', 'Add pay (Stay Overs)', 'Backpay', 'Holiday Pay / Holiday pay', 'BIK Voucher Payment', 
    'Commission', 'Statutory Redundancy', 'PILON', 'Enhanced Annual Leave', 'Regular Overtime', 'Tax', 'National 
    Insurance EE', 'Post Tax Pension EE', 'Student Loan', 'Advance', 'BIK Health Deduction / BIK Health', 'BIK Voucher 
    Deduction', 'National Insurance ER', 'Pension ER'
]

Sample payrun data:
   Basic Pay / SalaryUK  BIK Health  ...  National Insurance ER  Pension ER
0               3277.67       52.23  ...                    NaN         NaN
1               2525.50         NaN  ...                    NaN         NaN
2               6166.67       65.39  ...                    NaN         NaN
3               2250.00         NaN  ...                    NaN         NaN
4               2619.58         NaN  ...                    NaN         NaN

[5 rows x 23 columns]

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 37 entries, 0 to 36
Data columns (total 23 columns):
 #   Column                             Non-Null Count  Dtype  
---  ------                             --------------  -----  
 0   Basic Pay / SalaryUK               37 non-null     float64
 1   BIK Health                         9 non-null      float64
 2   BIK Company Car                    3 non-null      float64
 3   Bonus                              1 non-null      float64
 4   Enhanced AL                        1 non-null      float64
 5   Add pay (Stay Overs)               1 non-null      float64
 6   Backpay                            3 non-null      float64
 7   Holiday Pay / Holiday pay          1 non-null      float64
 8   BIK Voucher Payment                1 non-null      float64
 9   Commission                         3 non-null      float64
 10  Statutory Redundancy               1 non-null      float64
 11  PILON                              1 non-null      float64
 12  Enhanced Annual Leave              1 non-null      float64
 13  Regular Overtime                   1 non-null      float64
 14  Tax                                1 non-null      float64
 15  National Insurance EE              1 non-null      float64
 16  Post Tax Pension EE                1 non-null      float64
 17  Student Loan                       1 non-null      float64
 18  Advance                            2 non-null      float64
 19  BIK Health Deduction / BIK Health  9 non-null      float64
 20  BIK Voucher Deduction              1 non-null      float64
 21  National Insurance ER              1 non-null      float64
 22  Pension ER                         1 non-null      float64
dtypes: float64(23)
memory usage: 6.8 KB
"""
