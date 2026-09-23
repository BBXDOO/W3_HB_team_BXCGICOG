# Orchestration Workflow

- **AM type:** III Process
- **ID:** RN-F56 / GN-C / ASM-Space / OAS
- **Status:** scaffold / draft
- **Path:** `workflows/orchestration/`

## Role

พื้นที่สำหรับนิยาม แนวทาง และเครื่องมือที่ใช้ประสานการดำเนินงานระดับระบบของ W3

โครงสร้างนี้ยังไม่ประกาศอำนาจ Runtime และยังไม่ทำงานอัตโนมัติ ขอบเขตสุดท้ายจะกำหนดจากเอกสารออกแบบของ BBX19

## Movement

- **M1 — Contents:** definitions, guidelines, templates, assignments, handoffs, interventions
- **M2 — Evidence outputs:** `repo_events/`, `reports/`, `system_observations/`

## Boundaries

- เก็บนิยามและวิธีประสานงาน ไม่ใช้แทนหลักฐานเหตุการณ์
- ไม่แก้ไขหรือลบผลลัพธ์ต้นทาง
- การแต่งตั้งตัวแทนและการแทรกแซงต้องมีขอบเขต เหตุผล และร่องรอยตรวจสอบ
- Human authority และสัญญาของแต่ละระบบยังคงมีผล

## Owner

- **Owner:** BBX19
- **Maker:** W3 Human-AI Team
- **Log:** Git history


## Request Routing Baseline

คำร้องจาก `requests/` สามารถถูกประสานไปยัง Primary, Partner และ Observer หลายระบบโดยรักษา `request_id` และ source เดิม เพื่อสร้างประวัติการร่วมงานที่ตรวจย้อนกลับได้

- Route definition: `definitions/REQUEST_ROUTING.md`
- Collaboration assignment: `assignments/REQUEST_COLLABORATION.md`
- Handoff template: `templates/REQUEST_HANDOFF.md`

Baseline นี้กำหนด contract และเส้นทาง โดย runtime bridge ใช้งานผ่าน `tools/request_cycle.py` เพื่อ:

- ส่งต่อคำร้องไปยัง module ปลายทางที่ระบุ (พร้อม normalize ชื่อโมดูลที่มีสัญลักษณ์ต่างรูปแบบ)
- สร้างผลลัพธ์ที่ `requests/results/` และ trace event ที่ `repo_events/`
- บันทึก Check-in ทุกคำร้องที่ `logs/check-in/` และเขียน request log ที่ `logs/request_cycle/`
