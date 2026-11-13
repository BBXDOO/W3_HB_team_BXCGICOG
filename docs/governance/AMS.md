# Architecture Mapping Standard (AMS)
Architecture Mapping Standard
Status: Active Draft
Type: Governance
Layer: Core Governance

---

## Purpose

This document defines the minimum architecture mapping standard used by W3.

The purpose is not to control implementation.

The purpose is to preserve:

- origin meaning
- intent continuity
- architecture traceability
- interpretation consistency

across evolving structures.

---

## Core Principle

Structure may change.

Core meaning must remain traceable.

Every implementation must be able to explain:

- where it came from
- what it preserves
- what it adapts
- what it does not redefine

---

## Architecture Mapping Types

### AM:I — Core Meaning

Purpose:

Defines origin meaning, philosophy, intent, and identity.

Questions answered:

Why does this exist?

Examples:

- W3memoriea
- Core vs Structure
- Awareness Law
- Philosophy Papers

Rules:

- May define meaning.
- Must not define runtime behavior.
- May be referenced by all lower layers.
- Cannot be overridden by lower layers.

---

### AM:II — Adaptation Layer

Purpose:

Adapts origin meaning into a specific domain or strategy.

Questions answered:

How should this concept be applied in this context?

Examples:

- MPCP Color System
- Cross-X Strategy
- WHUB Architecture
- W3DB Relation Design

Rules:

- Must reference at least one AM:I source.
- May adapt behavior.
- Must preserve referenced meaning.
- Cannot redefine AM:I meaning.

---

### AM:III — Operational Layer

Purpose:

Implements executable workflows, runtime behavior, services, and processes.

Questions answered:

What happens now?

Examples:

- Runtime
- Agent
- Dashboard
- CRUD
- API
- Service

Rules:

- Must reference AM:I or AM:II sources.
- May optimize execution.
- May change implementation.
- Cannot redefine higher-layer meaning.

---

## Required Metadata

Every document should declare:

```yaml
AM_TYPE:
ROLE:
DERIVED_FROM:

Example:

AM_TYPE: II

ROLE: ADAPTATION

DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md


---

Traceability Rule

Every AM:III document must be traceable to:

AM:III → AM:II → AM:I

or

AM:III → AM:I

when no adaptation layer exists.


---

Interpretation Rule

Before interpreting a document:

1. Identify AM Type.


2. Identify source references.


3. Identify preserved meaning.


4. Interpret content.



Interpretation without layer identification is considered incomplete review.


---

## รหัสตำแหน่ง Gradation ใน Head บรรทัดที่ 4

ใช้รูป `Gradation : <ระดับ><ชนิด><ลำดับ><ชื่อย่อ> - <ระบบต้นทาง>` ในบรรทัดที่ 4 ของ Head สำหรับ README ที่ใช้รูปแบบนี้ ตัวอย่าง `Gradation : Cd4ra - screen_translator`

อ่านจากซ้ายไปขวา 4 ขั้น

1. **Gradation** — นับองค์ประกอบของพาธจากราก Git โดยให้ชื่อแรกใต้รากเป็น `A` แล้วเพิ่มหนึ่งระดับต่อองค์ประกอบจนถึงไฟล์ เช่น `w3_tool_store` = A, `screen_translator` = B, `README.md` = C
2. **Type** — ใช้ตัวพิมพ์เล็ก `f` สำหรับโฟลเดอร์ `d` สำหรับเอกสาร และ `c` สำหรับโค้ด README ใช้ `d` ในตัวอย่างนี้
3. **In folder** — นับจาก 1 ในกลุ่มชนิดเดียวกันของโฟลเดอร์แม่ สำหรับไฟล์ให้เทียบเฉพาะนามสกุลเดียวกัน เช่น `.md` หรือ `.py` แล้วต่อด้วยอักษรตัวแรกและตัวที่สามของชื่อก่อนนามสกุล ใช้ตัวพิมพ์เล็ก เช่น `README` → `ra` และ `loader` → `la`
4. **Base system** — ต่อท้ายด้วยชื่อระบบต้นทาง เช่น `mpcp`, `core` หรือ `screen_translator`

ตัวอย่างการอ้างอิงใช้รหัสคู่กับพาธ Git เมื่อส่งต่อข้ามพื้นที่ สำหรับตัวอย่างในเอกสารนี้ เรียงชื่อจากรายการไฟล์ที่ Git ติดตามตามลำดับอักขระแบบ `LC_ALL=C` ภายในกลุ่ม และนับ `__init__.py` เป็นไฟล์ `.py` ด้วย

| รหัส | พาธใน Git |
|---|---|
| `Dc2la - mpcp` | `protocol/mpcp/config/loader.py` |
| `Cc3eg - core` | `core/runtime/engine_v2.py` |
| `Cd4ra - screen_translator` | [`w3_tool_store/screen_translator/README.md`](../../w3_tool_store/screen_translator/README.md) |

เวลาอ่านรหัส ให้ใช้ระบบต้นทางจำกัดขอบเขต แล้วตรวจระดับ ชนิด ลำดับ และชื่อย่อกับรายการในโฟลเดอร์แม่ หากพบหลายพาธ ให้ใช้พาธเต็มประกอบ การเพิ่ม ลบ หรือเปลี่ยนชื่อไฟล์อาจเปลี่ยนลำดับในกลุ่ม จึงควรอ้าง commit ด้วยเมื่อต้องการย้อนตรวจรหัสของฉบับเดิม

---

Final Statement

Structure exists to support activity.

Core meaning exists to preserve identity.

Architecture Mapping exists to keep both connected.

---


## requests/RQ-AMS-MIGRATION-A001.md


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


สองฉบับนี้แยกหน้าที่ชัดเจน:

- **Governance** = นิยาม AMS และกฎกลางของรีโป้
- **Request** = สั่งงาน MPCP / Registry / Schema / BOX / WX ให้รองรับ AMS โดยไม่แตะ Core Meaning โดยตรง

ซึ่งสอดคล้องกับหลัก `Core vs Structure` ที่คุณเขียนไว้เดิมค่อนข้างตรงครับ.
