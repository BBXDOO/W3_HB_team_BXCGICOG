# wx:BOX + CN-Fold Integration Blueprint

> Blueprint ID: `BPD:WX_BOX_CN_FOLD_INTEGRATION_V1`  
> Status: draft / observe  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19

เอกสารนี้วางภาพรวมว่า `wx:BOX` จะรับแนวคิดของ `CN-Fold` มาใช้โดยไม่สร้างระบบใหม่ซ้อนทับ BOX

---

## 1. Position

```text
BOX / Library-WX
  = reference infrastructure

wx:BOX
  = reference container / manifest / visible unit

CN-Fold concept
  = folder-as-node behavior
```

สรุป:

```text
ใช้ wx:BOX เป็นแกน
เอา CN-Fold มาเป็น behavior ภายใน BOX
```

---

## 2. Why not split CN-Fold as a new system now

```text
1. BOX มีทิศทางและ registry อยู่แล้ว
2. CN-Fold เป็นแนวคิดจัดบริบท folder มากกว่าตัว runtime
3. การแยกเป็นระบบใหม่จะเพิ่มภาระเอกสารและ relation
4. การรวมเป็น BOX behavior ทำให้เห็นภาพเร็วกว่าและปลอดภัยกว่า
```

---

## 3. Integration Model

```text
GitHub source truth
      │
      ▼
wx:BOX manifest
      │
      ├── refs.identity
      ├── refs.registry
      ├── refs.template
      ├── refs.blueprint
      ├── host / parent / child
      ├── boundary
      ├── status
      └── index
```

---

## 4. CN-Fold Concepts Adopted

| CN-Fold concept | wx:BOX field | Note |
|---|---|---|
| identity | `box.id`, `box.name` | บอกตัวตนของกล่อง |
| host scope | `host.path`, `host.scope` | บอกพื้นที่เจ้าบ้าน |
| parent / child | `relations.parent`, `relations.children` | ใช้ทำ graph / tree |
| boundary | `boundary.*` | ไม่ให้ folder กลายเป็นอำนาจแก้ source truth |
| status | `box.status` | GREEN / BLUE / OBSERVE / REVIEW ฯลฯ |
| index | `index.files`, `index.folders` | รายการลูกแบบเบา |
| source truth | `refs.source_truth` | ชี้แหล่งจริง ไม่คัดลอกทั้งหมด |
| registry | `refs.registry` | ชี้ registry ที่ใช้ lookup |

---

## 5. Flow

```text
New folder / document group
→ ask 6 CN-Fold questions
→ create wx:BOX manifest from template
→ add registry entry only if useful
→ Graph View / WE PAPER / Base44 can read refs
→ no mutation unless a separate approved flow exists
```

6 คำถามจาก CN-Fold:

```text
1. folder นี้คืออะไร
2. เป็น host ของอะไร
3. มีไฟล์ลูกอะไรบ้าง
4. ขอบเขตเปิดเผยแค่ไหน
5. status ล่าสุดคืออะไร
6. ต้องลง registry หรือ graph ไหม
```

---

## 6. Boundary Law

```text
wx:BOX can point.
wx:BOX can describe.
wx:BOX can index.
wx:BOX can export reference data.
wx:BOX must not execute.
wx:BOX must not mutate source truth.
```

---

## 7. Relationship with MPCP Blueprint

```text
wx:BOX
= จัดบริบท / reference / host / relation / status

MPCP Blueprint
= สร้างสภาพแวดล้อมจาก template + config
```

ดังนั้น:

```text
BOX ไม่สร้าง ENV เอง
Blueprint ไม่ควรถูกใช้เป็น folder index
ทั้งสองระบบอ้างอิงกันได้ผ่าน refs
```

---

## 8. One-line Summary

```text
wx:BOX คือทางใช้งานจริงของ CN-Fold concept ใน BOX โดยเก็บเฉพาะ host, relation, boundary, status และ refs ที่จำเป็น
```
