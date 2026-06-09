# PLAN.md — Agent Plan Template

Goal:
- เป้าหมายของงานนี้

Scope:
- สิ่งที่จะทำในพื้นที่ตัวเอง

Non-goal:
- สิ่งที่จะไม่ทำ
- ระบบที่จะไม่ mutate

Steps:
1. ตรวจ context และไฟล์ที่เกี่ยวข้อง
2. ทำ draft/proposal ใน workspace ตัวเอง
3. ระบุ dependency และ risk
4. ส่ง handoff ให้ระบบที่เกี่ยวข้องถ้าจำเป็น
5. ระบุ proof/test ก่อนใช้งานจริง

Boundary:
- plan-only until approved
- MUTATION_ALLOWED:false unless explicitly approved

Related systems:
- `<system>`: `<reason it is related>`

Proof / test:
- `<command or review artifact>`

Handoff:
- To: `<agent/system/human>`
- Reason: `<why>`
