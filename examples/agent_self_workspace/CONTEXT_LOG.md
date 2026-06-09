# CONTEXT_LOG.md — Agent Context Template

Session: `<yyyy-mm-dd>/<short-id>`
G-State: `<BUILD|AUDIT|RESEARCH|RECOVERY|MAINTENANCE|LEARNING|none>`

Known context:
- สิ่งที่รู้จากไฟล์หรือ request ปัจจุบัน

Unknown / limitation:
- สิ่งที่ยังไม่รู้
- สิ่งที่ต้องตรวจ path/source ก่อน

Dependencies:
- ไฟล์ ระบบ หรือเอเจนท์ที่เกี่ยวข้องเฉพาะหน้าที่

Observation:
- สิ่งที่พบแบบไม่ mutate truth

Decision:
- การตัดสินใจระดับ workspace หรือ proposal

Next safe action:
- งานถัดไปที่ยังอยู่ใน boundary

MUTATION_ALLOWED:false
