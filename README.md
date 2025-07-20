# Payslip Validation

This project provides a framework for validating consistency between two Excel-based payroll data sources: `GTN.xlsx` and `Payrun.xlsx`. A third file, `mapping.json`, defines how pay elements should be aligned between the two files.

## 📁 Project Structure
```
├── main.py                   # Entry point
├── data_loader.py            # Data loading utilities
├── comparator.py             # Employee ID and pay element comparison logic
├── mapping_loader.py         # JSON mapping parser
├── validators/               # Validation logic for specific rules
├── tests/                    # Automated tests with Pytest
├── tests/data_case_*/        # Test cases with sample input data
```

## ✅ Validation Scenarios
1. The input file is a valid Excel file
2. The GTN file contains empty rows
3. The GTN file has multiple header rows
4. Some employees in Payrun are missing in GTN
5. Some employees in GTN are missing in Payrun
6. Some GTN pay elements are not mapped
7. Some Payrun pay elements are not mapped
8. Mapped GTN pay elements must contain numeric values

## 🧪 Running Tests
```bash
pytest tests/
```

## 🚀 How to Clone and Run
1. Clone the repository:
```bash
git clone https://github.com/GeorgiLukanov87/payslip_validation.git
cd payslip-validation
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run all tests:
```bash
pytest tests/
```

## 📦 Requirements
```
pandas
openpyxl
pytest
```

## ℹ️ Notes
- Each validation test is backed by a dataset under `tests/data_case_*`
- The validation logic is modular and easy to extend
- The `validators/` folder contains reusable rule-based checks

