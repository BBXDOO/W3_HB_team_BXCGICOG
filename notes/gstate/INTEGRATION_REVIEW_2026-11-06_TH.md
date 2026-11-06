# G-State / Hospitication — ตรวจจุดต่อและขอบเขตปัจจุบัน

วันที่: 6 พฤศจิกายน 2569 (Asia/Bangkok)  
ผู้ตรวจ: ChatGPT / Codex ตามคำขอ BBX19  
ฐานที่อ่าน: `refactor/v0.2` commit `acec9e62ac6302570720edf3055151bc1bdc7f14`  
สถานะ: บันทึกตรวจและข้อเสนอ ไม่เปลี่ยนหลักการหรือสิทธิ์ของระบบ

## G-State มีอะไร และส่วนไหนยังเป็นทางเดินต่อ

| พื้นที่ | สิ่งที่ตรวจพบ | ขอบเขต |
|---|---|---|
| [Foundation](../../docs/governance/G_STATE_PAPER.md) | shared operational awareness พร้อม 6 สถานะ และ hooks ที่สงวนไว้ | ให้บริบท ไม่ใช่ executor |
| [Distributed family draft](../../protocol/mpcp/W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md) | เอกสาร `ACTIVE_DRAFT` ใช้คำ Runtime Brain / Adaptive Control | อ่านเป็นเจตนาในร่าง ไม่ใช่หลักฐานว่ามีตัวควบคุมทำงานแล้ว และไม่แก้ให้ตรงกันด้วยการเดา |
| [W3Lgu boot display](../../protocol/w3lgu/bin/runtime.py) | พิมพ์ `G-State: ACTIVE/DEGRADED` จากการมีโฟลเดอร์ adapters/signals/memory | เป็นการตรวจโหนดของ W3Lgu ไม่ใช่การอ่าน 6 สถานะใน Foundation |
| [Process layer](../../core/runtime/process_layer.py) | มี package/payload และหลักฐานรายขั้น | เป็นจุดศึกษาสำหรับส่งต่อบริบท ยังไม่พบ G-State contract โดยเฉพาะในไฟล์นี้ |
| [Orchestration](../../workflows/orchestration.py) | มีสถานะงานและการส่งต่อ | สถานะงานกับสภาพแวดล้อมร่วมต้องแยกกัน |
| [MPCP runtime](../../protocol/mpcp/runtime/README.md) | มี Paper และงานอุปกรณ์จริง | จากการค้น runtime/adapter รอบนี้ยังไม่พบ G-State consumer โดยเฉพาะ |
| [System inspection](../../w3_tool_store/agent_workbench/tools/system_inspection/runner.py) | catalog 7 ระบบ | ไม่มีชุดตรวจ G-State/Hospitication โดยเฉพาะใน catalog นี้ ไม่ใช่ข้อพิสูจน์ว่าไม่มีการตรวจจากทางอื่น |

การทดสอบ G-State เดิมตรวจข้อความและตัวอย่าง ไม่ได้พิสูจน์ว่า runtime รับบริบท
แล้วใช้งานจริง ข้อเสนอถัดไปคือกำหนดกับ BBX19 ว่าใครประกาศสภาพแวดล้อม
ขอบเขตใด เวลาใด และใครอ่าน แล้วทดลองแนบบริบทผ่านงานหนึ่งงานพร้อมหลักฐาน
ผู้ส่ง/ผู้รับก่อนขยาย ไม่สร้างตัวควบคุมใหม่จากชื่อในร่าง

รอบนี้คง Foundation เดิมไว้ และไม่ได้ประกาศว่า G-State ได้ runtime adapter แล้ว

## Hospitication ที่ปรับในรอบนี้

