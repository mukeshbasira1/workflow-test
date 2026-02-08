"""
MightyBot reconciliation Rule
---
Description: Calculate total retainage across pay apps (should be ~10% of work completed) and contingency utilization against budget. Reconcile against prior draws to ensure no premature release. Fail if retainage <8% or contingency burn rate indicates risk (e.g., >25% used before 50% completion).
Position: 1
---
"""
def validate_retainage_contingency_reconciliation(context):
    """Reconcile retainage and contingency utilization against budget and prior draws, ensuring no premature release."""
    # Note: The input schema lacks fields for work_completed, budget, retainage, and contingency.
    # Using available fields to attempt reconciliation, but calculations will be incomplete.
    
    current_draw_id = context.get('draw_id', '')
    current_amount = context.get('amount_extracted', 0)
    document_type = context.get('document_type', '')
    
    # Assume pay apps are documents with 'pay' in type (guessing based on rule)
    pay_apps = context.select("documents", filters={"document_type": {"$regex": "pay"}}) or []
    total_pay_app_amount = sum(p.get('amount_extracted', 0) for p in pay_apps)
    
    # Assume prior draws are other documents with different draw_id
    prior_draws = context.select("documents", filters={"draw_id": {"$ne": current_draw_id}}) or []
    prior_total_amount = sum(p.get('amount_extracted', 0) for p in prior_draws)
    
    # Since required fields are missing, we cannot calculate retainage or contingency properly
    retainage = 0  # Not available
    work_completed = 0  # Not available
    budget = 0  # Not available
    contingency_used = 0  # Not available
    
    discrepancies = []
    matches = []
    
    # Check if retainage < 8% (but can't check since no data)
    if retainage / work_completed < 0.08 if work_completed > 0 else True:
        discrepancies.append({"issue": "Retainage calculation not possible due to missing data", "details": "work_completed and retainage fields not in schema"})
    
    # Contingency burn rate (can't check)
    if contingency_used / budget > 0.25 if budget > 0 and work_completed < 0.5 else False:
        discrepancies.append({"issue": "Contingency burn rate check not possible", "details": "budget, contingency, work_completed not in schema"})
    
    # No premature release check possible
    discrepancies.append({"issue": "No premature release check", "details": "Prior draws data incomplete"})
    
    completeness_score = 0.1  # Very low since key fields missing
    status = "failed"
    recommendation = "Update data schema to include work_completed, budget, retainage, and contingency fields for accurate reconciliation."
    reasoning = "Reconciliation cannot be performed accurately due to absence of required fields in the input schema. Used available amount_extracted for basic sums, but key calculations are impossible."
    
    return {
        "status": status,
        "matches": matches,
        "discrepancies": discrepancies,
        "completeness_score": completeness_score,
        "recommendation": recommendation,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_retainage_contingency_reconciliation(context)
