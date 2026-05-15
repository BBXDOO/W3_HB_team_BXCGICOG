# Usecase (ตัวอย่างกรณีการใช้งานจริง)

## กรณีที่ 1: สรุปข้อคิดเห็นประชุม
- **Task:** สรุปเรื่องประชุมทีม
- **Plan:** {"target": "จับใจความสำคัญ", "desc": "แยก Action item ออกมา"}
- **Context:** {"user": "เจ้าหน้าที่ทีมงาน", "urgency": "ปานกลาง"}
- **Agent:** ChatGPTAgent
- **Blueprint:** blueprints/Template_agent01.md
- **Document/Input:** "docs/meeting/meeting-2026-05-15.txt"
- **Output:** Markdown รายงานพร้อมหัวข้อ Action item

---

## กรณีที่ 2: วิเคราะห์ข้อมูลลูกค้า
- **Task:** วิเคราะห์เทรนด์จากข้อมูล
- **Plan:** {"target": "สรุปจุดเปลี่ยนยอดขาย", "desc": "แยกลูกค้าแต่ละกลุ่ม"}
- **Context:** {"user": "ทีม BI", "customer": "บริษัท A"}
- **Agent:** CastAgent
- **Document/Input:** "data/sale2025.csv"
- **Blueprint:** blueprints/SaleSummary.md
- **Output:** รายงานเชิงสถิติ & Recommendations

---

## กรณีที่ 3: ตรวจสอบข้อมูลแบบอัตโนมัติ
- **Task:** ตรวจสอบฟอร์แมตไฟล์นำเข้า
- **Plan:** {"target": "ตรวจรูปแบบ เทียบ spec", "desc": "ผิดประเภทต้องแจ้งเตือน"}
- **Context:** {"user": "QA"}
- **Agent:** ValidatorAgent
- **Document/Input:** "data/input/test-csv.csv"
- **Testcase:** "ส่งไฟล์ฟอร์แมตผิด ต้อง error"
- **Output:** สถานะ Validation + error log
