Name : MPCP Case Studies — evidence and retrospective  
AM Ⅱ - BUILD : กรณีศึกษาและบทเรียนที่ต้องแยกจากผลทดสอบปัจจุบัน  
Log time : 2026-11-22 (date only; time not recorded) ; ID : MPCP-CASE_STUDIES-README-001  
≡ Dr2ra - RAMS

```yaml
AM_TYPE: III
ROLE: VALIDATION_EVIDENCE
DERIVED_FROM:
  - protocol/mpcp/ROT_BASELINE.md
DOCUMENT_PATH: protocol/mpcp/case_studies/README.md
```

# MPCP Case Studies

เอกสารในโฟลเดอร์นี้ใช้บันทึก กรณีศึกษา (case study) วิเคราะห์ผลการทดลองจริง การเปลี่ยนแปลงที่สำคัญ และบทเรียนจากการทำระบบทดสอบ alignment และ operational semantics ของโมดูลต่างๆ ใน ecosystem ของ W3/MPCP

**เป้าหมาย:**
- เก็บผลลัพธ์ (success/failure/ข้อควรระวัง) จากแต่ละรอบปรับปรุงชุด test หรือ runtime agent ไว้เป็นฐานความรู้
- สรุปสิ่งที่ทำได้ สิ่งที่ควรปรับ และข้อเสนอเพื่อ phase ถัดไป
- ป้องกัน concept drift — ทุกข้อผิดพลาดและข้อดีในอดีตควรถูกนำมากำหนดแผนการพัฒนาระดับ ecosystem

---

## รายการ Case Studies

- `AGENT_MPCP_ALIGNMENT_TESTS_V1.md`  
  กรณีศึกษาประสบการณ์รอบแรกของการเพิ่ม semantic alignment layer ให้ runtime agents, วิเคราะห์ข้อดี ข้อจำกัด และทิศทางแก้ไขถัดไป

---

## แนวทางการใช้

1. ก่อนวางแผนปรับ agent หรือ test หาความรู้จาก case studies ก่อน
2. ใช้บทเรียนจากที่นี่เป็น checklist/guide ในการออกแบบ phase ถัดไป
3. เมื่อทดลองหรือแก้ไขจริงภายใต้ MPCP/W3 แล้วพบ pattern ใหม่หรือปัญหาใหญ่ ให้เขียน case study ใหม่เพิ่มเสมอ

---

**หมายเหตุ:**  
เอกสารหลักของ concept/system อยู่ที่  
- `protocol/mpcp/mpcp_concept_paper/`  
- `protocol/mpcp/w3lgu_integration_paper/`

ส่วนที่นี่สำหรับ retrospective analysis, practical report, และ knowledge aggregation เท่านั้น

## Movement — ตรวจสอบรายการในพื้นที่ตาม Git

### M1 — รายการไฟล์ใน `case_studies/`

| รายการ | หน้าที่ |
|---|---|
| [AGENT_MPCP_ALIGNMENT_TESTS_V1.md](AGENT_MPCP_ALIGNMENT_TESTS_V1.md) · `≡ Dd1ae - mpcp` | จุดตรวจสอบหลัก |
| [README.md](README.md) · `≡ Dd2ra - mpcp` | README และ AMS map |

### M2 — ต้นทางและระบบที่เกี่ยวข้อง

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [MPCP](../README.md) | ระบบแม่ |
| docs.origin | [MPCP Origin](../MPCP_ORIGIN.md) | ความหมายต้นทาง |
| docs.rot | [ROT Baseline](../ROT_BASELINE.md) | ขอบเขตการควบคุมและการตรวจสอบ |
| docs.ams | [AMS](../../../docs/governance/AMS.md) | กฎ AMS |

---

OWNER : BBX19 — เจ้าของ MPCP ตามเอกสารเดิม  
MAKER : ChatGPT / Codex — ปรับ README ตาม AMS และรักษาคำอธิบายเดิม
