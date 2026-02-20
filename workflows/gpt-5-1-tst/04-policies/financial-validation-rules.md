---
updated_by: mukesh@mightybot.ai
---

Variance thresholds, retainage calculations:

1. If there is an Invoice Log, look for a discrepancy between the individual Invoice Document and the amount for that invoice in the Invoice Log. Flag any discrepancies as a warning.

2. The summary amounts on the G702 should match the sum of line items on the G703. Flag any issues as a warning.

3. No individual line items exceed the remaining to fund balances for that line item. If one does, flag as a warning.

4. The retainage withheld must match the required percentage applied to that line item. If no percentage is outlined, then there is no issue. If a percentage is outlined, and the amounts don't match, flag as a warning.

5. If the draw includes reallocations across line items that are greater than 5% of the budget, flag as a warning.
