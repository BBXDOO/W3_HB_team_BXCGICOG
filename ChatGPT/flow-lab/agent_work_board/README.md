Name : Agent Work Boarding — W3 Systems / Survey workspace  
AM Ⅱ - BUILD : พื้นที่ประยุกต์เพื่อสำรวจบอร์ดตามรอยโค้ดและเหตุการณ์  
Log time : 2026-11-06 (Asia/Bangkok) ; ID : W3-AWB-BOARD-SURVEY-001  
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — ขอบเขตและคู่มืออ่าน

พื้นที่นี้เก็บงานสำรวจสำหรับบอร์ดช่วยค้นหาจุดเสียของ W3 ตามคำขอ BBX19
สถานะปัจจุบันคือสำรวจจุดเริ่มและเก็บหลักฐาน ยังไม่มีตัวบอร์ด HTML หรือเครื่องมือใหม่
เอกสารนี้อธิบายเฉพาะโฟลเดอร์นี้ ไม่กำหนดวิธีทำงานแทนระบบที่สำรวจ

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - docs/governance/AMS.md
  - docs/box/AMS/AMS_README.txt
```

วิธีใช้สำหรับคน: อ่าน [ผลสำรวจ](SURVEY_TH.md) ก่อน แล้วดู [สถานะและงานต่อ](status.json)
สำหรับระบบ/เอเจนท์: อ่าน `status.json` และ `survey_evidence.json` ซึ่งแยก source anchor,
ผลทดลองในเครื่อง และหลักฐานงานเก่าออกจากกัน ทุก source link ผูกกับ commit ที่อ่าน
ไม่มีข้อมูลใดในชุดนี้เป็นคำสั่งให้ execute, retry, ซ่อม หรืออนุมัติงาน

### ความหมายที่ต้องรักษา

- ระบบหนึ่งเข้าร่วมได้หลายเหตุการณ์ หลายเชน และหลายบทบาท
- ช่วงส่งต่อเป็นสิ่งที่บอร์ดต้องตามรอย ไม่ใช้ชื่อระบบเป็นรหัสของช่วงงาน
- แยก host/reference, source call, route proposal, recorded handoff, acknowledgement,
  result และ verification ไม่รวมทุกเส้นเป็น execution
- คงรหัสและสถานะต้นทาง พร้อม namespace ของ runtime/registry ที่ผลิตข้อมูล
- ไม่มีหลักฐานรับงานคือยังไม่ทราบ ไม่สรุปว่าปลายทางเสียหรือหยุดทำงาน

### การทำต่อแต่ละรอบ

1. ตรวจ source commit ใหม่และขอบเขตที่เลือกก่อนใช้หลักฐานเก่า
2. เลือกหนึ่งช่วงส่งต่อพร้อมตัวผลิต/ผู้รับ/ที่เก็บหลักฐานและโค้ดจริง
3. เพิ่มผลสำรวจรอบใหม่ แยกผลที่สังเกต ข้ออนุมาน และงานที่เสนอ
4. อัปเดตคู่มือและสถานะงาน พร้อมรายการที่ยังไม่ทราบ
5. เมื่อสร้างเครื่องมือที่ใช้ซ้ำ ให้เก็บใต้ Workbench `tools/` พร้อม README ประจำเครื่องมือ
   และเก็บข้อมูลโครงการ/ผลสำรวจในพื้นที่โครงการนี้ตามขอบเขต Workbench

## Movement

### M1 — เนื้อหาในพื้นที่นี้

| ไฟล์ | หน้าที่ |
|---|---|
| [README.md](README.md) | คู่มืออ่าน ขอบเขต และวิธีทำต่อ |
| [SURVEY_TH.md](SURVEY_TH.md) | ผลสำรวจแรก ข้อค้นพบ และจุดเริ่มที่เสนอ |
| [status.json](status.json) | สถานะรอบงาน สิ่งที่เสร็จ/ยังไม่ทำ และงานถัดไป |
| [survey_evidence.json](survey_evidence.json) | source hashes/anchors ผลทดลองย่อ และข้อมูลอ้างอิงงานเก่า |

### M2 — พื้นที่สัมพันธ์

- docs.ams : [AMS](../../../docs/governance/AMS.md)
- docs.workbench : [โต๊ะนายช่าง](../../../w3_tool_store/agent_workbench/README.md)
- docs.cross-x : [Cross-X](../../../cross_x/README.md)
- docs.cross-l : [CROLL / Cross-L](../../../croll/README.md)
- docs.wx : [WX](../../../wx/README.md)
- docs.box : [BOX](../../../docs/box/README_TH.md)
- docs.cn-fold : [CN-Fold](../../../BBX19/status/CN-Fold/README.md)
- docs.w3lgu : [W3Lgu](../../../protocol/w3lgu/README.md)
- docs.mfc : [MFC](../../../core/runtime/w3lgu_mfc_logic/README.md)

OWNER : BBX19  
MAKER : ChatGPT / Codex

## จุดต่อล่าสุด — 2026-11-06

อ่าน [ข้อสรุปและคู่มือทำต่อ](checkpoints/2026-11-06.md) ก่อนใช้ข้อเสนอเดิมในผลสำรวจ:
เริ่มฐานความสัมพันธ์ของโค้ดจริงและแอคชั่น แล้วทาบหลักฐานเหตุการณ์แต่ละรอบบนฐานเดียวกัน
เอกสารเป็นลิงก์ประกอบบริบท ไม่เป็นขั้น execution; ช่องว่าง Vertical Space คือพื้นที่แอคชั่น
ตั้งรอบทำงานทุกสองวัน เริ่ม 2026-11-08 ช่วงประมาณ 19:00 เวลาไทย พร้อมบันทึกผล/คู่มือ/สถานะทุกรอบ
