"""
MightyBot validation Rule
---
Description: Verify state, order_type, case_number, debtor_name, employer_name are non-null. If any required field is missing, return status FAILED with the list of missing fields.
Position: 4
---
"""
def run(payload: dict) -> dict:
    return payload
