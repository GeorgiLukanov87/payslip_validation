# data_loader.py

import pandas as pd
from pathlib import Path
from pandas import DataFrame
from logger_config import logger

GTN_PAY_ELEMENTS_START_INDEX = 4
PAYRUN_ELEMENTS_START_INDEX = 25


def load_gtn_excel(path: Path) -> pd.DataFrame:
    """
    Load GTN Excel file and return as DataFrame.
    Assumes pay elements start at column index 4 (i.e., column E).
    """
    try:
        if not path.exists():
            logger.error(f"GTN file not found at path: {path}")
            return pd.DataFrame()
        df = pd.read_excel(path, engine='openpyxl')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        logger.error(f"Error loading GTN Excel file: {e}")
        return pd.DataFrame()


def load_payrun_excel(path: str) -> pd.DataFrame:
    """
    Load Payrun Excel file and return as DataFrame.
    Assumes pay elements start at column index 25 (i.e., column Z).
    """
    try:
        if not Path(path).exists():
            logger.error(f"Payrun file not found at path: {path}")
            return pd.DataFrame()
        df = pd.read_excel(path, engine='openpyxl')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        logger.error(f"Error loading Payrun Excel file: {e}")
        return pd.DataFrame()


def extract_employee_ids(df: DataFrame, col_name: str) -> list:
    """
    Extracts employee IDs from given column.
    """
    try:
        if col_name not in df.columns:
            logger.warning(f"Column '{col_name}' not found in DataFrame.")
            return []
        return df[col_name].dropna().astype(str).unique().tolist()
    except Exception as e:
        logger.error(f"Error extracting employee IDs: {e}")
        return []


def get_gtn_elements(df: DataFrame) -> list:
    try:
        if df.empty or len(df.columns) < GTN_PAY_ELEMENTS_START_INDEX + 1:
            logger.warning("GTN DataFrame is empty or has insufficient columns.")
            return []
        return df.columns[GTN_PAY_ELEMENTS_START_INDEX:].tolist()  # from column E
    except Exception as e:
        logger.error(f"Error getting GTN elements: {e}")
        return []


def get_payrun_elements_from_row_2(filepath: str) -> list:  # from column Z2
    try:
        if not Path(filepath).exists():
            logger.error(f"Payrun file not found at path: {filepath}")
            return []
        df = pd.read_excel(filepath, sheet_name="Payrun file", header=1)
        df.columns = df.columns.str.strip()
        all_cols = df.columns.tolist()
        return [col for col in all_cols[PAYRUN_ELEMENTS_START_INDEX:] if not col.startswith("Unnamed")]
    except Exception as e:
        logger.error(f"Error getting payrun elements from row 2: {e}")
        return []


def get_combined_payrun_elements(filepath: str) -> list:
    """
    Combine payrun elements from both header=0 and header=1
    to include all valid pay elements (e.g., Net Pay, Gross Pay).
    """
    try:
        if not Path(filepath).exists():
            logger.error(f"Payrun file not found at path: {filepath}")
            return []
        df0 = pd.read_excel(filepath, sheet_name="Payrun file", header=0)
        df1 = pd.read_excel(filepath, sheet_name="Payrun file", header=1)

        cols0 = [col.strip() for col in df0.columns if not str(col).startswith("Unnamed")]
        cols1 = [col.strip() for col in df1.columns if not str(col).startswith("Unnamed")]

        return sorted(set(cols0 + cols1))
    except Exception as e:
        logger.error(f"Error combining payrun elements: {e}")
        return []


def get_complete_mapped_payrun_data(filepath: str, extra_columns: list) -> pd.DataFrame:
    """
    Load Payrun data and combine columns from header=1 and header=0
    and return as DataFrame.
    """
    try:
        if not Path(filepath).exists():
            logger.error(f"Payrun file not found at path: {filepath}")
            return pd.DataFrame()
        df_main = pd.read_excel(filepath, sheet_name="Payrun file", header=1)
        df_main.columns = df_main.columns.str.strip()
        valid_cols = get_payrun_elements_from_row_2(filepath)
        df_main = df_main[valid_cols]

        df_header0 = pd.read_excel(filepath, sheet_name="Payrun file", header=0)
        df_header0.columns = df_header0.columns.str.strip()
        existing_extras = [col for col in extra_columns if col in df_header0.columns]
        df_extras = df_header0[existing_extras]

        df_combined = pd.concat([df_main, df_extras], axis=1)
        return df_combined

    except Exception as e:
        logger.error(f"Error getting complete mapped payrun data: {e}")
        return pd.DataFrame()


