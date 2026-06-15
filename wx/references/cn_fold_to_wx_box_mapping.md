# CN-Fold to wx:BOX Mapping Reference

> Status: draft / observe  
> Runtime: none  
> Mutation: false  
> Owner approval: BBX19

เอกสารนี้ใช้เป็นแผ่นเทียบความหมายระหว่างแนวคิด `CN-Fold` กับโครง `wx:BOX`

---

## 1. Core Meaning

```text
CN-Fold = Cross-Nodes Folder
wx:BOX  = reference container / manifest / lightweight node box
```

ทั้งสองแนวคิดมีจุดร่วมคือทำให้สิ่งที่เป็น folder/document group มีบริบทที่อ่านได้ ไม่ใช่แค่ที่เก็บไฟล์

---

## 2. Mapping Table

| CN-Fold | wx:BOX | ความหมาย |
|---|---|---|
| Folder + Node | `box.id`, `box.type` | โฟลเดอร์ถูกมองเป็น node อ้างอิง |
| Host | `host.path`, `host.scope` | พื้นที่เจ้าบ้านของกล่อง |
| Boundary | `boundary.*` | ขอบเขตการมองเห็น / การแก้ / การส่งออก |
| Index | `index.files`, `index.folders` | รายการลูกในกล่อง |
| Relation | `relations.*` | parent / child / linked nodes |
| Status | `box.status` | สถานะล่าสุดของกล่อง |
| Source Truth | `refs.source_truth` | แหล่งความจริงหลัก |
| Registry | `refs.registry` | จุด lookup / latest result |
| External Surface | `refs.external_surface` | WE PAPER / Base44 / Graph View |

---

## 3. Separation Rule

```text
CN-Fold concept = behavior
wx:BOX = usable form
```

ไม่ต้องให้ CN-Fold เป็น protocol ใหม่ในรอบนี้
ให้ wx:BOX รับพฤติกรรมที่จำเป็นเข้ามาแทน

---

## 4. Good Use

```text
Folder group เยอะ
เอกสารกระจาย
ต้องให้ WE PAPER / Base44 / Graph View อ่านได้
ต้องชี้กลับ GitHub source truth
ต้องรู้ parent/child relation
ต้องมี boundary เบื้องต้น
```

ใช้ `wx:BOX`

---

## 5. Bad Use

```text
ต้องการ execute งาน
ต้องการสร้าง environment จริง
ต้องการแก้ source truth
ต้องการแทน MPCP Blueprint
ต้องการแทน IDP
ต้องการให้ folder เป็น authority
```

ไม่ควรใช้ `wx:BOX` ในบทนั้น

---

## 6. Difference from MPCP Blueprint

| Item | wx:BOX | MPCP Blueprint |
|---|---|---|
| งานหลัก | อ้างอิง / จัดบริบท | สร้างสภาพแวดล้อม |
| Runtime | ไม่มี | ใช้โดย runtime/adapter ได้ |
| Config | ชี้ไปหา config ได้ | ใช้ config เติม template |
| Source truth | ชี้ไปหา | ไม่ใช่ source truth เองเสมอ |
| Output | manifest / reference | environment shape |

---

## 7. One-line Summary

```text
CN-Fold ให้แนวคิด folder-as-node; wx:BOX ให้รูปแบบใช้งานจริงแบบเบาและอ้างอิงได้
```
