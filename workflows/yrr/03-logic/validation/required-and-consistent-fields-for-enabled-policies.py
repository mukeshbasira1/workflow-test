"""
MightyBot validation Rule
---
Description: Ensures that any policy_rule with enabled=true has the minimum viable configuration to be safely executed by the policy agent. The rule checks that title, category, severity, policy_key, evaluation_scope, and comparator are present when enabled is true, and that at least one of the threshold_* fields is provided. Failure behavior: if any required field is missing or inconsistent (e.g., enabled=true but no comparator or threshold provided), the record is rejected from execution and should be returned to the owner_team with a clear error summary so it cannot silently pass into production.
Position: 0
---
"""
def validate_policy_rule_configuration(context):
    """Validates that enabled policy rules have required fields and at least one threshold."""
    issues = []
    passed_checks = []
    
    enabled = context.get('enabled', False)
    
    if not enabled:
        passed_checks.append('Rule is disabled, no validation required')
        return {
            "status": "passed",
            "is_valid": True,
            "confidence": 0.95,
            "issues": issues,
            "passed_checks": passed_checks,
            "reasoning": "Rule is disabled, no checks performed"
        }
    
    # Required fields when enabled
    required_fields = ['title', 'category', 'severity', 'policy_key', 'evaluation_scope', 'comparator']
    for field in required_fields:
        value = context.get(field, '')
        if not value:
            issues.append(f'Missing required field: {field}')
        else:
            passed_checks.append(f'Required field present: {field}')
    
    # At least one threshold field
    threshold_fields = ['threshold_days', 'threshold_number', 'threshold_percent', 'threshold_currency']
    has_threshold = False
    for field in threshold_fields:
        value = context.get(field, None)
        if value is not None and (field == 'threshold_days' and value or field != 'threshold_days'):
            has_threshold = True
            passed_checks.append(f'Threshold field present: {field}')
            break
    
    if not has_threshold:
        issues.append('At least one threshold field must be provided')
    
    is_valid = len(issues) == 0
    status = "passed" if is_valid else "failed"
    confidence = 0.95 if is_valid else 0.8
    
    reasoning = f"Validation {'passed' if is_valid else 'failed'}: {len(issues)} issues found"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_policy_rule_configuration(context)
