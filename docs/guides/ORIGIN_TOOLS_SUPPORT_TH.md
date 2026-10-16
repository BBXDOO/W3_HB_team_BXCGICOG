---
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - workflows/orchestration/README.md
  - tools/README.md
OWNER: BBX19
MAKER: ChatGPT
---

# เครื่องมือใน tools/ สำหรับงานสนับสนุน Origin

## หน้าที่

เครื่องมือใน tools/ มีไว้ให้โมดูลและเอเจนท์ใช้สนับสนุนงาน
Orchestration เป็นผู้ประสานและเรียกเครื่องมือที่เหมาะสม ไม่รับ ownership ของงานจาก Origin
การเข้าถึงเครื่องมือไม่ขยายสิทธิแก้ไฟล์ปลายทางโดยอัตโนมัติ

## การเชื่อมครั้งนี้

เมื่อไม่มีคู่ที่ทำงานได้ หรือ Origin ทำงานไม่สำเร็จ:

1. บันทึก blocker และเข้าสู่ ASSISTING ผ่าน Orchestration.assist()
2. ตัวเชื่อม tools/origin_support.py อ่าน receipt จริงของงาน
3. ตรวจสถานะไฟล์ปลายทางตาม operations โดยคำนึงถึงการแก้/ย้าย/ลบในงานเดียวกัน
4. เรียกฟังก์ชันของเครื่องมือเดิมใน tools/ ตามชนิดผลงาน
5. เก็บรายงาน *-support.json และคืน evidence ให้ Orchestration
6. ถ้าผ่าน ส่ง RETURNED กลับเจ้าของงาน; ถ้าไม่ผ่าน คง BLOCKED พร้อมเหตุผลและ next_steps

| เครื่องมือเดิม | การเรียกใช้ในตัวเชื่อม |
|---|---|
| check_portable_paths.py | path_problems() ตรวจพาธผลงาน; ข้อสังเกต portability เป็น REVIEW |
| validate_metadata.py | validate_file() ตรวจ Markdown ที่เป็นผลงาน/หลักฐานในขอบเขต |
| validate_modules.py | ModuleValidator.validate_module() เมื่อพาธนั้นเป็น module.json |

ตัวเชื่อมใช้สิทธิอ่านของ Origin เดิม; พาธที่ไม่มีสิทธิอ่านรายงานว่าไม่สามารถตรวจยืนยันได้
ไม่เรียก main() เพื่อสแกนทั้งรีโป้โดยไม่เกี่ยวกับงาน และไม่ execute เนื้อหาไฟล์ที่ตรวจ
เครื่องมืออื่นใน tools/ ยังใช้ผ่าน handler ที่เหมาะกับงานได้ตาม Orchestration contract เดิม
สามรายการนี้เป็นการเลือกใช้อัตโนมัติของตัวเชื่อมนี้ ไม่ใช่การจำกัดว่า Orchestration ใช้เครื่องมืออื่นไม่ได้
ตัวอย่างเดิมที่มีอยู่แล้วคือ W3 Document Allocator ซึ่งมี make_orchestration_handler()

## ดูหลักฐาน

ใต้ repo_events/origin_agents/<module>/collaboration/:

- *-support.json: owner_reason, checks, findings, tools_used, next_steps และ resolved
- W3-ORC-*.json: ประวัติ BLOCKED → ASSISTING → RETURNED หรือ BLOCKED
- *-review.json: ผลรายงานรวมและ support_status

resolved ของ support หมายถึงผ่านงานช่วยตรวจในขอบเขตนี้ ไม่รับรองคุณภาพทุกด้าน
owner ที่ FAILED ยังคง FAILED แม้เครื่องมืออ่าน log ได้สำเร็จ
เครื่องมือไม่แก้เนื้อหาต้นทางเอง งานที่ยังค้างจะติดตามใน state.followups

## งานปกติกับงานซ่อมจากรอบตรวจ

งานปกติใช้สิทธิ IDP/ENV เดิม ไม่ต้องสร้างรายงานซ่อมเพราะอยู่ใน core/ หรือ docs/architecture/
หากไม่มีสิทธิก็ยังถูก OriginFiles ปฏิเสธตามเดิม
งานซ่อมที่เสนอจากรอบตรวจระบุ payload.structural_repair=true และให้ BBX19 เลือกพาธจากรายงาน
สิทธิเพิ่มจากการเลือกนั้นเป็นสิทธิชั่วคราวเฉพาะใบงาน ไม่เปลี่ยน IDP ถาวร

## ขอบเขตที่ยังมี

การเชื่อมนี้ทำการตรวจผลและหาสาเหตุด้วยเครื่องมือเดิม ไม่เลือกวิธีซ่อมโค้ดทุกประเภทแทนมนุษย์
งานที่แก้ต่อไม่ได้ต้องคืนเหตุผลให้ผู้รับผิดชอบ ไม่รายงานสำเร็จเพื่อปิดวงจร

[กลับคู่มือ Origin](ORIGIN_COLLABORATION_TH.md)

Owner: BBX19 · Maker: ChatGPT · Log: 2026-10-16
