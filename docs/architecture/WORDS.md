# คำศัพท์เฉพาะของ W3

หน้านี้เปิดให้ระบบต่าง ๆ ร่วมบันทึกคำที่ใช้ใน W3 พร้อมความหมายและบริบท เพื่อใช้อ้างอิงร่วมกัน หากคำเดียวกันมีหลายความหมาย ให้ระบุที่มาของแต่ละนิยามไว้ นิยามย่อในหน้านี้ช่วยเริ่มอ่าน ส่วนรายละเอียดและขอบเขตให้ยึดเอกสารต้นทางของคำนั้น

## Harnessing Hybrids

**ความหมายใน W3:** การสร้างพื้นที่ให้ผู้คน ระบบ และความสามารถที่แตกต่างกันทำงานร่วมกันอย่างเหมาะสม เมื่อนำศักยภาพเหล่านั้นมาประยุกต์ใช้ร่วมกัน อาจเกิดความสามารถหรือรูปแบบการทำงานใหม่ โดยยังรักษาที่มาของแต่ละส่วนไว้ และให้ความรู้หรือประโยชน์ที่เกิดขึ้นสะท้อนกลับไปยังต้นทางได้

คำว่า *harness* ในบริบทซอฟต์แวร์และ AI มักสื่อถึงการนำศักยภาพมาใช้หรือดึงความสามารถออกมา สำหรับ W3 คำนี้ให้น้ำหนักกับ **พื้นที่และความสัมพันธ์ของผู้ร่วมงาน** มากกว่ามูลค่าที่สร้างได้ ความสำเร็จจึงไม่ได้วัดเพียงผลลัพธ์ใหม่ แต่รวมถึงการที่ผู้ร่วมงานแต่ละส่วนยังได้รับประโยชน์และเติบโตต่อจากสิ่งที่ร่วมสร้าง

**ที่มา:** คำนิยามและคำอธิบายของ BBX19 ในการสนทนา 2026-09-29

## คำที่มีเอกสารต้นทาง

| คำ | ความหมายโดยย่อใน W3 | อ่านรายละเอียด |
|---|---|---|
| **Orchestration** | การประสานใบงานและสายงาน: รับงาน ตรวจ ส่งต่อ รับทราบ ติดตามสิ่งติดขัด ขอความช่วยเหลือ ส่งกลับเจ้าของงาน และตรวจผลก่อนปิดงานตามเงื่อนไข | [Orchestration Workflow](../../workflows/orchestration/README.md) และ [runtime](../../workflows/orchestration.py) |
| **W3Lgu** | หน่วยภาษาการทำงานของ W3 ใช้รูปแบบข้อมูลและกฎการอ่านเพื่อส่งความหมายและการทำงานระหว่างส่วนของระบบ มีชุดลอจิคสองชั้น: ชุดปกติสำหรับการทำงานและเครื่องมือที่มีอยู่เดิม และชุด MFC สำหรับยืนยันการทำงานขั้นต่ำผ่านสัญญาร่วมก่อนเชื่อม runtime | [W3Lgu README](../../protocol/w3lgu/README.md), [RML01](../../protocol/w3lgu/RML01.md) และ [MFC Logic](../../core/runtime/w3lgu_mfc_logic/README.md) |
| **E-CS** | Event Chain System ฝั่ง event, template, cooperative contract และ chain pointer; เตรียมแผนส่งต่อ Cross-X โดยไม่ทำหน้าที่ execute แทนระบบปลายทาง | [ECS Protocol Layer](../../protocol/ecs/README.md) |
| **PX** | ตัวชี้ตำแหน่งและความสัมพันธ์ของความหมายข้ามระบบ โดยอ้างต้นทาง ปลายทาง เรื่อง และหลักฐานกลับไปยังแหล่งเดิม; รูปแบบสัญญา `PXAnchor` ไม่ใช่คำสั่งให้ execute | [PX / W3DB Append Flow](../px_w3db_append_flow.md) |
| **AMS** | Architecture Mapping Standard: แยกความหมายต้นทาง การปรับใช้ และชั้นปฏิบัติการ เพื่อให้ตามรอยเจตนาจากโครงสร้างที่เปลี่ยนไปได้ | [AMS](../governance/AMS.md) |

