# comparator.py

from logger_config import logger


def normalize_employee_ids(ids: list[str]) -> list[str]:
    """
    Normalize employee IDs by removing decimals and converting to string.
    Ex: 1000.0 -> '1000'
    """
    try:
        return [str(int(float(emp_id))) for emp_id in ids]
    except Exception as e:
        logger.error(f"Error normalizing employee IDs: {e}")
        return []


def compare_employees(gtn_ids: list, payrun_ids: list) -> tuple:
    """
    Compares employee ID lists from GTN and Payrun.
    """
    try:
        gtn_ids_norm = set(normalize_employee_ids(gtn_ids))
        payrun_ids_norm = set(normalize_employee_ids(payrun_ids))

        missing_in_gtn = sorted(list(payrun_ids_norm - gtn_ids_norm))
        missing_in_payrun = sorted(list(gtn_ids_norm - payrun_ids_norm))

        logger.info("Employee comparison completed", extra={
            "missing_in_gtn": missing_in_gtn,
            "missing_in_payrun": missing_in_payrun
        })
        return missing_in_gtn, missing_in_payrun
    except Exception as e:
        logger.error("Error comparing employees", extra={"error": str(e)})
        return [], []


def compare_elements(gtn_elements: list[str], payrun_elements: list[str], mapping: dict) -> tuple:
    """
    Compare GTN and Payrun elements based on mapping.

    Returns:
        missing_in_gtn: elements from mapping that should be in GTN but are missing
        missing_in_payrun: elements from mapping that should be in Payrun but are missing
    """
    try:
        mapped_gtn_vendors = set(mapping['used'].keys())
        mapped_payrun_labels = set(mapping['used_reverse'].keys())

        gtn_elements_set = set(gtn_elements)
        payrun_elements_set = set(payrun_elements)

        missing_in_gtn = sorted(list(mapped_gtn_vendors - gtn_elements_set))
        missing_in_payrun = sorted(list(mapped_payrun_labels - payrun_elements_set))

        return missing_in_gtn, missing_in_payrun

    except Exception as e:
        logger.error(f"Error comparing elements: {e}")
        return [], []


if __name__ == "__main__":
    gtn = ['1000', '1001', '1002']
    payrun = ['1000.0', '1001.0', '1003.0']

    m1, m2 = compare_employees(gtn, payrun)
    logger.info("Missing in GTN: %s", m1)
    logger.info("Missing in Payrun: %s", m2)

    gtn_els = ['element1', 'element3', 'element4']
    payrun_els = ['Tax', 'Pension ER', 'Bonus']
    mock_mapping = {
        'used': {
            'element1': 'Tax',
            'element3': 'Pension ER',
            'element4': 'Bonus',
            'element6': 'Net Pay',
        },
        'used_reverse': {
            'Tax': 'element1',
            'Pension ER': 'element3',
            'Bonus': 'element4',
            'Net Pay': 'element6',
        }
    }

    mg, mp = compare_elements(gtn_els, payrun_els, mock_mapping)
    logger.info("Missing mapped GTN elements: %s", mg)
    logger.info("Missing mapped Payrun elements: %s", mp)
