"""
MightyBot preprocessing Rule
---
Description: Normalize all document dates (expiration, invoice dates, inspection dates) to ISO format and validate against current draw period. Flag expired documents or future-dated invoices.
Position: 3
---
"""
def validate_date_normalization(context):
    """Normalize document dates to ISO format and validate against current date, flagging expired or future-dated documents."""
    import datetime
    
    current_date = datetime.date.today()
    transformed = {}
    processed = []
    applied = []
    notes = []
    
    def normalize_date(date_str):
        if not date_str:
            return None
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
        for fmt in formats:
            try:
                dt = datetime.datetime.strptime(date_str, fmt)
                return dt.date().isoformat()
            except ValueError:
                continue
        return None
    
    # Process expiration_date
    exp_date_str = context.get('expiration_date', '')
    if exp_date_str:
        norm_exp = normalize_date(exp_date_str)
        if norm_exp:
            transformed['expiration_date'] = norm_exp
            processed.append('expiration_date')
            applied.append('Normalized expiration_date to ISO format')
            exp_date = datetime.date.fromisoformat(norm_exp)
            if exp_date < current_date:
                notes.append('Document is expired')
            else:
                notes.append('Document is not expired')
        else:
            notes.append('Failed to parse expiration_date')
    
    # Process revised_budget_date (assuming as invoice date for future-dated check)
    rev_date_str = context.get('revised_budget_date', '')
    if rev_date_str:
        norm_rev = normalize_date(rev_date_str)
        if norm_rev:
            transformed['revised_budget_date'] = norm_rev
            processed.append('revised_budget_date')
            applied.append('Normalized revised_budget_date to ISO format')
            rev_date = datetime.date.fromisoformat(norm_rev)
            if rev_date > current_date:
                notes.append('Future-dated document')
            else:
                notes.append('Document date is not future-dated')
        else:
            notes.append('Failed to parse revised_budget_date')
    
    status = 'completed' if processed else 'failed'
    notes_str = '; '.join(notes) if notes else None
    
    return {
        "status": status,
        "transformed_data": transformed,
        "fields_processed": processed,
        "transformations_applied": applied,
        "notes": notes_str
    }

# REQUIRED: Call function and assign to result
result = validate_date_normalization(context)
