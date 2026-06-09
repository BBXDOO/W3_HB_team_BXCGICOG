# CN-Fold Working Model

> Path: `BBX19/status/CN-Fold/README.md`  
> Status: draft / observe  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19  
> Purpose: อธิบายรูปแบบการทำงานของ CN-Fold เพื่อใช้เป็นแกนอ้างอิงสำหรับ WE PAPER, Base44, Hbtisocity, Graph View และระบบจัดทรัพยากรเอกสารภายนอก

---

## 1. ความหมายของ CN-Fold

**CN-Fold** ย่อจาก **Cross-Nodes Folder**

CN-Fold ไม่ใช่แค่โฟลเดอร์เก็บไฟล์แบบปกติ แต่เป็น **folder ที่ทำหน้าที่เป็น node / host / reference container** ภายในระบบ W3

กล่าวแบบสั้น:

```text
CN-Fold = Folder + Node + Host + Boundary + Index + Relation
```

หน้าที่หลักของ CN-Fold คือช่วยให้เอกสารจำนวนมากไม่กระจายแบบไร้แกน และช่วยให้ระบบภายนอกสามารถเข้าใจได้ว่า:

- โฟลเดอร์นี้คืออะไร
- อยู่ในขอบเขตไหน
- มีไฟล์อะไรอยู่ข้างใน
- เชื่อมกับ node หรือ hub ใด
- เปิดเผยได้แค่ไหน
- ใช้เป็นฐานของงานหรือ flow ประเภทใด

---

## 2. เหตุผลที่ต้องมี CN-Fold

เมื่อ W3 เริ่มมีเอกสาร, blueprint, module, agent, hub และระบบภายนอกจำนวนมาก การจัดไฟล์เป็น list ธรรมดาจะเริ่มไม่พอ

ปัญหาที่ CN-Fold ต้องช่วยลดคือ:

```text
เอกสารเยอะ
ไฟล์กระจาย
relation ไม่ชัด
folder เป็นแค่ที่เก็บ ไม่ใช่แกนอ้างอิง
agent อ่านบริบทไม่ครบ
Graph View เห็น node แต่ไม่รู้ host
external hub ไม่รู้ว่าไฟล์นี้อยู่ในบริบทไหน
```

CN-Fold จึงเกิดขึ้นเพื่อทำให้ folder กลายเป็น **พื้นที่อ้างอิงเชิงระบบ** ไม่ใช่เพียงที่วางไฟล์

---

## 3. หลักการพื้นฐาน

CN-Fold มีหลักการขั้นต่ำดังนี้:

```text
1. ทุก CN-Fold ต้องมี identity
2. ทุก CN-Fold ต้องมี host scope
3. ทุก CN-Fold ต้องรู้ parent / child relation
4. ทุก CN-Fold ต้องมี boundary เบื้องต้น
5. ทุก CN-Fold ต้องมี status ล่าสุด
6. ทุก CN-Fold ไม่ใช่ source truth ถ้าอยู่ใน external hub
7. ทุก CN-Fold ต้องคืนค่า/อ้างอิงได้ผ่าน Result Registry หรือเอกสารกำกับ
```

---

## 4. โครงสร้าง CN-Fold ขั้นต่ำ

ตัวอย่างโครงสร้างพื้นฐาน:

```text
CN-Fold_Name/
├── README.md              # อธิบายตัว folder / scope / วิธีใช้งาน
├── index.md               # รายการไฟล์หรือ node ภายใน
├── rules.md               # กฎหรือ boundary เบื้องต้น
├── status.md              # สถานะล่าสุดของ folder/node
├── links.md               # link ไป hub, repo, graph, health, table-x
└── files/                 # เนื้อหาหรือเอกสารลูก
```

ในระยะแรก ไม่จำเป็นต้องมีทุกไฟล์เสมอไป แต่ `README.md` ควรมีเป็นแกนขั้นต่ำ

---

## 5. Metadata ที่แนะนำ

CN-Fold แต่ละชุดควรมี metadata แบบอ่านง่าย เช่น:

```yaml
cn_fold:
  id: CNF.W3.STATUS.CN_FOLD
  name: CN-Fold
  type: status/reference
  host: BBX19/status
  parent: BBX19/status
  boundary: internal-working
  sensitivity: S2-S3
  status: observe
  mutation: false
  source_truth: GitHub
  registry: Airtable/latest-result
  review: BBX19
```

ความหมาย:

