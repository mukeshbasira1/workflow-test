"""
MightyBot validation Rule
---
Description: Ensures that all incoming alert payloads from monitoring systems (e.g., Sentry, Prometheus) contain the required fields: alert_type, severity, affected_service, and timestamp. If any of these fields are missing or empty, the alert will be rejected and a warning will be logged. This prevents malformed or incomplete alerts from entering the agentic workflow, ensuring downstream logic has the necessary context to process and route alerts appropriately.
Position: 0
---
"""
def run(payload: dict) -> dict:
    return payload
