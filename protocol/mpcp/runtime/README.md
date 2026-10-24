Name : MPCP Runtime — Event-bound Paper execution\
AM Ⅲ - BUILD : กระบวนการกระจายคำสั่งและคืนผลภายใต้ ROT\
Log time : 2026-10-24 (Asia/Bangkok; ไม่ระบุเวลา) ; ID : MPCP-RUNTIME-README-001\
Reserved : ยังไม่เปิดเผยตามต้นแบบ AMS

## Body — บทบาท

Runtime ใช้คำสั่งที่ผ่านกรอบ ROT เรียก Modew ที่ host ลงทะเบียน และบันทึกผลจริง การกระจาย Paper เป็นการทำงานของระบบ ไม่ได้บังคับว่าต้องมีไฟล์เอกสาร Paper หนึ่งไฟล์ต่อหนึ่งงาน

```yaml
AM_TYPE: III
ROLE: PROCESS
DERIVED_FROM:
  - protocol/mpcp/MPCP_ORIGIN.md
  - protocol/mpcp/ROT_PAPER.md
  - protocol/mpcp/CO_MODULE_LAW.md
```

### การใช้ Paper Pack

`prepare_paper_pack()` จัดคำสั่งหลายใบให้อยู่ใต้ `CHAIN_ID`, `EVENT_ID`, `PAPER_PACK_ID`, ผู้รับผิดชอบ และ `RETURN_TO` เดียวกัน โดยใช้กฎ inheritance ของ ROT เดิม แต่ละใบมี `PAPER_ID` ไม่ซ้ำและพกเฉพาะงานของตัวเอง

รายการ Paper ที่เป็นข้อความอ้างอิงต้องมี `resolve_reference` จาก host เพื่อคืนคำสั่งจริง ระบบไม่ตีความชื่อหรือข้อความอ้างอิงเป็นคำสั่งโดยอัตโนมัติ เก็บ source reference ไว้ในบันทึกชุดงาน

`PaperPackRuntime.run()` รับ routes ที่ host เลือก ตามด้วย `PaperPermit` ที่ผูก hash ของชุดงาน คำสั่ง เส้นทาง และข้อมูล Condien ที่ส่งจริง การระบุชื่อผู้อนุมัติในคำขอไม่สร้างสิทธิ์ Host ต้องยืนยันตัวตนและสิทธิ์ของผู้ใช้ก่อนสร้าง permit หรือเรียก reconcile API นี้เป็น trusted local API ไม่ใช่ public authentication service

ลำดับใช้งาน:

1. เรียก `run(pack, routes=..., verify=...)` โดยยังไม่ส่ง permit จะตรวจความพร้อมและคืน `WAIT` พร้อม `pack_hash` โดยไม่รัน Modew
2. Host ตรวจงานและสิทธิ์ แล้วสร้าง `PaperPermit(pack_hash, paper_id, modew, evidence)` เฉพาะใบที่อนุญาต
3. เรียก `run()` อีกครั้งพร้อม permits ใบที่มีสิทธิ์จึงเริ่ม ส่วนใบอื่นคง `PENDING`
4. Runtime ส่งเฉพาะ Paper นั้น, payload ของงาน, identity และ Condien ที่ประกาศ READ ให้ผู้ทำ ไม่ส่งทั้ง Pack หรือคู่มือ ROT ไปให้ทุกหน้างาน
5. Host verifier ตรวจผลจริงก่อนยอมรับ `COMPLETED` แล้วเก็บผลแยกราย Paper พร้อมจุดคืนผลเดิม

เริ่มหลาย Paper ได้ในคำขอเดียว และจัดแต่ละใบให้คนละ Modew/พื้นที่ได้ รุ่นนี้เรียกผู้ทำในเครื่องตามลำดับ ไม่ได้เปิด thread รันขนานหรือส่ง remote agent อัตโนมัติ Paper อิสระที่เหลือทำต่อได้แม้ใบหนึ่ง STOP; งานที่ต้องพึ่งผลกันต้องให้ผู้จัดงานแบ่งรอบและอนุญาตตามเงื่อนไข ยังไม่มี dependency scheduler

### การหยุดและกลับมาทำต่อ

