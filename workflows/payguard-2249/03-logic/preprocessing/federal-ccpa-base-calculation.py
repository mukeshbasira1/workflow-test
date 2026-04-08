"""
MightyBot preprocessing Rule
---
Description: Calculate the federal CCPA maximum garnishment amount. Consumer debt: federal_max = min(0.25 * disposable, max(0, disposable - 30 * 7.25 * pay_scale)). Child support: federal_max = ceiling * disposable (50/55/60/65% based on arrears + second family). Student loan: federal_max = 0.15 * disposable. IRS levy: federal_max = max(0, disposable - pub1494_exempt_amount). Pay scale: WEEKLY=1, BIWEEKLY=2, SEMIMONTHLY=2.17, MONTHLY=4.33.
Position: 1
---
"""
def run(payload: dict) -> dict:
    return payload