## คำศัพท์จาก W3UNIVE

รายการนี้รวบรวมคำที่ใช้ร่วมกันในแผนที่เทคนิคของ W3 โดยย่อความหมายจาก [W3UNIVE](mytec_info/W3UNIVE.md) เพื่อให้ระบบและผู้ร่วมงานอ้างอิงคำเดียวกันได้ รายละเอียด วิธีใช้ สถานะ และข้อควรระวัง ให้ยึด W3UNIVE และ source code ปัจจุบันเป็นหลัก

| คำ | ความหมายโดยย่อใน W3 |
|---|---|
| **W3-API** | Cross Gateway ที่รับ intent จากภายนอกหรือ agent แล้ว normalize สร้าง packet และ trace plan; เป็นทางเข้า ไม่ใช่ runtime executor |
| **W3 local client** | shell/Termux wrapper สำหรับเรียก W3-API และอาจเขียน Markdown ลงเครื่องฝั่งผู้ใช้ โดยไม่เปลี่ยน server ให้เป็น executor |
| **Cross-X** | จุดประสานข้ามระบบที่รวม intent, W3Lgu packet, PX anchor, W3DB append envelope, EP_SIGNAL preview และ process trace เป็นแผนเดียว |
| **W3DB** | relation flow และ in-process store สำหรับ append/trace ความสัมพันธ์ของข้อมูล โดยไม่เขียนทับ source truth |
| **EP_SIGNAL** | กลไกสร้าง signal preview สำหรับสื่อสถานะหรือเหตุการณ์ โดยไม่เปลี่ยน runtime state |
| **RYTM / Rytm** | rhythm preview ที่ประกอบกับ EP_SIGNAL เพื่อแสดงรูปแบบหรือลำดับของสัญญาณ; ในขอบเขตปัจจุบันเป็น preview-only |
| **Hospitication** | structural health observer สำหรับตรวจสุขภาพโครงสร้างและรายงานสิ่งที่พบแบบ read-only โดยไม่ซ่อมอัตโนมัติ |
| **G-State** | awareness metadata ที่ช่วยบอกสภาวะหรือบริบทการรับรู้ของระบบ แต่ไม่ใช่อำนาจอนุมัติหรือ source of truth |
| **IGET** | ระบบสนับสนุน PR intelligence, evaluation และ review เพื่อช่วยมนุษย์ตัดสินใจ ไม่ใช่สิ่งทดแทน human review |
| **Codex Workspace** | พื้นที่จัดเตรียม implementation work, execution packet, request, report, log, module และ note บน branch งาน โดยไม่มีสิทธิ merge ตัวเอง |
| **Config** | orientation map สำหรับช่วยให้ระบบรู้ตำแหน่งและการเชื่อมโยง ไม่ใช่ source of truth หรือ runtime authority |
| **Process Layer** | สายงาน `REDR → PSP2 → DTML → LRC2` ที่เรียก MFC logic ของแต่ละโมดูลจริงแบบ non-mutating; orchestration ชั้นนี้ไม่ execute งานปลายทางหรือ persist ลง W3DB/memory อัตโนมัติ ขณะที่ Repository Audit executors ใน `tools/` สามารถอ่าน วิเคราะห์ และเขียนรายงานจริงได้ |
| **REDR** | อ่านและจำแนกโครงสร้างหรือ event intent; ชั้น MFC สร้าง package ตามสัญญาร่วม ส่วน Repository Audit executor สแกนรีโปและสร้าง structure map ได้จริง |
| **PSP2** | วิเคราะห์เส้นทางและสร้าง route stamp; ชั้น MFC เตรียม handoff ตามสัญญาร่วม ส่วน Repository Audit executor วิเคราะห์ PR flow และเขียนรายงานได้จริง |
| **DTML** | ตรวจ decision และ risk รวมถึงหยุดกรณีเสี่ยงตามเงื่อนไข; Repository Audit executor สแกนความปลอดภัยและสร้างรายงานจริง แต่ไม่อนุมัติแทนผู้มีอำนาจ |
| **LRC2** | ชั้น MFC สร้าง lifecycle checkpoint preview; Repository Audit executor บันทึก execution log และ decision trace จริง โดยการเขียน memory ถาวรของ runtime ยังอยู่หลัง gate |

