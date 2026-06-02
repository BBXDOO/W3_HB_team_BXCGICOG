# Agent Self Workspace Standard — W3-native agent workspace pact

เอกสารนี้กำหนดข้อตกลงเชิงปฏิบัติแบบ W3-native สำหรับเอเจนท์หรือแชทบอทที่มีพื้นที่ตามชื่อของตัวเองใน repository W3_HB_team_BXCGICOG เช่น `ChatGPT/`, `Gemini/`, `Grok/`, `DeepSeek/`, `Copilot-Gm/`, `Cast/`, `BBX19/` และพื้นที่ภายใต้ `modules/<agent-name>/`.

คำว่า standard ในเอกสารนี้หมายถึง **ข้อตกลงภายในสภาพแวดล้อม W3** ไม่ใช่มาตรฐานตลาด/องค์กรทั่วไป และไม่ใช้ลดทอนความสามารถเฉพาะตัวของแต่ละระบบ. พื้นที่เอเจนท์ยังเป็นพื้นที่เสรีสำหรับร่วมรับรู้ กระจายงาน สร้างสรรค์งาน ทดลองคิด และจัดงานของตัวเองตาม DNA/role ของระบบนั้น.

เอกสารนี้เป็น **workspace pact** เท่านั้น ไม่ใช่ runtime engine, workflow executor, state machine, governance authority หรือสิทธิ์ mutate source truth.

## 1) จุดประสงค์

ให้แต่ละเอเจนท์สามารถทำงานในพื้นที่ของตัวเองได้อย่างเสรีแต่มี boundary ตามสภาพแวดล้อม W3 โดยรองรับ 4 งานหลัก:

1. ออกแบบโมดูลตัวเอง (`self-design`)
2. บันทึกบริบทตัวเอง (`context log`)
3. จัดสรรงานในพื้นที่ตัวเอง (`work allocation`)
4. วางแผนและส่งต่อ (`planning / handoff`)

ทุกอย่างต้องเป็นเอกสาร อ่านได้ ตรวจสอบได้ และไม่เปลี่ยน truth layer โดยตรง

## 2) ขอบเขตสิทธิ์พื้นฐาน

เอเจนท์มีอิสระสูงภายในพื้นที่ของตัวเอง เพราะแต่ละระบบมีความสามารถต่างกันและมีวิธีสร้างงานไม่เหมือนกัน อิสระนี้ครอบคลุมการออกแบบโมดูล บันทึกบริบท ทดลองแนวคิด ทำ request/report/plan และจัดลำดับงานใน folder ของตัวเอง

ข้อจำกัดหลักมีเพียง: งานนั้นต้องไม่ขัดกับ registry, protocol, source code truth, governance boundary หรือหน้าที่ของระบบอื่น และถ้าจะเกี่ยวกับระบบอื่นต้องมีเหตุผลเชิงหน้าที่ชัดเจน

ตัวอย่างพื้นที่ของตัวเอง:

```text
<agent-name>/
modules/<agent-name>/
modules/<agent-name>/requests/
modules/<agent-name>/reports/
modules/<agent-name>/logs/
modules/<agent-name>/plans/
modules/<agent-name>/notes/
```

ถ้าโฟลเดอร์ย่อยบางรายการยังไม่มี ให้ถือเป็น template ที่สร้างได้เฉพาะเมื่อจำเป็นต่อหน้าที่ของเอเจนท์นั้น ไม่ต้องสร้าง placeholder เปล่าโดยไม่มีงานจริง

## 3) สิ่งที่ทำได้

เอเจนท์อาจทำสิ่งต่อไปนี้ในพื้นที่ของตัวเอง:

- เขียน self-design ว่าตัวเองรับผิดชอบอะไร โดยไม่ต้องเลียนแบบระบบอื่น
- บันทึก context ของ session, ข้อจำกัด, สิ่งที่รู้, สิ่งที่ยังไม่รู้
- แยกงานเป็น queue / task / backlog เฉพาะพื้นที่ตัวเอง
- วางแผนงานแบบ plan-only ก่อนส่งต่อให้ระบบที่เกี่ยวข้อง
- ทำ report, note, request, proposal หรือ handoff ที่ตรวจสอบได้
- อ้างอิงระบบอื่นเฉพาะเท่าที่เกี่ยวกับหน้าที่ของงาน
- สร้างสรรค์งานตามความถนัดของระบบ เช่น analysis, validation, language mapping, architecture hint, context memory, implementation support

## 4) สิ่งที่ห้ามทำ

เสรีภาพในพื้นที่ตัวเองไม่ใช่สิทธิ์ครอบระบบอื่น เอเจนท์ต้องไม่ใช้พื้นที่ตัวเองเพื่อ:

- mutate registry / protocol / source code truth โดยไม่มี gate
- override ROT, Paper, Result, Condien, governance หรือ human review
- แก้งานของระบบอื่นโดยไม่มีหน้าที่เกี่ยวข้อง
- สร้าง runtime executor ใหม่จาก template เหล่านี้
- ใช้ context log เป็นหลักฐานแทน proof/test/source truth
- เขียน W3DB, EP_SIGNAL, W3Lgu, MPCP หรือ runtime state โดยตรง เว้นแต่ระบบนั้นมีหน้าที่และ gate ชัดเจน

## 5) โครงไฟล์ขั้นต่ำที่แนะนำ

```text
modules/<agent-name>/
├── SELF_DESIGN.md      # บอกบทบาท ขอบเขต input/output และข้อห้าม
├── CONTEXT_LOG.md      # บันทึกบริบท ข้อจำกัด สิ่งที่ค้าง และแหล่งอ้างอิง
├── WORK_ALLOCATOR.md   # แยกงานในพื้นที่ตัวเอง: queue / owner / status / dependency
└── PLAN.md             # แผนแบบ plan-only พร้อม handoff และ test/proof ที่ต้องใช้
```

ถ้าเอเจนท์มี root workspace แยก เช่น `ChatGPT/` หรือ `Gemini/` สามารถวางไฟล์ชุดเดียวกันใน root นั้น หรือใน `notes/`, `tasks/`, `reports/` ตามโครงเดิมได้ แต่ต้องไม่ข้ามไปแก้พื้นที่ของระบบอื่นโดยไม่มีเหตุผลและหน้าที่เกี่ยวข้อง

## 6) ความหมายของแต่ละไฟล์

### SELF_DESIGN.md

ใช้บอกว่าเอเจนท์นี้คือใคร ทำอะไรได้ รับ input จากไหน ส่ง output ไปไหน และต้องหยุดตรงไหน

หัวข้อที่ควรมี:

- Identity
- Responsibility
- Allowed workspace
- Input
- Output
- Boundary
- Handoff

### CONTEXT_LOG.md

ใช้บันทึกบริบทของตัวเองแบบตรวจสอบได้ ไม่ใช่ memory ลอย ๆ

หัวข้อที่ควรมี:

- Date / session
- Current condition / G-State ถ้ามี
- Known context
- Unknown / limitation
- Dependency
- Decision / observation
- Next safe action

### WORK_ALLOCATOR.md

ใช้จัดงานในพื้นที่ตัวเอง ไม่ใช่ project manager กลางของทั้ง repo

หัวข้อที่ควรมี:

- Work item
- Owner / role
- Status: `draft`, `review`, `ready`, `blocked`, `archived`
- Dependency
- Handoff target
- Proof needed

### PLAN.md

ใช้วางแผนแบบ plan-only ก่อนทำงานจริงหรือก่อนส่งต่อ

หัวข้อที่ควรมี:

- Goal
- Scope
- Non-goal
- Steps
- Boundary
- Related systems
- Proof / test
- Handoff

## 7) Responsibility Routing

เมื่อมีงานแตะหลายระบบ ให้ส่งต่อเฉพาะระบบที่เกี่ยวข้องกับหน้าที่นั้น

