"""
MightyBot validation Rule
---
Description: Verify disposable_earnings <= gross_earnings and both > 0. If disposable exceeds gross, return status FAILED. If either is zero or negative, return status FAILED with details.
Position: 5
---
"""
def validate_earnings_relationship(context):
    """Verify that disposable_earnings <= gross_earnings and both > 0. Return failed if conditions not met or fields unavailable."""
    issues = []
    passed_checks = []
    
    # Note: disposable_earnings and gross_earnings are not available in the provided schema
    disposable_earnings = None  # Not in schema
    gross_earnings = None  # Not in schema
    
    issues.append('disposable_earnings not available in schema')
    issues.append('gross_earnings not available in schema')
    
    is_valid = False
    status = "failed"
    confidence = 0.0
    reasoning = "Required fields not available in schema"
    
    return {
        "status": status,
        "is_valid": str(is_valid).lower(),
        "confidence": str(confidence),
        "issues": ", ".join(issues),
        "passed_checks": "",
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_earnings_relationship(context)
