---
template_id: BOX:WX_BOX_MINIMUM_V1
version: 0.1.0
scope: reference_container
boundary: reference_only
deny: truth_mutation,runtime_execute,source_write,auto_copy
owner: BBX19
status: draft
created_at: 2026-06-15
---

# wx:BOX Minimum Template

> Template ID: `BOX:WX_BOX_MINIMUM_V1`  
> Status: draft  
> Runtime: none  
> Mutation: false  
> Copy before use: yes

Template นี้ใช้สร้างกล่องอ้างอิงแบบเบา โดยรับแนวคิด CN-Fold เข้ามาเฉพาะส่วนที่จำเป็น ได้แก่ host, relation, boundary, index และ status

---

## 1. Minimal Shape

```yaml
box:
  id: BOX.EXAMPLE.NODE
  name: example-box
  type: reference/container
  status: observe
  owner: BBX19
  mutation: false

host:
  path: wx/templates/box
  parent: wx/templates
  scope: internal-working

refs:
  identity: null
  registry: wx/registry/template_registry.json
  source_truth: GitHub
  template: wx/templates/box/wx_box_minimum.md
  blueprint: null

relations:
  parent: wx/templates
  children: []
  linked_nodes: []
  graph: null

boundary:
  visibility: internal
  sensitivity: S2-S3
  can_execute: false
  can_mutate_source: false
  can_export_reference: true
  requires_review: true

index:
  files: []
  folders: []
  notes: []

return:
  result_ref: null
  latest_registry: null
  trace: optional
```

---

## 2. Compact W3/WX Form

```text
WX:BOX,ID:BOX.EXAMPLE.NODE,STATUS:observe,OWNER:BBX19,MUTATION:false
HOST:wx/templates/box,PARENT:wx/templates,SCOPE:internal-working
REF:REGISTRY:wx/registry/template_registry.json,SOURCE_TRUTH:GitHub
BOUNDARY:internal,SENS:S2-S3,EXEC:false,MUTATE:false,REVIEW:true
INDEX:files[],folders[],notes[]
```

---

## 3. Use Rule

```text
BOX = reference container
ไม่ใช่ runtime
ไม่ใช่ source truth
ไม่ใช่ identity เอง
ไม่ใช่ Paper
ไม่ใช่ ROT
```

---

## 4. CN-Fold Behavior Inside BOX

เมื่อ folder ใดถูกยกระดับให้ใช้รูปแบบนี้ ให้มองว่า folder นั้นมีพฤติกรรมแบบ CN-Fold:

```text
Folder ปกติ = ที่เก็บไฟล์
Folder ใน wx:BOX = ที่เก็บ + host + relation + boundary + status + index
```

---

## 5. Required Fields

ขั้นต่ำที่ควรมี:

```text
id
name
type
status
owner
host.path
refs.source_truth
boundary.can_execute
boundary.can_mutate_source
```

---

## 6. Forbidden Use

```text
- ห้ามให้ BOX execute งานเอง
- ห้ามให้ BOX กลายเป็น source truth แทน GitHub หรือแหล่งหลัก
- ห้าม copy identity ทั้งก้อนเข้ามาใน BOX ถ้าอ้างอิงได้
- ห้ามบังคับทุก folder ให้เป็น BOX
- ห้ามใช้ BOX เพื่อเลี่ยง review หรือ boundary
```

---

## 7. One-line Summary

```text
wx:BOX คือกล่องอ้างอิงที่ทำให้ folder/node มีบริบท โดยใช้ reference แทนการล็อกข้อมูลหนักลงไฟล์เดียว
```
