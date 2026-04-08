"""
MightyBot preprocessing Rule
---
Description: Apply state-specific garnishment formula from state rules data. If is_prohibited, state_max = 0. Otherwise calculate using pct_of_disposable or pct_of_gross, min_wage_multiplier, and formula_type (LESSER_OF or GREATER_OF). Apply head-of-household overrides: FL complete exemption below $750/week, CA 50% reduction. Use LOCAL_IF_HIGHER for min wage source when applicable. Return state_max and statute citation.
Position: 2
---
"""
def run(payload: dict) -> dict:
    return payload
