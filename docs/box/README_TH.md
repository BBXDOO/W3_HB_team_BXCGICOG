# BOX / Library-WX — คู่มือภาพรวมภาษาไทย

- **เวอร์ชัน:** 1.0
- **สถานะ:** Knowledge Infrastructure / Reference Layer
- **Owner:** BBX19
- **ขอบเขต:** Planner-only
- **Runtime authority:** ไม่มี
- **Mutation:** `false`

## BOX คืออะไร

BOX คือโครงสร้างพื้นฐานสำหรับจัดเก็บ ค้นหา และอ้างอิงความรู้ที่นำกลับมาใช้ซ้ำได้ใน W3
โดยไม่ต้องสร้างเอกสารซ้ำทุกครั้ง เปรียบได้กับห้องสมุดกลางที่มีสารบัญสำหรับมนุษย์และระบบ
แต่ไม่มีอำนาจเรียก runtime หรือแก้ไขต้นฉบับแทนผู้ใช้

```text
ความต้องการ / PX / Work Type
        │
        ▼
Engine-Index หรือ Indexor
        │
        ▼
ตำแหน่ง Template / Blueprint ที่แนะนำ
        │
        ▼
มนุษย์ตรวจสอบและคัดลอกไป Workspace
        │
        ▼
แก้ไขสำเนา → Review → ใช้งานใน Flow อื่น
```

BOX ช่วยให้ระบบอื่นอ้างอิงเอกสารด้วย `template_id`, `blueprint_id` และ repository-relative
path แทนการคัดลอกเนื้อหาเดิมไปไว้หลายแห่ง

## ส่วนประกอบหลัก

| ส่วน | ตำแหน่ง | หน้าที่ |
|---|---|---|
| Library-WX | `wx/templates/`, `wx/blueprints/`, `wx/references/` | เก็บต้นฉบับสำหรับอ้างอิง |
| Registry | `wx/registry/` | สารบัญ JSON ที่ระบบอ่านได้ |
| Human Index | `wx/index/` | แผนที่ Markdown สำหรับมนุษย์ |
| Engine-Index | `wx/engine_index.py` | ค้นหาด้วย PX, work type หรือ Rytm |
| Indexor | `wx/indexor.py` | แนะนำรายการอ้างอิงแบบ Binder |
| PortDC | `wx/portdc.py` | อ่านและส่งออกต้นฉบับเป็นข้อมูลโดยไม่เขียนปลายทาง |
| Log-Info | `wx/log_info/` | พื้นที่บันทึกเหตุการณ์แบบ append-only |

## BOX ทำอะไรได้

- ตรวจและอ่าน registry
- ค้นหา template ด้วย `PX`, `work_type` หรือ `rytm`
- แนะนำ path และ metadata ที่เกี่ยวข้อง
- ส่งออกเนื้อหาของ template ที่ลงทะเบียนในรูปข้อมูล
- ส่ง suggestion เพิ่มให้ CROLL และ W3-API เมื่อผู้เรียกเปิดใช้โดยชัดเจน
- รองรับ `external_ref` เพื่อเตรียมเชื่อม WHUB ในอนาคต

## BOX ไม่ทำอะไร

- ไม่ execute Modew, script หรือ template
- ไม่เขียนหรือแก้ repository
- ไม่คัดลอก template เข้า workspace อัตโนมัติ
- ไม่ append log อัตโนมัติ
- ไม่เรียก network
- ไม่เปลี่ยน source truth
- ไม่อนุมัติ PR หรือ merge
- ไม่แทนที่ CROLL, MPCP, W3DB หรือระบบ governance

## โครงสร้างโดยย่อ

```text
wx/
├── README.md
├── templates/          # ต้นฉบับ template — copy before use
├── blueprints/         # declaration ของโครงสร้าง
├── references/         # ความรู้อ้างอิงที่คงที่
├── registry/           # machine-readable source of truth
├── index/              # human-readable navigation
├── log_info/           # append-only audit surfaces
├── collections/        # กลุ่มอ้างอิงแบบเลือกใช้
├── engine_index.py     # read-only lookup
├── indexor.py          # suggestion layer
└── portdc.py           # read-only export boundary
```

## หลักสำคัญ

