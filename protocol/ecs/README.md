Name : E-CS — Event Chain System  
AM Ⅲ - BUILD : ชุดโค้ด event, template, cooperative contract, chain pointer และ integration สำหรับสร้างแผน Cross-X โดยไม่ถือว่าการสร้าง plan คือการ execute หรืออนุมัติงาน  
Log time : 2026-11-22 (date only; time not recorded) ; ID : ECS-README-001  
≡ Br1ra - RAMS

## Body — บทบาทและขอบเขต

ชุดโค้ด event, template, cooperative contract, chain pointer และ integration สำหรับสร้างแผน Cross-X โดยไม่ถือว่าการสร้าง plan คือการ execute หรืออนุมัติงาน

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/ecs/event_template.py
  - protocol/ecs/cooperative_contract.py
DOCUMENT_PATH: protocol/ecs/README.md
```

**ขอบเขต:** README นี้อธิบายเฉพาะ `protocol/ecs/` ไม่ขยายสิทธิ์ของระบบอื่นและไม่ยืนยันผลทดสอบที่ไม่ได้มีหลักฐาน

## Movement — การนำทาง

### M1 — รายการในโฟลเดอร์นี้

| รายการ | ประเภท |
|---|---|
| [README.md](README.md) | README / AMS |
| [chain_pointer_operator.py](chain_pointer_operator.py) | Python source / test |
| [cooperative_contract.py](cooperative_contract.py) | Python source / test |
| [event_chain_integration.py](event_chain_integration.py) | Python source / test |
| [event_chain_system.py](event_chain_system.py) | Python source / test |
| [event_registry.py](event_registry.py) | Python source / test |
| [event_template.py](event_template.py) | Python source / test |
| [versioned_registry.py](versioned_registry.py) | Python source / test |

### M2 — เอกสารอ้างอิงนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [พื้นที่ protocol](../README.md) | พื้นที่ protocol |
| docs.mpcp | [boundary ของ MPCP](../mpcp/README.md) | boundary ของ MPCP |
| docs.core | [หลักความหมายต้นทาง](../../knowledge/philosophy/corevsstructure.md) | หลักความหมายต้นทาง |
| docs.ams | [กฎ AMS](../../docs/governance/AMS.md) | กฎ AMS |

---

### บันทึกเนื้อหา README เดิม (รักษาข้อมูลต้นทาง)

# ECS Protocol Layer

**Status:** ACTIVE  
**Owner:** BBX19  
**Scope:** Event / Contract / Template / Chain Pointer

---

## Purpose

`protocol/ecs/` คือฝั่ง **Event Chain System (E‑CS)** ที่ทำหน้าที่สร้าง event, ตรวจสอบ payload, สร้าง cooperative contract, และแปลงเป็น Cross‑X plan โดยไม่ละเมิด boundary ของ MPCP

---

## File Structure

| File | Description |
|------|-------------|
| **cooperative_contract.py** | สร้าง contract ฝั่ง ECS สำหรับ event flow (RESPONSIBLE_MODULE, ASSIST_MODULES, CROSS_FIELD, TRACE, etc.) |
| **event_template.py** | กำหนด template ของ event, scope, required payload, allowed assist, และ hint สำหรับ Paper Pack / Cross‑X |
| **chain_pointer_operator.py** | อ่าน event ที่ผ่าน template แล้ว แปลงเป็น Paper Pack และ Cross‑X plan (ไม่ execute) |
| **event_chain_integration.py** | ตัวอย่างการรวมการทำงานระหว่าง ECS และ MPCP (event → contract → paper pack → cross‑x plan) |

---

## Flow Overview

```text
EventTemplate → validate payload
       ↓
ECSCooperativeContract → สร้าง contract ฝั่ง ECS
       ↓
ChainPointerOperator → สร้าง Paper Pack / Cross‑X plan
       ↓
Integration → ส่ง trace กลับ MPCP
```

---

OWNER : BBX19 — เจ้าของแนวคิด/ระบบตามข้อมูลต้นทาง  
MAKER : ChatGPT / Codex — ปรับ README ให้สอดคล้อง AMS โดยรักษาเนื้อหาเดิม
