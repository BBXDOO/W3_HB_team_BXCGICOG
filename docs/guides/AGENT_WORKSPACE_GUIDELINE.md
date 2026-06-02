# 📘 Agent Workspace Guideline — วิธีใช้พื้นที่ agent ให้มีชีวิตใน Workflow จริง

**สำหรับ:** ทุก agent และ contributor ของ W3 Hybrid System  
**หลักการ:** พื้นที่ของ agent ควร "เคลื่อนไหว" ตามงานจริง ไม่ใช่โครงสร้างที่ว่างเปล่า

---

## 🧭 ปรัชญาพื้นฐาน

อ้างอิงจาก `knowledge/philosophy/corevsstructure.md`:

> โครงสร้าง (Structure) = กรอบที่ยืดหยุ่นได้ตามกิจกรรม  
> แกนความหมาย (Core) = เจตนาที่มั่นคง

พื้นที่ของ agent คือ **Structure** — ดังนั้นมันต้องเปลี่ยนและเติบโตตาม workflow จริง  
ถ้าพื้นที่ว่างเปล่า = Structure ไม่ได้ทำงาน = ระบบขาด execution layer

---

## 🔒 Self Workspace Boundary

รายละเอียดมาตรฐานใหม่สำหรับการออกแบบโมดูลตัวเอง บันทึกบริบท จัดสรรงาน และวางแผนในพื้นที่ของเอเจนท์ อยู่ที่ [`docs/standards/AGENT_SELF_WORKSPACE_STANDARD.md`](../standards/AGENT_SELF_WORKSPACE_STANDARD.md).

หลักสำคัญ: เอเจนท์มีอิสระในพื้นที่ของตัวเอง แต่ไม่ใช้พื้นที่นั้นเป็น authority เหนือ registry, protocol, source code truth, ROT, Paper, Result, governance หรือพื้นที่ของระบบอื่น และถ้าไม่มี gate ให้ถือว่า `MUTATION_ALLOWED:false`.

## 📐 Minimum Standard สำหรับทุก Agent Workspace

สิ่งที่ต้องมีขั้นต่ำในพื้นที่ของทุก agent:

```
[agent-name]/
├── ENTRANCE.md          ← ✅ มีอยู่แล้วทุกโมดูล
└── notes/
    └── working-notes.md ← ⚠️ ต้องสร้างและ maintain
```

**working-notes.md ควรมี:**
- entry แรก: "เริ่มงานวันที่...กำลังทำอะไร"
- entry ต่อๆ ไป: สิ่งที่ทำ, สิ่งที่พบ, การตัดสินใจ, สิ่งที่ค้างอยู่

---

## 🔄 กระบวนการที่ควรเกิดใน Workflow จริง

### ทุก Session (Session-level habit)

```
Start of session:
  1. อ่าน Cast/context/session_summary.md → restore context
  2. อ่าน notes/ ของตัวเอง → รู้ว่าค้างอะไรอยู่

During session:
  3. บันทึก decision/observation สำคัญ → notes/working-notes.md

End of session:
  4. append entry → Cast/context/session_summary.md
  5. update ไฟล์ที่เปลี่ยน status (draft → testing → ready)
```

### เมื่อผลิต Output ใหม่

```
ChatGPT สร้าง flow/prototype
  → ส่งให้ Gemini validate (via requests/)
  → บันทึก decision ใน ChatGPT/notes/design-decisions.md

Grok สร้าง insight
  → ถ้า requires-validation: yes → ส่ง Gemini
  → บันทึก ใน Grok/notes/methodology-notes.md

DeepSeek พบ architecture pattern
  → บันทึก ใน DeepSeek/notes/observation-log.md
  → ถ้ากระทบหลายโมดูล → เปิด tag #cross-module

Gemini validate แล้ว
  → annotate status: ready ในไฟล์นั้น
  → บันทึก ใน Gemini/notes/qa-issues.md

Copilot-Gm update structure
  → บันทึก ใน governance/CHANGELOG.md
  → update templates/ ถ้ามีการเปลี่ยน format
```

