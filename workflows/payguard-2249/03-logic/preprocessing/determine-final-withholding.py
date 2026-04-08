"""
MightyBot preprocessing Rule
---
Description: Final withholding = min(federal_max, state_max, ordered_amount). The most protective limit wins. If ordered_amount is null, use ordered_percentage * disposable_earnings. Output the final_withholding amount along with federal_max, state_max, applied_max for the Why-Trail.
Position: 3
---
"""
def preprocess_final_withholding(context):
    """Calculate final withholding as the minimum of federal_max, state_max, and ordered_amount. If ordered_amount is null, mark as partial since required fields for alternative calculation are unavailable."""
    import decimal
    
    # Get required fields
    federal_max = context.get('federal_max')
    state_max = context.get('state_max')
    ordered_amount = context.get('ordered_amount')
    
    # Calculate applied_max as min of federal_max and state_max, handling None values
    if federal_max is not None and state_max is not None:
        applied_max = min(decimal.Decimal(federal_max), decimal.Decimal(state_max))
    elif federal_max is not None:
        applied_max = decimal.Decimal(federal_max)
    elif state_max is not None:
        applied_max = decimal.Decimal(state_max)
    else:
        applied_max = None
    
    fields_processed = ['federal_max', 'state_max', 'ordered_amount']
    transformations_applied = ['Calculated applied_max as minimum of federal_max and state_max']
    notes = []
    
    if ordered_amount is not None:
        final_withholding = min(applied_max, decimal.Decimal(ordered_amount)) if applied_max is not None else decimal.Decimal(ordered_amount)
        status = "completed"
        transformed_data = {
            "final_withholding": float(final_withholding),
            "federal_max": federal_max,
            "state_max": state_max,
            "applied_max": float(applied_max) if applied_max is not None else None
        }
        transformations_applied.append('Calculated final_withholding as minimum of applied_max and ordered_amount')
    else:
        status = "partial"
        transformed_data = {
            "final_withholding": None,
            "federal_max": federal_max,
            "state_max": state_max,
            "applied_max": float(applied_max) if applied_max is not None else None
        }
        notes.append("ordered_amount is null; alternative calculation requires ordered_percentage and disposable_earnings which are not available")
    
    return {
        "status": status,
        "transformed_data": transformed_data,
        "fields_processed": fields_processed,
        "transformations_applied": transformations_applied,
        "notes": notes
    }

# REQUIRED: Call function and assign to result
result = preprocess_final_withholding(context)
