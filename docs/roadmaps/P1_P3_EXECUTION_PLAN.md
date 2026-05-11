# P1–P3 Execution Plan (Repository Action Plan)

อ้างอิงจากสถาปัตยกรรมหลักหัวข้อ Immediate Priorities
(`architecture/W3_MASTER_ARCHITECTURE.md`) และแปลงเป็นงานที่ทำได้จริงในรีโปนี้

## Scope
- ใช้กับทั้ง repo
- เน้นงานที่ merge ได้ทีละชิ้น (small reversible PR)
- ทุกงานต้องมี owner + evidence file

---

## P1 — Stabilization

เป้าหมาย: ลดความซ้ำซ้อนและทำให้โครงสร้างนิ่งก่อนขยายระบบ

### Tasks
1. **Unify naming conventions**
   - จัดรูปแบบชื่อไฟล์/โฟลเดอร์ให้สอดคล้อง (snake_case สำหรับ Python, kebab-case สำหรับเอกสาร)
   - สร้าง `docs/standards/NAMING_CONVENTION.md`
2. **Remove duplicated systems**
   - ตรวจและรวมไฟล์ที่ซ้ำหน้าที่กัน (เช่น router path ที่ชื่อใกล้กัน)
   - เก็บรายการใน `docs/review/DUPLICATION_TRACKER.md`
3. **Standardize folders**
   - ประกาศโครงสร้างมาตรฐานต่อหมวด (`core/`, `docs/`, `modules/`, `tools/`, `tests/`)
   - สร้าง `docs/standards/REPO_STRUCTURE.md`
4. **Central config**
   - รวมค่า config สำคัญเข้าศูนย์กลาง และระบุแหล่งเดียวของความจริง (SSOT)
   - บันทึก mapping ใน `docs/standards/CONFIG_SSOT.md`

### Done Criteria (P1)
- ไม่มีโครงสร้างซ้ำซ้อนที่ไม่ตั้งใจ
- มีมาตรฐาน naming + structure + config ชัดเจน
- งานทั้งหมด trace ได้จากเอกสารหลัก

---

## P2 — Visibility

เป้าหมาย: ทำให้สถานะระบบมองเห็นได้ง่ายทั้งทีม

### Tasks
1. **Architecture dashboard (docs-first)**
   - สร้าง dashboard แบบ markdown ที่สรุปสถานะ layer/โมดูล
   - ไฟล์เป้าหมาย: `docs/dashboard/ARCHITECTURE_STATUS.md`
2. **Public documentation refresh**
   - ปรับ README และ quick-start ให้ชี้เส้นทางใช้งานจริง
   - อัปเดตสารบัญเอกสารกลาง
3. **Metrics layer baseline**
   - กำหนด metric ขั้นต่ำ: PR volume, lead time, risk distribution
   - บันทึก schema ที่ `docs/metrics/METRIC_DEFINITIONS.md`

### Done Criteria (P2)
- คนใหม่เข้ามาแล้วหาเอกสารหลักเจอภายใน 5 นาที
- มี dashboard กลางและ metric definition ใช้งานได้

---

## P3 — Intelligence Upgrade

เป้าหมาย: เพิ่มความฉลาดของระบบโดยไม่กระทบความเสถียร

### Tasks
1. **Trust memory (phase-1 design)**
   - ออกแบบโครงข้อมูล trust signals ต่อ contributor/module
   - เริ่มจาก read-only ก่อน (ยังไม่ใช้ตัดสินใจ auto-merge)
2. **Predictive routing (safe mode)**
   - ทดลอง rule-based routing พร้อม confidence score
   - ถ้า confidence ต่ำ ให้ fallback เป็น manual review
3. **Self-healing workflows (guarded)**
   - เพิ่มขั้นตอน recovery playbook สำหรับ failure pattern ที่พบบ่อย
   - log ทุกการ recover เพื่อ audit ย้อนหลัง

### Done Criteria (P3)
- มี design doc + guardrails + rollback plan ครบ
- ไม่มี automation ที่ข้าม human oversight ในงานเสี่ยง

---

## Delivery Model

- ใช้ลำดับ **P1 -> P2 -> P3** เท่านั้น
- แต่ละงานออกเป็น PR ย่อยที่ rollback ได้
- ทุก PR ต้องแนบ:
  - impact summary
  - risk + rollback
  - evidence files

## Suggested Milestones

- **M1 (P1 complete):** โครงสร้างนิ่ง + standards ครบ
- **M2 (P2 complete):** มองเห็นสถานะระบบชัดเจน
- **M3 (P3 baseline):** มี intelligence layer แบบ guarded พร้อม auditability

## Change Log

- 2026-05-11: เพิ่มแผนปฏิบัติ P1–P3 ลงรีโป (initial draft)


## Execution Status (2026-05-11)

- [x] P1.1 Unify naming conventions (`docs/standards/NAMING_CONVENTION.md`)
- [x] P1.2 Duplication tracker (`docs/review/DUPLICATION_TRACKER.md`)
- [x] P1.3 Repo structure standard (`docs/standards/REPO_STRUCTURE.md`)
- [x] P1.4 Config SSOT mapping (`docs/standards/CONFIG_SSOT.md`)
- [x] P2.1 Architecture dashboard (`docs/dashboard/ARCHITECTURE_STATUS.md`)
- [x] P2.2 Public docs refresh baseline (linked from roadmap + architecture)
- [x] P2.3 Metrics definition (`docs/metrics/METRIC_DEFINITIONS.md`)
- [x] P3.1 Trust memory phase-1 design (`docs/intelligence/TRUST_MEMORY_PHASE1.md`)
- [x] P3.2 Predictive routing safe-mode (`docs/intelligence/PREDICTIVE_ROUTING_SAFE_MODE.md`)
- [x] P3.3 Self-healing playbook (`docs/operations/SELF_HEALING_WORKFLOWS_PLAYBOOK.md`)
