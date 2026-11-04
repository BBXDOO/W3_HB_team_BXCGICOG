# คู่งาน Origin และ Cast — ผลดำเนินการ 4 พฤศจิกายน 2569

เพิ่มการแยกผู้เดินงาน/ผู้ส่ง ผู้ตรวจ และผู้รับในใบส่งงาน พร้อมจุดเริ่มก่อนเกิดผล
ผู้รับอ่านหลักฐานซ้ำ และ Orchestration ตรวจย้อนใบส่งถึงข้อมูลเริ่มต้นก่อนสรุป
หมายเหตุทุกข้อคงอยู่ แม้มีคำชี้แจงแล้ว รวมคำขอให้เจ้าของอธิบาย ทำอะไร/อย่างไร/เพราะเหตุใด
คำชี้แจงไม่ใช่หลักฐานอนุมัติและไม่ลบข้อผิดพลาด

หากผิดรูปแบบหรือหลักฐานขัดแย้ง หยุดพร้อมรายงานเต็ม เลือกผู้ตรวจใหม่จากความสามารถและสิทธิ์ที่มีจริง
เมื่อระบุหน่วยที่ผิดชัดเจนจึงบันทึกในพื้นที่ตนเอง /notes โดยไม่ทับประวัติ
ถ้าไม่รู้ว่าใครเปลี่ยนหลักฐาน จะไม่กล่าวโทษจากการคาดเดา
ถ้าคู่ใหม่ไม่มีความสามารถรับงานนั้นจริง ให้ระบุว่าหาคู่ไม่ได้ ไม่สร้างผลสำเร็จแทน

แก้ 5 ข้อจาก PR #320: ตัวไฟล์ซ้ำ/alias, IDP ไม่ตรง Cast, ข้ออ้างไม่มีการเขียนซอร์ส,
เปลี่ยนผลระหว่างส่งกับรับ และพาธซ้ำ รวมผลรับเสียรูปแบบที่ต้องยังมี delivery รายงานข้อผิดพลาด

## ผลตรวจ

- unittest ที่เกี่ยวข้อง 133 ข้อผ่าน รวม regression ของ Origin, Cast, paired receipts, รายงานเสีย/ถูกเปลี่ยน และหมายเหตุ
- งานจริงภายในรีโป้ `RQ-PAIRED-20261104-final`: Cast สร้างรายงานกับ private pattern → Gemini ตรวจ → Orchestration ส่งคืน BBX19
- ผล VERIFIED / WAITING_HUMAN ตามจุดหยุดที่กำหนด ใบส่งคู่ 5 ใบ ตรวจย้อนผ่าน
- แนบหมายเหตุ 1 ข้อเรื่องยังไม่รับรอง dynamic callers/ความหมายทั้งหมด/การรันครบปลายทาง
- ไม่มีการสร้าง human approval ผลนี้รอผู้ดูแลรับมอบ
- เพิ่มชุดทดสอบใหม่ใน CI ของ Origin และ MAIN readiness; สถานะ CI บน PR ต้องดูหลังเปิด PR

## ขอบเขต

เชื่อมจริงที่ Origin intake/collaboration กับเครื่องมือ artifact_handoff ในรอบนี้
ตัวส่งงานอื่นของ W3 ยังต้องนำ protocol ไปเชื่อมก่อนจึงจะมีใบส่งแบบเดียวกัน
ไฟล์เก่าที่ไม่มี intake จะไม่ถูกแต่งจุดเริ่มย้อนหลัง
การเปลี่ยนคู่เป็นการเลือกผู้ตรวจใหม่รอรับงานที่แก้แล้ว ไม่รันงานเดิมซ้ำอัตโนมัติ
ผู้ผลิตยังเป็นเจ้าของงานเดิม การเปลี่ยนผู้ผลิตต้องมีผู้แทนที่ทำงานชนิดนั้นได้จริง
ค่าก่อนเริ่มตรวจเฉพาะไฟล์ที่รับตรวจและ Cast IDP ณ จุดตรวจ ไม่ใช่ sandbox เฝ้าการเขียนทุกไฟล์
ใช้ executors Python ภายในและเครื่องมือ host ไม่เรียก AI ภายนอก

