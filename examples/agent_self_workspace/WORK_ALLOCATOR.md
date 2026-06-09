# WORK_ALLOCATOR.md — Agent Work Allocation Template

| Work item | Owner/role | Status | Dependency | Handoff target | Proof needed |
|---|---|---|---|---|---|
| `<task>` | `<agent-name>` | draft | `<files/systems>` | `<agent/system>` | `<test/report>` |

Status values:
- draft
- review
- ready
- blocked
- archived

Rules:
- จัดสรรเฉพาะงานในพื้นที่ของเอเจนท์นี้
- ถ้างานแตะระบบอื่น ให้ระบุ handoff target
- ถ้าไม่มี gate ให้ถือว่า `MUTATION_ALLOWED:false`
