# Cast IDP v2 และการสะสาง #306 / #309

OWNER: BBX19 · MAKER: ChatGPT / Codex · วันที่ตรวจ: 2 พฤศจิกายน 2026

ฐานซอร์สก่อนปรับ: `f3330b6fd75d09373d9fbafaa1ec8a354126449e`
อนุมัติรอบนี้: ตรวจ Cast เทียบ IDP v2 ปรับปรุงเพื่อทีม แล้วสะสางงานเก่า
รายงานนี้ส่งเข้าวาระถัดไป ไม่บันทึก APPROVE หรือตรวจรับผลงานแทน BBX19

## 1. Cast — สิ่งที่พบและดำเนินการ

อ่าน IDP v2 ของ BBX19, runtime profile, manifest, context protocol,
registry/router, Cast executor และชุดทดสอบแล้ว

| บทบาท/จุดตรวจ | ก่อนปรับ | หลังปรับและข้อจำกัด |
|---|---|---|
| structural_inspect / structural_adapt / capability_learn | registry ส่งได้ แต่ executor คืน UNAVAILABLE | รับ source_paths ที่มีจริง อ่าน IDP และสร้าง source-bound report/private pattern |
| reasoning / interpretation | อาจใช้ memory matches ของงานอื่นแทน observation ปัจจุบันจน COMPLETED | ต้องมี observation/evidence ที่ส่งชัดเจน; memory เก่าไม่ใช้เติมหลักฐาน |
| context continuity | ยังไม่มีการอ่าน context ของ Cast ใน capability ใหม่ | อ่านและเก็บ hash ของ session_summary เป็น historical context แยกจาก facts |
| non-destructive design | มีบทบาทใน IDP แต่ไม่มี source inspection รองรับ | AST symbols/imports/calls กับข้อเสนอ review extension points; ไม่ apply patch เอง |
| private pattern | ไม่ได้สร้างจากงานตรวจ | แยกไฟล์จาก report ผูก trace/request/source hashes; ไม่ใช่ source truth |
| metadata | Cast README ยัง candidate / interpreter-only | ปรับเป็น partial-active และอธิบายบทบาท/ขอบเขตตาม IDP v2 |

ไม่แก้ตัวตนหรือเพิ่มอำนาจใน IDP v2 ไม่ย้ายขอบเขตของโมดูลอื่นมาให้ Cast
ตัวปฏิบัติใหม่เลือก repo_root จาก host เท่านั้น ตรวจขอบเขตอ่านจาก manifest
และพื้นที่ Cast เอง ไม่รับ output path/import/command จาก payload
missing input, path escape, symlink escape, syntax error คืน REVIEW_REQUIRED
กรณีเขียนผลงานได้เพียงบางส่วนเก็บ artifact ที่มีจริงและแจ้ง mutated/review

การเรียก Cast กับไฟล์จริง 5 ไฟล์สร้าง report และ private pattern แล้ว:
[ผลเรียกจริง](2026-11-02_cast_execution.json)
[กรณีก่อน/หลัง](2026-11-02_cast_regression.json)

สิ่งที่ยังไม่อ้างว่ามี: general deep-reasoning model, autonomous training,
full structural adaptation หรือการแก้/รับรองทุกระบบจากการอ่าน AST
COMPLETED ของ capability ใหม่นี้หมายถึงผลงานตรวจถูกสร้าง ไม่ใช่บทบาททั้งหมดใน IDP สำเร็จ

## 2. ความน่าเชื่อถือหลักฐานจาก #310

แก้ข้อสังเกตเรื่องผลเก่ารับรอง dependency ใหม่ โดยเก็บ source-manifest.json
และ verifier เปรียบเทียบ hash กับซอร์สปัจจุบันในขอบเขตที่ประกาศ
ชุดทดสอบเปลี่ยน implementation ที่ไม่ใช่ entry point แล้ว verifier ปฏิเสธผลเดิมจริง
ไม่รวม mutable memory, generated evidence, symlink, dependencies ที่ติดตั้ง และ xrea
ผลเก่าไม่มี manifest ยังเป็นประวัติ ไม่ถูกยกระดับเป็นหลักฐานซอร์สปัจจุบัน
review thread ใน PR เก่ายังไม่ถูกทำเครื่องหมาย resolved จากฝั่งนี้

## 3. ผลตรวจเจ็ดระบบรอบใหม่

เรียก fixed inspection เดิมในสำเนาแยก ไม่วนรันใบงาน A/B ที่ตรวจรับแล้ว
ผลรอบสุดท้าย: 134 tests ผ่าน ไม่มี skipped/failure/error และ verifier ผ่านทุกข้อ

