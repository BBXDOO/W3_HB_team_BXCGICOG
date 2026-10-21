# Orchestration Workflow

- **AM type:** III Process
- **ID:** RN-F56 / GN-C / ASM-Space / OAS
- **Status:** executable coordination; capability support and registered workflow recipes
- **Path:** `workflows/orchestration/`

## Head — Role

ประสานคำร้อง ส่งงาน รับหลักฐาน ติดตาม blocker เลือกเครื่องมือหรือโมดูลช่วย และคืนงานให้เจ้าของเดิม โดยเก็บบริบทและสิทธิ์ของงานไว้ การมีชื่อโมดูลในแผนไม่ใช่หลักฐานว่าโมดูลทำงานสำเร็จ

## Body — Current implementation

| ส่วน | โค้ด | การทำงานจริง |
|---|---|---|
| ใบงานและสถานะ | `workflows/orchestration.py` + schema | REQUEST / REPORT / ISSUE / SIGNAL / INTERNAL, routing, support, evidence, human gate |
| วงจรหลายขั้น | `workflows/runtime_circuit.py` | บันทึกแผน ส่งผลระหว่างขั้น ตรวจผล ทำงานต่อหลังรีสตาร์ต และ reconciliation |
| ทะเบียนช่วยงาน | `workflows/support_catalog.py` | เลือกตาม capability / kind / request type / availability / scope; เลือกคู่ที่ไม่ใช่เจ้าของงาน |
| ตัวเชื่อมที่ทำงานได้ | `tools/orchestration_support.py` | เครื่องมือตรวจพาธและ metadata, คู่ตรวจไฟล์ผ่าน Origin executors, CLI และทะเบียนโฟลว |
| คำร้องจาก root | `tools/request_cycle.py` + `tools/runtime_circuit_intake.py` | ใบงาน `runtime_circuit` ใช้ explicit stages หรือเรียกชื่อ workflow ที่ลงทะเบียน |
| คู่ทำงาน Origin | `tools/origin_collaboration.py` | หากระบุคู่ที่ไม่มี เลือก Origin ที่พร้อมแทนและตรวจหลักฐานการอ่าน receipt |
| งานเอกสาร | `tools/document_creation_flow.py` | ขอ W3 Document Allocator ช่วยเขียนไฟล์ แล้วตรวจผล |

ระบบสแกนคำร้องผ่าน `.github/workflows/w3_request_cycle.yml` และตัวเรียก `--pending` มีอยู่แล้ว ไม่ใช่ daemon บนเครื่องผู้ใช้ที่ติดตั้งให้โดยอัตโนมัติ ส่วนการสำรวจ Origin ตามรอบเป็นอีก workflow หนึ่ง

## Movement — Support and return

1. บันทึก blocker ก่อนขอความช่วยเหลือ; ขั้นที่ประกาศ `support` ไว้จะขอช่วยอัตโนมัติหนึ่งครั้งเมื่อสะดุด มิฉะนั้น host เรียก `support_for()` เอง
2. `support_for()` เลือก TOOL หรือ SPECIALIST จากทะเบียนที่ host สร้าง
3. บันทึกเหตุผลการเลือก พร้อม intent ก่อนเรียกตัวทำงาน
4. ส่ง payload, blocker, source_id, destination, effective stage และ input ให้ตัวทำงาน
5. ตรวจผลด้วย verifier ของ adapter; คำว่า `resolved: true` จากตัวทำงานเพียงอย่างเดียวไม่พอ
6. สำเร็จแล้วเข้าสู่ RETURNED โดยไม่เปลี่ยนเจ้าของหรือข้ามขั้น ผู้เรียกจึงสั่ง `continue_work()` เมื่อต้องการลองขั้นเดิมอีกครั้ง
7. ถ้าผลของการเรียกไม่แน่นอน ให้ reconciliation ก่อนเรียกซ้ำหรือเปลี่ยนผู้ช่วย

คู่ Origin มีขอบเขตตรวจ receipt: อ่านไฟล์จริง ตรวจ hash และ Python/JSON syntax ไม่ใช่การรับรองความหมายของผลงานทั้งหมด หากไม่ระบุคู่ เส้นทางช่วยด้วย Orchestration เดิมยังอยู่

## Boundaries

- เครื่องมือทุกตัวใน `tools/` สามารถเพิ่ม adapter ได้ ไม่จำกัดเฉพาะตัวที่เชื่อมไว้แล้ว แต่การพบชื่อไฟล์ไม่ทำให้มันรันได้เอง
- host ลงทะเบียน callable, verifier, availability และขอบเขตสิทธิ์ คำร้องเลือกชื่อ/ความสามารถได้ แต่ไม่ใช่ Python import, shell command หรือคำสั่งอนุมัติ
- โฟลวเรียงตาม dependency และ route จริง ไม่ใช้ tier เป็นลำดับความสำคัญ
- RETURNED คือการคืนผลช่วย ไม่ใช่ COMPLETED ของงานเดิม
- เจ้าของ host ต้องถือ lock ขณะเปลี่ยน task; CLI ที่จัดให้ใช้ lock เดียวกับ request cycle
- ขอบเขต human review, merge และ deploy ของแต่ละระบบยังมีผล

## Usage and references

- [คู่มือการใช้งานและเพิ่มเครื่องมือ/คู่ทดแทน](../../docs/guides/ORCHESTRATION_CAPABILITY_SUPPORT_TH.md)
- [วงจรคำร้องจริง](../../docs/runtime/REAL_REQUEST_CIRCUIT.md)
- [Request routing](definitions/REQUEST_ROUTING.md)
- [Multi-system assignment](assignments/REQUEST_COLLABORATION.md)
- [Handoff template](templates/REQUEST_HANDOFF.md)

## Owner

- **Owner:** BBX19
- **Maker:** W3 Human-AI Team
- **Log:** Git history / saved task history / support receipts
