# Request Routing Definition

Status: minimum baseline / non-executing

## Purpose

กำหนดเส้นทางขั้นต่ำสำหรับนำคำร้องจาก `requests/` ไปยังระบบหรือโมดูลที่ระบุ โดย Orchestration ทำหน้าที่ประสานและสร้างร่องรอย ไม่ทำงานแทนปลายทาง

## Route

`requests/ -> intake -> resolve participants -> assignment -> handoff -> target inbox -> collaboration -> result/evidence -> final sign-off`

## Participants

คำร้องหนึ่งรายการอาจมีหลายระบบร่วมกัน:
- Primary — เจ้าของงานหลักจาก `target_module`
- Partner — ระบบที่ร่วมวิเคราะห์หรือสร้างผลลัพธ์
- Observer — ระบบที่ตรวจดู/ให้หลักฐานโดยไม่รับอำนาจของ Primary
- Final decision node — ผู้มีอำนาจปิดคำร้อง

การมีชื่อในสายงานไม่โอน ownership หรือ authority โดยปริยาย

## Minimum request fields

- `request_id`
- `target_module`
- `requester`
- `request_type`
- `authority_requested`
- `final_signoff_required`
- `mutated`
- `review`

หาก `request_id` ขัดกับชื่อไฟล์ ให้หยุด route และขอ review แทนการเดา

## Evidence

ทุก handoff ควรรักษา `request_id` เดิมและอ้าง source request
ผลการส่งต่อ/รับทราบควรมี trace ใน `repo_events/` หรือ evidence surface ที่ระบบนั้นกำหนด
ผลลัพธ์ของคำร้องเก็บ/อ้างกลับผ่าน `requests/results/` เมื่อเหมาะสม

## Boundary

Router ส่งงาน ไม่ใช่ executor
ห้ามตีความ proposal เป็น approval
ห้ามเปลี่ยน source intent
ห้าม merge/deploy จาก routing เพียงอย่างเดียว
