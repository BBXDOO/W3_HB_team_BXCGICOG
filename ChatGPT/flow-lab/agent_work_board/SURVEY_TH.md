# สำรวจรอบแรก — จะเริ่ม Agent Work Boarding จากอะไร

วันที่: 6 พฤศจิกายน 2569 (Asia/Bangkok)  
ฐาน: `refactor/v0.2` / `aa48fb86b86a41d895e44d485c41a7856944b168`  
ประเภท: OBSERVE / ข้อเสนอประยุกต์ ไม่เปลี่ยนความหมายหรือสัญญาของระบบ

## จุดเริ่มที่เสนอ

เริ่มจาก **ตัวอ่านหลักฐานช่วงส่งต่อ + ตัวชี้ตำแหน่งโค้ด** แล้วจึงทำหน้าบอร์ด
ใช้ชุดงานเก่าที่มี request, handoff, acknowledgement, result, verification และ paired receipts
เป็นตัวอย่างตั้งต้น เพื่อพิสูจน์ว่าเลือกเหตุการณ์แล้วเปิดกลับไปยังหลักฐานและโค้ดได้จริง

หน่วยบนสายงานควรเป็นการเข้าร่วมของระบบ/เอเจนท์ในเหตุการณ์ครั้งหนึ่ง ไม่ใช้ระบบเป็นขั้นงานถาวร
เอกลักษณ์ของระบบคงอยู่ แต่การเข้าร่วมต้องแยกตามต้นทาง เชน เหตุการณ์ ช่วง และครั้งที่ส่ง/รับ
ชื่อและฟิลด์ที่จะใช้ในบอร์ดยังเป็นแบบร่าง ไม่บังคับเปลี่ยน schema ของระบบต้นทาง

## บทบาทของส่วนที่กำหนดทิศทาง

| ส่วน | สิ่งที่อ่านพบจากโค้ด/ต้นทาง | ผลต่อบอร์ด |
|---|---|---|
| Cross-X | `build_cross_x_plan` สร้าง configured event-chain plan และเรียก local process layer แยกกันในผลเดียว | แยกแผนทั้งเชนออกจากผลคำนวณของ local executors |
| E-CS ใน Cross-X | `EventChainRecord` มี chain/event/sequence และ predecessor/successor; `bind_event_return` เก็บผลกลับ | เก็บ planned, inactive, waiting, returned result และ return history ตามต้นทาง |
| Native E-CS | `ecs/event_chain_system.py` ใช้ `EventFrame`, confidence, rooms, active/standby และ next | มี adapter ของตัวเอง; ไม่สมมุติว่ามีทุกฟิลด์เหมือน Cross-X E-CS |
| Cross-L / Table-X | PX เลือก workset, Modew style, boundary และ return contract; dispatch เป็น planner | แสดงเส้นเลือก/เสนอทาง และ stub target; การเรียกฟังก์ชัน planner ไม่เท่ากับ execute Modew |
| WX / BOX | Engine-Index อ่าน registry/front matter; Indexor แนะนำ; PortDC ส่ง registered content เป็นข้อมูล | แยกการค้นหา/อ้างอิง/ส่งออกข้อมูลออกจากการเรียกโค้ดปลายทาง |
| CN-Fold / wx:BOX | host, parent/children, linked nodes, boundary, refs และ status; แนวทางยัง draft/observe | ใช้จัดบริบทและย่อ/ขยายภาพ; parent-child ไม่ใช่ลำดับส่งต่องาน |
| AMS | แยก Core / Adaptation / Operation และที่มา; README อธิบายพื้นที่ของตน | ใส่ provenance/ที่มาและประเภท โดยไม่ยกระดับเอกสารเป็น runtime node |
| W3Lgu operational | มี stages และ LRC2 ledger จริงในหน่วยความจำ; rooms เป็นบริบท ไม่บังคับเดิน 1→6 | ผูก stage/record กับโค้ด แยกการบันทึกใน process ออกจาก persistence ข้าม process |
| W3Lgu 6ROOM | เลือก slot และคืน next handler, support, active/standby; เรียก lens ที่ host ลงทะเบียนได้ | active_systems เป็นข้อมูลจัดสรร ไม่ถือว่าระบบที่ถูกเอ่ยชื่อรันแล้วทุกตัว |
| MFC | REDR/PSP2/DTML/LRC2 มี pure logic; next/standby และ local event identity | เก็บข้อเสนอเส้นทางและผลจริงแยกกัน; ใช้ wrapper/host เป็นจุดตามไปหาการเรียก |
| Orchestration + WorkflowRuntime | host recipes, registered task route, result/verification refs, support selection และสถานะค้าง | ใช้เป็นอีกสายงานที่เกิดได้จริง ไม่บังคับทุกเหตุการณ์ต้องเข้า Cross-X หรือผ่านทุกระบบ |
| MPCP / Paper | host ลงทะเบียน Modew/route, Paper ผูกกับ CHAIN_ID/EVENT_ID/PAPER_PACK_ID และมี permit/verifier | ต้องตาม registry/callback ณ host และผลคืน; TARGET หรือชื่อในเอกสารยังไม่พอระบุผู้ execute |

