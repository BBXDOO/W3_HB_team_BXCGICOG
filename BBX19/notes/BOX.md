BOX.md

W3 Knowledge Infrastructure Blueprint

Library-WX / Indexor / Engine-Index / PortDC / WHUB Ready

Version: Draft v0.1
Status: Blueprint
Owner: BBX19
Scope: Planner-Only
Runtime: None
Mutated: False

---

1. Purpose

BOX คือ Infrastructure Layer สำหรับการจัดเก็บ อ้างอิง ค้นหา และสร้างองค์ความรู้ภายใน W3

BOX ไม่ใช่ Runtime

BOX ไม่ใช่ Database

BOX ไม่ใช่ Execution Engine

BOX คือโครงสร้างกลางสำหรับ

- Template
- Blueprint
- Knowledge
- Index
- Navigation
- Traceability

เพื่อให้มนุษย์ เอเจนท์ และระบบต่างๆ ใช้ร่วมกันได้ในระยะยาว

---

2. Concept Model

เปรียบเทียบ BOX เป็นโรงแรมขนาดใหญ่

Building

BOX

Floor

Collection

Room

Folder

Object in Room

File

Library

Library-WX

Librarian

Indexor Agent

Elevator

Engine-Index

Import / Export Counter

PortDC

Future External Hub

WHUB

---

3. Core Principles

P1 — Single Source of Truth

ไฟล์ต้นฉบับมีได้เพียง 1 ฉบับ

ทุกการใช้งานต้องอ้างอิงจากต้นฉบับ

ห้ามแก้ไขต้นฉบับโดยตรง

---

P2 — Copy Before Use

การใช้งาน Template

ต้อง

COPY

ก่อนเสมอ

ตัวอย่าง

Library-WX
↓
Template
↓
Copy
↓
Workspace
↓
Edit

ห้าม

Library-WX
↓
Edit Directly

---

P3 — Planner First

BOX ทำหน้าที่

- Suggest
- Locate
- Reference
- Trace

เท่านั้น

ไม่มีสิทธิ์ Execute

---

P4 — Human First

มนุษย์เป็นผู้ตัดสินใจขั้นสุดท้าย

Agent ทำหน้าที่เสนอ

ไม่ทำหน้าที่บังคับ

---

P5 — Traceability

ทุกการสร้างงานใหม่

ต้องสามารถย้อนกลับได้ว่า

- มาจาก Template ใด
- ใครร้องขอ
- สร้างเมื่อใด
- ใช้เพื่ออะไร

---

4. Architecture

W3
│
├─ WHUB (Future)
│
├─ PortDC
│
├─ BOX
│   │
│   ├─ Engine-Index
│   ├─ Library-WX
│   ├─ Registry
│   ├─ Log-Info
│   └─ Indexor Agent
│
├─ Cross-L
├─ MPCP
└─ Runtime Systems

---

5. Library-WX

Library-WX คือห้องสมุดกลาง

หน้าที่

- เก็บ Template
- เก็บ Blueprint
- เก็บ Reference Knowledge
- เก็บ Mapping

ไม่เก็บ Runtime State

ไม่เก็บ Dynamic Data

---

Structure

wx/

├── README.md

├── templates/
│
├── blueprints/
│
├── references/
│
├── registry/
│
├── index/
│
├── log_info/
│
└── collections/

---

6. Template System

Template คือแม่แบบ

Template มีหน้าที่

- กำหนดโครงสร้าง
- กำหนดหัวข้อ
- กำหนด Metadata

Template ไม่มีหน้าที่

- Execute
- Modify Runtime

---

Required Metadata

template_id:

version:

scope:

boundary:

deny:

owner:

status:

created_at:

---

7. Blueprint System

Blueprint คือคำอธิบายโครงสร้าง

Blueprint

สามารถอธิบาย

- Folder
- System
- Agent
- Collection
- Flow

Blueprint ไม่ Execute

Blueprint ไม่ Run

Blueprint เป็น Structural Declaration

---

8. Registry Layer

Registry คือสารบัญหลัก

Single Source of Metadata

---

registry/

template_registry.json

agent_registry.json

collection_registry.json

blueprint_registry.json

---

Registry ทำหน้าที่

- ระบุตำแหน่ง
- ระบุเจ้าของ
- ระบุสถานะ
- ระบุเวอร์ชัน

---

9. Engine-Index

Engine-Index คือ Elevator

หน้าที่

- ค้นหา
- นำทาง
- เชื่อมโยง
- จัดอันดับผลลัพธ์

ไม่ตีความ

ไม่สร้างเอกสาร

ไม่แก้ไขไฟล์

---

Input

- PX
- Intent
- Work Type
- Template ID

Output

- Path
- Registry Entry
- Suggested Resources

---

10. Indexor Agent

Indexor Agent คือบรรณารักษ์

หน้าที่

- อ่าน Registry
- อ่าน Index
- อ่าน Collection

จากนั้นแนะนำ

- Template
- Blueprint
- Knowledge

ที่เหมาะสม

---

Indexor ไม่มีสิทธิ์

- Execute
- Patch
- Modify Truth

---

11. Index System

Index คือแผนที่

index/

by_px.md

by_work_type.md

by_agent_role.md

by_collection.md

---

ตัวอย่าง

PX
↓
Work Type
↓
Template
↓
Collection
↓
Location

---

12. Log-Info

Append Only

ไม่มีการลบ

ไม่มีการแก้ย้อนหลัง

---

log_info/

requests.jsonl

activities.jsonl

creation.jsonl

---

ต้อง Log เมื่อ

- Create
- Generate
- Borrow
- Export

ไม่ต้อง Log เมื่อ

- Read
- Learn
- Study

---

13. PortDC

PortDC

Document Channel

Input / Output Gateway

---

Input

External Request

↓

PortDC

↓

BOX

---

Output

Document

Blueprint

Reference

Template

---

PortDC ไม่มีสิทธิ์

Execute

Mutate

Patch

---

14. Collections

Collection เปรียบเหมือนชั้นของอาคาร

แต่ละ Collection

มี README ของตนเอง

---

Collection Rule

README

↓

Folder

↓

Files

---

กฎทั้งหมดของไฟล์

สืบทอดจาก

README

ของ Collection

---

15. WHUB Ready

BOX ต้องรองรับ WHUB ในอนาคต

WHUB

ทำหน้าที่เชื่อม

- Library
- Collection
- External Node
- Knowledge Hub

---

WHUB ไม่มีสิทธิ์แก้ไขต้นฉบับ

ใช้ Reference เท่านั้น

---

16. Lifecycle

Need

↓

Search

↓

Indexor

↓

Engine-Index

↓

Locate Template

↓

Copy Template

↓

Create New Content

↓

Log Creation

↓

Deliver

---

17. Non Goals

BOX ไม่ใช่

- Runtime
- Database
- Execution Engine
- Memory Store
- State Manager
- Governance System

---

18. Definition

BOX

Knowledge Infrastructure

Library-WX

Knowledge Repository

Indexor

Reference Librarian

Engine-Index

Navigation System

PortDC

Document Gateway

WHUB

Future Knowledge Network

Template

Reusable Source

Blueprint

Structural Declaration

Registry

Metadata Source of Truth

Log-Info

Creation Trace System

---

Final Principle

One Source

Many References

No Direct Mutation

Copy Before Use

Trace Before Trust

Human Before Runtime