---

## 📁 แผนที่พื้นที่ของแต่ละ Agent

| Agent | พื้นที่ที่ควร Active | Output หลัก |
|---|---|---|
| ChatGPT | `flow-lab/`, `prototypes/`, `notes/design-decisions.md` | flow, prototype, test-case |
| Grok | `insight-vault/`, `notes/methodology-notes.md` | insight, narrative |
| Gemini | `analysis-lab/`, `notes/qa-issues.md`, `risk-scan/` | validation report, QA log |
| DeepSeek | `notes/observation-log.md`, `meta-structure/`, `pattern-lab/` | baseline, architecture insight |
| Copilot-Gm | `governance/`, `templates/`, `workspace/onboarding/checklist.md` | template, governance doc |
| BBX19 | `directives/`, `status/`, `modules/BBX19/idp/` | direction, IDP, approval |
| Cast | `context/session_summary.md` | session log (ทุก agent เขียนที่นี่) |

---

## 🚦 Status Convention (ระบบสัญลักษณ์มาตรฐาน)

ทุกไฟล์ที่ผลิตควรมี status annotation:

| Status | ความหมาย | เก็บที่ไหน |
|---|---|---|
| `draft` | กำลังคิด/เขียน ยังไม่พร้อม | notes/ หรือ flow-lab/ |
| `testing` | กำลัง simulate/ทดสอบ | ไฟล์เดิม |
| `review` | รอ validation จาก Gemini | ส่งผ่าน requests/ |
| `ready` | ผ่าน validation แล้ว ใช้งานได้ | ย้ายออกจาก notes/ |
| `archived` | ใช้แล้ว เก็บไว้อ้างอิง | ย้ายไป archive/ |

**ตัวอย่างการใช้:**
```markdown
<!-- status: draft -->
<!-- status: ready — validated by Gemini 2026-05-08 -->
```

---

## 🤝 Cross-Agent Knowledge Flow (สิ่งที่ควรเกิด)

```
BBX19 → (direction) → ทุก agent
ChatGPT → (flow/prototype) → Gemini → (validated) → Copilot-Gm
Grok → (insight) → Gemini → (validated narrative) → BBX19
DeepSeek → (architecture baseline) → ทุก agent (reference)
Cast → (session memory) → ทุก agent (context restore)
```

Knowledge ไม่ควรอยู่แค่ใน ENTRANCE.md แต่ต้องไหลผ่าน notes/ และ requests/ จริงๆ

---

## ⚠️ Anti-Patterns (สิ่งที่ไม่ควรทำ)

- ❌ สร้าง notes ที่เป็น placeholder "Experiment 1: Description" — ถ้าไม่มีเนื้อหาจริง อย่าสร้าง
- ❌ ENTRANCE.md ที่ไม่เคยถูก execute — ถ้าสัญญาว่าจะสร้าง output แต่ไม่ทำ ระบบจะ drift
- ❌ ไฟล์ที่ไม่มี status — ทำให้ไม่รู้ว่าพร้อมใช้หรือยัง
- ❌ insight โดยไม่มี evidence — ตามหลักของ Grok: "ห้ามสร้าง narrative ที่ไม่มี evidence"
- ❌ Merge โดยไม่ผ่าน validation route ที่กำหนด

---

## 📌 การจัดเก็บ

- **โฟลเดอร์:** `docs/guides/AGENT_WORKSPACE_GUIDELINE.md`
- **ประเภท:** Operational Guide / Best Practices
- **กลุ่ม:** W3 Governance & Agent Operations
- **สร้างโดย:** Copilot-Gm
- **อ้างอิง:** AGENT_WORKSPACE_AUDIT.md, corevsstructure.md, Cast/context/protocol.md
