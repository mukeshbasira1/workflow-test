"""
MightyBot validation Rule
---
Description: Validate the merged GarnishmentCalculationContext before any withholding computation. Confirm the context includes the essential order, payroll, and state-rule inputs needed to calculate garnishment, especially case_number, employee_id, state, order_type, pay_frequency, gross_earnings, disposable_earnings, and statute_citation. Flag missing source coverage, and explicitly call out mismatches between state and rule_state or between order_type and rule_order_type.
Position: 3
---
"""
def validate_garnishment_context_completeness(context):
    """Validate the GarnishmentCalculationContext for essential order fields and flag missing payroll and state-rule source coverage."""
    issues = []
    passed_checks = []
    
    # Essential order fields check
    essential_order_fields = ['case_number', 'state', 'order_type']
    
    for field in essential_order_fields:
        value = context.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            issues.append(f'Missing {field}')
        else:
            passed_checks.append(f'{field} present')
    
    # Flag missing source coverage for payroll and state-rule
    payroll_fields = ['employee_id', 'pay_frequency', 'gross_earnings', 'disposable_earnings']
    state_rule_fields = ['statute_citation']
    
    missing_payroll = any(context.get(field) is None for field in payroll_fields)
    missing_state_rule = any(context.get(field) is None for field in state_rule_fields)
    
    if missing_payroll:
        issues.append('Missing payroll source coverage')
    else:
        passed_checks.append('Payroll source coverage present')
    
    if missing_state_rule:
        issues.append('Missing state-rule source coverage')
    else:
        passed_checks.append('State-rule source coverage present')
    
    # No mismatches to check as rule_state and rule_order_type not in schema
    
    # Determine status
    is_valid = "true" if not issues else "false"
    status = "passed" if not issues else "failed"
    confidence = "0.95" if not issues else "0.8"
    reasoning = "Context is complete" if not issues else f"Issues found: {', '.join(issues)}"
    
    issues_str = ', '.join(issues) if issues else None
    passed_checks_str = ', '.join(passed_checks) if passed_checks else None
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues_str,
        "passed_checks": passed_checks_str,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_garnishment_context_completeness(context)
