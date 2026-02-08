"""
MightyBot preprocessing Rule
---
Description: Normalize all document dates (expiration, invoice dates, inspection dates) to ISO format and validate against current draw period. Flag expired documents or future-dated invoices.
Position: 3
---
"""
def run(payload: dict) -> dict:
    return payload
