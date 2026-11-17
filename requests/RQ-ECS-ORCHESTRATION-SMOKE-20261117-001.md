---
request_id: RQ-ECS-ORCHESTRATION-SMOKE-20261117-001
task_keyword: design
target_module: ChatGPT
requester: BBX19
request_type: runtime_circuit
language: th
priority: NORMAL
final_signoff_required: true
---

# ตรวจการกระตุ้น Orchestration และ E-CS ผ่าน Root Request จริง

งานทดสอบหนึ่งใบ เพื่อพิสูจน์ว่า GitHub push ที่เพิ่ม requests/*.md กระตุ้น W3 Request Cycle, pending intake อ่านใบงานนี้, Orchestration ส่งต่อให้ host executor, และบันทึกหลักฐาน E-CS native กับ Cross-X ตามชุดตรวจที่ลงทะเบียนแล้ว

ใช้ workflow system_inspection เดิมเท่านั้น: ChatGPT host executor เรียก fixed inspection profile และ Gemini ตรวจหลักฐานอีกชั้นหนึ่ง ห้ามขยายสิทธิ์หรืออ้างว่าเป็น production end-to-end chain

```w3-circuit
{
  "workflow": "system_inspection",
  "input": {"payload": {"inspection": "w3_systems_v1"}}
}
```

## เกณฑ์รับผล

1. พบ GitHub Actions run ของ W3 Request Cycle ที่เกิดจาก commit เพิ่มใบงานนี้ (ถ้า workflow ไม่ถูกกระตุ้น ต้องรายงานว่า NOT_TRIGGERED)
2. พบ requests/results/RQ-ECS-ORCHESTRATION-SMOKE-20261117-001_RESULT.json และ runtime_circuit task/evidence ที่อ้าง request_id เดียวกัน
3. รายงาน system_inspections run ใหม่แสดง E-CS suite tests/test_ecs_native_inspection.py และ tests/test_event_chain.py พร้อมผล JUnit และ input hashes
4. Gemini verifier ตรวจ evidence; final state อาจ WAITING_HUMAN ไม่ถือว่า APPROVED
5. แยกผลว่า native E-CS/Cross-X contract tests ผ่านออกจากการส่งงานจริง W3-API -> E-CS -> downstream; ไม่กล่าวอ้างว่าเส้นทาง production ครบหากไม่มี handoff evidence

ห้ามแก้ source implementation, deploy, หรืออนุมัติ human gate โดยอัตโนมัติ
