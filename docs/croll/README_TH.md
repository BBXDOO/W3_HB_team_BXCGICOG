# CROLL / Cross-Lgu — คู่มือภาพรวมภาษาไทย

**สถานะ:** Reference planner สำหรับเครือข่าย W3  
**ขอบเขต:** วางแผนและตรวจสัญญาเท่านั้น ไม่ execute CrossCode  
**ผู้ใช้เป้าหมาย:** W3, WHUB และระบบคู่ร่วมงานที่ได้รับขอบเขตชัดเจน

## CROLL คืออะไร

CROLL เป็นส่วนอ้างอิงของ Cross-Lgu สำหรับแปลงจุดอ้างอิง `PX` ให้เป็น **workset** และ
**dispatch plan** ที่อ่านได้ทั้งโดยมนุษย์และระบบอื่น เป้าหมายไม่ใช่การสร้างภาษาโปรแกรมใหม่
แต่เป็นการรักษาความหมาย ขอบเขต ข้อห้าม รูปแบบผลลัพธ์ และการ review เมื่อหลายภาษา/agent
ทำงานร่วมกัน

```text
Paper/WHUB request
  → PX + context
  → Table-X lookup
  → CROLL planner
  → bounded dispatch plan
  → Modew/MPCP review (ภายนอก CROLL)
```

## สิ่งที่ CROLL ทำ

- ตรวจและแปลง PX เช่น `1,1` หรือ `PX:[2,1]`
- เลือก Rytm, work type, Modew style และ language candidates จาก Table-X
- แนบ boundary, deny list, return contract และ review condition
- คืน JSON ที่มี `contract_version`
- ตรวจ workset, dispatch plan และ W3 boundary manifest แบบ dependency-free

## สิ่งที่ CROLL ไม่ทำ

- ไม่ execute Modew หรือ CrossCode
- ไม่เขียน repository
- ไม่ merge
- ไม่แก้ truth
- ไม่ให้สิทธิ์ network หรือ subprocess
- ไม่ใช้ชื่อ W3/WHUB เป็นหลักฐานการอนุญาตโดยอัตโนมัติ

## โครงสร้างที่เกี่ยวข้อง

```text
croll/
├── table_x.py                 # lookup และ PX parser
├── cross_l_dispatcher.py      # planner-only dispatch
├── contracts.py               # safety invariant checks
├── cli.py                     # python -m croll
├── examples/                  # ตัวอย่างที่ตรวจได้
└── schema/                    # JSON Schema Draft 2020-12

docs/croll/
├── README_TH.md               # ภาพรวม
├── USAGE_TH.md                # วิธีใช้งาน
└── BOUNDARY_TH.md             # กติกาขอบเขตและการสงวนระบบ
```

## หลักที่ต้องรักษา

1. **Capability ไม่เท่ากับ Authority** — ทำได้ไม่ได้แปลว่าได้รับอนุญาต
2. **Boundary Before Execution** — ต้องรู้ขอบเขตก่อนส่งต่อให้ executor
3. **No Truth Mutation by Default** — ค่าเริ่มต้นคือห้ามแก้ truth
4. **Review on Uncertainty** — ไม่แน่ใจต้องคืน `review`
5. **Planner Is Not Executor** — CROLL ไม่รับอำนาจ execution
6. **Human/W3 Governance Remains Final** — schema ช่วยรักษาความเข้าใจ แต่ไม่แทนการอนุมัติ

## เริ่มต้นอย่างเร็ว

```sh
python -m croll lookup "1,1"
python -m croll plan "PX:[2,1]" --context @croll/examples/paper-context.json
python -m croll validate boundary croll/examples/boundary.w3-internal.json
```

อ่านวิธีใช้งานต่อที่ [USAGE_TH.md](USAGE_TH.md) และกติกาขอบเขตที่
[BOUNDARY_TH.md](BOUNDARY_TH.md)
