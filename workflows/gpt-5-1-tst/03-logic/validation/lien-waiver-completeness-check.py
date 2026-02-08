"""
MightyBot validation Rule
---
Description: Verify that all required lien waivers for the current draw period are present and match the invoice amounts from the submitted documents. Cross-reference vendor names, amounts, and dates against the invoice log and pay application. If any waiver is missing, expired, or does not match (e.g., amount discrepancy >5%), flag as failed with details on missing/mismatched items.
Position: 0
---
"""
def run(payload: dict) -> dict:
    return payload
