"""
MightyBot validation Rule
---
Description: Ensures that all incoming alert payloads from monitoring systems (e.g., Sentry, Prometheus) contain the required fields: alert_type, severity, affected_service, and timestamp. If any of these fields are missing or empty, the alert will be rejected and a warning will be logged. This prevents malformed or incomplete alerts from entering the agentic workflow, ensuring downstream logic has the necessary context to process and route alerts appropriately.
Position: 0
---
"""
def validate_alert_completeness(context):
    """Validate that alert payloads contain required fields: alert_type, severity (alert_severity), affected_service (service_name), and timestamp."""
    issues = []
    passed_checks = []
    
    # Get required fields
    alert_type = context.get('alert_type', '')
    alert_severity = context.get('alert_severity', '')
    service_name = context.get('service_name', '')
    timestamp = context.get('timestamp', '')
    
    # Check required fields
    if not alert_type:
        issues.append('Missing or empty alert_type')
    else:
        passed_checks.append('alert_type present')
    
    if not alert_severity:
        issues.append('Missing or empty alert_severity')
    else:
        passed_checks.append('alert_severity present')
    
    if not service_name:
        issues.append('Missing or empty service_name')
    else:
        passed_checks.append('service_name present')
    
    if not timestamp:
        issues.append('Missing or empty timestamp')
    else:
        passed_checks.append('timestamp present')
    
    # Determine status
    is_valid = len(issues) == 0
    status = "passed" if is_valid else "failed"
    confidence = 1.0 if is_valid else 0.9
    reasoning = "All required fields are present and non-empty" if is_valid else f"Found {len(issues)} missing or empty required fields"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_alert_completeness(context)
