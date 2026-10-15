---
AM_TYPE: III
ROLE: OPERATIONAL
DERIVED_FROM:
  - docs/governance/DECLARATION_IV.md
  - iget/README.md
  - iget/docs/SIGNAL_SYSTEM.md
OWNER: BBX19
MAKER: ChatGPT
---

# IGET: ตรวจโครงสร้างและติดตามหลักฐาน

ปรับใช้ 0.5 กับรอบตรวจ Origin: มองเห็นสถานการณ์ก่อนตัดสินใจ รักษาเหตุผลและสิ่งที่ยังไม่รู้
การปรับครั้งนี้ไม่เปลี่ยนตัวให้คะแนน PR เกณฑ์สีเดิม หรือระบบ MPCP

## ผลที่อ่านได้เร็ว

| สิ่งที่พบ | การรายงาน |
|---|---|
| อ่านไฟล์และตรวจในขอบเขตได้ | EVIDENCED พร้อม hash และพาธ |
| พบไฟล์ขาด อ่านไม่ได้ หรือ syntax เสีย | DEFECT และ finding ที่ติดตามได้ |
| ยังไม่พิสูจน์กลไกข้ามระบบ | UNVERIFIED พร้อม unknowns; ไม่สร้าง finding อัตโนมัติ |

สีของรายงานตรวจโครงสร้างเป็น Yellow พร้อมเหตุผลทั้งเมื่อมีข้อบกพร่องที่ต้องตรวจ
และเมื่อได้เพียงหลักฐาน static ที่ยังไม่ยืนยัน runtime สีไม่ใช่ผลอนุมัติหรือคำสั่งซ่อม
ไม่ใช้รอบ 15 วันเป็นสีเขียวหรือคำรับรองว่ากลไกครบ

## ตรวจอะไรจริง

`inspect_structure(root, paths)` อ่านพาธที่ผู้เรียกประกาศเท่านั้น ตรวจ bytes/hash,
Python/JSON syntax และรวบรวมฟังก์ชัน/ชื่อที่ถูกเรียกจาก Python AST
ไม่ execute โค้ดที่อ่าน ไม่ถือว่าการพบชื่อฟังก์ชันเป็นหลักฐานว่ามีการเรียกจริง
พาธซ้ำไม่ถูกอ่านซ้ำ ไฟล์ที่อ่านไม่ได้ถูกแสดงเป็นข้อบกพร่อง

ใช้ ProofTracer เดิมบันทึก scope → observation → findings → limits
รายงาน collaboration/*-review.json มี `iget.proof.trace` พร้อมหลักฐานและเวลา
จึงเปิดอ่านได้หลัง process จบ ไม่เหลือเพียงชื่อขั้นตอนในหน่วยความจำ
ไม่สร้าง causal relation ระหว่างโมดูลจากชื่อหรือการคาดเดา

## ติดตามเรื่องเดิม

รหัส finding คำนวณจาก kind + path + check จึงไม่เปลี่ยนเพราะเวลา/ข้อความอธิบายเปลี่ยน
state.review_findings เก็บ first_seen, last_seen, occurrences และสถานะ:

- OPEN: พบข้อบกพร่องในรอบนี้ ใช้รหัสเดิมเมื่อพบซ้ำ
- RESOLVED: ตรวจพาธนั้นซ้ำแล้วไม่พบข้อบกพร่องเดิม
- NOT_RECHECKED: เรื่องเดิมไม่ได้ตรวจซ้ำ ยังถือว่าค้าง

การแก้ syntax แล้วอ่านไฟล์ไม่ได้ไม่ถือว่าแก้สำเร็จ
ประวัติที่ปิดแล้วไม่ถูกลบ หากกลับมาพบใหม่จะเปิดรหัสเดิม
รายงานแต่ละรอบยังคงอยู่ แยกจาก snapshot สถานะปัจจุบัน

ข้อจำกัดทั่วไปจากเวอร์ชันเดิมชื่อ circuit_verification_required จะถูกนำออกจากบัญชี defect
เมื่อรอบตรวจถัดไปทำงาน ความไม่แน่นอนยังปรากฏในรายงาน ไม่ถูกเปลี่ยนเป็นการตรวจผ่าน
ข้อมูลประวัติรายงานเก่าไม่ถูกเขียนทับ

## รอบ 7 / 15 วัน

- 7 วัน: Origin ตรวจไม่ผ่าน มี defect OPEN/NOT_RECHECKED หรือ follow-up ยังเปิด
- 15 วัน: ตรวจผ่านในขอบเขต ไม่มี defect ค้างและไม่มี follow-up เปิด

หลักฐานตัดสินรอบและรายการติดตามอยู่ในรายงานรอบตรวจ `reports/*.md`
ทั้งสองรอบอาจยังมี UNVERIFIED ได้ เพราะความถี่ติดตามและความครอบคลุมเป็นคนละข้อมูล
ไม่มีสิทธิซ่อมเพิ่มจากการเปลี่ยนช่วงเวลา การซ่อมโครงสร้างยังต้องรอ BBX19 เลือกจุด

## ใช้งานและตรวจสอบ

ใช้คำสั่ง Origin เดิม:

```bash
python tools/origin_cycle.py --periodic
```

คำสั่งนี้สามารถรับใบงานค้างด้วย อ่าน [คู่มือ Origin](../../docs/guides/ORIGIN_COLLABORATION_TH.md) ก่อนใช้
ชุดทดสอบตรวจทั้ง IGET เดิมและกรณีไฟล์เสีย → พบซ้ำ → แก้จริง → ปิดเรื่อง:

```bash
python -m pytest --import-mode=importlib iget/tests tests/test_origin_operations.py tests/test_origin_collaboration.py tests/test_request_cycle.py tests/test_orchestration.py -q
```

Owner: BBX19 · Maker: ChatGPT · Log: 2026-10-16
