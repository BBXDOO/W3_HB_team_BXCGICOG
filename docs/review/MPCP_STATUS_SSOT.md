# MPCP Status — Single Source of Truth (SSOT)

ไฟล์นี้คือแหล่งอ้างอิงเดียวสำหรับสถานะ MPCP เพื่อให้ AI ตอบแบบอิงหลักฐานและไม่คาดเดา

---

## กติกาการตอบของ AI (ต้องใช้ไฟล์นี้ก่อนตอบ)

1. ใช้ข้อมูลจากไฟล์นี้เป็นหลักก่อนตอบคำถามสถานะ MPCP
2. ถ้าไม่มี evidence ที่ยืนยันได้ ให้ตอบว่า: `ยังไม่พบหลักฐาน`
3. ห้ามเติมรายละเอียดที่ไม่อยู่ในรายการสถานะด้านล่าง
4. อัปเดตไฟล์นี้ทุกครั้งที่มี merge/change สำคัญ และทบทวนอย่างน้อยรายสัปดาห์

---

## โครงสร้างมาตรฐานต่อรายการ

- `status: applied | implemented | planned | concept`
- `evidence: <absolute path(s)>`
- `runtime_usage: ใช้จริง | ยังไม่ใช้จริง`
- `last_verified: YYYY-MM-DD`
- `owner: <ผู้รับผิดชอบ>`

---

## 1) เสร็จแล้ว (Implemented + Applied)

### [FACT] MPCP runtime รองรับ canonical result envelope และ packet input
- `status: applied`
- `evidence:`
  - `protocol/mpcp/kernel/contract.py` (`build_result_envelope`, strict validation)
  - `protocol/mpcp/runtime/executor.py` (`run_packet`)
  - `protocol/mpcp/modew/base_modew.py`
- `runtime_usage: ใช้จริง`
- `last_verified: 2026-08-18`
- `owner: BBX19`

### [FACT] A–F ถูกแยกจาก runtime operation order ตาม MPCP Origin
- `status: applied`
- `evidence:`
  - `protocol/mpcp/lib/pillar.py`
  - `protocol/mpcp/modew/base_modew.py`
  - `protocol/mpcp/mpcp_pillar.md`
- `runtime_usage: ใช้จริง; runtime trace ใช้ชื่อ operation แทน A–F`
- `last_verified: 2026-08-18`
- `owner: BBX19`

### [FACT] ROT ถูกบังคับใช้ใน runtime executor จริง
- `status: applied`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py` (เรียก `MPCPRot.validate_core` และ `MPCPRot.validate_fail_condition`)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/kernel/rot.py` (นิยามกฎ `validate_core` และ `validate_fail_condition`)
- `runtime_usage: ใช้จริง`
- `last_verified: 2026-05-09`
- `owner: BBX19`

---

## 2) เสร็จแต่ยังไม่ถูกใช้จริง (Implemented, Not Applied)

### [FACT] Cross-L / ENV / MPCP runtime boundary พร้อมเรียกใช้ แต่ยังไม่ผูกเข้า W3-API
- `status: implemented`
- `evidence:`
  - `protocol/mpcp/env/boundary.py`
  - `protocol/mpcp/env/gateway.py`
  - `protocol/mpcp/env/models.py`
  - `protocol/mpcp/env/probe.py`
  - `protocol/mpcp/config/default.json`
  - `protocol/mpcp/lib/registry.py`
- `runtime_usage: ยังไม่ใช้จริงใน W3-API; public API พร้อมใช้งานและไม่ execute หากไม่มี ExecutionAgreement`
- `last_verified: 2026-08-18`
- `owner: BBX19`

### [FACT] Condien มี implementation และ MPCP ENV ใช้ scoped-read ได้แล้ว
- `status: implemented`
- `evidence:`
  - `src/core/condien.py`
  - `protocol/mpcp/env/boundary.py` (`scope_condien`)
  - `protocol/mpcp/test_condien_blueprint.py`
- `runtime_usage: ใช้ได้เมื่อ caller ส่ง Condien object เข้า ENV boundary; ยังไม่ auto-load จาก Paper file`
- `last_verified: 2026-08-18`
- `owner: BBX19`

### [FACT] Paper documentation มีอยู่ แต่ runtime ยังไม่พบ document-loader ที่ผูกไฟล์ Paper เข้าการรันโดยตรง
- `status: implemented`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/README.md` (ระบุบทบาท Paper/Rot/Modew/Condien)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/mpcp_concept_paper/mpcp_concept_paper.md` (มีเอกสารแนว Paper/Concept)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py` (มี parser ข้อความอินพุต `TASK:...` แต่ไม่พบการ load ไฟล์ Paper)
- `runtime_usage: ยังไม่ใช้จริง`
- `last_verified: 2026-05-09`
- `owner: BBX19`

### [FACT] Blueprint documentation มีอยู่ แต่ยังไม่พบการเชื่อมเข้า MPCP runtime โดยตรง
- `status: implemented`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/mpcp_blueprint_paper/mpcp_blueprint_paper.md` (นิยาม Blueprint ชัดเจน)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/blueprints/abstract/overview.md` (มีโครงสร้าง blueprint ระดับรีโป)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py` (ไม่พบการ load blueprint เข้ารันไทม์โดยตรง)
- `runtime_usage: ยังไม่ใช้จริง`
- `last_verified: 2026-05-09`
- `owner: BBX19`

---

## 3) รอดำเนินการ (Planned / Backlog)

### [PROPOSAL] เพิ่มตัวเชื่อม Paper file → runtime execution
- `status: planned`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/README.md` (ประกาศแนวคิด Paper-driven operation)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py` (ปัจจุบันรับ text input โดยตรง)
- `runtime_usage: ยังไม่ใช้จริง`
- `last_verified: 2026-05-09`
- `owner: BBX19`

### [PROPOSAL] เพิ่มตัวเชื่อม Blueprint file → runtime/bootstrap flow
- `status: planned`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/mpcp_blueprint_paper/mpcp_blueprint_paper.md` (มี blueprint spec)
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py` (ยังไม่มี blueprint bootstrap path)
- `runtime_usage: ยังไม่ใช้จริง`
- `last_verified: 2026-05-09`
- `owner: BBX19`

---

## 4) แนวคิดสำคัญ (Concept Only)

ยังไม่มีรายการ Concept-only ที่ตรวจยืนยันใหม่ในรอบ 2026-08-18
