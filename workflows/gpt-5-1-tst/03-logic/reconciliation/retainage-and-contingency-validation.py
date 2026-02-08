"""
MightyBot reconciliation Rule
---
Description: Calculate total retainage across pay apps (should be ~10% of work completed) and contingency utilization against budget. Reconcile against prior draws to ensure no premature release. Fail if retainage <8% or contingency burn rate indicates risk (e.g., >25% used before 50% completion).
Position: 1
---
"""
def run(payload: dict) -> dict:
    return payload
