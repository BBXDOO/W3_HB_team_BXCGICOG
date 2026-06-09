# วิธีใช้งาน CROLL ภาษาไทย

เอกสารนี้ใช้คำสั่งจาก root ของ repository และรองรับ CPython 3.9 ขึ้นไปโดยไม่ต้องติดตั้ง
package เพิ่ม

## 1. ดูรายการ PX

```sh
python -m croll list
python -m croll --compact list
```

## 2. Lookup workset

```sh
python -m croll lookup "1,1"
python -m croll lookup "PX:[2,1]"
```

ผลลัพธ์มีข้อมูล เช่น `rytm`, `work_type`, `modew_style`, `boundary`, `deny` และ
`return_contract` แต่ผล lookup **ไม่ใช่การอนุญาตให้ execute**

## 3. สร้าง dispatch plan

```sh
python -m croll plan "PX:[2,1]"
```

ส่ง context แบบ inline JSON:

```sh
python -m croll plan "1,1" --context '{"paper_id":"WHUB-001","scope":"CROSS_L_ONLY"}'
```

สำหรับ Windows/มือถือ แนะนำไฟล์ UTF-8 เพื่อลดปัญหา quote:

```sh
python -m croll plan "1,1" --context @croll/examples/paper-context.json
```

## 4. ตรวจ artifact

```sh
python -m croll validate boundary croll/examples/boundary.w3-internal.json
python -m croll validate workset croll/examples/workset.rock.json
python -m croll validate plan croll/examples/dispatch-plan.jazz.json
```

สำเร็จจะคืน:

```json
{
  "contract_version": "1.0",
  "valid": true,
  "kind": "boundary",
  "file": "croll/examples/boundary.w3-internal.json"
}
```

ถ้าไม่ผ่านจะคืน exit code `2` และเหตุผลทาง `stderr` โดยไม่ execute artifact

## 5. ใช้ผ่าน Python API

```python
from croll import (
    dispatch_workset,
    get_workset_from_px,
    validate_boundary_manifest,
    validate_dispatch_plan,
)

workset = get_workset_from_px("1,1")
plan = dispatch_workset("2,1", paper_context={"paper_id": "WHUB-001"})
validate_dispatch_plan(plan)
```

## 6. ใช้กับ WHUB

WHUB ควรส่งเพียง:

- PX
- task/paper identifier
- intent
- scope
- boundary manifest ที่ระบุ owner และ network scope

WHUB ไม่ควรส่ง token, secret, patient data, private key หรือข้อมูลส่วนบุคคลลง Paper context
เพราะ CROLL เก็บเฉพาะ marker ของ context และไม่ได้ออกแบบเป็น secret store

ลำดับที่แนะนำ:

```text
WHUB request
→ validate boundary manifest
→ CROLL plan
→ validate dispatch plan
→ W3/Modew review
→ executor ภายนอก (ถ้าได้รับอนุมัติ)
```

## 7. การทดสอบ

```sh
python -m compileall croll
python -m unittest discover -s croll -p "test_*.py" -v
```

CI จะทดสอบบน Ubuntu, Windows และ macOS ตาม `.github/workflows/croll.yml`
