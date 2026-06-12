# BOX / Library-WX — ขอบเขต ความปลอดภัย และการสงวนระบบ

เอกสารนี้กำหนดสิ่งที่ BOX อนุญาตและไม่อนุญาต เพื่อไม่ให้ reference layer กลายเป็น
runtime หรือสร้างอำนาจใหม่โดยไม่ตั้งใจ

## 1. Boundary หลัก

```text
BOX authority
├── read registry
├── validate metadata/path
├── locate references
├── suggest references
└── export registered source as response data

BOX has no authority to
├── execute
├── copy to workspace
├── write or mutate repository
├── append logs automatically
├── call network
├── approve governance
└── merge
```

## 2. Safety invariants

| ค่า | ค่าที่อนุญาต |
|---|---|
| `planner_only` | `true` |
| `execution_allowed` | `false` |
| `mutated` | `false` |
| `copy_allowed_by_runtime` | `false` |
| `write_performed` | `false` |
| `human_review_required` | `true` |

CROLL plan ที่มี BOX suggestion ต้องยังรักษา safety fields ของ CROLL เดิมทั้งหมด

## 3. ความหมายของ Source of Truth

- Registry JSON คือ machine-readable source of truth สำหรับการค้นหา
- Template/blueprint file คือ source content
- Human Markdown index เป็น navigation aid ไม่ใช่ registry ทดแทน
- Registry และ front matter ต้องสอดคล้องกัน
- การมี path ใน registry ไม่ได้ให้ execution authority แก่ไฟล์นั้น

## 4. Copy-Before-Use

ผู้ใช้ต้องคัดลอก template ไปยัง workspace ที่ผ่าน governance ก่อนแก้ไข งาน instance ต้องไม่
เปลี่ยน template ต้นฉบับเพื่อให้เข้ากับงานเฉพาะหน้า

การดูแลต้นฉบับทำได้เฉพาะในฐานะ library maintenance ที่ตั้งใจ มี version และผ่าน review
ไม่ใช่ผลข้างเคียงจากการใช้ template

## 5. Path safety

Engine-Index ปฏิเสธ:

- absolute paths
- path ที่มี `..`
- path ที่ออกนอก repository
- path ที่ชี้ไปยังไฟล์ซึ่งไม่มีอยู่
- filename ที่ไม่ portable ซึ่งถูกตรวจโดย `tools/check_portable_paths.py`

ข้อกำหนดนี้ช่วยให้ BOX ใช้ได้บน Linux, macOS, Windows และ Termux

## 6. Metadata lock แบบเบา

BOX ใช้การตรวจสองชั้น:

1. JSON Schema ตรวจรูปแบบ registry
2. Engine-Index ตรวจความสัมพันธ์ระหว่าง registry, path และ front matter

metadata ที่ต้องตรงกัน:

- `template_id`
- `version`
- `owner`
- `status`
- `boundary`

นี่เป็น lock เพื่อป้องกัน drift ไม่ใช่ governance authority หรือระบบ validation ขนาดใหญ่

## 7. Log-Info boundary

- ไฟล์ `.jsonl` เป็น append-only
- BOX runtime ไม่ append ให้อัตโนมัติ
- ผู้ append ต้องได้รับอนุมัติและตรวจข้อมูลก่อน
- ห้ามแก้หรือลบบรรทัดเก่าเพื่อเปลี่ยนประวัติ
- ห้ามบันทึก secret, credential, token, patient data หรือข้อมูลส่วนบุคคลที่ไม่จำเป็น

## 8. PortDC boundary

PortDC อ่านได้เฉพาะ template ที่ลงทะเบียน และคืนเนื้อหาเป็น response data เท่านั้น
`export` ในที่นี้ไม่หมายถึงการเขียนไฟล์ภายนอกหรือส่งผ่าน network

ผู้รับยังต้อง:

1. ตรวจ template ID และ boundary
2. ตัดสินใจว่าจะคัดลอกหรือไม่
3. เลือก workspace ที่ถูกต้อง
4. บันทึก provenance
5. ขอ review ก่อนใช้งาน

## 9. W3-API boundary

`include_box_suggestion` มีค่าเริ่มต้นเป็น `false` เพื่อรักษา response เดิม ผู้เรียกต้องเปิดใช้
โดยชัดเจน และ suggestion ที่ได้เป็น reference metadata เท่านั้น

endpoint ไม่ควร:

- เปิดไฟล์ตาม path ที่ผู้ใช้ส่งมาโดยตรง
- รับ arbitrary filesystem path
- ส่ง content ออก network โดยอัตโนมัติ
- เปลี่ยน `execution_allowed` หรือ `mutated`
- ทำ fallback ไป execute เมื่อหา template ไม่พบ

## 10. WHUB / External Reference

`external_ref` เป็น metadata เตรียมความพร้อมเท่านั้น ปัจจุบัน BOX:

- ไม่ fetch URL
- ไม่เชื่อถือ external node อัตโนมัติ
- ไม่ sync เนื้อหา
- ไม่ตรวจสิทธิ์เครือข่าย

การเชื่อม WHUB จริงต้องมี trust model, allowlist, provenance, integrity check และ owner review
แยกต่างหาก

## 11. Failure behavior

เมื่อ registry ผิดหรือไม่ปลอดภัย BOX ควร fail closed ด้วย `BoxRegistryError` ไม่เดา path,
ไม่ข้าม validation และไม่คืน execution fallback

เมื่อ PX ไม่พบ CROLL ต้องคง `state: review` และไม่สร้าง suggestion ปลอม

## 12. Checklist ก่อน merge

- [ ] template มี front matter ครบ
- [ ] registry metadata ตรงกับไฟล์
- [ ] path เป็น repository-relative และไฟล์มีอยู่จริง
- [ ] template ID ไม่ซ้ำ
- [ ] PX และ status ถูกต้อง
- [ ] human index ได้รับการอัปเดต
- [ ] ไม่มี secret/PII/patient data
- [ ] BOX tests ผ่าน
- [ ] CROLL tests ผ่าน
- [ ] W3-API focused integration tests ผ่าน
- [ ] portable-path check ผ่าน
- [ ] มี human review
