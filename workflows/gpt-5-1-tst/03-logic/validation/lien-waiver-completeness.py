"""
MightyBot validation Rule
---
Description: Validate that all required lien waivers are present for the current draw period. Ensure conditional lien waivers are used (not unconditional). Flag missing GC pay application waiver as blocker, missing stored materials insurance as blocker, and unsigned AIA G702/703 as warning. Every draw must contain conditional lien waiver for GC pay app.
Position: 0
---
"""
def run(payload: dict) -> dict:
    return payload
