import json
from pathlib import Path


def load_mapping(mapping_path):
    """
    Load and parse the mapping.json file.
    Returns:
        dict: with keys 'mappings', 'not_used', and others for future use.
    """
    with open(mapping_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    used_mappings = data.get('mappings', {})
    not_used = data.get('not_used', [])

    # Flatten the vendor field for easier comparison later
    mapping_dict = {
        'used': {v['vendor']: k for k, v in used_mappings.items() if v.get('map')},
        'used_reverse': {k: v['vendor'] for k, v in used_mappings.items() if v.get('map')},
        'not_used': [x['vendor'] for x in not_used]
    }
    return mapping_dict


if __name__ == "__main__":
    path = Path('data/mapping.json')
    mappings = load_mapping(path)
    print(json.dumps(mappings, indent=2))

"""
{
  "used": {
    "element6": "Net Pay",
    "element1": "Tax",
    "element3": "Pension ER",
    "element7": "Gross Pay",
    "element5": "BIK Voucher Payment",
    "salary": "Basic Pay / SalaryUK",
    "element2": "BIKHealth",
    "element4": "Bonus",
    "element9": "Backpay",
    "element10": "Total Employer Cost"
  },
  "used_reverse": {
    "Net Pay": "element6",
    "Tax": "element1",
    "Pension ER": "element3",
    "Gross Pay": "element7",
    "BIK Voucher Payment": "element5",
    "Basic Pay / SalaryUK": "salary",
    "BIKHealth": "element2",
    "Bonus": "element4",
    "Backpay": "element9",
    "Total Employer Cost": "element10"
  },
  "not_used": [
    "element8"
  ]
}
"""
