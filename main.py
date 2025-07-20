# main.py

from pathlib import Path

from logger_config import logger
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
    try:
        gtn_path = Path("data/GTN.xlsx")
        payrun_path = Path("data/Payrun.xlsx")
        mapping_path = Path("data/mapping.json")

        mapping = load_mapping(mapping_path)
        gtn_df = load_gtn_excel(gtn_path)
        payrun_df = load_payrun_excel(str(payrun_path))

        gtn_ids = extract_employee_ids(gtn_df, "employee_id")
        payrun_ids = extract_employee_ids(payrun_df, "Employee ID")

        missing_in_gtn, missing_in_payrun = compare_employees(gtn_ids, payrun_ids)
        logger.info("\n--- Employee ID Comparison ---")
        logger.info("Missing in GTN: %s", missing_in_gtn)
        logger.info("Missing in Payrun: %s", missing_in_payrun)

        gtn_elements = get_gtn_elements(gtn_df)
        payrun_elements = get_combined_payrun_elements(str(payrun_path))

        missing_gtn_elements, missing_payrun_elements = compare_elements(
            gtn_elements, payrun_elements, mapping
        )
        logger.info("\n--- Pay Element Comparison ---")
        logger.info("Missing mapped GTN elements: %s", missing_gtn_elements)
        logger.info("Missing mapped Payrun elements: %s", missing_payrun_elements)

        target_columns_df = get_final_payrun_target_columns(str(payrun_path), mapping)
        logger.info("\n--- Mapped Payrun Data (target columns) ---")
        logger.info("Columns: %s", target_columns_df.columns.tolist())
        logger.info("Sample data:\n%s", target_columns_df.head())

        non_numeric = check_gtn_numeric_elements(gtn_df, mapping)
        logger.info("\n--- GTN Numeric Value Check ---")
        if non_numeric:
            logger.warning("Non-numeric values found in columns: %s", non_numeric)
        else:
            logger.info("All mapped GTN element columns are numeric.")

    except Exception as e:
        logger.error(f"Fatal error in main(): {e}")


if __name__ == "__main__":
    main()