ตำแหน่งโค้ดและลิงก์ commit+บรรทัดอยู่ใน `survey_evidence.json`
การสำรวจครอบคลุม entrypoints/การเชื่อมที่เลือก ไม่ใช่การรับรองทุกสายงานของ W3

## ข้อค้นพบที่เปลี่ยนวิธีออกแบบ

1. **ชื่อเดียวกันใช้แทน occurrence ไม่ได้** — ระบบหนึ่งกลับมาใช้ซ้ำได้ในเชนอื่นหรือช่วงอื่น
   ส่วน Cross-X `build_event_chain` รุ่นนี้ห้ามชื่อระบบซ้ำในแผนหนึ่งเชน เป็นขอบเขตของตัวผลิตนี้
   ไม่ใช่ข้อจำกัดที่ควรนำไปบังคับทุกข้อมูลบนบอร์ด
2. **Logic27 มีคนละ registry** — MFC มี 27 slots ของตน ขณะที่ SixRoomRuntime มี default slot subset
   และเปิดให้ host register เพิ่มได้ รหัส slot ต้องมีที่มา; ห้าม join ด้วย slot_id ลอย ๆ
3. **PSP2 next ไม่ใช่หลักฐานเรียกปลายทาง** — `route_package` และ wrapper คืน handoff preview
   `process_layer` เป็นผู้เรียกสี่ executors ในทางเดินของมันเอง และมี compatibility projection ของ route
   จึงต้องเก็บทั้ง raw result กับ projection พร้อมชื่อผู้ผลิต
4. **การรันโค้ด planner ก็เป็นเหตุการณ์จริง แต่ผลของมันเป็นแผน** — แยกระหว่าง
   “เรียก planner แล้ว” กับ “เรียกทุก participant ที่อยู่ในแผนแล้ว”
5. **ไอดีต่างตระกูลยัง join อัตโนมัติไม่ได้ทุกจุด** — Cross-X cross_id, process_id,
   EventFrame event_id, Orchestration task/source_id, Paper ids และ trace_id มีเจ้าของต่างกัน
   ต้องอาศัยหลักฐาน handoff/adapter เชื่อม; เมื่อขาดให้เก็บ unknown ไม่สร้างความสัมพันธ์จากชื่อที่คล้าย
6. **สถานะคนละขอบเขตต้องแสดงคู่กันได้** — delivery หนึ่งมี technical_result VERIFIED
   และ task WAITING_HUMAN พร้อมกัน นั่นเป็นจุดหยุดที่กำหนดไว้ ไม่ใช่ระบบเสีย
7. **เว็บปัจจุบันเป็นจุดแสดงผลที่นำมาใช้ต่อได้** — โค้ด `docs/index.html` ที่อ่านมีภาพ/ข้อความสถานะใน HTML
   และ script สำหรับติดตั้ง PWA/service worker; ยังไม่พบตัวอ่าน event evidence ใน script นี้
   รอบนี้ไม่ได้ตรวจ deployed Pages หรือ cache บนโทรศัพท์ จึงไม่สรุปว่าเว็บจริงตรงกับ source ทุกจุด

## ผลที่ลองจริงในรอบนี้

- CROLL: 39 tests ผ่าน; WX: 8 tests ผ่าน; MFC EventField/Logic27: 6 tests ผ่าน;
  MFC module logic: 21 tests ผ่าน รวม **74 tests** เป็น unittest ของขอบเขตเหล่านี้
- ทดลอง `build_cross_x_plan`: ได้ configured events 12 รายการที่ยัง planned และผล local process 4 stages
  ซึ่ง PSP2/DTML คืน review_required ใน input ทดลองนั้น ไม่ใช่การรันครบ 12 ระบบ
- ทดลอง Cross-L ที่ PX 1,1: ได้ BOX suggestion พร้อม event binding; execution_allowed=false
- ทดลอง input ชัด/คลุมเครือกับ MFC และ SixRoomRuntime: ได้ slot/next ต่างกันตามกติกาของแต่ละตัว
- อ่าน paired delivery เก่าหนึ่งงาน มี 5 receipts กับ task history 13 รายการ;
  ตรวจ SHA-256 ของไฟล์ receipts ตามรายการที่ delivery อ้าง แล้วเก็บผลย่อใน evidence
  นี่เป็นหลักฐานงานในอดีต ไม่ใช่การเรียกบริการ AI ภายนอกหรือผล live ในรอบนี้

ไม่ได้รัน FastAPI/HTTP integration หรือ pytest suite เพราะ host รอบนี้ไม่มี fastapi/httpx/pytest
ไม่ได้เรียก xrea MCP หรือเครื่องผู้ใช้ ไม่สร้างงาน production ใหม่ และไม่ทดสอบทุก runtime

## แบบข้อมูลที่ควรทดลองก่อนลงสีหรือวางโหนด

