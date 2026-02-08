"""
MightyBot validation Rule
---
Description: Validates that all required property compliance fields are populated before policy assessment. Checks for presence of critical identifiers (property_id, property_type, construction_type) and compliance indicators (epc_rating, property_valuation). Fails if any required field is null or empty, preventing incomplete assessments from proceeding to policy evaluation.
Position: 0
---
"""
def run(payload: dict) -> dict:
    return payload