| ระบบ | ชุดตรวจผ่าน |
|---|---:|
| MPCP | 45 |
| E-CS | 10 |
| W3Lgu MFC Logic | 35 |
| Cross-X | 8 |
| CROLL | 17 |
| Table-X | 14 |
| PX | 5 |

[ผลและ verifier รอบสุดท้าย](2026-11-02_system_recheck_final.json)
[รายงานเต็ม](../../../repo_events/system_inspections/runs/5c5942db8bc7427ba5af51e048266382/REPORT_TH.md)

มีความผิดพลาดที่ต้องเก็บไว้: รอบแรก JUnit ผ่าน 134 ข้อ แต่ตอน verifier อ่านซ้ำ
Cross-X/pytest.log เป็นไฟล์ว่างและไม่ตรง hash ที่บันทึก จึงไม่รับผลรอบแรก
ยังไม่ทราบเหตุที่ไฟล์ว่าง ไม่แต่ง/ซ่อม log เพื่อให้ผ่าน เก็บรอบแรกไว้และรันใหม่
รอบสุดท้ายตรวจ hash/log/JUnit/source manifest ผ่านครบ 34 checks
มีรอบ candidate ระหว่างทางที่ผ่านก่อนแก้ alias critical_reasoning; เก็บเป็นประวัติและรันตรวจใหม่กับซอร์สสุดท้าย ไม่ย้ายผลเก่ามาผูก hash ใหม่

## 4. รับ–ส่งที่เรียกจริงเพิ่มเติม ไม่ใช้จำนวน tests แทนเชน

[ข้อมูลเข้า/ออกทั้งหมดและ read receipts](2026-11-02_chain_handoff_audit.json)

| จุด | เรียกอะไร/รับส่งจริง | ผลและขอบเขต |
|---|---|---|
| W3-API → W3Lgu MFC | POST /w3/cross ใน TestClient พร้อม intent จริง; สังเกต route_package ถูกเรียก 1 ครั้ง | HTTP 200 accepted; PSP2 และ DTML ยัง REVIEW_REQUIRED |
| W3-API → PX | output เดียวกันเรียก px_from_five_line 1 ครั้ง | สร้าง PX/append envelope จริงใน response; ไม่มีการเขียน W3DB |
| CROLL → Table-X | POST /w3/cross/plan, px=2,1; สังเกต get_workset_from_px 1 ครั้ง; validate_dispatch_plan ผ่าน | planned, execution_allowed=false; ไม่เรียก Modew execution |
| Cross-X | build_cross_x_plan กับ intent เดียวกันใน probe แยก | planned/trace/PX/process preview; ไม่ใช่ downstream call จาก /cross |
| E-CS native | EventFrame + EventChainSystem.process_event ใน probe แยก | CONTINUE; ไม่มีหลักฐานว่า gateway ส่ง event นี้เข้า E-CS เอง |
| MPCP local setup | sandbox CLI เดิมพร้อม execute ในสำเนาแยก | SUCCESS, manifest/ledger verified, source unchanged, phase_ready=false |

ทุก probe เป็น local invocation ใน host ไม่ใช่ production traffic
ไม่สร้าง event_id/package_id ร่วมขึ้นมาให้ independent probes ดูเป็นสายเดียวกัน
read receipt ครบ 8 พาธของ #306 มาจาก host ที่ได้รับมอบหมายในรอบนี้
ไม่ใช่การเพิ่ม IDP grant ของ Origin และไม่แก้ทับ receipt FAILED เดิม

จุด gate ที่พบในเส้นทาง /cross จริง: PSP2 → REVIEW_REQUIRED ตามด้วย DTML → REVIEW_REQUIRED
accepted ของ API จึงไม่ใช่การอนุมัติ execution ปลายทาง
ช่องว่างภาพรวม: ไม่มี registered dispatch path สำหรับคำร้องหนึ่งใบเดินครบ
MPCP / native E-CS / MFC / Cross-X / CROLL / Table-X / PX ในการเรียกเดียว
Cross-X และ CROLL รักษาขอบเขต plan-only ของตน; ไม่ข้ามขอบเขตเพื่อให้เชนดูสำเร็จ

## 5. สะสางสถานะเก่า

### #306

