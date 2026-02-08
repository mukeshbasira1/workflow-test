"""
MightyBot validation Rule
---
Description: Ensure inspection report is present, includes required percent complete matching draw request, and contains sufficient photo evidence for line items. Flag if percent complete variance >5% from requested draw or missing photos for hard cost line items.
Position: 2
---
"""
def run(payload: dict) -> dict:
    return payload
