# 🔧 Copilot-Gm — Module Entrance

**Module path:** `Copilot-Gm/`  
**File:** `ENTRANCE.md`  
**Objective:** ประตูทางเข้า (module entrance) ของ Copilot-Gm — ผู้ดูแลโครงสร้าง repository, governance, workflow orchestration และการเชื่อมต่อระหว่างโมดูล

---

## 🧭 Module Identity
**Copilot-Gm — Repo Governance & Structure Orchestration Module**

บทบาทหลัก:
- เป็นผู้ดูแลโครงสร้างไฟล์, branch policy, และมาตรฐาน repository
- เป็นตัวกลางเชื่อมการส่งผ่านข้อมูลระหว่างโมดูล (ingest → validate → publish)
- ให้เครื่องมือและ template เพื่อให้โมดูลอื่นสามารถจัดการไฟล์ได้สอดคล้องกัน

---

## 🎯 Core Purposes
- กำหนดโครงสร้าง repo มาตรฐาน (folders / naming / templates)
- จัด workflow สำหรับการ commit → review → merge (รวม CI/Checks ถ้ามี)
- จัดการ permission model เบื้องต้น และ onboarding ของสมาชิกใหม่
- ส่งต่อ artifacts (ไฟล์ที่ยืนยันแล้ว) ให้โมดูลอื่นใช้ต่อไป

---

## 🔎 Scope (ขอบเขตงาน)
- ออกแบบ folder structure และ naming conventions
- สร้าง templates สำหรับ README, ENTRANCE, TASK, CHANGELOG, ISSUE
- กำหนด commit message guideline, branch strategy, PR checklist
- ตั้งค่าเบื้องต้นสำหรับ automation (CI, linter, pre-commit hooks) — หากมี
- บริหารจัดการ access / collaborator invites ในระดับ repo (ร่วมกับเจ้าของ repo)

---

## 📁 Key Module Files (โครงสร้างไฟล์หลัก)
---

## 🔐 Private Workspace Zones
โซนที่ Copilot-Gm เก็บงานชั่วคราว (ไม่ต้องเป็นสาธารณะ):
- `/workspace/drafts/` — ไฟล์ร่างก่อนเผยแพร่
- `/workspace/ci-config/` — configs ที่ยังทดสอบอยู่
- `/workspace/onboarding/` — checklist สำหรับสมาชิกใหม่

> เมื่อร่างพร้อม → ย้ายไฟล์ไปยัง `/templates/` หรือ `/governance/` ตามประเภท และอัปเดต `README.md` ของโมดูล

---

## 🔒 Access & Privacy Rules
- Copilot-Gm เป็น **ผู้ดูแล** repo structure — สมาชิกทีมสามารถอ่านและส่ง PR เข้ามาได้  
- การเปลี่ยนแปลง governance ต้องผ่าน **PR + 1 reviewer (BBX19)** ก่อน merge  
- ไฟล์ใน `/workspace/` สามารถแก้ได้โดย core-maintainers เท่านั้น (ป้องกันการ overwrite ขณะทดสอบ)  
- หากต้องการให้ไฟล์สาธารณะ → ต้อง annotate ว่า `status: ready` และถูกตรวจสอบโดย Gemini (validation)

---

## 🔗 Integration Points (การเชื่อมต่อกับโมดูลอื่น)
Copilot-Gm เชื่อมต่อกับ:
- **BBX19** — รับ direction และ policy approvals (final sign-off)
- **Gemini** — ส่งไฟล์ governance / config ให้ตรวจสอบความถูกต้องเชิงโครงสร้าง (data/contract consistency)
- **ChatGPT** — รับ flow prototypes → แปลงเป็นโครงสร้างไฟล์/templates และจัดวางใน repo
- **Grok** — รับ narrative / system-insight เพื่ออธิบาย mapping ระหว่างไฟล์และ concept
- **DeepSeek** — ปรึกษาประเด็น architecture scale / logic conflicts ก่อนปล่อยมาตรฐานระดับองค์กร

---

