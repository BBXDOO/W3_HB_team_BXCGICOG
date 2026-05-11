# Self-Healing Workflows Playbook (Guarded)

## Scope
Operational recoveries for known failure patterns only.

## Recovery flow
1. Detect known failure signature.
2. Apply bounded recovery action.
3. Re-run validation.
4. If still failing, escalate to human owner.

## Mandatory logging
- incident_id
- signature
- action_taken
- result
- rollback_applied
- reviewer
