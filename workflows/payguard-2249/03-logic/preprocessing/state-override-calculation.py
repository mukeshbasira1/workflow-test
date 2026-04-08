"""
MightyBot preprocessing Rule
---
Description: Apply state-specific garnishment formula from state rules data. If is_prohibited, state_max = 0. Otherwise calculate using pct_of_disposable or pct_of_gross, min_wage_multiplier, and formula_type (LESSER_OF or GREATER_OF). Apply head-of-household overrides: FL complete exemption below $750/week, CA 50% reduction. Use LOCAL_IF_HIGHER for min wage source when applicable. Return state_max and statute citation.
Position: 2
---
"""
def preprocess_garnishment_state_max(context):
    """Apply state-specific garnishment formula where possible, using available fields; partial if required data missing."""
    transformed_data = {}
    
    # Copy all existing fields
    fields = ['case_number', 'compliance_status', 'effective_date', 'employee_id', 'final_withholding', 'garnishment_type', 'pay_frequency', 'withholding_amount', 'warnings', 'state_max', 'why_trail', 'applied_max', 'federal_max', 'ordered_amount', 'protected_floor', 'employee_retained']
    for f in fields:
        transformed_data[f] = context.get(f, None)
    
    # If compliance_status is PROHIBITED, set state_max = 0 (matches 'if is_prohibited')
    compliance_status = context.get('compliance_status')
    if compliance_status == 'PROHIBITED':
        transformed_data['state_max'] = 0.0
        status = "completed"
        notes = "State max set to 0 due to prohibited compliance status."
        transformations_applied = ['Set state_max to 0 for prohibited compliance status']
        # Update dependent fields
        federal_max = transformed_data.get('federal_max')
        state_max = transformed_data['state_max']
        applied_max = min(federal_max, state_max) if federal_max is not None else state_max
        transformed_data['applied_max'] = applied_max
        
        ordered_amount = transformed_data.get('ordered_amount')
        final_withholding = min(applied_max, ordered_amount) if ordered_amount is not None else applied_max
        transformed_data['final_withholding'] = final_withholding
        transformed_data['withholding_amount'] = final_withholding
        
        fields_processed = ['state_max', 'applied_max', 'final_withholding', 'withholding_amount']
    else:
        # Required fields for full formula (pct_of_disposable, etc.) are missing, so partial
        status = "partial"
        notes = "Required fields for state formula calculation (pct_of_disposable, pct_of_gross, etc.) are missing from schema."
        transformations_applied = []
        fields_processed = []
    
    return {
        "status": status,
        "transformed_data": transformed_data,
        "fields_processed": fields_processed,
        "transformations_applied": transformations_applied,
        "notes": notes
    }

# REQUIRED: Call function and assign to result
result = preprocess_garnishment_state_max(context)