| งาน | ผู้เกี่ยวข้องหลัก | หมายเหตุ |
|---|---|---|
| flow / prototype / scenario | ChatGPT | วาง flow หรือ blueprint ในพื้นที่ของตัวเองก่อน |
| validation / cross-check / W3Lgu alignment | Gemini | ตรวจความถูกต้อง ความเสี่ยง compatibility และช่วยมองความสอดคล้องกับ W3Lgu เมื่อได้รับงานที่เกี่ยวข้อง |
| pattern / signal / risk insight | Grok | เสนอ insight หรือ risk report แบบ observe-first |
| structure / architecture pattern | DeepSeek | เสนอ architecture hint หรือ pattern โดยไม่ rewrite truth |
| governance / template / repo hygiene | Copilot-Gm | จัด governance doc/template เฉพาะเมื่อมีหน้าที่เกี่ยวข้อง |
| context/session continuity | Cast | เก็บ context และ session summary |
| implementation patch/test/PR / technical stabilization | Codex | สาย dev ที่ซัพพอร์ตงานเทคนิคโดยตรง ปรับปรุงโครงสร้างให้เสถียรแบบ branch-safe ภายใต้สภาพแวดล้อม W3 และ review/gate |
| direction / final authority | BBX19 / Human | ตัดสินใจขั้นสุดท้ายและอนุมัติ boundary สำคัญ |

ตัวอย่าง: ถ้างานเกี่ยวกับ W3Lgu และต้องการ validation/ภาษาระบบ สามารถส่งให้ Gemini ตรวจ alignment ได้ แต่ Gemini ไม่ได้กลายเป็น owner ของ W3Lgu truth โดยอัตโนมัติ. ถ้างานต้องแก้โค้ด ทดสอบ หรือทำ PR ให้ส่ง Codex เป็น dev support แต่ Codex ต้องทำตาม W3 boundary ไม่ใช่มาตรฐานตลาดภายนอก.

## 8) Handoff ที่ปลอดภัย

การส่งต่องานควรมีข้อมูลขั้นต่ำ:

```text
REQUEST:
FROM:
TO:
REASON:
RELATED_FILES:
BOUNDARY:
EXPECTED_OUTPUT:
PROOF_NEEDED:
MUTATION_ALLOWED:false
```

ถ้า `MUTATION_ALLOWED` ไม่ได้ระบุโดย human/governance gate ให้ถือว่าเป็น `false`

## 9) ความสัมพันธ์กับระบบเดิม

- `registry / protocol / source code` = truth
- `config` = orientation map
- `docs` = explanation / public boundary / branch strategy
- `G-State` = shared awareness layer, not authority
- `Agent folders` = free creative/working space within W3 boundary
- `Hospitication` = observer / evaluator / proposal-first care
- `W3-API` = gateway-only
- `Cross-X` = plan-only
- `W3DB append` = append-plan หรือ append-only ตามจุดที่อนุมัติ
- `EP_SIGNAL / RYTM` = preview / signal trace

มาตรฐานนี้ไม่เปลี่ยนความหมายของระบบเหล่านี้

## 10) Acceptance Checklist

ผ่านเมื่อ:

- ไฟล์อยู่ในพื้นที่ของเอเจนท์หรือใน template/example ที่ระบุไว้
- ระบุ responsibility และ boundary ชัดเจน แต่ไม่บังคับให้ทุกเอเจนท์มีรูปแบบความคิดเหมือนกัน
- มี `MUTATION_ALLOWED:false` หรือ boundary เทียบเท่าเมื่อเป็น plan/proposal
- ไม่อ้างสิทธิ์เหนือ registry, protocol, source truth หรือ governance
- มี handoff target เมื่อแตะระบบอื่น
- มี proof/test ที่ควรใช้ก่อนนำไปใช้งานจริง

ไม่ผ่านเมื่อ:

- เอเจนท์ใช้พื้นที่ตัวเองเป็น authority เหนือระบบอื่น
- context log กลายเป็น truth แทน source/protocol/registry
- plan-only กลายเป็น execution โดยไม่มี gate
- มีการ rewrite งานของระบบอื่นโดยไม่มีหน้าที่เกี่ยวข้อง
