# W3 Runtime

Runtime ทำหน้าที่ประมวลผลงานผ่านเอเจนท์ที่ลงทะเบียนไว้ใน W3

1. รับ task/event
2. route ไปยังโมดูลจาก `modules/registry.json`
3. โหลด module manifest จาก `modules/<name>/module.json`
4. โหลดประสบการณ์เดิมจาก memory context (`search_memory`)
5. เรียก agent runtime module (`core/runtime/agents/*.py`)
6. runtime consumer ที่ต้องใช้ IDP metadata อ่านจาก `core/identity/profiles/`
7. บันทึกผลกลับ memory เพื่อใช้เสริมบริบทครั้งถัดไป

---

## Runtime Flow

Event → Modules Registry → Module Manifest → Runtime Agent → Optional IDP Consumer → Memory / Result

---

## Identity Boundary

- Module routing และ module manifest เป็น ownership ของ `modules/`
- W3-IDP runtime profiles เป็น identity/context data แยกจาก module loader
- `core/identity/` เป็น runtime-compatible projection สำหรับ consumer ที่ต้องอ่าน IDP
- IDP cards ต้นทางสำหรับ session/context restore อยู่ภายใต้ `BBX19/modules/BBX19/idp/`
- historical/evidence paths ไม่ควรถูก rewrite เพียงเพราะ runtime path เปลี่ยน

---

## Registered Runtime Agents

- BBX19 (`bbx19.py`)
- BBEX-Core (`bbex_core.py`)
- ChatGPT (`chatgpt.py`)
- Gemini (`gemini.py`)
- Grok (`grok.py`)
- DeepSeek (`deepseek.py`)
- Copilot-Gm (`copilot_gm.py`)
- Cast (`cast.py`)
