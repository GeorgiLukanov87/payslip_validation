# mapping_loader.py

import json
from pathlib import Path


def update_mapping_dict(mapping_dict):
    # update mapping_dict "element2": "BIKHealth" to "BIK Health" in used
    mapping_dict['used'] = {k: v.replace('BIKHealth', 'BIK Health') for k, v in mapping_dict['used'].items()}

    # update mapping_dict "BIK Health": "element2" to "BIK Health" in used_reverse
    mapping_dict['used_reverse'] = {k.replace('BIKHealth', 'BIK Health'): v for k, v in
                                    mapping_dict['used_reverse'].items()}


def load_mapping(mapping_path) -> dict:
    try:
        """
        Load and parse the mapping.json file.
        Returns:
            dict: with keys 'mappings', 'not_used'
        """
        with open(mapping_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        used_mappings = data.get('mappings', {})
        not_used = data.get('not_used', [])

        # Create a dictionary for used mappings
        mapping_dict = {'used': {v['vendor']: k for k, v in used_mappings.items() if v.get('map')},
                        'used_reverse': {k: v['vendor'] for k, v in used_mappings.items() if v.get('map')},
                        'not_used': [x['vendor'] for x in not_used]}
        update_mapping_dict(mapping_dict)
        return mapping_dict

    except Exception as e:
        print(f"Error loading mapping file: {e}")
        return {}


if __name__ == "__main__":
    path = Path('data/mapping.json')
    mappings = load_mapping(path)
    print(json.dumps(mappings, indent=2))

""" 
mapping_dict = 
{
  "used": {
    "salary": "Basic Pay / SalaryUK",
    "element1": "Tax",
    "element2": "BIK Health",
    "element3": "Pension ER",
    "element4": "Bonus",
    "element5": "BIK Voucher Payment",
    "element6": "Net Pay",
    "element7": "Gross Pay",
    "element9": "Backpay",
    "element10": "Total Employer Cost"
  },
  "used_reverse": {
    "Basic Pay / SalaryUK": "salary",
    "BIK Health": "element2",
    "Bonus": "element4",
    "Backpay": "element9",
    "BIK Voucher Payment": "element5",
    "Gross Pay": "element7",
    "Tax": "element1",
    "Net Pay": "element6",
    "Pension ER": "element3",
    "Total Employer Cost": "element10"
  },
  "not_used": [
    "element8"
  ]
}
"""
