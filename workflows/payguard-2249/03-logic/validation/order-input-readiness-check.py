"""
MightyBot validation Rule
---
Description: Validate the extracted GarnishmentOrder before downstream processing. Confirm state, order_type, case_number, debtor_name, and employer_name are present and coherent. Flag contradictory order values, impossible amount combinations such as both ordered_amount and ordered_percentage missing when one is needed, and clearly explain any missing or suspect inputs needed for garnishment processing.
Position: 1
---
"""
def validate_garnishment_order(context):
    """Validate GarnishmentOrder fields for presence, coherence, and required amounts."""
    issues = []
    passed_checks = []
    
    # Required fields check
    required_fields = ['state', 'order_type', 'case_number', 'debtor_name', 'employer_name']
    for field in required_fields:
        value = context.get(field, '')
        if not value or str(value).strip() == '':
            issues.append(f'Missing or empty {field}')
        else:
            passed_checks.append(f'{field} present')
    
    # Amount validation
    ordered_amount = context.get('ordered_amount', None)
    ordered_percentage = context.get('ordered_percentage', None)
    if ordered_amount is None and ordered_percentage is None:
        issues.append('Both ordered_amount and ordered_percentage are missing; at least one is required')
    else:
        if ordered_amount is not None:
            passed_checks.append('ordered_amount present')
        if ordered_percentage is not None:
            passed_checks.append('ordered_percentage present')
    
    # Coherence checks
    state = context.get('state', '')
    valid_states = ["CA", "TX", "NY", "OH", "FL", "IL", "NJ", "PA", "GA", "NC"]
    if state and state not in valid_states:
        issues.append(f'Invalid state: {state}')
    else:
        passed_checks.append('Valid state')
    
    order_type = context.get('order_type', '')
    valid_order_types = ["CONSUMER_CREDITOR", "CHILD_SUPPORT", "IRS_TAX_LEVY", "STATE_TAX_LEVY", "FEDERAL_STUDENT_LOAN", "BANKRUPTCY", "FEDERAL_DEBT_AWG"]
    if order_type and order_type not in valid_order_types:
        issues.append(f'Invalid order_type: {order_type}')
    else:
        passed_checks.append('Valid order_type')
    
    # Determine status
    is_valid = "true" if len(issues) == 0 else "false"
    status = "passed" if is_valid == "true" else "failed"
    confidence = "0.95" if is_valid == "true" else "0.8"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": ", ".join(issues) if issues else None,
        "passed_checks": ", ".join(passed_checks) if passed_checks else None,
        "reasoning": f"Validation {'passed' if is_valid == 'true' else 'failed'} with {len(issues)} issues and {len(passed_checks)} passed checks"
    }

# REQUIRED: Call function and assign to result
result = validate_garnishment_order(context)
