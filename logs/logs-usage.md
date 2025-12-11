Use case: บันทึกการใช้งาน IDP ทุกครั้งที่เปิดงานในหัวแชทว่างหรือโมดูลคู่

วางไฟล์นี้เป็นแม่แบบ แล้วค่อย copy → rename ตามวันที่ เช่น
logs/idp/2025-12-11-idp-usage.md
---

📄 TEMPLATE (พร้อมใช้งานทันที)
# W3 Hybrid — IDP Usage Log
Date: __________
Report ID: W3-IDP-__________

---

## 1. Session Info
- User: __________
- Module Activated: __________
- IDP Presented: (Yes/No)
- Context: __________
- Task Type: __________   # เช่น OCR, JSON-Check, Research, Simulation
- Start Time: __________

---

## 2. Module Pair Check
- Primary Module: __________
- Secondary Module: __________
- Pair Validation: (Passed / Failed)
- Notes: ________________________________________

---

## 3. IDP Verification
- IDP File Used: __________
- Version: __________
- Integrity Check: (OK / Warning / Fail)
- Notes: ________________________________________

---

## 4. Task Execution Log
- Input: (Short description)  
- Output: (Short description)  
- Issues Found: __________________________________
- Drift Detected (Grok): (Yes/No)
- Escalated to Gemini: (Yes/No)

---

## 5. Final Status
- Result: (Success / Partial / Failed)
- End Time: __________
- Duration: __________ seconds
- Logged By: __________

---

## 6. Meta Notes
Additional Notes:
________________________________________
________________________________________