คง issue ปิด แต่ชี้แจงว่า original attempt ถูกแทนที่ด้วยการติดตาม #309
ไม่ใช่การรับรอง execution สำเร็จทั้งเชน
ใช้ resolve_followup() เดิมพร้อม hash ของรายงานนี้สะสาง Origin follow-up เก่า
เป็น SUPERSEDED / consolidated into #309 และเก็บ FAILED receipt/เหตุผลเดิมไว้
state เปลี่ยนใน branch แพตช์ ต้อง merge ก่อนจึงมีผลต่อรอบ Origin ของ branch ใช้งาน
ไม่เปลี่ยน last_review/next_due เพื่อซ่อนงานค้าง

### #309

คง OPEN ด้วยเหตุผลเฉพาะ: production/native traversal ทั้งเจ็ดยัง BLOCKED
อัปเดตหัวข้อสถานะปัจจุบันให้ไม่ใช้ NOT_DISPATCHED ก่อนมีตัวเชื่อม หรือ WAITING_HUMAN
เก่าแทนผล B ที่ตรวจรับแล้ว แยก A/B เดิมที่จบ กับ current handoff gap ที่เหลือ
ไม่ขออนุมัติ A/B ซ้ำและไม่สร้าง Issue ซ้ำเพื่อย้ายปัญหาไปมา
ขั้นต่อไปคือออกแบบ/ลงทะเบียน route และตัวตรวจที่ตรงงานใช้งานจริง โดยรักษา
planner boundary และ identity ของแต่ละระบบ ไม่ใช่ต่อทุก API เป็นลำดับสมมุติ

### งานรายงาน Cast เดิม / Vision

ไม่แก้ hash ใบงานเก่า ไม่เติม APPROVE หรือทำว่า Cast Platform report เดิมเสร็จ
การเพิ่ม capability รอบนี้ตอบงานปรับสมรรถนะ ไม่ใช่รายงานรับ–ส่ง Platform↔W3
ฉบับที่คำร้องเก่าต้องการ จึงคงวาระรายงานเดิมตาม BBX19 ขอไว้รอบถัดไป
Vision อยู่นอกลำดับงานรอบนี้และยังไม่มีผลงานตามโจทย์ จึงไม่ตรวจรับแทน

## 6. ปัญหาที่พบระหว่างอัปเดตสถานะ และการสะสาง

อัปเดต issue body แล้ว Origin บน branch ใช้งานตีความข้อความประวัติเป็นงานใหม่จริง
เกิด directed runs 41448287117 (success ของตัว review) และ 41448291424 (failure)
มี follow-up ซ้ำจาก #309 และ #306 เพิ่มใน state วันที่ 2 พ.ย.
ไม่ถือ success ของ review ว่าคำร้องเชนสำเร็จ และไม่ลบ receipt ใหม่ที่เกิดขึ้น

เพิ่ม marker `<!-- w3-status-update -->` ให้ intake ไม่ dispatch ข้อความสถานะ
และไม่สร้างงานจากการ edited ของ issue ที่ปิดแล้ว; reopened request ยังรับได้
มี regression 5 ข้อพร้อม CI และปรับ issue bodies ให้ไม่มี executable block
ของประวัติเดิม; คำร้องต้นฉบับเก็บใน issue_history.json และ GitHub edit history

นำ state ล่าสุดจาก branch ใช้งานมารวมก่อนสะสาง follow-up ทั้งสามรายการ
เป็น SUPERSEDED/STATUS_UPDATE_DUPLICATE โดยใช้ resolve_followup เดิมพร้อม hash
การแก้ state อยู่ใน PR และจะมีผลเมื่อ merge ไม่เขียนทับ state จาก scheduler อย่างเงียบ ๆ

## 7. การตรวจและสิ่งที่ต้องทำต่อ

- Cast/new evidence binding + existing runtime/Origin: 114 tests ผ่าน (48 คำเตือน utcnow เดิม)
- เจ็ดระบบในสำเนาแยกรอบสุดท้าย: 134 tests ผ่าน และ evidence verifier ผ่านครบ
- native host probes ตามตารางมีผลจริง เก็บ input/output/hash ไว้ ไม่ได้รัน REA ใหม่
- ไม่แก้ xrea prototype, IDP permissions, ไม่ merge/deploy และไม่ลงนามตรวจรับแทน

สิ่งที่เสนอให้ BBX19 พิจารณาในวาระถัดไปคือ PR แพตช์ Cast/source binding/
การสะสาง Origin state นี้ ส่วน #309 ยังคงเปิดด้วยหลักฐานและ next action ชัดเจน
ไม่ใช่เพราะกำลังรอคำอนุมัติที่ไม่มีโจทย์ แต่เพราะยังไม่มีเส้นทาง execution นั้นจริง