| Field | ความหมาย |
|---|---|
| `id` | identity ถาวรของ folder/node |
| `name` | ชื่อใช้อ่าน |
| `type` | ประเภทของ CN-Fold |
| `host` | พื้นที่หรือ folder แม่ที่เป็นเจ้าบ้าน |
| `parent` | parent node หรือ parent folder |
| `boundary` | ขอบเขตการใช้งาน |
| `sensitivity` | ระดับความไว เช่น S1-S4 |
| `status` | สถานะล่าสุด เช่น GREEN / BLUE / OBSERVE / BLOCK |
| `mutation` | มีการเปลี่ยน source truth หรือไม่ |
| `source_truth` | แหล่งความจริงหลัก |
| `registry` | กระดานอ้างอิงผลลัพธ์ล่าสุด |
| `review` | ผู้ตรวจหรือผู้อนุมัติ |

---

## 6. ความสัมพันธ์กับระบบอื่น

CN-Fold ทำหน้าที่เป็นจุดกลางระหว่างหลายระบบ:

```text
GitHub Repo
  = source truth / blueprint / fossil

WE PAPER / Base44
  = external document surface / visual folder tree

Airtable
  = latest result registry / table-x reference board

Graph View
  = แสดง node, folder, host, relation

Hbtisocity
  = city-level system map / external operation model

w3api / Rytm Gate
  = port/gate access model ในอนาคต
```

CN-Fold ไม่ควรแย่งหน้าที่ของระบบเหล่านี้ แต่ต้องช่วยให้แต่ละระบบรู้ว่าเอกสารหรือ node นั้นอยู่ในบริบทไหน

---

## 7. ความสัมพันธ์กับ WE PAPER / Base44

ใน WE PAPER หรือ Base44, CN-Fold ควรถูกแสดงเป็น folder tree ที่มี parent-child structure ชัดเจน

ความต้องการขั้นต่ำ:

```text
1. แสดง folder tree ได้
2. expand / collapse folder ได้
3. สร้าง folder ใหม่ได้
4. สร้าง sub-folder ใต้ HOST folder ได้
5. ย้ายไฟล์เข้า folder ได้
6. ไฟล์ต้องจำ folderId / parentId / path ได้
7. Graph View ต้องอ่าน relation นี้ไปใช้ได้
```

ตัวอย่าง:

```text
HOST: blueprints/
└── abstract/
    ├── W3_INTERNAL_NODE_MAP_TH.md
    ├── W3_BOUNDARY_MODEL_TH.md
    ├── W3_NODE_RELATIONS_TABLE_TH.md
    └── W3_PUBLIC_SURFACE_PLAN_TH.md
```

ในกรณีนี้ `abstract/` สามารถถูกมองเป็น CN-Fold ได้ เพราะมีบทบาทชัดเจนและมีเอกสารลูกที่อยู่ในบริบทเดียวกัน

---

## 8. ชนิดของ CN-Fold

ตัวอย่างชนิดที่อาจใช้:

| Type | ความหมาย |
|---|---|
| `status/reference` | ใช้เก็บสถานะหรือคำอธิบายระบบ |
| `blueprint` | ใช้เก็บแบบจำลองหรือแผนโครงสร้าง |
| `protocol` | ใช้เก็บกฎ วิธีเชื่อม หรือภาษากลาง |
| `evidence` | ใช้เก็บ log, report, outcome |
| `hub` | ใช้เป็นจุดรวม link / port / external references |
| `experiment` | ใช้แยกพื้นที่ทดลอง |
| `fossil` | ใช้เก็บของผิด/เก่า/บทเรียนที่ยังมีค่า |

---

## 9. Boundary และสิทธิ์

CN-Fold ไม่ได้แปลว่าใครก็แก้ไขได้

กฎเบื้องต้น:

```text
- GitHub ยังเป็น source truth
- Airtable เป็น latest result registry เท่านั้น
- WE PAPER/Base44 เป็น external document surface
- CN-Fold ช่วยอธิบายและจัด relation
- การแก้ source ต้องมาจาก BBX19, ระบบที่ได้รับมอบหมาย, หรือขอบเขตอำนาจของ project
- ถ้าไม่แน่ใจ ให้ใช้ status: OBSERVE หรือ UNKNOWN
```

CN-Fold จึงเป็นเครื่องมือจัดบริบท ไม่ใช่สิทธิ์ในการแก้ความจริงหลัก