[กติกาและวิธีชี้แจง](../../../workflows/orchestration/definitions/PAIRED_WORK.md)
[ผลส่งมอบและหมายเหตุทั้งหมด](handoffs/RQ-PAIRED-20261104-final/delivery.json)

## แก้ตามรีวิว PR #322 รอบที่สอง

ตรวจและแก้ประเด็นไม่ซ้ำกัน 10 ข้อจาก Codex และ Copilot:

| ประเด็น | สิ่งที่แก้และหลักฐานทดสอบ |
| --- | --- |
| เนื้อหา edit ถูกเก็บใน intake | เก็บเฉพาะ metadata ที่อนุญาต ไม่เก็บ old/new หรือคีย์แทรกอื่น; test_edit_bodies_and_unrecognized_fields_are_not_persisted |
| กล่าวโทษหน่วยที่เพียงอ่านไฟล์เสีย | ผูก hash ใบปฏิบัติงานจาก host กับผลผลิตของรอบนั้น และตรวจ hash ปัจจุบันก่อนระบุเจ้าของความผิด; test_read_only_invalid_input_does_not_create_owner_fault / test_unknown_writer_invalid_output_does_not_create_owner_fault / test_tampered_owner_receipt_cannot_establish_producer_fault |
| Baseline ยังไม่ถูกตรวจแต่สรุปว่า Cast ผิด | ตรวจ baseline แยกจาก parser เสมอ ถ้าหาย/เปลี่ยน/อ่านไม่ได้ไม่ระบุผู้กระทำ; test_missing_or_invalid_source_does_not_imply_cast_fault |
| operations ผิดชนิดทำให้ไม่เกิดใบ FAILED | ตรวจรูปแบบก่อนวนเก็บ metadata และยังคืนใบล้มเหลว; test_non_list_operations_still_get_failure_receipts |
| หมายเหตุหายเมื่อใช้ request.payload | อ่านผ่านตัวแกะ transport เดียวกับ operations ครบทั้ง direct/payload/request/request.payload; test_all_supported_context_transports_keep_notes_and_explanations |
| ผู้ตรวจแจ้งว่าไฟล์หายแต่กลับถูกกล่าวโทษ | เปรียบเทียบ findings/status/evidence จริง ยอมรับผล REVIEW_REQUIRED ที่ตรงกัน; test_correct_missing_receipt_review_does_not_blame_reviewer |
| หมายเหตุผิดรูปแบบทำ collaboration ล้มซ้ำ | ตรวจแบบ atomic และเก็บเหตุปฏิเสธในรายงาน BLOCKED พร้อม snapshot/follow-up; test_rejected_annotations_block_with_report_and_followup |
| คำขอ/กติกาเสียก่อนส่งให้ Gemini | ตรวจและสร้างใบส่งก่อน QUEUED หากเสียให้ BLOCKED พร้อม delivery และ snapshot; test_request_and_rules_damage_always_leave_blocked_delivery |
| ไม่มีผู้ตรวจเดิมทำ replacement ล้ม | สร้างรายการเว้นผู้ตรวจเดิมเฉพาะเมื่อมีชื่อ คืนผลหาคู่ไม่ได้พร้อม snapshot; test_no_independent_reviewer_returns_saved_block |
| คำชี้แจงถูกเพิ่มหลังส่งแต่ถูกนับว่าส่งแล้ว | ตรวจความต่อเนื่องและเทียบคำชี้แจงท้ายสุดกับใบที่ส่งจริง; test_explanation_added_after_last_handoff_is_not_certified / test_explanation_omission_or_rewrite_breaks_continuity |

ชุดทดสอบกรณีข้างต้นอยู่ที่ `tests/test_paired_review_regressions.py` และเพิ่มเข้า CI แล้ว

ผลตรวจรอบแก้: unittest ที่เกี่ยวข้อง **146 ข้อผ่าน** และ pytest สำหรับ Orchestration support/recovery กับ system inspection **24 ข้อผ่าน**
pytest มีคำเตือน utcnow เดิม 8 รายการ ไม่มี test ล้ม
หลักฐานการเดินงานรอบแรกคงไว้ตามที่เกิดจริง การแก้ครั้งนี้ยังรอ CI และการรีวิว commit ใหม่บน GitHub