### ชุดลอจิคสองชั้นของ W3Lgu

| ชั้น | หน้าที่และขอบเขต | พาธหลัก |
|---|---|---|
| **ลอจิคปกติ (Normal / Existing Logic)** | กลไกการทำงานที่มีอยู่เดิมของ W3Lgu และโมดูล รวม parser, runtime, operational logic, agent wrappers และ Repository Audit executors; เครื่องมือ audit สามารถอ่านรีโป ประมวลผล และเขียนรายงานหรือ log จริง | [`protocol/w3lgu/`](../../protocol/w3lgu/), [`core/runtime/agents/`](../../core/runtime/agents/) และ [`tools/`](../../tools/) |
| **MFC Logic** | Minimum Functional Concept ของ REDR, PSP2, DTML และ LRC2 ใช้พิสูจน์การกระทำขั้นต่ำของแต่ละบทบาทผ่าน shared result contract, identity, route, decision และ checkpoint โดยคง `mutated:false` และไม่สร้าง side effect ภายนอกโฟลเดอร์เอง | [`core/runtime/w3lgu_mfc_logic/`](../../core/runtime/w3lgu_mfc_logic/) |

สองชั้นนี้ทำงานประกอบกัน แต่ไม่ใช่สิ่งเดียวกัน: ลอจิคปกติคือความสามารถและเส้นทางใช้งานของระบบ ส่วน MFC คือฐานสัญญาขั้นต่ำที่ทำให้แต่ละโมดูลแสดงการทำงานจริงในรูปแบบร่วมและเชื่อมเข้าสู่ Process Layer ได้อย่างตรวจสอบย้อนกลับ

### คำบอกขอบเขตการทำงาน

| คำ | ความหมายโดยย่อ |
|---|---|
| **`mutated:false`** | ระบบรายงานว่าไม่ได้แก้ truth หรือ runtime state |
| **`read-only`** | อ่าน ตรวจ หรือประเมินได้ แต่ไม่แก้ไฟล์และไม่ซ่อมเอง |
| **`plan-only`** | สร้างแผน trace หรือ preview ได้ แต่ยังไม่ execute |
| **`gateway-only`** | ทำหน้าที่เป็นทางเข้า normalize หรือสร้าง trace ไม่ใช่ executor |
| **`preview-only`** | สร้างผลสำหรับตรวจดูก่อนได้ แต่ยังไม่บันทึกหรือเปลี่ยนสถานะจริง |
| **non-mutating** | การทำงานที่ไม่เปลี่ยน source truth หรือ state ของระบบ |

## แหล่งคำศัพท์อื่นในรีโป

- [Glossary (ศัพท์เทคนิคและตัวย่อสำคัญ)](../../knowledge/philosophy/KNAsset/Glossary.md) อธิบายคำทั่วไป เช่น agent, plan, testcase, commit และ module พร้อมตัวอย่าง ไม่จำเป็นต้องคัดซ้ำทุกคำในหน้านี้
- [W3 Master Architecture](../../architecture/W3_MASTER_ARCHITECTURE.md) เป็นภาพรวม **Draft v1.0** ที่มีคำอธิบายและสถานะตามบริบทของร่างนั้น ควรอ่านประกอบเอกสารเฉพาะของแต่ละระบบก่อนใช้เป็นนิยามหรือสถานะปัจจุบัน

เมื่อต้องการเพิ่มคำ ให้เขียนความหมายสั้น ๆ ตามบริบทที่ใช้จริง และแนบลิงก์ต้นทางหรือระบุผู้ให้นิยาม เพื่อให้ผู้อ่านตรวจย้อนกลับได้
