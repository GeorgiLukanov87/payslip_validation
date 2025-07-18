def normalize_employee_ids(ids):
    """
    Normalize employee IDs by removing decimals and converting to string.
    Ex: 1000.0 -> '1000'
    """
    return [str(int(float(emp_id))) for emp_id in ids]


def compare_employees(gtn_ids, payrun_ids):
    """
    Compares employee ID lists from GTN and Payrun.

    Returns:
        missing_in_gtn: IDs present in Payrun but not in GTN
        missing_in_payrun: IDs present in GTN but not in Payrun
    """
    gtn_ids_norm = set(normalize_employee_ids(gtn_ids))
    payrun_ids_norm = set(normalize_employee_ids(payrun_ids))

    missing_in_gtn = sorted(list(payrun_ids_norm - gtn_ids_norm))
    missing_in_payrun = sorted(list(gtn_ids_norm - payrun_ids_norm))

    return missing_in_gtn, missing_in_payrun


if __name__ == "__main__":
    # test the function with example data
    gtn = ['1000', '1001', '1002']
    payrun = ['1000.0', '1001.0', '1003.0']

    m1, m2 = compare_employees(gtn, payrun)
    print("Missing in GTN:", m1)  # ['1003']
    print("Missing in Payrun:", m2)  # ['1002']
