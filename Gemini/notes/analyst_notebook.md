# 📒 Analyst Notebook (Gemini)

สมุดบันทึก brainstorm และข้อสังเกตรายวันของ Gemini  
**Rule:** บันทึกได้ทันทีที่พบ ไม่ต้องรอ evidence ครบ — แต่ต้องระบุว่า "hypothesis" หรือ "confirmed"

---

## 🧠 Ideas & Hypotheses

### [2026-05-08] Idea: Lightweight session log format สำหรับ agent
**ที่มา:** สังเกตว่า Cast protocol ไม่ถูกใช้ เพราะ format entry ซับซ้อน  
**Hypothesis:** ถ้ามี "minimal entry" (2-3 field แทน 8 field) → adoption จะสูงขึ้น  
**Status:** hypothesis — ต้องทดสอบกับ agent อื่น  

### [2026-05-08] Idea: Auto-validate agent workspace ใน CI
**ที่มา:** ปัญหา .gitkeep ว่างเปล่าใน notes/  
**Hypothesis:** ถ้า CI ตรวจว่า notes/ มีไฟล์จริงหรือเปล่า → agents จะ incentivized ให้เขียนมากขึ้น  
**Status:** hypothesis — ต้องพูดคุยกับ Copilot-Gm ก่อน implement

---

## 🔍 Daily Observations

### [2026-05-08] Agent workspace audit session
**สังเกต:** ทุก agent มี ENTRANCE.md สมบูรณ์ แต่ "living documentation" ไม่เกิด  
**Pattern:** โครงสร้างที่ดีไม่รับประกัน execution — ต้องมี habit + protocol  
**Confirmed:** ใช่ — ดู `docs/reports/AGENT_WORKSPACE_AUDIT.md` สำหรับ evidence ครบ  

### [2026-05-08] Cast protocol adoption
**สังเกต:** มีเพียง 1 session log entry จาก Copilot (bootstrap) — agent อื่นไม่เคยเขียน  
**Pattern:** Protocol ที่ดีแต่ไม่มี reminder/enforcement = protocol ที่ไม่ถูกใช้  
**Status:** confirmed issue — logged ใน `Gemini/notes/qa-issues.md`

---

## 📚 Reference Links

- Agent Workspace Audit: `docs/reports/AGENT_WORKSPACE_AUDIT.md`
- Workspace Guideline: `docs/guides/AGENT_WORKSPACE_GUIDELINE.md`
- Cast Protocol: `Cast/context/protocol.md`
- Core vs Structure: `knowledge/philosophy/corevsstructure.md`
