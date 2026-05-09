# รายงานสถานะการปฏิบัติงานของโมดูล `Copilot-Gm`

- วันที่จัดทำ: 2026-05-09
- ผู้ดูแล: Copilot-Gm
- ขอบเขต: สรุปโครงสร้างการทำงานของโมดูลนี้เท่านั้น
- กติกา: ยึดตามหลักฐานในรีโปเท่านั้น; หากไม่พบให้ใช้ `ยังไม่พบหลักฐาน`

## 1. ข้อมูลระบุตัวตน
- ชื่อโมดูล: `Copilot-Gm`
- บทบาทหลัก: `Policy / Merge / Compliance`
- เจ้าของ/ผู้รับผิดชอบ: `Copilot-Gm`
- ระดับอำนาจ/สิทธิ์: authority = `BBX19`, tier = `L3`
- สถานะในระบบ: `active`

## 2. ขอบเขตหน้าที่

### 2.1 สิ่งที่โมดูลนี้ทำได้
- ดูแลโครงสร้างไฟล์และมาตรฐาน repository
- กำหนด branch policy และ commit / PR guidance
- จัด workflow สำหรับ commit → review → merge
- สร้าง templates สำหรับ README, ENTRANCE, TASK, CHANGELOG, ISSUE
- ดูแล governance / compliance ของ repo
- เชื่อม ingest → validate → publish ระหว่างโมดูล

### 2.2 สิ่งที่โมดูลนี้ห้ามทำ
- ห้าม merge โดยไม่ผ่าน PR และ reviewer
- ห้าม force-push หรือ rewrite history ยกเว้นมีเงื่อนไขประกอบ
- governance changes ต้องผ่าน PR แยก
- ไฟล์ที่พร้อมใช้งานจริงต้องผ่าน Gemini validation ก่อน annotate `status: ready`

### 2.3 งานที่เหมาะจะส่งให้โมดูลนี้
- governance
- policy
- compliance
- branch strategy
- repo structure
- merge readiness

## 3. อินพุต / เอาต์พุต

### 3.1 อินพุตหลัก
- request path: `modules/Copilot-Gm/requests/`
- context/document source: `core/governance/`, `knowledge/`, `docs/`, `modules/registry.json`
- upstream module: `BBX19`, `Gemini`, `ChatGPT`, `Grok`, `DeepSeek`
- required files: `modules/Copilot-Gm/module.json`

### 3.2 เอาต์พุตหลัก
- reports path: `modules/Copilot-Gm/reports/`
- governance path: `modules/Copilot-Gm/governance/`
- logs path: `modules/Copilot-Gm/logs/`
- expected deliverables:
  - governance docs
  - branch policy
  - commit guidelines
  - templates
  - onboarding docs
  - structure-ready artifacts

## 4. วิธีถูกเรียกใช้งาน
- task keywords: `governance`, `policy`, `compliance`
- invoke path / channel: routing ผ่าน `core/module-loader/module-registry.json`
- router mapping: `governance|policy|compliance -> Copilot-Gm`
- runtime path: `ยังไม่พบหลักฐาน` เฉพาะโมดูลในชุดหลักฐานนี้
- CLI / workflow ที่เกี่ยวข้อง: อ่าน `.github/workflows/` ได้ตาม file access

## 5. การตรวจสอบและการกำกับ
- validation gate: `Gemini`
- governance gate: `BBX19`
- ต้องมี human review หรือไม่: มี
- ต้องมี sign-off จากใคร: `BBX19`
- เงื่อนไขก่อน merge / deploy:
  - `No direct commit to main`
  - PR ต้องมี reviewer อย่างน้อย 1 AI engine
  - governance changes ต้องผ่าน PR + reviewer
  - final sign-off โดย `BBX19`
  - high-risk docs ต้องใช้ `Gemini`

## 6. การยกระดับปัญหา (Escalation)
- กรณี critical merge: ต้อง approval
- กรณี governance shift: ต้อง approval
- กรณี cross-module impact: เปิด issue `#cross-module`
- ปลายทาง escalation: `BBX19`

## 7. Context / Memory
- context source ที่เกี่ยวข้อง: `core/governance/`, `docs/`, `knowledge/`
- memory source ที่เกี่ยวข้อง: ใช้กติกากลางผ่าน `Cast/context/protocol.md`
- session continuity:
  - ต้องอ่าน memory ก่อนเริ่มงาน
  - ต้องเขียน summary หลังงาน
- ข้อจำกัดด้าน context: `ยังไม่พบหลักฐาน` ของ backend memory เฉพาะโมดูล

## 8. สถานะการใช้งานปัจจุบัน
- readiness: `ready`
- ความเสี่ยงหลัก: governance choke-point / enforcement gap
- blockers: `ยังไม่พบหลักฐาน`
- จุดที่ยังเป็น experimental: `ยังไม่พบหลักฐาน`
- จุดที่ยังไม่พบหลักฐาน:
  - runtime executable path เฉพาะโมดูล
  - deployment authority ที่ละเอียดกว่านี้
- หมายเหตุเชิงปฏิบัติการ:
  - เป็นแกน governance และ merge readiness ของระบบ
  - ควรใช้คู่กับ Gemini ในงานเสี่ยงหรือ governance-sensitive เสมอ

## 9. แหล่งหลักฐาน
- `modules/Copilot-Gm/module.json`
- `Copilot-Gm/ENTRANCE.md`
- `core/module-loader/module-registry.json`
- `core/governance/operating-guidelines.md`
- `Cast/context/protocol.md`
- `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.md`