- บันทึก `IN_PROGRESS` ก่อนเรียกผู้ทำ ใช้ OS file lock ต่อชุดงานเพื่อกันการรันซ้ำจากหลาย process
- เมื่อ restart พบงานค้าง จะเปลี่ยนเป็น `NEEDS_RECONCILIATION` ไม่เรียก executor นั้นซ้ำ
- งานที่สำเร็จแล้วจะตรวจชิ้นงานซ้ำด้วย host verifier ทุกครั้งที่อ่านกลับ หากชิ้นงานเปลี่ยนจะรอการจัดการ ไม่เขียนทับซ่อมเอง
- `reconcile()` ให้ trusted host บันทึกผลที่ตรวจพบพร้อมหลักฐานโดยไม่รันซ้ำ เก็บผลก่อนหน้าใน history
- `review_accepted=True` ยอมรับได้เฉพาะผลสำเร็จที่ตรงกับผลบันทึกเดิมและตรวจผ่าน ไม่เปลี่ยน STOP/WAIT เป็นสำเร็จด้วยการกดอนุมัติ
- เปลี่ยนคำสั่ง เส้นทาง หรือข้อมูลที่ผูกไว้ภายใต้ identity เดิมจะถูกปฏิเสธ ให้สร้างชุดงาน/เหตุการณ์ใหม่โดยรักษาหลักฐานเดิม
- `SUCCESS` ของรายงานหมายถึง Paper ทุกใบใน Pack นี้มีผลที่ตรวจผ่าน ไม่ได้ประกาศปิดเหตุการณ์อื่นหรือรับรองความพร้อมของ W3 ทั้งระบบ

ใช้ `fcntl` lock บน Linux/Termux/macOS รุ่นนี้ยังไม่รองรับ Windows ใน API กระจาย Paper การแยก output directory ไม่ใช่ OS security sandbox ต้องใช้ source และ host ที่เชื่อถือได้ ไม่มีการ rollback ผลภายนอกหรือกู้ข้อมูลจากดิสก์เสียหายอัตโนมัติ

### อุปกรณ์สร้างไฟล์ที่ใช้จริงรอบแรก

`FileVoidTextModew` รับ template, values และ target จาก `CONTENT` ใช้ text resolver ทำรูปจากต้นทางผ่าน File.void แล้วสร้าง persistence handoff ก่อนให้ external writer เขียนไฟล์ใน root ที่ host กำหนด

File.void ยังคงไม่เขียน final storage เอง `write_performed:false` ใน handoff ไม่ได้แปลว่า external writer ไม่เขียน ผลของ writer แยก `write_performed:true` และ `mutated:true` พร้อม path/hash/จำนวน bytes ให้ตรวจได้

รองรับ `.md` และ `.txt` ด้วย Python `string.Template` เท่านั้น ไม่อ้างว่าแปลง PDF หรือรองรับทุก lib ไม่เขียนทับไฟล์เดิม ไม่อ่าน template จากพาธที่คำขอสั่ง และไม่ติดตั้ง dependency ตามคำขอ

### เรียกจาก CLI

จาก root รีโป้:

```sh
python tools/mpcp_papers.py --request tools/agent_sandbox/paper_pack.json --output local_workspace/paper-work
python tools/mpcp_papers.py --request tools/agent_sandbox/paper_pack.json --output local_workspace/paper-work --execute
```

คำสั่งแรกคืน WAIT; คำสั่งที่สองอนุญาตเฉพาะ local text capability สำหรับชุดงานนี้ เกิด `artifacts/report.md` และ `artifacts/continuity.txt` พร้อม `result.json`, `trace.log` และ journal ใน `papers/` เรียกซ้ำด้วยชุดเดิมได้โดยไม่สร้างไฟล์ซ้ำ

CLI เป็นการใช้สิทธิ์ของผู้ปฏิบัติงานในเครื่อง ไม่อ้างว่า BBX19 อนุมัติคำขอที่ไม่ได้ให้จริง Exit code: 0 = ทุก Paper ผ่าน, 2 = ยัง WAIT/STOP, 1 = input/host error

## Movement — การนำทาง

### M1 — สิ่งที่อยู่ใน runtime/

| รายการ | หน้าที่ |
|---|---|
| [README.md](README.md) | ขอบเขตและวิธีใช้ runtime |
| [entry.py](entry.py) | จุดนำเข้า API เดิมและ Paper API |
| [executor.py](executor.py) | รับงานเดี่ยว เรียก Modew และตรวจผล |
| [paper.py](paper.py) | เตรียม กระจาย ผูกผล และกู้สถานะ Paper Pack |
| [trace.py](trace.py) | บันทึก operation trace |
| [__init__.py](__init__.py) | exports ของ runtime เดิม |

### M2 — เอกสารและอุปกรณ์ที่สัมพันธ์กัน

- docs.rot : [ROT Baseline](../ROT_BASELINE.md)
- docs.cooperation : [Cooperative Module Law](../CO_MODULE_LAW.md)
- docs.file-void : [File.void tool](../../files_void/README.md)
- docs.text-equipment : [FileVoidTextModew](../modew/file_artifact.py)
- docs.cli : [Paper CLI](../../../tools/mpcp_papers.py)
- docs.example : [ตัวอย่างสอง Paper](../../../tools/agent_sandbox/paper_pack.json)
- docs.tests : [Paper runtime tests](../../../tests/test_mpcp_paper_runtime.py)

---

OWNER : BBX19\
MAKER : ChatGPT / Codex — ผู้ดูแลที่ BBX19 มอบหมายในบทสนทนารอบนี้
