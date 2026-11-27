Name : MPCP Orchestrator  
AM Ⅲ - BUILD : ตัวจัดการลำดับ flow และ step ผ่าน runtime executor; state SUCCESS/done ไปต่อ, WAIT พัก, STOP/fail/block หยุด และ lifecycle state ที่ไม่ใช่ผลปลายทางต้องไม่ถูกนับว่าสำเร็จ  
Log time : 2026-11-22 (date only; time not recorded) ; ID : MPCP-ORCHESTRATOR-README-001  
≡ Dr1ra - RAMS

## Body — ตัวตนของพื้นที่และขอบเขต

`protocol/mpcp/orchestrator/` — ตัวจัดการลำดับ flow และ step ผ่าน runtime executor; state SUCCESS/done ไปต่อ, WAIT พัก, STOP/fail/block หยุด และ lifecycle state ที่ไม่ใช่ผลปลายทางต้องไม่ถูกนับว่าสำเร็จ

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
  - protocol/mpcp/orchestrator/manager.py
DOCUMENT_PATH: protocol/mpcp/orchestrator/README.md
```

### หลักการอ่านและสิ่งที่ห้ามสับสน

- **ต้นทาง:** [manager.py](manager.py) เป็นแหล่งตรวจสอบข้อกำหนดหรือพฤติกรรมของพื้นที่นี้; การอธิบาย README ไม่แก้เนื้อหาต้นทาง
- **ขอบเขต:** การมีเอกสารหรือโค้ดไม่เท่ากับการอนุมัติ execution, deployment, persistence หรือการรับรองผลทดสอบ
- **การพิสูจน์:** แยก design claim ออกจาก implementation และ test evidence เสมอ; ให้ตรวจผลทดสอบเฉพาะชุดที่เกี่ยวข้องก่อนสรุปสถานะ
- **ความต่อเนื่อง:** รักษาความต่างระหว่าง Structure, Meaning, Paper, ROT และ Runtime ตามกติกาของ MPCP ไม่ให้ README นี้นิยามระบบอื่นแทนเจ้าของ

## Movement — แผนที่และเส้นทางอ้างอิง

### M1 — รายการภายใน `orchestrator/`

| รายการ | บทบาท |
|---|---|
| [README.md](README.md) · `≡ Dd1ra - mpcp` | AMS README ของพื้นที่ |
| [__init__.py](__init__.py) · `≡ Dc1_i - mpcp` | Python module / implementation |
| [flow.py](flow.py) · `≡ Dc2fo - mpcp` | Python module / implementation |
| [manager.py](manager.py) · `≡ Dc3mn - mpcp` | เอกสาร/โค้ดต้นทางหลัก |

### M2 — เอกสารภายนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [MPCP README](../README.md) | แผนที่ระบบแม่ |
| docs.origin | [MPCP Origin](../MPCP_ORIGIN.md) | ความหมายต้นทาง |
| docs.related | [เอกสาร/ระบบที่สัมพันธ์](../runtime/README.md) | จุดตรวจสอบความสัมพันธ์โดยไม่รวม authority |
| docs.core | [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md) | หลักรักษาความหมาย |
| docs.ams | [AMS Governance](../../../docs/governance/AMS.md) | กฎ AM และ Gradation |

---

OWNER : BBX19 — เจ้าของระบบ MPCP ตามเอกสารต้นทาง  
MAKER : ChatGPT / Codex — สร้างแผนที่ README ตาม AMS จากเอกสารและรายการไฟล์
