"""
MightyBot validation Rule
---
Description: Verify 0 <= final_withholding <= disposable_earnings. If withholding is negative or exceeds disposable earnings, return status FAILED with the violation details.
Position: 6
---
"""
def validate_withholding_limits(context):
    """Verify that final_withholding is between 0 and disposable_earnings inclusive."""
    final_withholding = context.get('final_withholding', None)
    employee_retained = context.get('employee_retained', None)
    
    if final_withholding is None or employee_retained is None:
        return {
            "status": "failed",
            "is_valid": "false",
            "confidence": "0.5",
            "issues": "Missing final_withholding or employee_retained data",
            "passed_checks": "",
            "reasoning": "Required fields not available for validation"
        }
    
    disposable_earnings = employee_retained + final_withholding
    
    if 0 <= final_withholding <= disposable_earnings:
        status = "passed"
        is_valid = "true"
        issues = ""
        passed_checks = "Final withholding within limits"
        reasoning = "Withholding amount is valid"
        confidence = "0.95"
    else:
        status = "failed"
        is_valid = "false"
        issues = f"Final withholding {final_withholding} not between 0 and disposable earnings {disposable_earnings}"
        passed_checks = ""
        reasoning = "Withholding violates limits"
        confidence = "0.9"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_withholding_limits(context)