---

## 10. Color State ที่แนะนำ

CN-Fold สามารถผูกกับระบบสีได้:

| Color / State | ความหมาย |
|---|---|
| GREEN | ใช้งานได้ / stable |
| BLUE | observe / active movement / กำลังขยาย |
| YELLOW | review / ต้องตรวจ |
| RED | block / ห้ามเดินต่อ |
| PURPLE | relation-heavy / กระทบหลาย node |
| DARK | inactive / unknown / no data |

ตัวอย่าง:

```yaml
status: BLUE
reason: external folder model is active but still under observe
mutation: false
```

---

## 11. ตัวอย่าง CN-Fold: blueprints/abstract

```yaml
cn_fold:
  id: CNF.BLUEPRINTS.ABSTRACT
  name: blueprints/abstract
  type: blueprint
  host: blueprints
  boundary: internal-working
  sensitivity: S2-S3
  status: GREEN-BLUE
  mutation: false
  source_truth: GitHub
  registry: Airtable/latest-result
  review: BBX19
```

ไฟล์หลักใน CN-Fold นี้:

```text
W3_INTERNAL_NODE_MAP_TH.md
W3_BOUNDARY_MODEL_TH.md
W3_NODE_RELATIONS_TABLE_TH.md
W3_PUBLIC_SURFACE_PLAN_TH.md
```

บทบาท:

```text
Internal Node Map = กระดูก
Boundary Model = ผิวหนัง / กำแพง
Relation Table = เส้นประสาท
Public Surface Plan = หน้าต่าง / Lamp
```

---

## 12. วิธีใช้งานจริงแบบง่าย

เมื่อเจอ folder หรือกลุ่มเอกสารใหม่ ให้ถาม 6 ข้อ:

```text
1. folder นี้คืออะไร
2. เป็น host ของอะไร
3. มีไฟล์ลูกอะไรบ้าง
4. ขอบเขตเปิดเผยแค่ไหน
5. status ล่าสุดคืออะไร
6. ต้องลง registry หรือ graph ไหม
```

ถ้าตอบได้ครบ folder นั้นสามารถยกระดับเป็น CN-Fold candidate ได้

---

## 13. ข้อควรระวัง

```text
- อย่าทำให้ CN-Fold หนักเกินไปตั้งแต่แรก
- อย่าบังคับทุก folder ให้เป็น CN-Fold
- อย่าใช้ CN-Fold แทน source truth
- อย่าให้ external hub แก้เนื้อหาหลักโดยไม่มีอำนาจ
- อย่าเปิด internal CN-Fold เป็น public surface โดยไม่มี boundary
```

CN-Fold ควรช่วยลดภาระ ไม่ใช่เพิ่มภาระ

---

## 14. สถานะปัจจุบัน

```text
CN-Fold status: draft / observe
Use case: WE PAPER folder tree, Base44 repository library, Hbtisocity, Graph View
Source truth: GitHub
Registry: Airtable latest-result only
Mutation: false
Approval: BBX19
```

---

## 15. Next Actions

รายการที่ควรทำต่อเมื่อพร้อม:

```text
1. ให้ WE PAPER แสดง Folder Tree ให้ชัด
2. ให้สร้าง sub-folder ใต้ HOST folder ได้
3. ให้ move file เข้า folder ได้
4. ให้ไฟล์จำ parentId / folderId / path ได้
5. ให้ Graph View อ่าน relation จาก CN-Fold ได้
6. เพิ่ม CN-Fold field ใน Airtable เฉพาะผลลัพธ์ที่เกิดแล้ว
7. สร้างตัวอย่าง CN-Fold จริง 1 ชุด เช่น blueprints/abstract
```

---

## 16. สรุป

CN-Fold คือรูปแบบ folder แบบ W3 ที่ทำให้ folder กลายเป็น node ที่มีบริบท

```text
Folder ปกติ = ที่เก็บไฟล์
CN-Fold = ที่เก็บ + แกนอ้างอิง + host + relation + boundary + status
```

เป้าหมายไม่ใช่ทำให้ระบบซับซ้อนขึ้น แต่ทำให้ระบบจัดการเอกสารจำนวนมากได้โดยไม่หลุดจากแกน

CN-Fold จึงเป็นฐานสำคัญของ:

```text
WE PAPER
Base44
Airtable latest-result registry
Graph View
Hbtisocity
w3api / Rytm Gate ในอนาคต
```