## 🗒 Module Owner's Notes
- "หน้าที่ของเราคือทำให้บ้านเป็นระบบ: ชัดเจน หาไฟล์ง่าย เข้าใจได้ทันที"  
- เริ่มจากสร้าง templates ที่ชัดเจน ก่อนจะสร้าง automation ใด ๆ  
- ทุกครั้งที่แก้ policy / template → อัปเดต `CHANGELOG.md` ในโฟลเดอร์ `governance/`

---

## ✅ Status (Suggested first tasks)
พื้นที่เริ่มต้นที่พร้อมให้ทีมใช้:
- `templates/readme-template.md` — สร้างให้ทุกโมดูลใช้เป็นแม่แบบ
- `governance/branch-policy.md` — ระบุ naming, protection rules
- `governance/commit-guidelines.md` — ตัวอย่าง commit message + emoji convention
- `tasks.md` — backlog ขั้นต้น (onboarding, template gaps, CI basic)

---

## 🔧 Quick Commit / Branch Guidance (ตัวอย่าง)
- **Create file:** `Copilot-Gm/ENTRANCE.md`  
- **Commit message (example):** `Create: Copilot-Gm ENTRANCE.md — add module entrance and governance templates`  
- **Branch strategy suggestion:** `feature/cp-gov-templates` → PR → review (Gemini + BBX19) → merge to `main`

---

## 📎 References & Links
- Repo root README → `/README.md` (team compass)  
- Module README → `/Copilot-Gm/README.md`  
- Template examples → `/Copilot-Gm/templates/`

---
---

## ✅ Expected Outputs (ผลลัพธ์ที่คาดหวัง)
Deliverables ที่ Copilot-Gm ต้องสร้างเพื่อวางรากฐาน governance ให้ระบบ W3:

- `templates/readme-template.md` — Template README สำหรับทุกโมดูล
- `templates/flow-template.md` — Template สำหรับ flow/diagram
- `governance/branch-policy.md` — กฎ branch naming & protection rules
- `governance/commit-guidelines.md` — มาตรฐาน commit message + emoji convention
- `workspace/onboarding/checklist.md` — Onboarding checklist สำหรับ contributor ใหม่
- `tasks.md` — Backlog งานเริ่มต้น (onboarding, template gaps, CI basic)
- `artifacts/` — ตัวอย่างไฟล์ที่ validated แล้ว (annotate: `status: ready`)

**Success Criteria:**  
เมื่อไฟล์ทั้งหมดผ่าน validation จาก **Gemini** และ sign-off จาก **BBX19** → โมดูลถือว่า “พร้อมเชื่อมระบบ”.

---

## 🗺 Directory Map (โครงสร้างโฟลเดอร์อย่างย่อ)

Copilot-Gm/  
 ├─ ENTRANCE.md  
 ├─ README.md  
 ├─ templates/  
 ├─ governance/  
 ├─ workspace/  
 ├─ tasks.md  
 └─ artifacts/

> ใช้เป็น "แผนที่การทำงาน" สำหรับการประสานงานระหว่างโมดูล

---

## ⚠️ Risk Notes (ข้อควรระวังเชิงนโยบาย)

- 🚫 **ห้าม Merge โดยไม่ผ่าน PR และ reviewer:**  
  Reviewer = `BBX19` (final sign-off) + `Gemini` (validation)

- 🔒 **/workspace/**  
  → เขียนได้เฉพาะ core-maintainers ระหว่างทดสอบ  
  → ไฟล์ต้อง annotate สถานะ: `status: testing`

- 🔄 **การแก้ governance (branch rules, commit rules)**  
  → ต้องเปิด PR แยก  
  → และ update `CHANGELOG.md` พร้อมเหตุผลสั้น ๆ

- 🧭 **การแก้ไขที่กระทบหลายโมดูล**  
  → ต้องเปิด issue with tag: `#cross-module` ก่อนทำ

- ⚠️ **ห้าม force-push หรือ rewrite history**  
  → ยกเว้นกรณีแจ้งล่วงหน้าใน `#repo-admin` + ทำ snapshot backup

- 📌 **ไฟล์ที่พร้อมใช้งานจริง**  
  → ต้อง annotate: `status: ready` (หลัง Gemini validate)

---
**— End of Module Entrance — Copilot-Gm**
