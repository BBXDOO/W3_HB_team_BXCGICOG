# Agent Alignment Tests v2 — Planning Draft (Cast)

## เป้าหมาย
แนวทางเพิ่ม test & alignment สำหรับ Cast ในรอบ v2 สอดคล้องกับ role continuity/context bridge

---

## 1. จุดที่เรียนรู้จาก v1
- role “continuity_context” ยังตรวจแบบ presence
- test เรื่อง handoff/context bridge ขาด relation check
- ไม่มี test ว่า Cast สื่อสารกับ memory/agent อื่นอย่างไร

## 2. เป้าหมาย v2 สำหรับ Cast Agent
- เพิ่ม relation test: Cast <> ChatGPT, Cast <> DeepSeek
- ตัวอย่าง test: Cast สื่อสารหรือ handoff context ระหว่าง agent
- ตรวจว่า Cast ไม่หมายถึง governance/result

## 3. แนวทาง/test idea
- fixture: context chain/handoff ระหว่าง agent
- test Continuity: ตรวจว่า Cast สร้าง trace/context ได้จริง

## 4. สิ่งที่ไม่ควรเร่ง
- full semantic continuity/live context weaving
- memory virtualization ข้าม-agent

---

## หมายเหตุ
เติม test/idea/brainstorm ได้ตามสะดวก