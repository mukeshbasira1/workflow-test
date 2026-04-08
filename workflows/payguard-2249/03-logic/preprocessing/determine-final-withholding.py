"""
MightyBot preprocessing Rule
---
Description: Final withholding = min(federal_max, state_max, ordered_amount). The most protective limit wins. If ordered_amount is null, use ordered_percentage * disposable_earnings. Output the final_withholding amount along with federal_max, state_max, applied_max for the Why-Trail.
Position: 3
---
"""
def run(payload: dict) -> dict:
    return payload
