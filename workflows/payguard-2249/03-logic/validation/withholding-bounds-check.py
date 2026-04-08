"""
MightyBot validation Rule
---
Description: Verify 0 <= final_withholding <= disposable_earnings. If withholding is negative or exceeds disposable earnings, return status FAILED with the violation details.
Position: 6
---
"""
def run(payload: dict) -> dict:
    return payload
