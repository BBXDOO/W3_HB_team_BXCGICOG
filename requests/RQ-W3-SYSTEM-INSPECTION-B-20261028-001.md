---
request_id: RQ-W3-SYSTEM-INSPECTION-B-20261028-001
task_keyword: design
target_module: ChatGPT
requester: BBX19
request_type: runtime_circuit
language: th
priority: NORMAL
final_signoff_required: true
discussion_url: https://github.com/BBXDOO/W3_HB_team_BXCGICOG/issues/309
---

# ตรวจระบบขั้น B ผ่านตัวเชื่อมที่รันได้

BBX19 อนุญาตให้สร้างตัวเชื่อมเพื่อตรวจระบบต่อ เมื่อระบบใดสะดุดให้เก็บรายงาน
แยกแล้วตรวจระบบถัดไปที่ทำได้ ไม่ข้ามข้อกำหนดของระบบที่ตรวจไม่ผ่าน

ใช้ host executor ของ ChatGPT รัน fixed inspection profile แล้วให้ Gemini
ตรวจไฟล์ผล, hash, source inputs, JUnit counts และสถานะที่คำนวณซ้ำ
Orchestration เก็บวงจรและรอการตรวจรับรายงานรวมตาม final human gate เดิม

```w3-circuit
{
  "workflow": "system_inspection",
  "input": {"payload": {"inspection": "w3_systems_v1"}}
}
```

ตรวจ MPCP / E-CS / W3Lgu MFC Logic / Cross-X / CROLL / Table-X / PX
โดยเรียก native/contract/regression tests ที่ระบุไว้ใน catalog ของตัวเชื่อมจริง
แต่ละชุดรันในสำเนาแยก มี timeout และ input hashes ไม่มีการแก้ source ต้นทาง

ขอบเขตผลคือชุดตรวจที่ระบุและข้อมูลทดสอบ ไม่รับรองว่า production request เดียว
เดินเชื่อมครบเจ็ดระบบ ระบบที่ FAIL/BLOCKED/TIMEOUT/PARTIAL ยังคงเป็นเรื่องเปิด
แม้ตัวรวบรวมจะตรวจครบรายการและส่งรายงานสำเร็จ

ผลอ่านได้ที่ repo_events/system_inspections/latest.json ซึ่งชี้ไป run ที่มี
report.json, REPORT_TH.md, log/JUnit รายระบบ และ blockers/*.md แยกเรื่อง
รอบสรุป 3/7 วันอ่านเรื่องค้างจากหลักฐานนี้ โดยไม่รันงาน A เดิมซ้ำ

อ้างงาน A ที่ปิดแล้ว: requests/RQ-W3-SYSTEM-RECHECK-20261028-001.md
ไม่แก้ใบงาน A หรือใช้การอนุมัตินั้นอนุมัติ B โดยปริยาย
