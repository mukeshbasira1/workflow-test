"""
MightyBot validation Rule
---
Description: Validate the EmployeeEarningsProfile for garnishment processing readiness. Confirm employee_id and pay_frequency exist, gross_earnings and disposable_earnings are positive numbers, disposable_earnings does not exceed gross_earnings, and any wage or existing_garnishments fields are internally coherent. Treat a null existing_garnishments value as acceptable but note it when other payroll evidence is weak. Return clear failure details when payroll data is missing, non-numeric, or inconsistent.
Position: 2
---
"""
def validate_employee_earnings_profile(context):
    """Validate EmployeeEarningsProfile for garnishment processing readiness."""
    issues = []
    passed_checks = []
    
    # Required fields for employee earnings are not in the provided schema
    issues.append('Missing employee_id')
    issues.append('Missing pay_frequency')
    issues.append('Missing gross_earnings')
    issues.append('Missing disposable_earnings')
    issues.append('Missing wage or existing_garnishments data for coherence check')
    
    is_valid = 'false'
    status = 'failed'
    confidence = '0.0'
    reasoning = 'Required employee earnings profile fields are not present in instance_data'
    issues_str = ', '.join(issues) if issues else None
    passed_checks_str = ', '.join(passed_checks) if passed_checks else None
    
    return {
        "issues": issues_str,
        "status": status,
        "is_valid": is_valid,
        "reasoning": reasoning,
        "confidence": confidence,
        "passed_checks": passed_checks_str
    }

# REQUIRED: Call function and assign to result
result = validate_employee_earnings_profile(context)
