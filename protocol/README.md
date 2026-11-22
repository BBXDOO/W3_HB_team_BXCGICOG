Name : W3 Protocol — พื้นที่รวมระบบย่อยและต้นแบบเฉพาะของ W3  
AM Ⅱ - BUILD : การจัดโครงสร้างและเชื่อมโยงระบบย่อยตามแนวคิดต้นทาง  
Log time : 2026-11-22 (date only; time not recorded) ; ID : RT100A9  
≡ Ar1ra - RAMS

## Body — ความหมายและขอบเขตของ protocol/

`protocol/` ใน W3 **ไม่ได้หมายถึง protocol ตามนิยามสากลโดยอัตโนมัติ** แต่เป็นชื่อพื้นที่สำหรับแนวคิดและ prototype ของระบบย่อยที่ออกแบบเฉพาะในระบบนิเวศ W3 ตามความหมายของเอกสารเดิม การจัดกลุ่มนี้ช่วยให้ค้นหาและเชื่อมโยงองค์ประกอบได้ โดยไม่ทำให้ระบบย่อยกลายเป็นระบบเดียวกันหรือรับสิทธิ์จากกันโดยปริยาย

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - docs/governance/AMS.md
  - protocol/mpcp/MPCP_ORIGIN.md
DOCUMENT_ID: RT100A9
DOCUMENT_PATH: protocol/README.md
SCOPE: protocol/
```

### ขอบเขตการตีความ

- **Preserve:** แนวคิดต้นทางของแต่ละระบบและความแตกต่างระหว่างโครงสร้างกับความหมาย; README ระดับนี้ทำหน้าที่เป็นแผนที่ ไม่ใช่แหล่งนิยามใหม่แทนเอกสารของระบบย่อย
- **Adapt:** จัดกลุ่มเอกสาร โค้ด และส่วนเชื่อมต่อภายใต้ `protocol/` เพื่อให้ตามรอยโครงสร้างและความสัมพันธ์ได้
- **Do not redefine:** ไม่เปลี่ยนกฎของ MPCP, W3Lgu, W3DB, EP-Signal, ECS หรือ File.void และไม่ให้สิทธิ์ execute, deploy, approve หรือ write จากการอ้างอิงใน README
- **Status discipline:** การมีโฟลเดอร์หรือเอกสารไม่ยืนยันว่า implementation หรือ integration ผ่านการทดสอบแล้ว ให้ดูหลักฐานของแต่ละระบบก่อนอ้างความพร้อม

### ที่มาจาก README ฉบับก่อน

README เดิมบรรยายว่า `protocol/` เป็นโครงสร้างใหม่ของโมดูลมาตรฐานกลาง W3 (version 2026) โดยระบุการย้ายบางส่วนจาก root และ `SYSTEM/TESTS/` รวมทั้งหมายเหตุว่า `iget/` ยังอยู่ root ข้อความดังกล่าวเป็น **บันทึกประวัติการจัดโครงสร้าง** ไม่ใช่คำยืนยันว่าการย้ายหรือการอัปเดต import/path/config/test ทุกจุดเสร็จสมบูรณ์แล้ว

บันทึกต้นฉบับ: `13:22 - 110869TH`, `10:34 - 140869TH`, ปรับปรุงล่าสุดที่ระบุ `2026-05-25`, `IDC - RT100A9`, `USE : FOR W3HBT`. ข้อมูลนี้เก็บเพื่อ traceability โดยไม่แปลงรูปแบบวันที่หรืออนุมานเวลาใหม่

## Movement — แผนที่พื้นที่และเส้นทางอ้างอิง

### M1 — รายการใน `protocol/`

| รายการ | บทบาทและขอบเขต |
|---|---|
| [README.md](README.md) | แผนที่ระดับโฟลเดอร์และกติกาการอ้างอิง AMS |
| [w3lgu/](w3lgu/README.md) | ภาษา/ไวยากรณ์การทำงานภายใน W3; ยังต้องตรวจรายละเอียดกฎจากเอกสารระบบ |
| [mpcp/](mpcp/README.md) | ระบบ MPCP และสถาปัตยกรรมที่อ้างอิงแนวคิดเสาปูนลายหินอ่อน |
| [w3db/](w3db/) | พื้นที่ W3DB ที่ README เดิมเชื่อมกับ identity, memorie, signature และการสื่อสาร; ยังไม่พบ README ของพื้นที่นี้ในการตรวจครั้งนี้ |
| [EP_SIGNAL/](EP_SIGNAL/README.md) | EP-Signal: โมเดลการเข้ารหัสข้อมูลด้วยจังหวะสัญญาณ; เอกสารระบุสถานะ Experimental |
| [Files.void/](Files.void/README.md) | เอกสารแนวคิด File.void และสถานะการส่งผ่านที่ยังไม่ resolve |
| [files_void/](files_void/README.md) | แพ็กเกจ Python สำหรับ staging ของ File.void; แยกจากเอกสารแนวคิดใน `Files.void/` |
| [ecs/](ecs/README.md) | Event Chain System: event, contract, template และการสร้างแผน โดยคง boundary กับ MPCP |

**ข้อควรระวัง:** `Files.void/` และ `files_void/` เป็นคนละพาธและคนละบทบาท; ห้ามตีความว่าใช้แทนกันได้เพียงเพราะชื่อคล้ายกัน

### M2 — เอกสารที่เกี่ยวข้องนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.ams | [Architecture Mapping Standard](../docs/governance/AMS.md) | หลัก AM Type, lineage และ Gradation |
| docs.ams-template | [AMS README template](../docs/box/AMS/AMS_README.txt) | รูปแบบ Head / Body / Movement / OWNER / MAKER |
| docs.core | [Core vs Structure](../knowledge/philosophy/corevsstructure.md) | หลักการรักษาความหมายต้นทาง |
| docs.workbench | [Agent Workbench](../w3_tool_store/agent_workbench/README.md) | พื้นที่พัฒนาเครื่องมือที่อาจอ้างอิงระบบใน protocol แต่ไม่ใช่เจ้าของกฎของระบบเหล่านั้น |
| docs.mpcp-architecture | [MPCP architecture](../docs/MPCP_architecture) | ลิงก์อ้างอิงเดิม; ไม่ยืนยันความพร้อมของปลายทางจาก README นี้ |

---

OWNER : BBX19 — เจ้าของระบบตาม README ต้นฉบับ  
MAKER : ChatGPT / Codex — เรียบเรียง README ใหม่ตาม AMS; เครดิตผู้จัดทำเดิม BBX19
