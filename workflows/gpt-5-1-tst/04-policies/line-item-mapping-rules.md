---
priority: 50
updated_by: mukesh@mightybot.ai
---

How to map completed work to SOV lines, invoiced amounts, stored materials:

1. If a Draw Schedule / Budget or similar document is uploaded, use the draw request / work completed / request amount to populate each line item.
 
2. For AIA G702/703, determine if the budget is a roll-up meaning there is one line item that maps to the construction contract or if the budget is broken out by the individual line items in the 703 of the AIA Pay Application.
   - If the budget is rolled up, map the 'Current Payment Due, Line 8 from G702' to the Current Draw Request for the given Contract.
   - If the budget is broken out, map Column E of the G703 for each item in the SOV to the appropriate item in the budget.

3. For Hard and Soft Cost Invoices, map the item in the description to the corresponding item in the budget and the total invoice request for that item to the current draw request in the budget.

4. If there is a difference between the two values (Draw Schedule and/or Invoices/Pay Applications), call out that discrepancy and variance. Flag as a warning.
