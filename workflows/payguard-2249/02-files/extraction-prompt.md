# File Extraction Prompt

You are extracting data from a court-issued wage garnishment order. Extract all fields precisely as they appear in the document.

CRITICAL EXTRACTION RULES:
1. **state**: Extract the two-letter US state code from the court name or address (e.g., "Superior Court of California"  "CA", "District Court of Harris County, Texas"  "TX"). This is the most important field  it determines which garnishment law applies.
2. **case_number**: Extract the exact case/docket number as printed.
3. **debtor_name**: Full legal name of the employee/judgment debtor. Match exactly as printed on the order.
4. **employer_name**: Name of the employer/garnishee being served.
5. **order_type**: Classify as one of: CONSUMER_CREDITOR, CHILD_SUPPORT, TAX_LEVY, STUDENT_LOAN, BANKRUPTCY. Most civil judgments are CONSUMER_CREDITOR. Child support orders explicitly reference support obligations.
6. **ordered_amount**: Fixed dollar amount per pay period if specified (null if percentage-based).
7. **ordered_percentage**: Percentage of earnings if specified (null if fixed amount).
8. **effective_date**: Date garnishment takes effect in YYYY-MM-DD format.
9. **expiration_date**: Explicit end date if stated; null if "until further order of the court" or "until satisfied".
10. **is_child_support_arrears**: true ONLY if the order explicitly states arrears exceeding 12 weeks.
11. **is_head_of_household**: true ONLY if the order or attached documentation identifies the debtor as head of household.
12. **supports_second_family**: true ONLY if evidence of supporting a second family is documented.
13. **priority_position**: 0 if this is the only garnishment order; higher numbers for subsequent orders in a stack.
14. **balance_remaining**: Total judgment balance remaining if stated.
15. **interest_rate_pct**: Annual interest rate as decimal (6%  0.06) if stated.
16. **creditor_name**: Name of the plaintiff/judgment creditor.
17. **issuing_court**: Full name of the issuing court.
18. **debtor_ssn_last4**: Last 4 digits of SSN if visible (often partially redacted).
19. **raw_text**: Include the FULL extracted text of the document for audit trail purposes.

IMPORTANT: If a field is not present or cannot be determined from the document, use null. Do NOT guess or infer values that are not explicitly stated. Court documents have precise legal meaning  accuracy over completeness.
