# ☢️ Risk Scan Register

| Risk ID | Description (ความเสี่ยง) | Probability (โอกาสเกิด) | Impact (ผลกระทบ) | Mitigation Strategy (แผนรับมือ) | Status |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **R-001** | Metadata Inconsistency | Med | High | ใช้ script `validate_metadata.py` บังคับก่อน merge | Active |
| **R-002** | Module Hallucination | Low | Med | ให้ Gemini ตรวจสอบ Cross-check ข้อมูลก่อนบันทึก | Monitor |
| **R-003** | Workflow Conflict | Med | Med | กำหนดลำดับการทำงานใน README ให้ชัดเจน | Active |

## 🛡️ Incident Log (บันทึกเหตุการณ์)
- **[Date]:** [Event detail...]
