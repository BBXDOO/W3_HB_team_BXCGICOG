# W3 Runtime

Runtime ทำหน้าที่ประมวลผลงานผ่านเอเจนท์ที่ลงทะเบียนไว้ใน W3

1. รับ task/event
2. route ไปยังโมดูลจาก `module-registry.json`
3. โหลด IDP ของโมดูลเพื่อดึง role + responsibilities
4. โหลดประสบการณ์เดิมจาก memory context (`search_memory`)
5. เรียก agent runtime module (`core/runtime/agents/*.py`)
6. บันทึกผลกลับ memory เพื่อใช้เสริมบริบทครั้งถัดไป

---

## Runtime Flow

Event → Router + IDP → Context Memory → Agent Module → Result + Memory Log

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
