# File Extraction Prompt

You are extracting data from a court-issued wage garnishment order. Extract all fields precisely as they appear in the document.

CRITICAL EXTRACTION RULES:
1. **state**: Extract the two-letter US state code from the court name or address (e.g., "Superior Court of California" -> "CA", "District Court of Harris County, Texas" -> "TX"). This is the most important field because it determines which garnishment law applies.
2. **case_number**: Extract the exact case or docket number as printed.
3. **debtor_name**: Full legal name of the employee or judgment debtor. Match exactly as printed on the order.
4. **employer_name**: Name of the employer or garnishee being served.
5. **order_type**: Classify as exactly one of these enum values: `CONSUMER_CREDITOR`, `CHILD_SUPPORT`, `IRS_TAX_LEVY`, `STATE_TAX_LEVY`, `FEDERAL_STUDENT_LOAN`, `BANKRUPTCY`, `FEDERAL_DEBT_AWG`. Most civil judgments are `CONSUMER_CREDITOR`. IRS orders are `IRS_TAX_LEVY`. State revenue or tax agency orders are `STATE_TAX_LEVY`. Federal student-loan administrative wage garnishment orders are `FEDERAL_STUDENT_LOAN`.
6. **ordered_amount**: The fixed dollar amount the court orders withheld per pay period. Set to null if the order is percentage-based (e.g., "withhold 25% of disposable earnings"). Do NOT confuse employer processing fees, court costs, judgment balances, attorney fees, or administrative charges with the ordered withholding amount. A "$3.00 processing fee per pay period" is not the ordered amount. The total judgment balance is not the ordered amount either.
7. **ordered_percentage**: Percentage of earnings to withhold, expressed as a decimal (25% = 0.25). Set to null if a fixed dollar amount is ordered instead.
8. **effective_date**: Date garnishment takes effect in YYYY-MM-DD format.
9. **expiration_date**: An explicitly stated end date for the garnishment in YYYY-MM-DD format. Set to null if the order says until further order of the court, until satisfied, until the judgment is paid in full, or any other open-ended language. Do NOT reuse the filing date or effective date as the expiration date.
10. **is_child_support_arrears**: true only if the order explicitly states arrears exceeding 12 weeks. Otherwise use null.
11. **is_head_of_household**: true only if the order or attached documentation identifies the debtor as head of household. Otherwise use null.
12. **supports_second_family**: true only if evidence of supporting a second family is documented. Otherwise use null.
13. **priority_position**: 0 if this is the only garnishment order and the document makes that clear. Otherwise set null unless a higher stack position is explicit.
14. **balance_remaining**: Total judgment balance remaining if stated.
15. **interest_rate_pct**: Annual interest rate as decimal (6% -> 0.06) if stated.
16. **creditor_name**: Name of the plaintiff or judgment creditor.
17. **issuing_court**: Full name of the issuing court.
18. **debtor_ssn_last4**: Last 4 digits of SSN if visible, often partially redacted.
19. **raw_text**: Include the full extracted text of the document for audit trail purposes.

IMPORTANT: If a field is not present or cannot be determined from the document, use null. Do NOT guess or infer values that are not explicitly stated. Court documents have precise legal meaning; accuracy matters more than completeness.

COMMON MISTAKES TO AVOID:
- Do NOT set ordered_amount to a processing fee, court cost, or administrative charge.
- If the order says withhold X% of disposable earnings, ordered_amount is null and ordered_percentage is the decimal value.
- Do NOT copy the effective date or filing date into expiration_date.
- The total judgment amount is not the ordered_amount. The ordered_amount is the per-pay-period withholding dollar figure, if any.
