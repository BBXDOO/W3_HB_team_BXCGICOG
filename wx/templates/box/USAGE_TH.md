# คู่มือใช้งาน wx:BOX

> Status: draft / observe  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19  
> Source truth: GitHub

คู่มือนี้อธิบายวิธีใช้ `wx:BOX` เป็นกล่องอ้างอิงแบบเบา โดยรับแนวคิด CN-Fold เข้ามาเฉพาะส่วนที่ช่วยให้ folder/node มีบริบท เช่น host, relation, boundary, index และ status

---

## 1. wx:BOX ใช้เมื่อไหร่

ใช้ `wx:BOX` เมื่อมี folder, กลุ่มเอกสาร, template, blueprint หรือ node ที่ต้องการให้ระบบอื่นเข้าใจว่า:

```text
- สิ่งนี้คืออะไร
- อยู่ใน host ไหน
- มี parent / child relation อย่างไร
- อ้างอิง identity / registry / source truth ที่ไหน
- เปิดเผยหรือแก้ไขได้แค่ไหน
- มี status ล่าสุดอะไร
```

ตัวอย่างที่เหมาะ:

```text
- กลุ่มเอกสาร WE PAPER
- folder สำหรับ Base44 library
- กลุ่ม blueprint
- กลุ่ม template
- node ที่ Graph View ต้องอ่าน relation
- folder ที่ต้องชี้กลับ GitHub source truth
```

---

## 2. wx:BOX ไม่ควรใช้เมื่อไหร่

ไม่ควรใช้ `wx:BOX` เพื่อ:

```text
- execute งาน
- mutate source truth
- แทน MPCP Blueprint
- แทน Paper
- แทน ROT
- แทน IDP
- บังคับทุก folder ให้มี schema หนัก
```

กฎสั้น:

```text
BOX ชี้ / อธิบาย / จัด index ได้
BOX ไม่ใช่ตัวสั่งงาน
```

---

## 3. ขั้นตอนสร้าง BOX ใหม่

### Step A — เลือก folder หรือกลุ่มเอกสาร

ถามก่อนว่า folder นี้ควรถูกยกระดับเป็น BOX หรือยัง:

```text
1. folder นี้คืออะไร
2. เป็น host ของอะไร
3. มีไฟล์ลูกอะไรบ้าง
4. ขอบเขตเปิดเผยแค่ไหน
5. status ล่าสุดคืออะไร
6. ต้องลง registry หรือ graph ไหม
```

ถ้าตอบได้ครบ ค่อยสร้าง BOX

---

### Step B — copy template

ใช้ template นี้เป็นต้นแบบ:

```text
wx/templates/box/wx_box_minimum.md
```

copy ไปยังพื้นที่งานหรือ folder ที่ต้องการ เช่น:

```text
some/path/BOX.md
```

ไม่ควรแก้ต้นฉบับ template โดยตรง

---

### Step C — เติมค่าขั้นต่ำ

ค่าที่ควรเติมก่อน:

```yaml
box:
  id: BOX.EXAMPLE.NODE
  name: example-box
  type: reference/container
  status: observe
  owner: BBX19
  mutation: false

host:
  path: some/path
  parent: some
  scope: internal-working

refs:
  source_truth: GitHub
  registry: wx/registry/template_registry.json

boundary:
  can_execute: false
  can_mutate_source: false
  requires_review: true
```

---

### Step D — เพิ่ม refs แทนการ copy ของหนัก

ถ้าต้องอ้างอิง identity, registry, template หรือ blueprint ให้ใช้ path/reference แทนการคัดลอกเนื้อหาทั้งก้อน

ตัวอย่าง:

```yaml
refs:
  identity: core/module-loader/identity/ChatGPT.idp.json
  registry: wx/registry/agent_registry.json
  source_truth: GitHub
  template: wx/templates/box/wx_box_minimum.md
  blueprint: wx/blueprints/system/wx_box_cn_fold_integration.md
```

หลักจำง่าย:

```text
อะไรที่เปลี่ยนได้ → อ้างอิง
อะไรที่เป็น source truth → ชี้ไปหา
อะไรที่เป็น identity → อ้างอิง IDP / registry
```

---

### Step E — ลง registry เฉพาะเมื่อจำเป็น

ไม่ใช่ทุก BOX ต้องเข้า registry

ควรลง registry เมื่อ:

```text
- ต้องให้ Engine-Index lookup
- ต้องให้ Graph View อ่าน
- ต้องให้ WE PAPER / Base44 ใช้แสดง tree
- ต้องเป็น template หรือ blueprint ที่ใช้ซ้ำ
```

ถ้าเป็น note หรือ folder ทดลองเล็ก ๆ ให้ใช้ `status: observe` และยังไม่ต้องลง registry

---

## 4. โครงสร้างที่แนะนำ

```text
Some_BOX_Folder/
├── BOX.md          # manifest ของ wx:BOX
├── README.md       # อธิบายเนื้อหาให้คนอ่าน
├── index.md        # รายการไฟล์ / child node
├── status.md       # สถานะล่าสุด ถ้าจำเป็น
└── files/          # เอกสารลูก ถ้ามี
```

ไม่จำเป็นต้องมีทุกไฟล์ตั้งแต่แรก

ขั้นต่ำสุดคือ:

```text
BOX.md หรือ README.md ที่มี box metadata ชัดเจน
```

---

## 5. สถานะที่แนะนำ

```text
observe  = กำลังดู / ยังไม่ล็อก
active   = ใช้งานได้
review   = ต้องตรวจ
block    = ห้ามใช้ต่อจนกว่าจะเคลียร์
archive  = เก็บเป็นหลักฐาน/ประวัติ
```

ใช้สีร่วมได้ตาม context:

```text
GREEN  = stable
BLUE   = observe / active movement
YELLOW = review
RED    = block
PURPLE = relation-heavy
DARK   = inactive / unknown
```

---

## 6. Boundary พื้นฐาน

ทุก BOX ควรตอบได้ว่า:

```text
can_execute: false
can_mutate_source: false
can_export_reference: true | false
requires_review: true | false
```

ค่า default ที่ปลอดภัย:

```yaml
boundary:
  can_execute: false
  can_mutate_source: false
  can_export_reference: true
  requires_review: true
```

---

## 7. ตัวอย่าง BOX แบบสั้น

```text
WX:BOX,ID:BOX.BLUEPRINTS.ABSTRACT,STATUS:observe,OWNER:BBX19,MUTATION:false
HOST:blueprints/abstract,PARENT:blueprints,SCOPE:internal-working
REF:SOURCE_TRUTH:GitHub,REGISTRY:Airtable/latest-result
BOUNDARY:internal,SENS:S2-S3,EXEC:false,MUTATE:false,REVIEW:true
INDEX:W3_INTERNAL_NODE_MAP_TH.md,W3_BOUNDARY_MODEL_TH.md,W3_NODE_RELATIONS_TABLE_TH.md
```

---

## 8. Flow การใช้งาน

```text
พบ folder/group ใหม่
→ ถาม 6 คำถาม CN-Fold
→ copy wx_box_minimum.md
→ เติม id/host/refs/boundary/status
→ ลง registry เฉพาะเมื่อจำเป็น
→ ให้ WE PAPER / Base44 / Graph View อ่านจาก refs
→ ไม่ mutate source truth
```

---

## 9. One-line Summary

```text
wx:BOX ใช้ทำให้ folder หรือกลุ่มเอกสารกลายเป็นกล่องอ้างอิงที่มีบริบท โดยใช้ reference แทนการล็อกข้อมูลหนักลงไฟล์เดียว
```
