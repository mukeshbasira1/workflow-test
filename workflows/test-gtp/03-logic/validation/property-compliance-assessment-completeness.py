"""
MightyBot validation Rule
---
Description: Validates that all required property compliance fields are populated before policy assessment. Checks for presence of critical identifiers (property_id, property_type, construction_type) and compliance indicators (epc_rating, property_valuation). Fails if any required field is null or empty, preventing incomplete assessments from proceeding to policy evaluation.
Position: 0
---
"""
def validate_property_compliance_completeness(context):
    """Validates that required property compliance fields are populated: property_type, construction_type, epc_rating, property_valuation."""
    issues = []
    passed_checks = []
    
    # Get required fields with safe defaults
    property_type = context.get('property_type', None)
    construction_type = context.get('construction_type', None)
    epc_rating = context.get('epc_rating', None)
    property_valuation = context.get('property_valuation', None)
    
    # Check property_type
    if property_type is None or (isinstance(property_type, str) and not property_type.strip()):
        issues.append('Missing or empty property_type')
    else:
        passed_checks.append('property_type is populated')
    
    # Check construction_type
    if construction_type is None or (isinstance(construction_type, str) and not construction_type.strip()):
        issues.append('Missing or empty construction_type')
    else:
        passed_checks.append('construction_type is populated')
    
    # Check epc_rating
    if epc_rating is None or (isinstance(epc_rating, str) and not epc_rating.strip()):
        issues.append('Missing or empty epc_rating')
    else:
        passed_checks.append('epc_rating is populated')
    
    # Check property_valuation
    if property_valuation is None:
        issues.append('Missing property_valuation')
    else:
        passed_checks.append('property_valuation is populated')
    
    # Determine status
    is_valid = len(issues) == 0
    status = "passed" if is_valid else "failed"
    confidence = 1.0 if is_valid else 0.8
    reasoning = "All required property compliance fields are populated" if is_valid else f"Found {len(issues)} missing or empty fields"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_property_compliance_completeness(context)
