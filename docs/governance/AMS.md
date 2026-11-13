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

## รหัสตำแหน่ง Gradation

ใช้สัญลักษณ์ `≡` แทนคำว่า Gradation หน้ารหัส ตัวอย่างเดียวกันเขียนได้สองแบบตามตำแหน่งที่ใช้

| ตำแหน่งที่ใช้ | รูปแบบ | ตัวอย่าง |
|---|---|---|
| Head บรรทัดที่ 4 ของ README | `≡ <ระดับ>r<ลำดับ><ชื่อย่อ> - RAMS` | `≡ Cr4ra - RAMS` |
| แผนผัง | `≡ <ระดับ><ชนิด><ลำดับ><ชื่อย่อ> - <ระบบต้นทาง>` | `≡ Cd4ra - screen_translator` |

ใน Head ตัว `r` ระบุว่าไฟล์คือ README และ `RAMS` ระบุว่า README นี้ใช้รูปแบบ AMS โดย `R` หมายถึง README ในแผนผังใช้ชนิดทั่วไป `f` (โฟลเดอร์), `d` (เอกสาร), `c` (โค้ด) จึงจัด README ไว้ในชนิด `d` และระบุชื่อระบบต้นทางท้ายรหัส

### วิธีสร้างและอ่านรหัส

1. **Gradation** — นับองค์ประกอบของพาธจากราก Git โดยให้ชื่อแรกใต้รากเป็น `A` เช่น `w3_tool_store` = A, `screen_translator` = B, `README.md` = C
2. **Type** — เลือกชนิดตามตำแหน่งที่ใช้ สำหรับ README เดียวกันให้ใช้ `r` ใน Head และ `d` ในแผนผัง
3. **In folder** — นับจาก 1 ในกลุ่มเดียวกันภายในโฟลเดอร์แม่ สำหรับไฟล์ให้นับเฉพาะนามสกุลเดียวกัน เช่น `.md` หรือ `.py` แล้วต่อด้วยอักษรตัวแรกและตัวที่สามของชื่อก่อนนามสกุลในรูปตัวพิมพ์เล็ก เช่น `README` → `ra` ดังนั้น `r` ใน Head ยังคงใช้ลำดับที่ 4 จากกลุ่ม `.md` ของตัวอย่างนี้
4. **ส่วนท้าย** — ใช้ `RAMS` ใน Head ของ README และใช้ชื่อระบบต้นทางในแผนผัง เช่น `mpcp`, `core` หรือ `screen_translator`

### วิธีอ้างอิง

อ่านรหัสใน Head ควบคู่กับพาธของ README ส่วนรหัสในแผนผังใช้ชื่อระบบท้ายรหัสจำกัดพื้นที่ค้น แล้วตรวจระดับ ชนิด ลำดับ และชื่อย่อกับรายการในโฟลเดอร์แม่ หากพบหลายพาธ ให้ระบุพาธเต็มประกอบ การเพิ่ม ลบ หรือเปลี่ยนชื่อไฟล์อาจเปลี่ยนลำดับ หากต้องย้อนตรวจรหัสฉบับเดิม ให้ระบุ commit ด้วย

ตัวอย่างนี้เรียงชื่อจากรายการที่ Git ติดตามแบบ `LC_ALL=C` ภายในกลุ่ม และนับ `__init__.py` ในกลุ่ม `.py` ด้วย

| รหัสในแผนผัง | พาธใน Git |
|---|---|
| `≡ Dc2la - mpcp` | `protocol/mpcp/config/loader.py` |
| `≡ Cc3eg - core` | `core/runtime/engine_v2.py` |
| `≡ Cd4ra - screen_translator` | [`w3_tool_store/screen_translator/README.md`](../../w3_tool_store/screen_translator/README.md) |

---

## Final Statement

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
