---
blueprint_id: BPD:BOX_KNOWLEDGE_INFRASTRUCTURE_V1
type: system
path: /wx
description: Planner-only knowledge reference infrastructure for W3
owner: BBX19
status: proposed
created_at: 2026-06-12
---

# BOX Knowledge Infrastructure v1.0

BOX is the W3 reference layer for locating templates, blueprints, and stable
knowledge without executing runtime systems or mutating source truth.

## Invariants

- Source templates and blueprints live once under `wx/`.
- Consumers copy a source into their own reviewed workspace before editing.
- Engine-Index and Indexor only read and recommend.
- PortDC exports registered content as data and never writes a destination.
- Creation/borrow/export events may be appended manually to `wx/log_info/`.
- Human review remains required.

## Non-goals

BOX is not a runtime, database, dynamic memory store, governance authority,
execution engine, or replacement for Cross-L/MPCP.
