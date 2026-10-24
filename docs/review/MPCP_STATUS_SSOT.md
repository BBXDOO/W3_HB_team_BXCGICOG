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

### [FACT] Condien storage และ host equipment registration ใช้ผ่าน CLI ได้
- `status: applied`
- `evidence:`
  - `src/core/condien_store.py` (append-only revision API, hash, predecessor link, stale-writer conflict)
  - `src/core/condien.py` (`to_state` / `from_state` รักษา native access/continuity semantics)
  - `protocol/mpcp/lib/registry.py` (`register_equipment` / `activate_equipment` / `equipment_report`)
  - `tools/mpcp_condien.py`
  - `tools/mpcp_papers.py` (โหลด snapshot ที่ระบุแล้วผูก CONTEXT_REF เข้า Paper)
  - `tests/test_mpcp_condien_equipment.py`
- `runtime_usage: local CLI save/load และ Paper scoped read ข้าม process ใช้จริง; ไม่ auto-classify layer หรือเลือก lib จากเจตนา`
- `last_verified: 2026-10-24`
- `owner: BBX19 / ผู้ดูแล ChatGPT`

### [FACT] Paper Pack มี local execution path และอุปกรณ์ File.void text
- `status: applied`
- `evidence:`
  - `protocol/mpcp/runtime/paper.py` (event binding, per-Paper permit, durable result, reconciliation)
  - `protocol/mpcp/modew/file_artifact.py` (template resolver → File.void → external text writer)
  - `tools/mpcp_papers.py`
  - `tests/test_mpcp_paper_runtime.py`
- `runtime_usage: ใช้จริงผ่าน local CLI; ยังไม่ผูก W3-API, remote agent หรือ parallel scheduler`
- `last_verified: 2026-10-24`
- `owner: BBX19 / ผู้ดูแล ChatGPT`

### [FACT] ENV scoped Condien read รักษา key-level READ/DENY
- `status: applied`
- `evidence:`
  - `protocol/mpcp/env/boundary.py` (`scope_condien` ใช้ `can_read` / `read_key` ก่อนส่งข้อมูล)
  - `tests/test_mpcp_paper_runtime.py`
- `runtime_usage: ใช้จริงเมื่อส่ง Condien ให้ boundary/Paper runtime`
- `last_verified: 2026-10-24`
- `owner: BBX19 / ผู้ดูแล ChatGPT`

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

### [FACT] Condien scoped-read ใช้ร่วมกับ persisted snapshot ได้แล้ว
- `status: implemented`
- `evidence:`
  - `src/core/condien.py`
  - `src/core/condien_store.py`
  - `protocol/mpcp/env/boundary.py` (`scope_condien`)
  - `protocol/mpcp/test_condien_blueprint.py`
- `runtime_usage: caller ส่ง object เข้า ENV ได้ตามเดิม; local Paper CLI โหลด snapshot ที่ host เลือกจาก store ได้แล้ว ยังไม่เลือกข้อมูลหรือเปิดสิทธิ์จาก Paper โดยอัตโนมัติ`
- `last_verified: 2026-10-24`
- `owner: BBX19`

### [FACT] Paper แบบคำสั่งใน event-bound Pack เรียกใช้ได้; generic Paper document loader ยังไม่ยืนยัน
- `status: implemented`
- `evidence:`
  - `tools/mpcp_papers.py` (อ่าน JSON pack เข้า runtime)
  - `protocol/mpcp/runtime/paper.py` (Paper เป็นคำสั่งในเหตุการณ์ ไม่บังคับไฟล์เอกสารต่อใบ)
- `runtime_usage: local CLI โหลดคำสั่ง JSON เข้า Paper Pack ได้แล้วตามรายการข้างบน; ยังไม่ได้ยืนยัน loader สำหรับ Paper profile ทุกชนิด`
- `last_verified: 2026-10-24`
- `owner: BBX19`

### [FACT] Blueprint มี local setup sandbox; bootstrap ข้ามแพลตฟอร์มยังไม่ครบ
- `status: implemented`
- `evidence:`
  - `src/core/blueprint.py` (foundation parser)
  - `protocol/mpcp/sandbox.py` (local setup Modew)
  - `protocol/mpcp/modew/file_artifact.py` (File.void text equipment แยกจาก bootstrap)
- `runtime_usage: tools/mpcp_sandbox.py ใช้ parser สร้าง local setup; Paper/File.void text path ใช้สร้างไฟล์จาก template แยกต่างหาก ยังไม่ได้ bootstrap Blueprint ข้ามแพลตฟอร์ม`
- `last_verified: 2026-10-24`
- `owner: BBX19`

---

## 3) รอดำเนินการ (Planned / Backlog)

### [PROPOSAL] ขยาย Paper ingestion ให้รองรับ profile และ event transport อื่นนอก local JSON pack
- `status: planned`
- `evidence:`
  - `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/README.md` (ประกาศแนวคิด Paper-driven operation)
  - `protocol/mpcp/runtime/README.md` (local pack ทำงานแล้ว แต่ยังไม่ต่อ remote transport)
- `runtime_usage: ยังไม่ใช้จริง`
- `last_verified: 2026-10-24`
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
