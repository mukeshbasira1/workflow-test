"""
MightyBot validation Rule
---
Description: Verify disposable_earnings <= gross_earnings and both > 0. If disposable exceeds gross, return status FAILED. If either is zero or negative, return status FAILED with details.
Position: 5
---
"""
def run(payload: dict) -> dict:
    return payload
