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
