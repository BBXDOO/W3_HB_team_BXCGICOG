# รายงานโครงสร้างระบบ W3 + MPCP (ภาษาไทย)

> เอกสารนี้จัดทำเพื่ออธิบายภาพรวมโครงสร้างรีโป ความเชื่อมโยงของโฟลเดอร์/ไฟล์ และลำดับการส่งงานเมื่อเกิดเหตุการณ์ เช่น เปิด Issue หรือ Pull Request

---

## 1) ภาพรวมระบบ

รีโปนี้ทำงานแบบ **หลายชั้น (multi-layer)** โดยมีแกนหลัก 3 ส่วน:

1. **Runtime / Routing Core**
   - จัดการการวิ่งงานจริง, route งานไปยัง agent/module ที่รับผิดชอบ
2. **Governance / CI Rules**
   - ตรวจความถูกต้องเชิงกติกา (เช่น metadata, module validity, schema pairing)
3. **Knowledge + Documents + Plans**
   - เก็บองค์ความรู้, แผนงาน, แนวทางปฏิบัติ, รายงานตรวจสอบ

แนวคิดสำคัญคือ: **MPCP เป็นกรอบควบคุมพฤติกรรม/สถานะ** และ **W3Lgu เป็นชั้น orchestration/การส่งต่อบทบาท**

---

## 2) แผนที่โฟลเดอร์หลัก และความเกี่ยวโยง

## 2.1 `core/` (แกน runtime + governance)

- `core/runtime/`
  - engine สำหรับรันงานและ dispatch ไปยัง agent
  - `core/runtime/agents/` คือ agent implementations (เช่น ChatGPT, Gemini, PSP2, REDR, DTML, LRC2)
- `core/module-loader/`
  - `module-registry.json` = routing table keyword -> module
  - `identity/*.idp.json` = identity/profile ที่ runtime ใช้อ่านตอนสร้าง execution plan
- `core/governance/`
  - กฎและหลักควบคุมระบบ เช่น ruleset สำหรับ CI agent
- `core/memory/`
  - memory bus/store สำหรับบันทึกเหตุการณ์, override, runtime traces

**ความเกี่ยวโยง:**
`module-loader` กำหนด “ใครทำอะไร” -> `runtime` วิ่งงานจริง -> `memory` เก็บประวัติ -> `governance` ตรวจว่าอยู่ในกรอบ

---

## 2.2 `modules/` (ทะเบียนโมดูลกลาง)

- `modules/registry.json` = single registry เชิงระบบ (module list, routing, trust, governance)
- `modules/<ModuleName>/module.json` = สเปกของแต่ละโมดูล (role, tier, scope, I/O)

โมดูลใหม่ที่เติมเข้าระบบ:
- `PSP2` = PR Flow Router / STAMP + ROUTE
- `REDR` = Risk Escalation Decision Router
- `DTML` = Decision Trace Mapping Layer
- `LRC2` = Lifecycle Review Checkpoint

**ความเกี่ยวโยง:**
`modules/registry.json` เป็นภาพรวมทั้งระบบ ส่วน `modules/*/module.json` เป็นรายละเอียดรายโมดูล

---

## 2.3 `SYSTEM/TESTS/mpcp/` (แกนทดสอบ MPCP)

- เก็บ runtime sanity tests, contract checks, schema, และเอกสารเชิงแนวคิด
- `schema/` ใช้ตรวจความสอดคล้องข้อมูลตาม schema

**ความเกี่ยวโยง:**
สะท้อนว่า runtime + orchestration ปฏิบัติตามสัญญา MPCP หรือไม่ (state/cause/trace/fail-safe)

---

## 2.4 `iget/` (PR governance assistant)

- `fetcher.py` = ดึงข้อมูล PR จาก GitHub API
- `scorer.py` = คำนวณ risk score และ state
- `reporter.py` = สร้างข้อความสรุป/คำแนะนำ
- `main.py` = จุดรัน flow หลัก
- `tests/` = ชุดทดสอบของ IGET

**ความเกี่ยวโยง:**
IGET เป็นชั้น “วิเคราะห์ PR” ที่เสริม governance และส่งสัญญาณให้การตัดสินใจ merge/review

---

## 2.5 `tools/` (เครื่องมือปฏิบัติการ)

- `tools/w3_agent_ci.py` = orchestrator สำหรับ rule-based CI checks
- `tools/validate_modules.py` / `validate_metadata.py` / `validate_json_schemas.py`
  - ตรวจคุณภาพเชิงโครงสร้างและกติกา

**ความเกี่ยวโยง:**
เป็น quality gate ก่อน merge เพื่อป้องกัน drift ของ metadata, schema, และ module contract

