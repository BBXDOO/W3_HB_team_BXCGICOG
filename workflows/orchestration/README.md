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

## Runtime baseline

`workflows/orchestration.py` และ `workflows/orchestration_task.schema.json` เป็นคู่ runtime/ใบงานที่ใช้ได้แบบ explicit call; ยังไม่มี watcher ที่สแกน request อัตโนมัติ และไม่แทน `tools/request_cycle.py` ซึ่งเป็น bridge เดิมของ request.

ตัวเรียกสร้าง task ด้วย `new_task()` แล้วบันทึกด้วย `save(task, directory)`; ใช้ `advance()` ผ่านสถานะที่กำหนด, `route(..., notify=adapter)` ส่งใบงาน, และ `assist(..., handler=adapter)` เรียก specialist หรือ tool เมื่อบันทึก blocker แล้วเท่านั้น. Adapter คืนหลักฐานอ้างอิงจริงเป็น `evidence`; ผลของ support มี `resolved: bool`. Adapter ถูกส่งเข้ามาโดย caller จึงไม่มีการรันคำสั่งจาก payload โดยตรง.

`ROUTED` หมายถึงส่งถึง, `ACKNOWLEDGED` ต้องมีหลักฐานการรับ, `COMPLETED` ต้องผ่าน `VERIFYING` และมี evidence; ถ้า `human_review_required` ต้องมี `approve()` พร้อมตัวตนและหลักฐานก่อนปิด. `tier` บอกตำแหน่ง ไม่ใช้จัด priority. การแก้ source, merge, deploy และการตัดสินแทนมนุษย์อยู่นอกอำนาจนี้.

การเชื่อมต่อ request cycle ในอนาคตควรรักษา `request_id` ใน `source_id` และอ้างผลเดิมที่ `requests/results/` โดยไม่สร้างผลสำเร็จซ้ำ. ตัวเรียกต้องจัดการการล็อกและ retry เมื่อต้องมีผู้เขียนพร้อมกันหลายตัว; `save()` ให้เพียง atomic snapshot ต่อครั้ง.


## Request Routing Baseline

คำร้องจาก `requests/` สามารถถูกประสานไปยัง Primary, Partner และ Observer หลายระบบโดยรักษา `request_id` และ source เดิม เพื่อสร้างประวัติการร่วมงานที่ตรวจย้อนกลับได้

- Route definition: `definitions/REQUEST_ROUTING.md`
- Collaboration assignment: `assignments/REQUEST_COLLABORATION.md`
- Handoff template: `templates/REQUEST_HANDOFF.md`

Baseline นี้กำหนด contract และเส้นทาง โดย runtime bridge ใช้งานผ่าน `tools/request_cycle.py` เพื่อ:

- ส่งต่อคำร้องไปยัง module ปลายทางที่ระบุ (พร้อม normalize ชื่อโมดูลที่มีสัญลักษณ์ต่างรูปแบบ)
- สร้างผลลัพธ์ที่ `requests/results/` และ trace event ที่ `repo_events/`
- บันทึก Check-in ทุกคำร้องที่ `logs/check-in/` และเขียน request log ที่ `logs/request_cycle/`