| ข้อมูล | สิ่งที่ต้องรักษา |
|---|---|
| Participant | ระบบ/โมดูล/เอเจนท์/คน พร้อมชนิดและเจ้าของ |
| Source locator | repo, commit, path, symbol, line, SHA-256; มีขอบเขต source-only ชัด |
| Occurrence | namespace ต้นทาง + raw identifiers + ลำดับ/ครั้งที่เข้าร่วมใน event/run |
| Relation | contains/references/imports/calls/selects/proposes/delivers/acknowledges/returns/verifies |
| Evidence | แหล่งไฟล์/เวลา/hash/ขอบเขต; แยก recorded จาก local probe และคำอธิบาย |
| Correlation | การผูกไอดีข้ามระบบจากหลักฐาน พร้อม unknown เมื่อยังเชื่อมไม่ได้ |

โครงนี้เป็นข้อเสนอของบอร์ดเท่านั้น ไม่ใช่ global runtime contract ใหม่
ข้อมูลส่งออกให้เอเจนท์ต้องรักษาความหมายเดียวกับเส้นที่คนมองเห็น

## ลำดับงานถัดไปที่เสนอ

| รอบ | ชิ้นงาน | เกณฑ์จบรอบ |
|---|---|---|
| 1 | Source locator + reader ของ paired handoff/history หนึ่งงาน | เปิดโค้ดได้ตรง commit; แยกส่ง/รับ/ผล/ตรวจ; ตรวจกรณีหลักฐานหาย/hash ไม่ตรง/ชื่อซ้ำ |
| 2 | บอร์ด HTML หนึ่งไฟล์พร้อมข้อมูลและ JSON export | ค้นพาธ/รหัสงาน; เลือกความสัมพันธ์; ตามย้อนและตามต่อ; ใช้ได้บนมือถือ |
| 3 | adapters ของ W3Lgu/MFC/6ROOM | namespace คนละ registry; next เป็น proposal; ไม่มี route ก็แสดง unknown |
| 4 | Cross-X E-CS / native E-CS / W3-API + Cross-L + WX | แสดงงานชนิดเดียวที่เข้ามาคนละทางได้ โดยไม่สร้างหนึ่งเชนบังคับ |
| 5 | MPCP/Paper/ENV, recipe/support และสายเพิ่มเติม | เก็บ host registration, support/return/retry/reconciliation ตามหลักฐาน |
| ต่อไป | การสร้าง snapshot ใหม่และเชื่อมหน้า Pages | เวลา/commit/coverage ชัด; ไม่มีข้อมูลไม่ถือว่าสุขภาพผ่าน |

ตัวอย่างงานเก่าที่เสนอเป็นรอบ 1:
`modules/ChatGPT/reports/handoffs/RQ-PAIRED-20261104-final/`
เหตุผลคือมีต้นทาง request และช่วงส่งกลับให้ตรวจ ไม่ต้องสั่งงานเดิมซ้ำเพื่อทำบอร์ด
ยังไม่ได้พิสูจน์ว่าทุก runtime สร้างหลักฐานในรูปนี้ จึงต้องมี adapter เพิ่มตามชนิดข้อมูล

## ทรัพยากรและการเก็บเครื่องมือ

เครื่องมือใช้ซ้ำจะเก็บใน `w3_tool_store/agent_workbench/tools/` แยกหมวดพร้อม README
ส่วนวิธีใช้เฉพาะระบบเก็บ profiles ตามโครง Workbench ผลงานโครงการนี้อยู่ในพื้นที่ ChatGPT
ตามกติกาแบ่งพื้นที่ที่อ่านแล้ว

เริ่มตัวชี้โค้ด Python จาก AST/แหล่งโค้ดที่มีอยู่ และใช้ paired receipts/history ที่ผลิตไว้แล้ว
xrea เป็นตัวเลือกสำหรับการวิเคราะห์ JS/TS และหลักฐานเชิงลึกเมื่อถึงขอบเขตนั้น
REA MCP probe เดิมมีบันทึกติด process ownership ใน host เก่า; รอบนี้ยังไม่ทดสอบใหม่
เมื่อเลือกส่วนจาก xrea ให้คัดลอกไปเครื่องมือแยกพร้อม source version, license และผลตรวจ

## จุดค้างที่ต้องรักษาไว้

- ยังไม่มีบอร์ด ไม่มีเครื่องมือใหม่ และไม่มี auto-refresh
- ยังไม่ได้ inventory ทุกโมดูล ทุก host registration หรือทุกสายของ Origin/Workflow
- ความละเอียดและประสิทธิภาพของ call graph/dynamic dispatch ยังไม่ตรวจ
- ยังต้องตัดสินจากงานจริงว่าจะเปิดข้อมูลหรือ payload ใดบน Pages; เริ่มแสดง refs/สถานะก่อน
- เก็บ state ต้นทางตามขอบเขตและเวลา ไม่ใช้สีเขียวจาก snapshot เก่ารับรองรันใหม่
- วันละส่วนได้ แต่ทุกครั้งต้องเพิ่มคู่มือ ผลตรวจ ขอบเขตที่ครอบคลุม และจุดต่อใน status
