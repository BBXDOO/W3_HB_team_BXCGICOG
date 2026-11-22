Name : MPCP Kernel  
AM Ⅲ - BUILD : กฎ contract, ROT, system identity, registry, event template, module bridge และ validator; Contract ตรวจรูปขั้นต่ำ ส่วน ROT ตรวจ relation/boundary ของข้อมูลที่ normalize แล้ว ไม่ใช่ตัวแปลภาษา  
Log time : 2026-11-22 (date only; time not recorded) ; ID : MPCP-KERNEL-README-001  
≡ Cr1ra - RAMS

## Body — ตัวตนของพื้นที่และขอบเขต

`protocol/mpcp/kernel/` — กฎ contract, ROT, system identity, registry, event template, module bridge และ validator; Contract ตรวจรูปขั้นต่ำ ส่วน ROT ตรวจ relation/boundary ของข้อมูลที่ normalize แล้ว ไม่ใช่ตัวแปลภาษา

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
  - protocol/mpcp/kernel/contract.py
DOCUMENT_PATH: protocol/mpcp/kernel/README.md
```

### หลักการอ่านและสิ่งที่ห้ามสับสน

- **ต้นทาง:** [contract.py](contract.py) เป็นแหล่งตรวจสอบข้อกำหนดหรือพฤติกรรมของพื้นที่นี้; การอธิบาย README ไม่แก้เนื้อหาต้นทาง
- **ขอบเขต:** การมีเอกสารหรือโค้ดไม่เท่ากับการอนุมัติ execution, deployment, persistence หรือการรับรองผลทดสอบ
- **การพิสูจน์:** แยก design claim ออกจาก implementation และ test evidence เสมอ; ให้ตรวจผลทดสอบเฉพาะชุดที่เกี่ยวข้องก่อนสรุปสถานะ
- **ความต่อเนื่อง:** รักษาความต่างระหว่าง Structure, Meaning, Paper, ROT และ Runtime ตามกติกาของ MPCP ไม่ให้ README นี้นิยามระบบอื่นแทนเจ้าของ

## Movement — แผนที่และเส้นทางอ้างอิง

### M1 — รายการภายใน `kernel/`

| รายการ | บทบาท |
|---|---|
| [README.md](README.md) | AMS README ของพื้นที่ |
| [__init__.py](__init__.py) | Python module / implementation |
| [co_module.py](co_module.py) | Python module / implementation |
| [contract.py](contract.py) | เอกสาร/โค้ดต้นทางหลัก |
| [event_template.py](event_template.py) | Python module / implementation |
| [module_bridge.py](module_bridge.py) | Python module / implementation |
| [module_registry.py](module_registry.py) | Python module / implementation |
| [module_validator.py](module_validator.py) | Python module / implementation |
| [rot.py](rot.py) | Python module / implementation |
| [system.py](system.py) | Python module / implementation |
| [validator.py](validator.py) | Python module / implementation |

### M2 — เอกสารภายนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [MPCP README](../README.md) | แผนที่ระบบแม่ |
| docs.origin | [MPCP Origin](../MPCP_ORIGIN.md) | ความหมายต้นทาง |
| docs.related | [เอกสาร/ระบบที่สัมพันธ์](../ROT_BASELINE.md) | จุดตรวจสอบความสัมพันธ์โดยไม่รวม authority |
| docs.core | [Core vs Structure](../../../knowledge/philosophy/corevsstructure.md) | หลักรักษาความหมาย |
| docs.ams | [AMS Governance](../../../docs/governance/AMS.md) | กฎ AM และ Gradation |

---

OWNER : BBX19 — เจ้าของระบบ MPCP ตามเอกสารต้นทาง  
MAKER : ChatGPT / Codex — สร้างแผนที่ README ตาม AMS จากเอกสารและรายการไฟล์