def get_payrun_data_from_row_2(filepath: str) -> pd.DataFrame:
    try:
        if not Path(filepath).exists():
            logger.error(f"Payrun file not found at path: {filepath}")
            return pd.DataFrame()
        df = pd.read_excel(filepath, sheet_name="Payrun file", header=1)
        df.columns = df.columns.str.strip()
        valid_cols = get_payrun_elements_from_row_2(filepath)
        df = df[valid_cols]
        return df

    except Exception as e:
        logger.error(f"Error getting payrun data from row 2: {e}")
        return pd.DataFrame()


def get_final_payrun_target_columns(filepath: str, mapping: dict) -> pd.DataFrame:
    try:
        if not Path(filepath).exists():
            logger.error(f"Payrun file not found at path: {filepath}")
            return pd.DataFrame()
        mapped_labels = list(mapping['used_reverse'].keys())
        special_cols = [col for col in mapped_labels if col in ["Net Pay", "Gross Pay", "Total Employer Cost"]]
        df = get_complete_mapped_payrun_data(filepath, special_cols)

        final_cols = [col for col in [
            'Net Pay', 'Tax', 'Pension ER', 'Gross Pay', 'BIK Voucher Payment', 'Basic Pay / SalaryUK',
            'BIK Health', 'Bonus', 'Backpay', 'Total Employer Cost'
        ] if col in df.columns]
        return df[final_cols]

    except Exception as e:
        logger.error(f"Error getting final payrun target columns: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    gtn_path = Path("data/GTN.xlsx")
    payrun_path = Path("data/Payrun.xlsx")
    payrun_path_str = "data/Payrun.xlsx"

    gtn_df = load_gtn_excel(gtn_path)
    payrun_df = load_payrun_excel(payrun_path_str)

    gtn_employee_ids = extract_employee_ids(gtn_df, 'employee_id')
    payrun_employee_ids = extract_employee_ids(payrun_df, 'Employee ID')

    logger.info(f"GTN count: {len(gtn_employee_ids)} \n employee_ids: {gtn_employee_ids}")
    logger.info(f"Payrun count: {len(payrun_employee_ids)} \n employee_ids: {payrun_employee_ids}")

    logger.info("\nGTN elements: %s", get_gtn_elements(gtn_df))
    logger.info("Payrun elements (combined): %s", get_combined_payrun_elements(payrun_path_str))

    payrun_data = get_payrun_data_from_row_2(payrun_path_str)
    logger.info("\nSample payrun data:\n%s", payrun_data.head())

"""
GTN count: 36
employee_ids:  
 [
     '1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', 
    '1010', '1011', '1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023', 
    '1024', '1025', '1026', '1027', '1028', '1029', '1030', '1031', '1032', '1033', '1034', '1035'
] 

Payrun count: 36 
employee_ids:  
[
    '1000.0', '1001.0', '1002.0', '1003.0', '1004.0', '1005.0', '1006.0', '1007.0', '1008.0', '1009.0', 
    '1010.0', '1011.0', '1012.0', '1013.0', '1014.0', '1015.0', '1016.0', '1017.0', '1018.0', '1019.0', '1020.0', 
    '1021.0', '1022.0', '1023.0', '1024.0', '1025.0', '1026.0', '1027.0', '1028.0', '1029.0', '1030.0', '1031.0', 
    '1032.0', '1033.0', '1034.0', '1035.0'
]

GTN elements: 
[
    'salary', 'element1', 'element2', 'element3', 'element4', 'element5', 'element6', 'element7', 
    'element8', 'element9', 'element10'
]

Payrun elements combined from row 1 and 2: 
[ 'Add pay (Stay Overs)', 'Advance', 'Annual Salary', 'BIK Company Car', 
'BIK Health', 'BIK Health Deduction / BIK Health', 'BIK Voucher Deduction', 'BIK Voucher Payment', 'Backpay', 
'Basic Pay / SalaryUK', 'Bonus', 'Business Unit', 'Commission', 'Company', 'Company Code', 'Cost Center', 'Country', 
'Currency', 'Department', 'Effective Date', 'Employee Deductions', 'Employee ID', 'Employee Net Deductions', 
'Employer Contributions', 'End Date', 'Enhanced AL', 'Enhanced Annual Leave', 'First Name', 'From Date', 'Gross Pay', 
'Holiday Pay / Holiday pay', 'Last Name', 'Management P&L', 'National Insurance EE', 'National Insurance ER', 
'Net Income', 'Net Pay', 'Ni Category Letter', 'Notes', 'Other Employee ID', 'Overtime', 'PILON', 'Pay Date', 
'Pay elements', 'Paygroup', 'Payment Type', 'Payroll', 'Pension ER', 'Post Tax Pension EE', 'Regular Overtime', 
'Start Date', 'Statutory Redundancy', 'Student Loan', 'System Employee ID', 'Tax', 'Tax Code', 'Time and Attendance', 
'To Date', 'Total Employer Cost', 'Total Taxable Income' ]
"""
