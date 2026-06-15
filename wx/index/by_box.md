# BOX Human Index — wx:BOX

> Status: draft / navigation aid  
> Source truth: `wx/registry/template_registry.json`  
> Runtime: none  
> Mutation: false

หน้านี้ใช้ให้คนเห็นภาพว่า `wx:BOX` อยู่ตรงไหนใน BOX / Library-WX และดึงแนวคิด CN-Fold เข้ามาอย่างไร

---

## Current wx:BOX components

| Item | Path | Role |
|---|---|---|
| Template family overview | `wx/templates/box/README.md` | อธิบายชุด template ของ wx:BOX |
| Minimum template | `wx/templates/box/wx_box_minimum.md` | copy-before-use shape ขั้นต่ำ |
| Integration blueprint | `wx/blueprints/system/wx_box_cn_fold_integration.md` | ภาพรวมรวม CN-Fold เข้า BOX |
| Mapping reference | `wx/references/cn_fold_to_wx_box_mapping.md` | ตารางเทียบ CN-Fold → wx:BOX |
| Registry entry | `BOX:WX_BOX_MINIMUM_V1` | template registry draft entry |

---

## Visual relation

```text
CN-Fold concept
  = folder-as-node behavior
       │
       ▼
wx:BOX
  = usable reference container
       │
       ├── identity / box id
       ├── host / parent / child
       ├── boundary / status
       ├── index / files / folders
       └── refs → IDP / Registry / Source Truth / Template / Blueprint
```

---

## Safety note

```text
wx:BOX can point, describe, index, and export reference data.
wx:BOX must not execute or mutate source truth.
```