- รุ่น 0.2.0 กรองชนิดไฟล์และ UTF-8 ก่อนนับบรรทัด ไม่แปลงภาพเป็นข้อความ
- แยก xrea ออกจากค่าเริ่มต้น เปิดรวมได้ด้วย `--include-prototypes`
- ระบุเวอร์ชัน ขอบเขต จำนวนที่ตรวจ และสิ่งที่ข้ามในรายงาน
- ไม่เดิน symlink และไม่สรุปว่าโฟลเดอร์ที่ไม่มีอยู่คือการตรวจสำเร็จ
- import metric นับเฉพาะ Python ที่มีตัวอ่านจริง พร้อมระบุส่วนภาษาอื่นที่ยังไม่วัด
- เติมรายการคำที่ semantic/replay analyzers ใช้แต่ตัว observer เดิมไม่ได้เก็บ
- หยุดสร้าง oscillation จากคะแนนคนละด้านในรอบเดียว ยังไม่มีการวิเคราะห์ประวัติตามเวลา
- runner แสดงจำนวนไฟล์ที่ตรวจจริง แยกจากจำนวน metrics

ผลทดลองก่อนเพิ่มเอกสารฉบับนี้: ค่าเดิมอ่าน 6,089 ไฟล์ โดยเป็น xrea 4,231 ไฟล์
และนับ `branding/logo/image.jpg` เป็น 17,689 บรรทัด หลังปรับ ค่าเริ่มต้นวัด
ข้อความ 1,684 ไฟล์; เปิดรวมต้นแบบวัด 5,773 ไฟล์ ตัวเลขนี้เป็นหลักฐานของรอบทดลอง
ก่อนเพิ่มเอกสาร/การแก้ภายหลัง ไม่ใช่จำนวนไฟล์ตายตัวของรีโป้

คะแนน cognitive_cost และ replay_complexity ยังแตะเพดาน 1.0 ทั้งสองขอบเขต
จึงยังแยกระดับภาระของรีโป้ขนาดนี้ได้ไม่ละเอียด การแก้ครั้งนี้ทำให้ขอบเขตซื่อสัตย์ขึ้น
ไม่ได้รับรองว่าสุขภาพระบบดีขึ้น และยังต้องพัฒนาวิธีเทียบกับ baseline ที่เหมาะสม

## จุดต่อที่มีจริงของ Hospitication

| จุดต่อ | ความสามารถจริง |
|---|---|
| CLI / runner | อ่านโครงสร้าง สร้างรายงานและข้อเสนอ ไม่ลงมือซ่อม |
| [W3DB adapter](../../hospitication/w3db_adapter.py) | เมื่อผู้เรียกใช้ชัดเจน สามารถ append สัญญาณ และแปลง detection confidence เป็น stability confidence |
| [Semantic router](../../core/semantic_router.py) | เลือกและคืน agent พร้อม trace; ฟังก์ชันนี้ไม่ได้อ่านรายงานและ execute การตีความให้จบเอง |
| [Six-room](../../protocol/w3lgu/sixroom_runtime.py) | มีชื่อ Hospitication ใน hints/การจัดสรรระบบ ชื่อในรายการไม่ใช่หลักฐานว่ารันสแกนแล้ว |
| [Layer checker](../../scripts/enforce_layer_separation.py) | รับ signals JSON ได้; ปัจจุบันเพียงมี signals จะลด severity RED เป็น YELLOW โดยยังไม่ผูกกับไฟล์หรือความสดของสัญญาณ เป็นเรื่องที่ต้องตรวจแยก ไม่แก้พฤติกรรมของระบบนี้ในรอบนี้ |

## วิธีตรวจและจุดต่อ

รัน tests ของ G-State, Hospitication core/CLI/runner/scope, semantic router,
W3 integration และ PX/W3DB; ผลสุดท้ายบันทึกในคำอธิบาย PR
ใช้ข้อมูลชั่วคราวสำหรับ tests และรายงานทดลองอยู่นอก checkout
ไม่มีการ merge, auto-repair, แก้ข้อมูลต้นฉบับย้อนหลัง หรืออ้างว่าเรียกบริการ AI ภายนอก

ลำดับต่อที่เสนอ: ตรวจความละเอียดของคะแนนกับ baseline → ทดลอง G-State context
หนึ่งงานที่มีผู้ส่ง/รับชัด → พิจารณาเพิ่มการตรวจเฉพาะเข้า inspection ตามขอบเขตที่ยืนยัน
