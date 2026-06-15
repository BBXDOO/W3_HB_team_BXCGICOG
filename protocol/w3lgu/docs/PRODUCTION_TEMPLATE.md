# W3Lgu Production Minimum Template

สถานะ: **Operational contract 1.0**

เอกสารนี้กำหนด “ขั้นต่ำที่นำไปใช้จริง” สำหรับระบบที่ต้องการพูดภาษา W3Lgu
ร่วมกัน โดยไม่บังคับให้ทุกระบบมี implementation เหมือนกันทั้งหมด

## หน่วยปฏิบัติการ

```text
EVENT:route,TARGET:W3DB,ROOM:EV,PX:LNEV'0007,STATE:ready,CONF:1
```

ผลที่ runtime ต้องสร้าง:

```text
REDR  -> PACKAGE + TAG + COPY(PSP2,LRC2)
PSP2  -> STAMP + ROUTE
DTML  -> READY | REVIEW | STOP
LRC2  -> APPEND HASH-LINKED RECORD
```

W3Lgu ทำงานจริงในขอบเขต **อ่าน จัดประเภท ส่งต่อ ตัดสินสถานะ และบันทึก**
แต่ไม่ถือสิทธิ์เรียก external side effect เอง การ execute ภายนอกต้องผ่าน adapter
ที่ได้รับอนุมัติแยกต่างหาก

## 6 Rooms

Rooms เป็นบริบท ไม่ใช่ pipeline บังคับ จึงไม่จำเป็นต้องไหล 1 → 6

| Room | Code | บริบท |
| --- | --- | --- |
| 1 | `CA` | Cause |
| 2 | `CU` | Cause + Result |
| 3 | `RE` | Result |
| 4 | `SI` | Situation |
| 5 | `AP` | Appearance / observed phenomenon |
| 6 | `EV` | Event |

ประกาศตรง:

```text
ROOM:CU,CAUSE:load,RESULT:slow
```

ถ้าไม่ประกาศ runtime จะจัดประเภทจาก key และเปิดเผยที่มาของการจัดประเภทใน
`ROOM_BASIS_*` tag จึงไม่มี implicit magic

## PX และ POC

รูปแบบ PX ขั้นต่ำ:

```text
LNCU'0001
```

- `CU` คือ room และแกน Y (`Y=2`)
- `0001` คือตำแหน่งบนแกน X (`X=1`)
- จุดตัด `(X=1,Y=2)` คือ relative point
- POC คือจุดบรรจบ Cross-X เช่น `POC'cross-01'X0001'Y0002`

หาก packet ไม่มี `PX` runtime จะสร้างตำแหน่งแบบ deterministic จาก packet และ
ติด tag `PX_DERIVED_STABLE`; replay ข้อมูลเดิมจึงได้ตำแหน่งเดิม

## DTML decision

| เงื่อนไข | Decision | Signal |
| --- | --- | --- |
| boundary clear | `READY` | `GREEN` |
| `CONF:0.5` | `REVIEW` | `YELLOW` |
| `!`, `STATE:STOP/BLOCK/FAIL`, `CONF:0` | `STOP` | `RED` |

ทุกผลลัพธ์รวมถึง `STOP` ต้องถูก LRC2 บันทึก

## LRC2 ledger

- append-only
- hash-linked จาก genesis ถึง record ล่าสุด
- event id เดิม append ซ้ำแล้วได้ record เดิม (idempotent)
- `verify()` ตรวจ sequence, duplicate event และ hash chain
- เป็น in-process operational ledger; durable storage ใช้ adapter ภายนอก

## 27 minimum laws

โค้ดจริงอยู่ใน `MINIMUM_LAWS` และตรวจได้ด้วย `validate_minimum_laws()` กฎถูกแบ่งเป็น:

1. การอ่านและไวยากรณ์
2. ความหมายของ symbol
3. PX / POC / 6 Rooms
4. REDR / PSP2 / DTML / LRC2
5. สถานะ 0.5, no implicit magic และ explicit authority

ระบบอื่นนำ template ออกมาใช้ได้โดย:

```python
from protocol.w3lgu import operational_template

contract = operational_template()
```

## Python runtime

```python
from protocol.w3lgu import W3LguOperationalRuntime

runtime = W3LguOperationalRuntime()
result = runtime.process_line(
    "CAUSE:load,RESULT:slow,TARGET:QUEUE,CONF:0.5",
    cross_id="cross-queue-01",
)

assert result.decision == "REVIEW"
assert runtime.ledger.verify()
```

ผลลัพธ์เป็น immutable dataclass และ `to_dict()` ได้สำหรับ API, event bus,
audit หรือ durable adapter
