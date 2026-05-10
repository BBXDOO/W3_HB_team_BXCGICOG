# Agent Alignment Tests v2 — Planning Draft (Grok)

## เป้าหมาย
เตรียมแนวคิด ยกระดับ test & alignment ของ Grok กับ MPCP/W3 concept ในเฟส v2

---

## 1. จุดที่เรียนรู้จาก v1
- role “pattern/signals/insight” ยังเป็น declarative concept
- ยังไม่ test ว่า Grok เก็บ/สแกน pattern/insight จริง
- ไม่ได้ตรวจ overlap หรือ confuse กับ validation/governance

## 2. เป้าหมาย v2 สำหรับ Grok Agent
- ทำ test ที่ชี้ว่า Grok ตอบโจทย์ pattern-insight จริง
- ไม่ overlap การวิเคราะห์กับ validation หรือ flow/execution
- มี test ตรวจเชิงความสัมพันธ์ pattern-signal กับ agent อื่น

## 3. แนวทาง/script idea
- test ว่า Grok highlight signal/pattern + แนะนำ insight  
- ตรวจว่า Grok ไม่ดึง execution/govern decision
- ตัวอย่าง fixture: pattern ที่ agent อื่น (Gemini/Govern) สามารถ check ได

## 4. สิ่งที่ไม่ควรเร่ง
- self-discovery/insight generation cross-module
- pattern GT-graph/semantic network ใหญ่

---

## หมายเหตุ
ทีม continue/brainstorm ตามจริงได้