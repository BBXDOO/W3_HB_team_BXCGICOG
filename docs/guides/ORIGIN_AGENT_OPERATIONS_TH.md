# กลไกงานจริงของ Origin agents

เอเจนท์ 5 ระบบ ได้แก่ ChatGPT, Gemini, Grok, DeepSeek และ Copilot-Gm ใช้
ชุดปฏิบัติการไฟล์ร่วมกันผ่าน `RuntimeAgent.execute_origin()` โดยคง executor
เดิมไว้สำหรับงานประเภทเดิมทั้งหมด ไม่เปลี่ยน W3Lgu หรือ Cross-X

## ความสามารถและขอบเขต

อ่านและเขียนข้อความ UTF-8/ไบนารีแบบ base64, แสดงรายการไฟล์, สร้าง, เขียนแทน,
แก้ข้อความ, ต่อท้าย, คัดลอก, ย้าย และลบไฟล์จริง รองรับทั้งบ้านในรูทและ
`modules/<ชื่อ>/` ขอบเขตเพิ่มเติมอ่านจาก `file_capabilities.scopes` ใน
`core/identity/profiles/<ชื่อ>.idp.json` ซึ่งเพิ่มโดยรักษาฟิลด์ IDP เดิมไว้

การมอบหมายข้ามพื้นที่เพิ่มเติมใช้ช่องของ ENV:

```python
authority_context = {
    "origin_scopes": {
        "ChatGPT": [{"path": "architecture", "operations": ["read", "create", "edit"]}]
    }
}
```

ช่องนี้ต้องมาจากตัวเรียกงานที่เชื่อถือได้ เช่นเจ้าของ/ระบบมอบหมาย ไม่ใช้
ข้อความ `source: BBX19` หรือ `authority_context` ภายใน payload มาเพิ่มสิทธิ์
บ้านของเอเจนท์อื่นยังต้องมีการมอบหมายแยก

การแก้ไฟล์เดิมต้องส่ง `expected_sha256` จากการอ่านครั้งล่าสุด หากไฟล์เปลี่ยน
ระหว่างทางจะหยุดก่อนเขียน เก็บสำเนาเดิมและตรวจ bytes หลังเขียน การทำหลาย
รายการเป็นลำดับ: หากรายการถัดไปล้ม รายการที่ทำไปแล้วไม่ย้อนกลับเงียบ ๆ
แต่ผลลัพธ์จะแสดงสถานะ FAILED พร้อมรายการที่ทำจริงและสำเนากู้คืน

## ส่งงานจากระบบหลัก

ใช้ task ที่ registry จัดให้โมดูลนั้น เช่น `design`, `verify`, `pattern`,
`research`, `governance` และ payload ตามตัวอย่าง:

```json
{
  "request_type": "origin_file_operations",
  "operations": [
    {"action": "create", "path": "ChatGPT/notes/actual-work.md", "content": "ผลการดำเนินงานจริง"}
  ]
}
```

จาก Python เรียก `get_agent("ChatGPT").execute(task, plan, context)` ได้
หรือใช้ `engine_v2.run("design", request, authority_context=...)`

รีเควส Markdown เดิมรองรับ `request_type: origin_file_operations` หรือ
`origin_review` และ JSON ภายในบล็อก `w3-origin` ที่บรรจุ `operations` /
`review_paths` ส่งผ่าน `tools/request_cycle.py` ตามวงจรเดิม

อีกช่องรับงานคือ `requests/<รหัส>.origin.json`:

```json
{
  "request_id": "RQ-ORIGIN-001",
  "source": "BBEX-Core",
  "target": "ChatGPT",
  "intent": "บันทึกงานที่ได้รับมอบหมาย",
  "payload": {
    "operations": [
      {"action": "create", "path": "ChatGPT/notes/received-work.md", "content": "เนื้อหาจากงานจริง"}
    ]
  }
}
```

