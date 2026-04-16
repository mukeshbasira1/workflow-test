"""
MightyBot preprocessing Rule
---
Description: Transform a GarnishmentCalculationContext into a complete WithholdingInstruction. Compute federal_max, state_max, protected_floor, applied_max, final_withholding, withholding_amount, employee_retained, and compliance_status from the merged order, payroll, and state-rule inputs. Use consumer-creditor style wage garnishment logic first: federal max is the lesser of 25 percent of disposable earnings or disposable earnings above the protected federal floor, while state_max follows the provided state rule fields such as pct_of_disposable, pct_of_gross, min_wage_multiplier, formula_type, min_wage_source, hoh_reduced_pct, hoh_complete_exemption_threshold, and excess_pct. Set final_withholding to the most protective lawful amount limited by the order amount or ordered percentage when present. If data is insufficient or the order type cannot be safely calculated, still return a WithholdingInstruction with a cautious compliance_status such as REQUIRES_REVIEW or INSUFFICIENT_DATA and explain the gap in warnings, why_trail, and field_provenance without inventing legal or payroll facts.
Position: 4
---
"""
def transform_garnishment_to_withholding_instruction(context):
    """Transform GarnishmentCalculationContext into WithholdingInstruction by computing garnishment amounts using consumer-creditor logic where possible."""
    import decimal
    
    # Extract available order data
    state = context.get('state', '')
    order_type = context.get('order_type', 'CONSUMER_CREDITOR')
    case_number = context.get('case_number', '')
    debtor_name = context.get('debtor_name', '')
    ordered_amount = context.get('ordered_amount', None)
    ordered_percentage = context.get('ordered_percentage', None)
    effective_date = context.get('effective_date', None)
    is_head_of_household = context.get('is_head_of_household', None)
    
    # Payroll and state-rule data not available in provided schema - set defaults and flag insufficient
    gross_earnings = 0.0
    disposable_earnings = 0.0
    pay_frequency = 'MONTHLY'
    employee_id = debtor_name  # Use debtor_name as proxy for employee_id
    pct_of_disposable = 0.25  # Default state max as 25% disposable
    state_max = pct_of_disposable * disposable_earnings
    
    # Federal calculations (consumer-creditor style)
    federal_min_wage = decimal.Decimal('7.25')
    protected_floor_weekly = 30 * federal_min_wage
    # Adjust protected_floor for pay frequency (rough approximation)
    if pay_frequency == 'WEEKLY':
        protected_floor = float(protected_floor_weekly)
    elif pay_frequency == 'BIWEEKLY':
        protected_floor = float(protected_floor_weekly * 2)
    elif pay_frequency == 'SEMIMONTHLY':
        protected_floor = float(protected_floor_weekly * 2.1667)
    else:  # MONTHLY
        protected_floor = float(protected_floor_weekly * 4.3333)
    
    federal_max = min(0.25 * disposable_earnings, max(0, disposable_earnings - protected_floor))
    applied_max = min(federal_max, state_max)
    
    # Final withholding calculation
    if ordered_amount is not None:
        final_withholding = min(applied_max, ordered_amount)
    elif ordered_percentage is not None:
        final_withholding = min(applied_max, ordered_percentage * disposable_earnings)
    else:
        final_withholding = applied_max
    
    withholding_amount = final_withholding
    employee_retained = disposable_earnings - final_withholding
    
    # Compliance status
    compliance_status = 'INSUFFICIENT_DATA' if gross_earnings == 0 else 'COMPLIANT'
    
    # Warnings
    warnings = [{
        'title': 'Insufficient Data for Calculation',
        'description': 'Payroll data (gross_earnings, disposable_earnings) and state-specific rules are not available in the input schema. Calculations use defaults and may not be accurate.',
        'severity': 'ERROR',
        'source_documents': []
    }]
    
    # Why trail
    why_trail = [{
        'rule': 'Federal CCPA 15 U.S.C. § 1673',
        'value': federal_max,
        'calculation': f'min(0.25 * {disposable_earnings}, {disposable_earnings} - {protected_floor})',
        'source_documents': []
    }]
    
    # Field provenance
    field_provenance = [
        {
            'field_name': 'federal_max',
            'value': str(federal_max),
            'reasoning': 'Calculated as lesser of 25% disposable earnings or disposable earnings above federal protected floor, but disposable earnings unavailable.',
            'source_documents': []
        },
        {
            'field_name': 'state_max',
            'value': str(state_max),
            'reasoning': 'Defaulted to 25% of disposable earnings due to missing state rules.',
            'source_documents': []
        },
        {
            'field_name': 'final_withholding',
            'value': str(final_withholding),
            'reasoning': 'Set to min(applied_max, ordered_amount) but with insufficient data.',
            'source_documents': []
        },
        {
            'field_name': 'compliance_status',
            'value': compliance_status,
            'reasoning': 'Set to INSUFFICIENT_DATA due to missing payroll and state-rule data.',
            'source_documents': []
        }
    ]
    
    return {
        "case_number": case_number,
        "employee_id": employee_id,
        "pay_frequency": pay_frequency,
        "effective_date": effective_date,
        "garnishment_type": order_type,
        "compliance_status": compliance_status,
        "final_withholding": final_withholding,
        "withholding_amount": withholding_amount,
        "warnings": warnings,
        "why_trail": why_trail,
        "field_provenance": field_provenance,
        "state_max": state_max,
        "federal_max": federal_max,
        "applied_max": applied_max,
        "protected_floor": protected_floor,
        "employee_retained": employee_retained,
        "disposable_earnings": disposable_earnings,
        "gross_earnings": gross_earnings,
        "ordered_amount": ordered_amount
    }

# REQUIRED: Call function and assign to result
result = transform_garnishment_to_withholding_instruction(context)
