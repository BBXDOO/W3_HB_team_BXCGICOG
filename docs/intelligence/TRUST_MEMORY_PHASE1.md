---
AM_TYPE: II
ROLE: DRAFT_DESIGN
GROUP: OBSERVE
DERIVED_FROM:
  - knowledge/philosophy/Selective_Input.md
OWNER: BBX19
---

# Trust Memory — Phase 1 (Design)

## Objective
Store trust-related signals in read-only mode for observability before automation.

## Data model (draft)
- actor_id
- scope (repo/module)
- signal_type (safe_merge, regression, rollback, review_quality)
- signal_score (-1..+1)
- timestamp
- evidence_ref

## Guardrails
- No auto-merge decisions in phase 1.
- Human review remains required for risky PRs.
