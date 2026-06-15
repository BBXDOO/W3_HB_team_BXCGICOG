# BOX Collections

Collections คือพื้นที่จัดกลุ่มเอกสารหรือองค์ความรู้แบบ curated grouping ภายใน BOX / Library-WX

Collections ไม่ใช่ที่ย้ายต้นฉบับ และไม่ใช่ runtime output

## Purpose

Collections มีไว้เพื่อทำให้มนุษย์และเอเจนท์มองเห็นกลุ่มความรู้ตามบริบท เช่น paper, Cross-L, MPCP, agent work หรือ knowledge lineage โดยไม่สร้าง source of truth ซ้ำ

## Core Rule

Collection ต้องอ้างอิง source documents เท่านั้น

ห้าม duplicate, relocate, rewrite หรือ claim ownership ของไฟล์ต้นฉบับ

## README Inheritance

แต่ละ collection ควรมี README ของตนเอง

README ของ collection ทำหน้าที่เป็นกฎแม่ของไฟล์และ reference ภายใน collection นั้น

ถ้าไฟล์หรือ reference ภายใน collection ไม่ประกาศกฎเฉพาะ ให้ถือว่าสืบทอดกฎจาก README ของ collection

## Allowed

- Curate references
- Group related templates, blueprints, and knowledge files
- Point to original source paths
- Explain scope, boundary, owner, and usage notes
- Support Indexor / Engine-Index navigation

## Denied

- Runtime execution
- Dynamic state storage
- Direct source mutation
- Duplicate source of truth
- Moving original files into collection without explicit review
- Treating collection output as W3DB or runtime memory

## Recommended Collection README Fields

```yaml
collection_id: COLLECTION:EXAMPLE_V1
scope: observe
boundary: planner_only
owner: BBX19
status: draft
deny:
  - runtime_execution
  - truth_mutation
  - duplicate_source
source_policy: reference_only
```

## Final Rule

Collections organize knowledge.

They do not own truth.
