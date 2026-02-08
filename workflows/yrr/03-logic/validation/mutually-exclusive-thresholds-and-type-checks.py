"""
MightyBot validation Rule
---
Description: Validates that only one threshold field is set among threshold_number, threshold_percent, and threshold_currency, and that its type and value range are appropriate. threshold_percent must be a number between 0 and 100 inclusive, threshold_currency must be a non-negative number, and threshold_number must be a valid number (negative allowed only if explicitly intended by comparator). Failure behavior: if multiple thresholds are provided or the single provided threshold is out of the permitted range or wrong type, the policy_rule is marked invalid and must be corrected before activation.
Position: 1
---
"""
def validate_threshold_exclusivity(context):
    """Validates that only one threshold field is set among threshold_number, threshold_percent, and threshold_currency, and that its value is within appropriate range."""
    issues = []
    passed_checks = []
    
    threshold_fields = ['threshold_number', 'threshold_percent', 'threshold_currency']
    set_fields = [f for f in threshold_fields if context.get(f) is not None]
    
    if len(set_fields) == 0:
        issues.append('No threshold field is set')
    elif len(set_fields) > 1:
        issues.append(f'Multiple threshold fields set: {", ".join(set_fields)}')
    else:
        field = set_fields[0]
        value = context.get(field)
        if field == 'threshold_percent':
            if not isinstance(value, (int, float)):
                issues.append('threshold_percent must be a number')
            elif not (0 <= value <= 100):
                issues.append('threshold_percent must be between 0 and 100 inclusive')
            else:
                passed_checks.append('threshold_percent is valid')
        elif field == 'threshold_currency':
            if not isinstance(value, (int, float)):
                issues.append('threshold_currency must be a number')
            elif value < 0:
                issues.append('threshold_currency must be non-negative')
            else:
                passed_checks.append('threshold_currency is valid')
        elif field == 'threshold_number':
            if not isinstance(value, (int, float)):
                issues.append('threshold_number must be a number')
            else:
                passed_checks.append('threshold_number is valid')
    
    is_valid = len(issues) == 0
    status = "passed" if is_valid else "failed"
    confidence = 1.0 if is_valid else 0.9
    reasoning = "Validation passed" if is_valid else f"Found {len(issues)} issues: {', '.join(issues)}"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_threshold_exclusivity(context)
