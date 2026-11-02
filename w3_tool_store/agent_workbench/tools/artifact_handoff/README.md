Name : Artifact handoff — งานสร้างและตรวจที่หยุดได้\
AM Ⅲ - BUILD / OBSERVE / LEARN / CONTINUE\
Log time : 2026-11-02 (Asia/Bangkok) ; ID : W3-ARTIFACT-HANDOFF-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body

หนึ่งงานมีจุดเริ่มและเงื่อนไขส่งมอบ: Cast สร้าง source report และ private pattern
แยกกัน แล้ว Gemini ตรวจตาม rules.json ที่ host กำหนดและคำนวณซ้ำจากไฟล์จริง
Orchestration เดิมบันทึก handoff/ack/result/verification และหยุดที่
WAITING_HUMAN ตามเงื่อนไขที่ตั้งไว้ก่อนเริ่ม ไม่ใช่ blocker ทางเทคนิค
ไม่มี human approval ที่สร้างขึ้นเอง และไม่เรียกทุกระบบเพียงเพื่อให้ครบรายชื่อ

เครื่องมือนี้ใช้ executor Python ภายใน ไม่ได้เรียกบริการ AI ภายนอก
static verification รับรองเฉพาะผลงานที่ตรวจ ไม่รับรองความหมายทุกอย่างในซอร์ส
หรือว่าการทำงานของระบบปลายทางทั้งหมดสำเร็จ

```sh
python -m w3_tool_store.agent_workbench.tools.artifact_handoff.runner \
  --output modules/ChatGPT/reports/handoffs/example-new-run \
  core/runtime/agents/cast.py core/runtime/capabilities/cast_structure.py
```

ข้อมูลเข้า: รายการไฟล์ในขอบเขตอ่านของ Cast และ output directory ใหม่
ผล: request/rules, handoffs, acks, results, task snapshot และ delivery.json
Cast artifacts อยู่ในพื้นที่ของ Cast โดยอ้างพาธและ hash กลับได้
หากตรวจไม่ผ่านให้ BLOCKED พร้อมหลักฐาน; output เดิมไม่ถูกรันซ้ำ
นี่เป็น host adapter ใช้ Orchestration transitions โดยตรง ไม่เปลี่ยนกฎของ
WorkflowRuntime หรืออนุมัติใบงานเก่าที่ค้างอยู่

## Movement

- [runner.py](runner.py) — สร้างงาน ส่งไม้ ตรวจไฟล์ และคืนผลงาน
- [Tools](../README.md) — กลับโต๊ะเครื่องมือ
- [Cast](../../../../modules/Cast/module.json) — ผู้ผลิต
- [Orchestration](../../../../workflows/orchestration.py) — สถานะและหลักฐาน

OWNER : BBX19\
MAKER : ChatGPT / Codex
