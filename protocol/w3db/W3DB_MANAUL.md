# คู่มือใช้งาน W3DB (ภาษาไทย)

W3DB (World 3 Database) คือ module สำหรับจัดการข้อมูลกลางในระบบ W3 เช่น log, state, perception, law  
ประกอบด้วย data model, CRUD, ใน-memory store, configuration และ orchestrator สำหรับ "relation flow"

-------------------------------

## องค์ประกอบหลักของ W3DB

- **XIZ** : Action log — เก็บเหตุการณ์แต่ละรายการ
- **TUF** : State snapshot — สถานะหรือผลการสังเกต
- **FBD** : Failure — ตำแหน่ง "ข้อผิดพลาด/เขตเสี่ยง"
- **WHB** : Law/Context — กติกา/เงื่อนไข (if-then)
- **PRX** : Perception output — ผลลัพธ์สุดท้าย (สัญญาณ, สี ฯลฯ)

-------------------------------

## เริ่มต้นใช้งาน

### 1. เตรียม environment

สร้าง Python venv แล้วติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

-------------------------------

### 2. เรียกใช้งานเบื้องต้น

```python
from src.w3db.store import W3DBStore
from src.w3db.flow import run_flow

# สร้าง store กลาง (memory)
store = W3DBStore()

result = run_flow(
    input_event="Patient arrived — BP 140/90",
    cix_id="CIX-001",
    confidence=0.72,
    store=store,
)

print(result["output"])  # ดู perception/สรุปผลแบบย่อ
```

**ผลลัพธ์:** จะได้ dict ที่รวม XIZ, TUF, FBD, WHB, PRX ออกมาให้ใช้งานต่อ

-------------------------------

### 3. จัดการข้อมูลแต่ละประเภท (CRUD)

```python
from src.w3db.crud.xiz import create_xiz, read_xiz, update_xiz, delete_xiz
from src.w3db.store import W3DBStore

store = W3DBStore()
# สร้าง XIZ log
xiz = create_xiz(
    "XIZ-001", action="Checked patient", timestamp="2026-01-01T00:00:00Z", store=store
)
# แก้ไข
xiz = update_xiz("XIZ-001", result="Stable", store=store)
print(read_xiz("XIZ-001", store=store).to_dict())
# ลบ
delete_xiz("XIZ-001", store=store)
```

-------------------------------

## การปรับแต่ง Config (Dev/Test/Prod)

```python
from src.w3db.config import get_config

cfg = get_config()
print(cfg.env, cfg.max_store_size)
```

หรือ โดยตรงผ่าน environment variable เช่น  
`export W3DB_ENV=prod`, `export W3DB_IMMUTABLE_XIZ=true`

-------------------------------

## ผูกกับ EP_SIGNAL ได้อย่างไร?

**ตัวอย่าง:**  
- สมมติรับข้อมูล binary หรือ signal จาก EP_SIGNAL module → นำ decode หรือรายละเอียดเพิ่มเติมมาเก็บใน W3DB (เป็น xiz, tuf, ฯลฯ)

```python
from SYSTEM.TESTS.EP_SIGNAL.ep_signal_adapter import from_ep_signal
from src.w3db.crud.xiz import create_xiz
from src.w3db.store import W3DBStore

ep_signal_string = "0/221112133-8'BIN"
decoded_bin = from_ep_signal(ep_signal_string)

store = W3DBStore()
create_xiz(
    "XIZ-777",
    action="EP_SIGNAL decoded",
    timestamp="2026-05-20T13:15:00Z",
    result=decoded_bin,
    store=store,
)
```

-------------------------------

## การทดสอบระบบ

- CRUD unit test: `python protocol/w3db/test_crud.py`
- Integration test: `python protocol/w3db/test_flow.py`
- ทดสอบครบ: `python tools/w3_agent_ci.py`

-------------------------------

## สารพัดข้อควรรู้

- ทุกตาราง (XIZ, ... PRX) มี id ของแต่ละ domain ต้องตั้งเอง (แนะนำเป็น "XIZ-001", ...)
- W3DBStore เป็น in-memory หากปิดแอปข้อมูลจะหายไปทั้งหมด (แต่เปลี่ยน backend ได้)
- immutable_xiz = True จะล็อคไม่ให้แก้ไข XIZ ได้

-------------------------------

## เชื่อมต่อกับโปรโตคอลภายนอก

- เชื่อม W3DB กับระบบอื่น (เช่น mpcp, W3Lgu, EP_SIGNAL) ได้ทันทีผ่าน Store หรือ Flow  
- สามารถดึงหรือแปลงข้อมูลระหว่าง adapter ของแต่ละโมดูลอย่างง่าย  
- โปรดดูตัวอย่างจริงใน integration README ของแต่ละโมดูล

-------------------------------

## ติดต่อ/เสนอแนะแก้ไข

- หากเจอ bug หรือใช้กับระบบ production แล้ว error โปรดแจ้งผ่าน issue tracker หรือที่นักพัฒนาหลัก

---

**W3DB ออกแบบให้ flexible, ใช้ง่าย, ปลอดภัยต่อไปขยาย backend อื่นในอนาคต**