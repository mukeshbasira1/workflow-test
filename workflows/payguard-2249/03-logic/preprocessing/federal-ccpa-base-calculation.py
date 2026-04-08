"""
MightyBot preprocessing Rule
---
Description: Calculate the federal CCPA maximum garnishment amount. Consumer debt: federal_max = min(0.25 * disposable, max(0, disposable - 30 * 7.25 * pay_scale)). Child support: federal_max = ceiling * disposable (50/55/60/65% based on arrears + second family). Student loan: federal_max = 0.15 * disposable. IRS levy: federal_max = max(0, disposable - pub1494_exempt_amount). Pay scale: WEEKLY=1, BIWEEKLY=2, SEMIMONTHLY=2.17, MONTHLY=4.33.
Position: 1
---
"""
import decimal

def calculate_federal_ccpa_max(context):
    """Calculate the federal CCPA maximum garnishment amount based on garnishment type, pay frequency, and disposable earnings."""
    garnishment_type = context.get('garnishment_type', '').lower()
    pay_frequency = context.get('pay_frequency', '').lower()
    disposable = context.get('employee_retained', 0.0)  # Assuming employee_retained represents disposable earnings
    
    pay_scale_map = {
        'weekly': 1,
        'biweekly': 2,
        'semimonthly': decimal.Decimal('2.17'),
        'monthly': decimal.Decimal('4.33')
    }
    pay_scale = pay_scale_map.get(pay_frequency, 1)
    
    federal_max = None
    transformations_applied = []
    fields_processed = ['garnishment_type', 'pay_frequency', 'employee_retained']
    
    if garnishment_type == 'consumer debt':
        protected_amount = 30 * 7.25 * float(pay_scale)
        federal_max = min(0.25 * disposable, max(0, disposable - protected_amount))
        transformations_applied.append('Calculated federal_max for consumer debt using 25% disposable or disposable minus protected amount')
    elif garnishment_type == 'student loan':
        federal_max = 0.15 * disposable
        transformations_applied.append('Calculated federal_max for student loan as 15% of disposable')
    elif garnishment_type == 'child support':
        # Assuming 50% ceiling as default since arrears/second family data not available
        federal_max = 0.5 * disposable
        transformations_applied.append('Calculated federal_max for child support assuming 50% ceiling (data on arrears/second family unavailable)')
    elif garnishment_type == 'irs levy':
        # Assuming pub1494_exempt_amount = 0 since not available in schema
        exempt_amount = 0
        federal_max = max(0, disposable - exempt_amount)
        transformations_applied.append('Calculated federal_max for IRS levy assuming exempt amount of 0 (pub1494_exempt_amount unavailable)')
    
    # Round federal_max to 2 decimal places if calculated
    if federal_max is not None:
        federal_max = round(federal_max, 2)
    
    # Build transformed_data dict with all schema fields, updating federal_max
    transformed_data = {
        "case_number": context.get('case_number', ''),
        "compliance_status": context.get('compliance_status', 'INSUFFICIENT_DATA'),
        "effective_date": context.get('effective_date', ''),
        "employee_id": context.get('employee_id', ''),
        "final_withholding": context.get('final_withholding', 0),
        "garnishment_type": context.get('garnishment_type', ''),
        "pay_frequency": context.get('pay_frequency', ''),
        "withholding_amount": context.get('withholding_amount', 0),
        "warnings": context.get('warnings', []),
        "state_max": context.get('state_max'),
        "why_trail": context.get('why_trail', []),
        "applied_max": context.get('applied_max'),
        "federal_max": federal_max,
        "ordered_amount": context.get('ordered_amount'),
        "protected_floor": context.get('protected_floor'),
        "employee_retained": context.get('employee_retained')
    }
    
    # Determine status
    if federal_max is not None:
        status = "completed" if garnishment_type in ['consumer debt', 'student loan'] else "partial"
    else:
        status = "failed"
    
    notes = f"Federal max calculation for {garnishment_type}. Status: {status}."
    
    return {
        "status": status,
        "transformed_data": transformed_data,
        "fields_processed": fields_processed,
        "transformations_applied": transformations_applied,
        "notes": notes
    }

# REQUIRED: Call function and assign to result
result = calculate_federal_ccpa_max(context)
