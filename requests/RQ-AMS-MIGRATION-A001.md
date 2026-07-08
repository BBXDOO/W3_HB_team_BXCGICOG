 requests/RQ-AMS-MIGRATION-A001.md

# Request — Architecture Mapping Standard Migration

ID: RQ-AMS-MIGRATION-A001

Status: Draft

Requester: BBX19

Scope:

- MPCP
- Registry
- Schema
- BOX
- WX

Mutation:

Structure Only

Core Meaning:

Preserve

---

## Objective

Introduce Architecture Mapping Standard (AMS)
into repository structures.

Purpose:

Reduce interpretation drift.

Increase traceability.

Preserve origin meaning during future upgrades.

---

## Required Actions

### Phase 1 — Governance

Add:

docs/governance/ARCHITECTURE_MAPPING_STANDARD.md

and establish repository-wide AMS definitions.

---

### Phase 2 — Metadata Support

Support metadata:

```yaml
AM_TYPE:
ROLE:
DERIVED_FROM:

for:

papers

specifications

blueprints

requests

architecture documents



---

Phase 3 — MPCP

Review:

protocol/mpcp/

Classify:

Core documents

Adaptation documents

Operational documents


Add AM metadata where appropriate.


---

Phase 4 — Registry

Extend registry structures to support:

{
  "am_type": "",
  "role": "",
  "derived_from": []
}

for architecture traceability.


---

Phase 5 — Schema

Review schema definitions.

Determine:

Core schema

Adaptation schema

Operational schema


where applicable.


---

Phase 6 — BOX / WX

Review:

wx/

Add architecture mapping support.

Suggested additions:

by_am_type index

architecture lineage references

source tracing



---

Acceptance Criteria

The request is considered complete when:

1. Governance document exists.


2. AM:I / AM:II / AM:III classifications are documented.


3. Registry supports architecture mapping metadata.


4. MPCP review is completed.


5. BOX/WX can trace operational structures back to origin meaning.


6. No AM:II or AM:III document redefines AM:I meaning.




---

Non-Goals

This request does not:

change philosophy

replace existing systems

modify runtime behavior


unless separately approved.


---

Expected Result

Future structures may evolve.

Origin meaning remains traceable.

Implementation remains reviewable.

Interpretation drift is reduced.

สองฉบับนี้แยกหน้าที่ชัดเจน:

- **Governance** = นิยาม AMS และกฎกลางของรีโป้
- **Request** = สั่งงาน MPCP / Registry / Schema / BOX / WX ให้รองรับ AMS โดยไม่แตะ Core Meaning โดยตรง

ซึ่งสอดคล้องกับหลัก `Core vs Structure` ที่คุณเขียนไว้เดิมค่อนข้างตรงครับ.