---

## 2.6 `docs/` (เอกสารนโยบายและคู่มือ)

- `docs/roadmaps/` = แผน P1-P3
- `docs/standards/` = naming, repo structure, config SSOT
- `docs/dashboard/` = architecture status dashboard
- `docs/intelligence/`, `docs/operations/`, `docs/metrics/` = แนวทางและ playbook
- `docs/reports/` = รายงานสรุปผล

**ความเกี่ยวโยง:**
ทำหน้าที่เป็น operational memory และ guideline สำหรับทีม/agent ทุกตัว

---

## 3) ลำดับการส่งงานเมื่อเกิดเหตุการณ์ (Issue/PR)

## 3.1 เหตุการณ์: เปิด Issue

1. ผู้ใช้/ทีมเปิด Issue
2. ระบบหรือผู้รับผิดชอบตีความโจทย์เป็น task keywords
3. `core/module-loader/module-registry.json` route keyword ไป module
4. runtime dispatch ไป agent ที่รับผิดชอบ
5. ผลลัพธ์/สถานะถูกบันทึกเข้าหน่วยความจำ/รายงาน

**บทบาทโมดูลโดยย่อ**
- PSP2: ตีตราและส่งต่อ package งานตาม flow
- REDR: ตัดสินใจเส้นทาง escalation เมื่อ risk สูง
- DTML: บันทึก decision trace / ความต่อเนื่องของเหตุผล
- LRC2: ตรวจ checkpoint ก่อนขยับ lifecycle ถัดไป

---

## 3.2 เหตุการณ์: เปิด Pull Request

1. PR ถูกสร้าง
2. IGET ทำงาน: fetch file list -> classify -> score -> state
3. ระบบโพสต์ summary/recommendation และ inline comments
4. CI (`tools/w3_agent_ci.py`) รัน rule checks:
   - module validity
   - metadata consistency
   - python syntax
   - schema validity/pairing
5. ถ้ามี error-severity fail -> บล็อค merge จนแก้ครบ
6. เมื่อผ่าน checks + reviewer อนุมัติ -> merge

---

## 4) แผนผังความสัมพันธ์แบบสั้น

- **Issue/Task Input**
  -> `module-registry` (route)
  -> `runtime/agents` (execute)
  -> `memory/logs` (trace)
  -> `docs/reports` (communication)

- **Pull Request Input**
  -> `iget` (risk scoring)
  -> `tools/w3_agent_ci.py` (governance gate)
  -> reviewer decision (merge/hold)

---

## 5) บทบาทของแต่ละระบบ (ตรงไหน/อย่างไร)

- **MPCP**: กรอบคิด contract/state/trace/fail-safe สำหรับความถูกต้องของ orchestration
- **W3Lgu**: กลไกจัดวางบทบาทและการส่งต่อ package ระหว่างหน่วย (module-based)
- **Runtime Core**: ตัว execute งานจริงตาม route
- **IGET**: ตัววิเคราะห์ PR risk และสื่อสารผลลัพธ์เชิงปฏิบัติ
- **Governance CI**: ประตูตรวจ non-negotiable rules ก่อนเข้า mainline
- **Docs/Standards**: แหล่งอ้างอิงเพื่อให้ทั้งคนและ agent ทำงานบนกติกาเดียวกัน

---

## 6) จุดแข็งและจุดที่ควรระวัง

## จุดแข็ง
- แยกชั้นชัดเจน (route/execute/validate/document)
- มี guardrail ชัดผ่าน CI rules
- รองรับการเพิ่มโมดูลโดยไม่กระทบระบบเดิมมาก

## จุดที่ควรระวัง
- registry หลายจุด ต้องคุมให้ sync เสมอ
- schema pairing ควรครบเพื่อเลี่ยง warning สะสม
- module metadata ใหม่ต้องผ่าน mandatory fields ทุกครั้ง

---

## 7) ข้อเสนอเพื่อความเสถียรระยะยาว

1. เพิ่ม integration test เฉพาะเส้นทางของ PSP2/REDR/DTML/LRC2
2. ทำ script ตรวจ cross-registry consistency อัตโนมัติ
3. ทำ runbook incident response สำหรับกรณี CI fail ตาม rule id
4. กำหนด release checklist มาตรฐานก่อน merge งานใหญ่

---

## 8) สรุป

ระบบนี้มีพื้นฐานดีมากในเชิงสถาปัตยกรรมและ governance
โดยเฉพาะแนวคิด MPCP + W3Lgu ที่วางการส่งงานเป็นขั้นเป็นตอน
หากรักษาวินัยเรื่อง registry/schema/metadata ต่อเนื่อง ระบบจะเสถียรและขยายได้ดี

