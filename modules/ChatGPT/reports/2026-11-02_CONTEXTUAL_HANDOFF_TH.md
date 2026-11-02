# งานหนึ่งชิ้น — สร้าง ส่งตรวจ ส่งคืน และหยุดตามบริบท

OWNER: BBX19 · MAKER: ChatGPT / Codex · 2 พฤศจิกายน 2026

## แก้เกณฑ์ที่ตีความผิดก่อนเริ่ม

BBX19 อธิบายว่าแต่ละระบบมีหน้าที่ต่างกันและใช้ความต่างสนับสนุนกัน
“เดินงานครบ” หมายถึงสร้างงาน/ปัญหา แบ่งงานหรือกระจายงานตามความจำเป็น
ให้อีกระบบตรวจตามกติกา แล้วหยุดที่ผลคาดหวังพร้อมตรวจย้อนกลับได้
ไม่ใช่เงื่อนไขให้คำร้องหนึ่งใบผ่านเจ็ดระบบหรือมี permanent chain

ดังนั้นข้อวินิจฉัยเดิมใน #309 ที่ว่าไม่มี single-task seven-system route
จึง BLOCKED ไม่ใช้เป็น acceptance criterion ต่อไป ผล native/regression เดิม
ยังเก็บเป็นหลักฐานตามขอบเขตของมัน ไม่แก้ hash หรือทำให้การรันทดสอบกลายเป็นงานผลิต

## งานที่เลือกและผลปลายทางที่กำหนดก่อนเริ่ม

สร้าง source inspection จากโค้ด Cast และ IDP v2 พร้อม private pattern แยกกัน
ให้คู่ตรวจตรวจจากไฟล์จริง แล้วคืนรายงานตรวจพร้อมกติกาและประวัติส่งไม้ให้ BBX19

จุดหยุดที่ระบุใน request/rules ก่อนผลิต: WAITING_HUMAN
ผลคาดหวังทางเทคนิค: VERIFIED พร้อมผลงานและร่องรอยทั้งหมด
ไม่มี human approval หรือคำสั่งให้เรียกระบบอื่นต่อโดยอัตโนมัติ

## แต่ละจุดทำอะไรและส่งอะไร

| ผู้ทำ | ทำอะไร/ด้วยอะไร | ส่งให้ใคร | ชื่อและรูปแบบ |
|---|---|---|---|
| Host ตามเจตนา BBX19 | ระบุงาน ไฟล์เข้า เกณฑ์ตรวจ และจุดหยุด | Orchestration | request.json / rules.json — JSON |
| Orchestration | บันทึก task/route/ack ก่อนลงมือ | Cast executor | Cast-handoff.json — request identity, source paths, rules path |
| Cast | อ่าน IDP/ไฟล์จริง ตรวจ AST และเขียน report แยก private pattern | ตัวรับของ Gemini | Cast-result.json — artifact paths/hash/trace; report และ pattern เป็น JSON คนละไฟล์ |
| Host verifier | อ่านผลงานที่บันทึกแล้ว คำนวณ hash และ AST ซ้ำตามกติกา | Gemini executor | checks list + artifact evidence; ไม่รับ PASS จากผู้ผลิต |
| Gemini | ตรวจ explicit checks และหลักฐานด้วย executor เดิม | Orchestration | Gemini-result.json — VERIFIED, checks, identity stamp |
| Orchestration | เก็บผลและคืนผลงานให้เจ้าของ แล้วหยุด | BBX19 | delivery.json + task snapshot; WAITING_HUMAN ตามเงื่อนไขก่อนเริ่ม |

Coordinator ใช้ workflows/orchestration.py จริง ไม่สร้างสถานะใหม่หรือเปลี่ยน
กฎ WorkflowRuntime เพื่อข้าม gate เป็น host adapter สำหรับงานตรวจ artifact
การขอ review ของ Cast ส่งให้คู่ตรวจทางเทคนิค; การตรวจรับสุดท้ายของมนุษย์ยังแยกไว้

## ผลที่เกิดจริง

