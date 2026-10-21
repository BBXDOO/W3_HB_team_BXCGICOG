# Request Routing Definition

Status: executable request bridge; registered flows and explicit stage plans supported

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

## Check-in

ทุก request ต้องมีการลงชื่อรับงานในเอกสาร Check-in ที่ `logs/check-in/`

- รูปแบบเอกสาร: `DOCS - ID : CID_@R000A1`
- 1 เอกสารรองรับ 50 request (`NO.1` ถึง `NO.50`)
- เมื่อครบ 50 รายการ ให้เปิดเอกสารใหม่โดยเพิ่มเลขท้าย ID (`A1 -> A2 ... -> A50`)
- เมื่อครบ `A50` ให้เปลี่ยน prefix ตัวอักษรเป็นลำดับถัดไปและเริ่มเลขใหม่ (`B1`, `B2`, ...)
- หลังจบงานต้องมี request log แยกใน `logs/request_cycle/`

## Boundary

Router ส่งงาน ไม่ใช่ executor
ห้ามตีความ proposal เป็น approval
ห้ามเปลี่ยน source intent
ห้าม merge/deploy จาก routing เพียงอย่างเดียว

## Executable planning and support

`runtime_circuit` รองรับ `stages` หรือ `workflow` ที่ host ลงทะเบียน ผ่าน `tools/runtime_circuit_intake.py`. ทะเบียน workflow เรียง dependency ก่อนบันทึกแผนจริง. เมื่อ BLOCKED ใช้ `WorkflowRuntime.support_for()` เลือก tools/specialist ตาม capability และตรวจผลก่อน RETURNED; ดู [คู่มือ](../../../docs/guides/ORCHESTRATION_CAPABILITY_SUPPORT_TH.md). Primary/Partner/Observer assignment ยังคงเป็น contract; ไม่ใช่ทุกบทบาทในเอกสารจะถูกค้นหาและเรียกอัตโนมัติ.