1. **Single Source of Truth** — template/blueprint ต้นฉบับมีตำแหน่งเดียว
2. **Copy Before Use** — งานแต่ละชิ้นแก้ในสำเนาที่ workspace ไม่แก้ต้นฉบับตามงานนั้น
3. **Planner First** — BOX แนะนำและอ้างอิงเท่านั้น
4. **Human First** — มนุษย์ตัดสินใจว่าจะคัดลอก แก้ไข หรือส่งต่อหรือไม่
5. **Traceability** — สำเนาควรเก็บ `template_id` และบันทึกที่มา
6. **Capability ≠ Authority** — อ่านหรือส่งออกได้ ไม่ได้หมายถึงได้รับสิทธิ์ execute

## เริ่มต้นอย่างเร็ว

```bash
# ตรวจ BOX registry และ Engine-Index
python -m unittest discover -s wx -p "test_*.py" -v

# ขอ CROLL plan พร้อม BOX suggestion
python -m croll --compact plan "PX:[1,1]" --box-suggestion
```

อ่านขั้นตอนใช้งานจริงที่ [USAGE_TH.md](USAGE_TH.md) และข้อจำกัดด้านความปลอดภัยที่
[BOUNDARY_TH.md](BOUNDARY_TH.md)


## การเชื่อม BOX กับ CN-Fold

จากโครงสร้างปัจจุบัน **ไม่จำเป็นต้องรวม BOX และ CN-Fold ให้กลายเป็นระบบเดียวกันทั้งหมด**
เพราะทั้งสองมีบทบาทต่างกัน แต่สามารถเชื่อมกันได้โดยให้ `wx:BOX` เป็นรูปแบบใช้งาน และรับ
พฤติกรรมที่จำเป็นของ CN-Fold เข้ามา

```text
BOX / Library-WX
  = พื้นที่อ้างอิง + registry + boundary + ต้นฉบับ

CN-Fold
  = folder-as-node + host + relation + status + index

ทางเชื่อม
  = wx:BOX manifest / refs / registry
```

แนวทางนี้มีอยู่แล้วใน repository ผ่าน:

- `wx/blueprints/system/wx_box_cn_fold_integration.md` — blueprint การเชื่อม
- `wx/references/cn_fold_to_wx_box_mapping.md` — ตารางเทียบความหมาย
- `wx/templates/box/wx_box_minimum.md` — template ขั้นต่ำ
- `wx/templates/box/USAGE_TH.md` — คู่มือ wx:BOX
- `wx/index/by_box.md` — human-readable index
- `BOX:WX_BOX_MINIMUM_V1` ใน `wx/registry/template_registry.json`

หลักสำคัญคือ **เชื่อมโดย reference ไม่ใช่ย้ายหรือทำสำเนาต้นฉบับทั้งหมด** และไม่เพิ่ม runtime
authority ให้ CN-Fold หรือ BOX

```text
CN-Fold บอกว่า folder/node นี้คืออะไรและสัมพันธ์กับอะไร
        ↓
wx:BOX เก็บ manifest + refs + boundary + status
        ↓
BOX Registry / Engine-Index ช่วยค้นและอ้างอิง
        ↓
PortDC อ่าน registered source เป็นข้อมูลเมื่อได้รับการเรียก
        ↓
มนุษย์หรือ flow ที่ได้รับอนุญาตเป็นผู้ตัดสินใจใช้งานต่อ
```

### สิ่งที่ยังไม่ควรทำ

- ไม่ย้าย CN-Fold ทั้งระบบเข้า `wx/`
- ไม่ทำให้ทุก folder ต้องเป็น CN-Fold หรือ wx:BOX
- ไม่ให้ CN-Fold กลายเป็น runtime/authority
- ไม่ให้ BOX แก้ source truth ตาม relation ที่พบ
- ไม่สร้าง registry ซ้ำอีกชุดถ้า `wx/registry/` รองรับข้อมูลนั้นอยู่แล้ว
- ไม่ถือ external surface เป็น source truth แทน GitHub

สถานะของการเชื่อมนี้ยังเป็น **draft / observe** ตาม blueprint ปัจจุบัน จึงควรขยายจาก use case
จริงและผลทดสอบ มากกว่าล็อก schema เพิ่มล่วงหน้า
