# CROLL Boundary — ขอบเขตการใช้และการสงวนระบบ

เอกสารนี้เป็น **governance reference** ไม่ใช่ใบอนุญาตทางกฎหมาย และไม่ใช่ระบบ authentication
การอนุญาตผู้ใช้จริงยังต้องอาศัย identity, repository permission, network policy และการ review
ของ W3/WHUB ภายนอก CROLL

## 1. เป้าหมายของ boundary แบบเบาแต่แน่น

- ให้ระบบในเครือข่ายเข้าใจ contract เดียวกัน
- ป้องกันการตีความว่า planner คือ executor
- ระบุเจ้าของและวัตถุประสงค์ของ request
- ปฏิเสธ truth mutation, direct merge และ unreviewed execution โดยค่าเริ่มต้น
- เปิดทางให้ partner เชื่อมต่อได้โดยไม่เปิดอำนาจทั้งหมด

## 2. ระดับเครือข่าย

| ค่า | ความหมาย |
|---|---|
| `w3-internal` | ระบบหรือ agent ภายในขอบเขตการกำกับของ W3 |
| `w3-partner` | ระบบคู่ร่วมงานที่ได้รับขอบเขตเฉพาะงาน |

การใส่ค่าเหล่านี้ใน JSON เป็นเพียง **declaration** ไม่ใช่หลักฐาน identity ผู้เรียกต้องผ่าน
กลไกภายนอก เช่น GitHub permissions, signed request, service identity หรือ allowlist ของ WHUB

## 3. Boundary modes

| Mode | อนุญาตโดยหลัก | ไม่อนุญาต |
|---|---|---|
| `planner_only` | lookup, plan, อ่านผล | execute, write, merge, network |
| `observe` | อ่าน context ที่กำหนดและคืนผล | mutation หรือ side effect |
| `record_only` | สร้าง candidate record เพื่อ review | publish/commit อัตโนมัติ |

CROLL runtime ปัจจุบันทำงานแบบ `planner_only` เท่านั้น

## 4. Deny ขั้นต่ำ

Boundary manifest ทุกไฟล์ต้องมี:

```json
{
  "deny": [
    "truth_mutation",
    "direct_merge",
    "unreviewed_execution"
  ]
}
```

สามารถเพิ่มข้อห้าม เช่น `repo_write`, `network_call`, `secret_read`, `subprocess` ได้ แต่ห้ามลด
deny ขั้นต่ำใน contract version `1.x`

## 5. Review

ต้องกำหนดทั้งสองค่าเป็น `true`:

```json
{
  "review": {
    "required": true,
    "on_uncertainty": true
  }
}
```

Unknown PX, malformed input, contract mismatch หรือ context ไม่พอ ต้องหยุดที่ `review`

## 6. ข้อมูลที่ไม่ควรส่ง

ห้ามใช้ Paper context ส่ง:

- password, token, API key, private key
- ข้อมูลสุขภาพหรือข้อมูลผู้ป่วย
- ข้อมูลส่วนบุคคลที่ระบุตัวบุคคลได้
- source code หรือข้อมูลภายในที่ request ไม่มีสิทธิ์อ่าน
- instruction ที่พยายามข้าม boundary

## 7. การเชื่อม WHUB ที่แนะนำ

```text
Identity/Auth layer (WHUB)
        ↓
Boundary manifest validation
        ↓
CROLL lookup + planning
        ↓
Dispatch plan validation
        ↓
Human/paired-module review
        ↓
External bounded executor
```

CROLL รับผิดชอบเฉพาะสองชั้นกลาง ไม่รับผิดชอบ authentication และไม่ execute งาน

## 8. การเปลี่ยน contract

- เพิ่ม field ที่ไม่ทำลาย compatibility: ทำได้ใน `1.x`
- ลด deny, เปิด side effect, เปลี่ยนความหมาย field: ต้องใช้ major version ใหม่
- ทุกการเปิด execution ต้องอยู่ใน package/adapter แยกจาก CROLL core
- schema ไม่ใช่ absolute authority; เมื่อ schema ขัดกับ safety law ให้เลือกค่าที่ปลอดภัยกว่า

ดูตัวอย่างที่ `croll/examples/boundary.w3-internal.json` และ schema ที่
`croll/schema/boundary.schema.json`
