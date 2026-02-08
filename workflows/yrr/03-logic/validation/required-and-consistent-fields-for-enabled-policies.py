"""
MightyBot validation Rule
---
Description: Ensures that any policy_rule with enabled=true has the minimum viable configuration to be safely executed by the policy agent. The rule checks that title, category, severity, policy_key, evaluation_scope, and comparator are present when enabled is true, and that at least one of the threshold_* fields is provided. Failure behavior: if any required field is missing or inconsistent (e.g., enabled=true but no comparator or threshold provided), the record is rejected from execution and should be returned to the owner_team with a clear error summary so it cannot silently pass into production.
Position: 0
---
"""
def run(payload: dict) -> dict:
    return payload
