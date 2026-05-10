# Agent Alignment Tests v2 — Planning Draft (Gemini)

## เป้าหมาย
ร่างแนวคิดเตรียมยกระดับการทดสอบและ alignment ของ Gemini กับ MPCP/W3 concept สำหรับเฟส v2

---

## 1. จุดสำคัญที่เรียนรู้จาก v1
- Test alignment ยัง keyword-based
- role “validation” ยังไม่ได้ test ว่าสอดคล้อง logic จริง
- ยังไม่มี relation check ระหว่าง Gemini–Grok/Copilot-Gm เรื่อง validation หรือ cross-check

## 2. เป้าหมาย v2 สำหรับ Gemini Agent
- เพิ่ม test ตรวจพฤติกรรม validation/cross-check จริง (ไม่ใช่แค่มีคีย์เวิร์ด validation ใน docs)
- ตรวจว่า Gemini ไม่กลืนบทบาท governance, pattern-insight
- เชื่อมโยง test ระหว่าง Gemini กับ output ของ agent อื่น (validation flow)

## 3. แนวทาง/idea ที่อยากลองเพิ่ม
- สร้าง test ตรวจ pattern: Gemini รับ validation task = ต้องเรียกหรือ validate output ของ module อื่น
- ตรวจว่า Gemini ไม่ trigger governance หรือ execution decision
- Exploration: ทำ fixture ของ cross-agent validation (Gemini+Cast, Gemini+Grok)

## 4. สิ่งที่ยังไม่ควรเร่ง
- ยังไม่ต้องเขียน agent auto-adapt ตาม result cross-agent
- ยังไม่ต้องผูก Gemini กับ orchestrator/workflow controller จริง

---

## หมายเหตุ
ใส่ brainstorm/test idea เพิ่มเติมได้อิสระ