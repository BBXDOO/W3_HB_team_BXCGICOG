Name : MPCP Agent Sandbox — หลักฐานการรัน Local Setup  
AM Ⅲ - BUILD : ผลการทดสอบและหลักฐานจากการรันในพื้นที่ทดลอง  
Log time : 2026-11-25 (Asia/Bangkok; เวลาไม่ระบุ) ; ID : W3-AGENT-SANDBOX-EVIDENCE-README-001  
≡ Cr1ra - RAMS

## Body — ขอบเขตและที่มาของหลักฐาน

`tools/agent_sandbox/evidence/` เก็บสำเนาหลักฐานของการรัน **MPCP + W3Lgu Agent Sandbox — local setup** ตามที่บันทึกไว้ใน README ฉบับเดิมของโฟลเดอร์นี้ เอกสารนี้จัดรูปแบบการนำทางตาม RAMS โดย **ไม่ได้รันทดสอบซ้ำ** หรือรับรองความพร้อมของระบบเพิ่มเติม

### สภาพแวดล้อมที่บันทึกไว้

การรันเดิมใช้ source ที่แก้ในสาขา `feat/mpcp-agent-sandbox` โดยอ้าง base commit `5e4882cc379356d521ac2a589e0b9b8cc5028ffc` ไม่ใช่การรัน source ของ base commit ที่ยังไม่แก้

คำสั่งที่บันทึกว่าใช้จริง (แสดงเพื่อสอบย้อน ไม่ใช่คำสั่งที่รันในการแก้ README ครั้งนี้):

```sh
python tools/mpcp_sandbox.py --request tools/agent_sandbox/local_setup.json --output local_workspace/mpcp-baseline-20261024 --execute
```

### ผลที่บันทึกจากการรันเดิม

- ผลลัพธ์ `SUCCESS` และ manifest SHA-256 ตรงกับไฟล์ที่เขียนจริง
- สร้าง partition directories `A/B/C` ใน workspace ที่แยกไว้
- LRC2 มี 8 records สำหรับ event ขาเข้าและผลขาออก; ตรวจ hash chain ผ่าน
- original source และ snapshot hashes หลังรันตรงกับก่อนรัน
- `phase_ready:false` — **ไม่ใช่หลักฐานว่าระบบ W3 ทั้งระบบพร้อมใช้งาน**

ผลทดสอบเพิ่มเติมที่ README เดิมบันทึกไว้:

| การตรวจ | ผลตามบันทึกเดิม |
|---|---|
| `python -m pytest -q tests/test_mpcp_agent_sandbox.py tests/test_w3lgu_core.py tests/test_w3lgu_operational.py tests/test_w3lgu_event_field_logic27.py tests/test_w3lgu_mfc_logic.py` | 62 passed, 2 subtests passed; มี `datetime.utcnow` deprecation warnings 8 รายการ |
| `python protocol/mpcp/runtime_sanity_sweep.py` | 81/81 passed |
| `python protocol/mpcp/test_condien_blueprint.py` | 69/69 passed |

**ข้อจำกัดของหลักฐานเดิม:** ยังไม่ได้ตรวจ Android/Termux/iOS, ไม่ได้เรียก REA provider, ไม่ได้ตรวจ deployment และยังไม่มีผล CI ระยะไกล ณ เวลาสร้างหลักฐานนี้ ผลข้างต้นเป็นบันทึกในไฟล์ ไม่ใช่ผลการทดสอบใหม่ ณ วันที่จัดรูปแบบ README

## Movement — การนำทางและสอบย้อน

### M1 — สิ่งที่มีอยู่ในโฟลเดอร์นี้

| รายการ | ประเภท | เนื้อหาที่ตรวจพบ |
|---|---|---|
| [`README.md`](README.md) | เอกสาร | บริบท ผลที่บันทึก ข้อจำกัด และทางเดินไปยังหลักฐาน |
| [`local_setup_result.json`](local_setup_result.json) | JSON | ผลการรันที่บันทึก source hashes และ trace |
| [`setup.json`](setup.json) | JSON | Manifest ของ setup; ระบุ `AGENT_LOCAL`, `TARGET: local`, partitions `A/B/C`, libraries `file/storage` |
| [`worker.log`](worker.log) | Log | ลำดับสถานะ MPCP ตั้งแต่รับ input จน `RESULT:RETURN 'SUCCESS'` |

### M2 — เอกสารและจุดเรียกที่เกี่ยวข้องนอกโฟลเดอร์

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.sandbox | [Agent Sandbox README](../README.md) | คู่มือเครื่องมือ ขอบเขต สิทธิ์ และขั้นตอนตรวจซ้ำ |
| docs.request | [local_setup.json](../local_setup.json) | คำขอที่อ้างในคำสั่งรันเดิม |
| docs.cli | [mpcp_sandbox.py](../../mpcp_sandbox.py) | CLI ที่ระบุในคำสั่งรัน |
| docs.ams | [Architecture Mapping Standard](../../../docs/governance/AMS.md) | หลักการอ้างอิงและรหัส Gradation |
| docs.rams | [AMS README](../../../docs/box/AMS/AMS_README.txt) | รูปแบบ Head / Body / Movement / OWNER / MAKER |

ลิงก์ M2 เป็นจุดอ้างอิงเพื่อสอบย้อนเท่านั้น ไม่ได้ยืนยันการรันใหม่หรือสร้างสิทธิ์ในการ deploy, เปลี่ยนระบบ หรืออนุมัติเฟส

---

OWNER : BBX19 — อ้างอิงเจ้าของพื้นที่ W3 ตามเอกสารที่เกี่ยวข้อง  
MAKER : ChatGPT / Codex — จัดรูปแบบ README เป็น RAMS เมื่อ 2026-11-25; ไม่ใช่ผู้รับรองผลรันเดิม
