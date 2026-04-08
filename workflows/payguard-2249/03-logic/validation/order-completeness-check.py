"""
MightyBot validation Rule
---
Description: Verify state, order_type, case_number, debtor_name, employer_name are non-null. If any required field is missing, return status FAILED with the list of missing fields.
Position: 4
---
"""
def validate_required_fields(context):
    """Verify that state, order_type, case_number, debtor_name, employer_name are non-null."""
    missing_fields = []
    passed_checks = []
    
    # Check existing field: case_number
    case_number = context.get('case_number', '')
    if not case_number:
        missing_fields.append('case_number')
    else:
        passed_checks.append('case_number')
    
    # Fields not in schema are considered missing
    missing_fields.extend(['state', 'order_type', 'debtor_name', 'employer_name'])
    
    is_valid = len(missing_fields) == 0
    status = "passed" if is_valid else "failed"
    
    issues = ", ".join(missing_fields) if missing_fields else None
    passed_checks_str = ", ".join(passed_checks) if passed_checks else None
    confidence = "1.0" if is_valid else "0.0"
    reasoning = "All required fields present" if is_valid else f"Missing fields: {issues}"
    
    return {
        "status": status,
        "is_valid": "true" if is_valid else "false",
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks_str,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_required_fields(context)
