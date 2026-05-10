# Agent Alignment Tests v2 — Planning Draft (DeepSeek)

## เป้าหมาย
ร่างแนวคิดเตรียมยกระดับ test & alignment ของ DeepSeek กับ MPCP/W3 concept รอบ v2

---

## 1. จุดที่เรียนรู้จาก v1
- role “planning/scale/structure” ยัง test แบบ flat concept list
- ไม่ test ว่า planning/scale แยกขอบเขตกับ execution/validation
- ยังไม่ได้ตรวจ relation กับ agent อื่นที่ต้องส่งต่องาน

## 2. เป้าหมาย v2 สำหรับ DeepSeek Agent
- เพิ่ม test ที่ curve ว่า DeepSeek process ขยาย scope หรือวางแผนจริง
- ตรวจว่าไม่ overlap กับ flow/execution (ChatGPT) หรือ validation (Gemini)
- มี test กรณี “handoff” concept

## 3. test idea ที่อยากเสริม
- test ว่า deep planning ของ DeepSeek ถูกรีพอร์ตเป็น result/blueprint, ไม่ใช่ runtime trigger
- ตรวจ cross-agent: DeepSeek ส่งแผนให้ใคร, agent ไหนหยิบ scope จาก DeepSeek
- fixture: planning-action ที่ต้องถูก validate ด้วย Gemini

## 4. สิ่งที่ไม่ควรเร่ง
- adaptive scalable agent/auto-planner
- cross-module handoff แบบ complex

---

## หมายเหตุ
ทีมเติม test/brainstorm เพิ่มได้เต็มที่