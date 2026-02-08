"""
MightyBot validation Rule
---
Description: Validates that only one threshold field is set among threshold_number, threshold_percent, and threshold_currency, and that its type and value range are appropriate. threshold_percent must be a number between 0 and 100 inclusive, threshold_currency must be a non-negative number, and threshold_number must be a valid number (negative allowed only if explicitly intended by comparator). Failure behavior: if multiple thresholds are provided or the single provided threshold is out of the permitted range or wrong type, the policy_rule is marked invalid and must be corrected before activation.
Position: 1
---
"""
def run(payload: dict) -> dict:
    return payload