- Cast สร้างผลงานสองไฟล์จริง และไม่ได้เขียนทับ source ที่อ่าน
- Gemini ตรวจ 15 checks ผ่านครบ; technical_result = VERIFIED
- source_id ผูก request, handoff ของทั้งสองบทบาท, ผลคืน และ task snapshot
- ประวัติ task มี Cast และ Gemini เป็นผู้รับไม้ตามบทบาท ไม่เรียกระบบอื่นให้ครบชื่อ
- ปลายทาง WAITING_HUMAN ตรง expected_stop_reached=true; automatic_continuation=false
- ไม่มีรายการ BLOCKED ทางเทคนิคในงานนี้ และไม่มี human_approval ที่สร้างแทน

[ผลส่งมอบ](handoffs/RQ-309-ARTIFACT-20261102-final/delivery.json)
[คำร้องก่อนเริ่ม](handoffs/RQ-309-ARTIFACT-20261102-final/request.json)
[กติกาตรวจ](handoffs/RQ-309-ARTIFACT-20261102-final/rules.json)
[ผลคู่ตรวจ](handoffs/RQ-309-ARTIFACT-20261102-final/Gemini-result.json)

ใน delivery มี task_snapshot ชี้ประวัติทั้งหมดและ artifacts ชี้ผลงานจริง
ไม่จำเป็นต้องเก็บเนื้อหาทุกอย่างซ้ำไว้ใน envelope เดียว

## สร้างปัญหาให้คู่ตรวจลองปฏิเสธด้วย

คัดลอกรายงานเป็น candidate แยก ลบรายการ Python symbols แล้วคำนวณ hash
ของไฟล์ candidate ใหม่ให้ตรงไฟล์ที่ผิด เพื่อทดสอบว่าแค่ hash ตรงไม่เพียงพอ
ไม่แตะรายงานต้นฉบับ

คู่ตรวจพบ structure ไม่ตรง source และความสัมพันธ์ pattern/report ไม่ตรง
คืน REVIEW_REQUIRED และ rejected=true; ไม่ปล่อย candidate นี้เป็นผลงานที่ตรวจผ่าน

[หลักฐานกรณีผิด](handoffs/RQ-309-ARTIFACT-20261102-final/negative-control.json)

## ความสามารถที่ได้และขอบเขต

เครื่องมือ reusable อยู่ใน Workbench: [artifact_handoff](../../../w3_tool_store/agent_workbench/tools/artifact_handoff/README.md)
ใช้ executor Python ของ Cast/Gemini และ Orchestration เดิม เป็นงานจริงใน local host
ไม่ได้เรียกบริการ AI ภายนอก ไม่ได้ทำ semantic proof ของทุกอย่างในซอร์ส
และไม่ได้สร้าง dependency chain ถาวรของ W3

ทดสอบกรณีปกติ, ไฟล์ถูกแก้, source เปลี่ยน, ปลอมโครงสร้างพร้อม hash ใหม่,
ปลอม rules, input หาย, output escape และห้าม replay output เดิม
ชุดที่รัน: unittest ของ handoff/Cast/agent contracts ผ่าน 37 ข้อ;
pytest ของ handoff/Cast/Orchestration/status intake ผ่าน 32 ข้อ
สองชุดมีรายการซ้ำกัน จึงไม่รวมเป็นจำนวนทดสอบไม่ซ้ำ

## สถานะ #309 / #306 หลังแก้ความเข้าใจ

- #309: เลิกใช้ “ต้องผ่านเจ็ดระบบในคำร้องเดียว” เป็น blocker
  งานตัวอย่างส่งมอบและตรวจเทคนิคผ่านแล้ว; คง OPEN เพื่อให้ BBX19 ตรวจรายงาน
  ตาม final sign-off เดิม ไม่คง OPEN เพราะขาด permanent chain
- #306: original attempt ยังคง superseded และเก็บประวัติไว้
  ส่วนงานที่รวมติดตามใน #309 ใช้ความหมายใหม่ ไม่รื้อ receipt เดิมมาทำซ้ำ
- งาน Vision/Cast Platform report เก่ามีเจตนาเฉพาะของมัน ไม่ใช้ตัวอย่างนี้ปิดแทน

วาระถัดไปตรวจผลที่ส่งมอบในรายงานนี้ได้โดยตรง ไม่ต้องอนุมัติงาน A/B เก่าซ้ำ
และไม่จำเป็นต้องสั่งให้ทุกระบบมารับไม้ในงานนี้
