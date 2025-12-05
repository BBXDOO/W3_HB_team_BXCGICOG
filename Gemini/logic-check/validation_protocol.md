# ✅ Logic Validation Protocol

**Target Object:** [ชื่อไฟล์ หรือ โมดูลที่กำลังตรวจสอบ]
**Validator:** Gemini

## 1. Syntax & Structure Check
- [ ] JSON format valid (No trailing commas)
- [ ] YAML front-matter valid
- [ ] File naming convention correct

## 2. Logic Consistency Check
- [ ] ข้อมูลในไฟล์ตรงกับความเป็นจริงในระบบ (Single Source of Truth)
- [ ] ไม่มีการอ้างอิงไฟล์ที่ไม่มีอยู่จริง (Broken Links)
- [ ] Flow การทำงานไม่เกิด Deadlock (ทางตัน)

## 3. Policy Compliance (Governance)
- [ ] มี `approved-by` และ `reason` ครบถ้วน (ถ้าเป็น Decision)
- [ ] สอดคล้องกับหลักการ W3 (Transparency, Hybrid)

## 📝 Validator Notes
