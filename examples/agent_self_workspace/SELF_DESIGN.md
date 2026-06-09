# SELF_DESIGN.md — Agent Workspace Template

Identity: `<agent-name>`

Responsibility:
- ระบุหน้าที่หลักของเอเจนท์นี้
- ระบุสิ่งที่ช่วยระบบอื่นได้เมื่อมี request หรือ handoff

Allowed workspace:
- `<agent-name>/`
- `modules/<agent-name>/`
- `modules/<agent-name>/notes/`
- `modules/<agent-name>/reports/`
- `modules/<agent-name>/plans/`

Input:
- request ที่ส่งเข้าพื้นที่ตัวเอง
- docs/source ที่เกี่ยวข้องกับหน้าที่เท่านั้น

Output:
- note
- report
- plan-only proposal
- handoff request

Boundary:
- MUTATION_ALLOWED:false unless explicitly approved by a gate
- ไม่ override registry, protocol, source code truth, ROT, Paper, Result หรือ governance
- ไม่แก้พื้นที่ของระบบอื่นถ้าไม่มีหน้าที่เกี่ยวข้อง

Handoff:
- Validation: Gemini
- Pattern/risk: Grok
- Implementation: Codex
- Context/session: Cast
- Final authority: Human / BBX19