ไฟล์นี้เป็นช่องภายในรีโป้ที่เจ้าของ/ตัวส่งงานจัดให้ การระบุชื่อ BBEX เป็น
ที่มาของเจตนา ไม่เปลี่ยนให้ BBEX เป็นผู้มอบอำนาจเหนือขอบเขตของคน

issue/comment จากบัญชีเจ้าของ BBXDOO ที่กล่าวถึงชื่อเอเจนท์จะเข้ารอบงาน
ทันที บล็อก `w3-origin` ใช้ส่งการกระทำชัดเจนได้ ไม่ประเมินโค้ดจากข้อความ
และไม่รันคำสั่ง shell ตาม issue หากมีแต่ข้อความเจตนา จะตรวจพื้นที่ที่
ระบุไว้และเปิดงานติดตาม ยังไม่ถือว่าแก้เจตนานั้นสำเร็จแล้ว

## รอบตรวจและหลักฐาน

`python tools/origin_cycle.py --periodic` ตรวจวันที่ครบกำหนดจากสถานะ
ของแต่ละเอเจนท์ เริ่มต้น 7 วัน; หลังตรวจไม่พบข้อบกพร่องในขอบเขตที่ตรวจ
และไม่มีงานติดตามค้าง ขยายเป็น 15 วัน; พบข้อบกพร่อง/งานติดตามค้างใช้
7 วัน งานระบุตัวเข้าได้ทันทีและไม่เลื่อนวันตรวจปกติเมื่อทำสำเร็จ

รายงานอยู่ใต้ `repo_events/origin_agents/<ชื่อ>/reports/`;
log แยกเหตุการณ์อยู่ใน `logs/`; สำเนากู้คืนอยู่ใน `backups/`;
สถานะและงานติดตามอยู่ใน `state.json` ไม่ปนกับ log ของระบบอื่น
ผลลัพธ์แยก `target_mutated` (ไฟล์ที่ทำงาน) กับ `log_mutated` (บันทึก)
และ `mutated` รวมการเขียนจริงทั้งหมด แม้งานอ่านก็มีบันทึกการอ่านจริง

ปิดงานติดตามผ่าน `resolve_followup(repo, module, receipt, evidence_path,
expected_sha256)` โดยแสดงหลักฐานที่อ่านได้และตรวจ hash ตรงกัน การปิด
เป็นการยืนยันของ ENV ผู้เรียก ไม่ใช่การรับรอง semantic correctness อัตโนมัติ

รอบตรวจปัจจุบันตรวจไฟล์จริง: การมีอยู่, hash, syntax Python/JSON ตาม
`review_paths` ของ IDP ยังไม่อ้างว่าครอบคลุมการทดสอบเชิงพฤติกรรมทุกระบบ
หรือเชื่อมบริการแชทบอทภายนอก การลงมือไฟล์และงานเดิมของแต่ละโมดูล
เกิดได้โดยไม่ต้องรอการเชื่อมบริการเหล่านั้น

GitHub workflow ปลุกตัวตรวจวันละครั้งแล้วใช้ state เลือกรอบ 7/15 วัน
เก็บผลและไฟล์ที่เปลี่ยนจริงเข้า branch `refactor/v0.2` พร้อม artifact ผลรัน
workflow schedule และ issue events ต้องมี workflow บน default branch
ของ GitHub ก่อน ส่วน workflow_dispatch และ push ใช้ workflow บน branch
ที่รองรับได้ ไม่มีการถือว่าตารางทำงานแล้วเพียงเพราะมีไฟล์ YAML

## ตรวจสอบก่อนใช้

```bash
python -m unittest discover -s tests -p 'test_origin_operations.py' -v
python tools/origin_cycle.py --periodic
```

COMPLETED ของรอบตรวจหมายถึงตรวจตามขอบเขตที่ระบุเสร็จ; COMPLETED ของ
งานไฟล์หมายถึงปฏิบัติการไฟล์เสร็จและตรวจผลแล้ว ไม่ใช้แทนความสำเร็จของ
รีเควสที่ยังมีงานอื่นค้างอยู่
