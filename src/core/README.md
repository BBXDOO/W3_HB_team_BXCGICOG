Name : W3 Core — Condien / Blueprint foundations\
AM Ⅲ - BUILD : โครงข้อมูล บริบท และอุปกรณ์จัดเก็บ Condien\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : W3-CORE-CONTEXT-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาท

Condien รักษาความหมาย สถานะ บริบท และความต่อเนื่องผ่าน layer ที่มีสิทธิ์อ่านชัดเจน Blueprint เก็บแบบแผนที่ประกาศไว้ ส่วน CondienStore เป็นอุปกรณ์เสริมให้บริบทอยู่ข้ามการหยุด–เริ่ม process ไม่เปลี่ยน Condien ให้เหลือเพียงตารางข้อมูล

```yaml
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
  - protocol/mpcp/w3lgu_integration_paper/W3LGU_CONDIEN_PROFILE.md
  - protocol/mpcp/w3lgu_integration_paper/W3LGU_MPCP_BLUEPRINT_PROFILE.md
```

### รูปแบบที่แยกหน้าที่กัน

- `Condien.to_dict()` / `to_w3lgu()` เป็น identity/inspection/profile ตามของเดิม ไม่กลายเป็น dump ข้อมูลทั้งระบบ
- `to_state()` / `from_state()` เป็นรูปเต็มสำหรับ trusted storage เก็บ payload ของทุก layer รวม READ/DENY ระดับ layer/key, active layer, carry, history และชื่อบริบทก่อนหน้า
- Runtime อ่านผ่าน `scope_condien()` และ access law ของ Condien เท่านั้น การโหลดจาก storage ไม่ยกเลิกสิทธิ์ที่บันทึกไว้

### การเก็บและเรียกคืน

`CondienStore(path)` ใช้ SQLite ใน standard library บันทึกแต่ละ revision เป็นแถวใหม่ พร้อม snapshot hash ของ state/identity/revision/ลิงก์ก่อนหน้า ไม่แก้ snapshot เก่า

```python
from pathlib import Path
from src.core.condien import Condien
from src.core.condien_store import CondienStore

store = CondienStore(Path("local_workspace/context.sqlite"))
context = Condien("REPORT", layers=["B"], continuity="carry-forward")
context.write_layer("B", "title", "report context")
context.carry("next", "continue")
first = store.save(context)  # expected_revision=0: สร้างชื่อใหม่
restored = store.load("REPORT")
assert restored.condien.recall("next") == "continue"
```

เมื่อบันทึก revision ถัดไป ต้องส่ง `expected_revision` ที่อ่านมา หากมีคนบันทึกใหม่ก่อนจะเกิด conflict โดยไม่เขียนทับ การเลือก `load(name, revision=...)` อ่านรุ่นเดิมได้ `versions(name)` แสดงรายการรุ่นและลิงก์ ส่วน `load_snapshot(id)` เลือกหลักฐานเฉพาะรุ่น

หากใช้ `carry_forward_from()` ให้บันทึกต้นทางก่อน แล้วระบุ `previous_snapshot_id` ของต้นทางตอน save ปลายทาง อุปกรณ์ตรวจชื่อและ state ของต้นทางให้ตรง ไม่อ้างว่าบันทึกการเปลี่ยนแปลงของต้นทางที่ยังไม่ถูกเก็บ เมื่อ load จะต่อ previous object กลับ พร้อม carry/history เดิม

Storage รับเฉพาะ state ที่ JSON เก็บกลับได้โดยไม่เปลี่ยนรูป ไม่แปลง object ที่ไม่รู้จักเป็นข้อความ และปฏิเสธ NaN/ชนิดที่ข้อมูลจะเปลี่ยนระหว่าง encode/decode ข้อมูลก่อนหน้าไม่ถูกย่อหรือตัดเพื่อให้ save ผ่าน

### ใช้เครื่องมือจาก root รีโป้

```sh
python tools/mpcp_condien.py --store local_workspace/context.sqlite --input tools/agent_sandbox/condien_state.json --save
python tools/mpcp_condien.py --store local_workspace/context.sqlite --name EQUIPMENT-CONTEXT
python tools/mpcp_papers.py --request tools/agent_sandbox/condien_paper.json --output local_workspace/context-paper --condien-store local_workspace/context.sqlite --condien-name EQUIPMENT-CONTEXT --condien-revision 1 --execute
```

CLI แรกเพิ่ม revision จริงเมื่อระบุ `--save` คำสั่งที่สองอ่าน metadata รุ่น คำสั่งที่สามเปิดอีก process แล้วให้ Paper อ่านเฉพาะ layer/key ที่อนุญาต พร้อมผูก snapshot ID เข้า `CONTEXT_REF` และ work hash จึงใช้คำอนุญาตเดิมกับบริบทคนละรุ่นโดยเงียบ ๆ ไม่ได้

### ขอบเขตที่ต้องรักษา

ฐานข้อมูลเก็บ state เต็ม รวมค่าที่ runtime ไม่มีสิทธิ์อ่าน จึงเป็นพื้นที่ของ trusted host ไม่ใช่ public scoped endpoint ไม่ใช่ฐานข้อมูลเข้ารหัสหรือกลไกตรวจตัวตน การมีสำเนา snapshot ไม่สร้างสิทธิ์รันงาน

ยังไม่จำแนกความหมายของข้อมูลเข้า layer ให้เอง ไม่เลือก lib จากเจตนาอัตโนมัติ ไม่ sync cloud/W3DB และไม่รับรอง filesystem/power-loss recovery จากผลเทส process restart การเชื่อมโยงที่เพิ่มคือ revision history และบริบทก่อนหน้าตามที่ประกาศ ไม่ใช่ knowledge graph ทั้งระบบ

## Movement — การนำทาง

### M1 — สิ่งที่อยู่ใน core/

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตและวิธีใช้ foundations |
| [condien.py](condien.py) | Native Condien model/access/continuity และ state round-trip |
| [condien_store.py](condien_store.py) | เก็บ เรียกคืน และเชื่อม snapshot รุ่นต่าง ๆ |
| [blueprint.py](blueprint.py) | Declarative Blueprint model/parser |
| [__init__.py](__init__.py) | exports foundations เดิม |

### M2 — เอกสารอ้างอิงนอกพื้นที่

- docs.condien : [W3Lgu-Condien Profile](../../protocol/mpcp/w3lgu_integration_paper/W3LGU_CONDIEN_PROFILE.md)
- docs.library : [Library equipment](../../protocol/mpcp/lib/README.md)
- docs.env : [ENV Boundary](../../protocol/mpcp/env/README.md)
- docs.paper : [Paper Runtime](../../protocol/mpcp/runtime/README.md)
- docs.tests : [Persistence/equipment tests](../../tests/test_mpcp_condien_equipment.py)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex
