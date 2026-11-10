[ต้นฉบับ](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/logs/logs-usage/logs-usage.md)

กรณีใช้งาน: บันทึกการใช้งาน IDP ทุกครั้งที่เปิดงานในหัวแชทว่างหรือโมดูลคู่

วางไฟล์นี้เป็นแม่แบบ แล้วค่อย copy → rename ตามวันที่ เช่น
logs/idp/2025-12-11-idp-usage.md
---

📄 แม่แบบ (พร้อมใช้งานทันที)
# W3 Hybrid — บันทึกการใช้งาน IDP
วันที่ (Date): __________
รหัสรายงาน (Report ID): W3-IDP-__________

---

## 1. ข้อมูลเซสชัน (Session Info)
- ผู้ใช้ (User): __________
- โมดูลที่เปิดใช้งาน (Module Activated): __________
- แสดง IDP แล้ว (IDP Presented): (Yes/No)
- บริบท (Context): __________
- ประเภทงาน (Task Type): __________   # เช่น OCR, JSON-Check, Research, Simulation
- เวลาเริ่มต้น (Start Time): __________

---

## 2. การตรวจสอบคู่โมดูล (Module Pair Check)
- โมดูลหลัก (Primary Module): __________
- โมดูลรอง (Secondary Module): __________
- การตรวจรับรองคู่ (Pair Validation): (Passed / Failed)
- หมายเหตุ (Notes): ________________________________________

---

## 3. การตรวจสอบ IDP (IDP Verification)
- ไฟล์ IDP ที่ใช้ (IDP File Used): __________
- เวอร์ชัน (Version): __________
- การตรวจสอบความสมบูรณ์ (Integrity Check): (OK / Warning / Fail)
- หมายเหตุ (Notes): ________________________________________

---

## 4. บันทึกการดำเนินงาน (Task Execution Log)
- ข้อมูลเข้า (Input): (คำอธิบายสั้น ๆ)
- ผลลัพธ์ (Output): (คำอธิบายสั้น ๆ)
- ปัญหาที่พบ (Issues Found): __________________________________
- ตรวจพบความเบี่ยงเบน (Drift Detected) (Grok): (Yes/No)
- ส่งต่อให้ Gemini (Escalated to Gemini): (Yes/No)

---

## 5. สถานะสุดท้าย (Final Status)
- ผลลัพธ์ (Result): (Success / Partial / Failed)
- เวลาสิ้นสุด (End Time): __________
- ระยะเวลา (Duration): __________ วินาที
- ผู้บันทึก (Logged By): __________

---

## 6. หมายเหตุเพิ่มเติม (Meta Notes)
หมายเหตุเพิ่มเติม:
________________________________________
________________________________________
