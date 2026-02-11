"""
MightyBot validation Rule
---
Description: Verify that all required lien mukesh waivers for the current draw period are present and match the invoice amounts from the submitted documents. Cross-reference vendor names, amounts, and dates against the invoice log and pay application. If any waiver is missing, expired, or does not match (e.g., amount discrepancy >5%), flag as failed with details on missing/mismatched items.
Position: 0
---
"""
import datetime

def validate_lien_waiver_completeness(context):
    """Validate that all required lien waivers for the draw are present, match invoice amounts, and are not expired."""
    issues = []
    passed_checks = []
    
    draw_id = context.get('draw_id', '')
    if not draw_id:
        return {
            "status": "failed",
            "is_valid": False,
            "confidence": 0.0,
            "issues": ["No draw_id provided"],
            "passed_checks": [],
            "reasoning": "Cannot validate without draw_id"
        }
    
    # Assume select returns lists of documents filtered by type and draw_id
    pay_apps = context.select('documents', {'document_type': 'pay_application', 'draw_id': draw_id})
    invoices = context.select('documents', {'document_type': 'invoice', 'draw_id': draw_id})
    lien_waivers = context.select('documents', {'document_type': 'lien_waiver', 'draw_id': draw_id})
    
    current_date = datetime.date.today()
    
    for pay_app in pay_apps:
        vendor = pay_app.get('vendor_name', '')
        pay_amount = pay_app.get('amount_extracted', 0)
        
        # Find matching invoice
        matching_invoice = None
        for inv in invoices:
            inv_vendor = inv.get('vendor_name', '')
            inv_amount = inv.get('amount_extracted', 0)
            if inv_vendor == vendor and pay_amount > 0 and abs(inv_amount - pay_amount) / pay_amount <= 0.05:
                matching_invoice = inv
                break
        
        if not matching_invoice:
            issues.append(f'No matching invoice for vendor {vendor} with pay amount {pay_amount}')
            continue
        
        inv_amount = matching_invoice.get('amount_extracted', 0)
        
        # Find matching lien waiver
        matching_waiver = None
        for waiver in lien_waivers:
            w_vendor = waiver.get('vendor_name', '')
            w_amount = waiver.get('amount_extracted', 0)
            exp_date_str = waiver.get('expiration_date', '')
            if w_vendor == vendor and inv_amount > 0 and abs(w_amount - inv_amount) / inv_amount <= 0.05:
                try:
                    exp_date = datetime.datetime.fromisoformat(exp_date_str).date()
                    if exp_date >= current_date and not waiver.get('is_conditional_waiver', False):
                        matching_waiver = waiver
                        break
                except ValueError:
                    pass  # Invalid date format
        
        if matching_waiver:
            passed_checks.append(f'Valid lien waiver for {vendor}')
        else:
            issues.append(f'No valid matching lien waiver for vendor {vendor} with invoice amount {inv_amount}')
    
    is_valid = len(issues) == 0
    status = "passed" if is_valid else "failed"
    confidence = 0.95 if is_valid else 0.85
    reasoning = "All required lien waivers are present and match invoices" if is_valid else f"Found {len(issues)} issues with lien waivers"
    
    return {
        "status": status,
        "is_valid": is_valid,
        "confidence": confidence,
        "issues": issues,
        "passed_checks": passed_checks,
        "reasoning": reasoning
    }

# REQUIRED: Call function and assign to result
result = validate_lien_waiver_completeness(context)
