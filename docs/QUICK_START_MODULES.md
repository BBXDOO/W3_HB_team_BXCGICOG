# 🚀 Quick Start: ใช้งานโมดูล W3 + เชื่อม GPT/Gemini API

> **คู่มือนี้ตอบ 3 คำถาม:**  
> 1. ใช้งานโมดูลแบบ Manual ได้เลย (ไม่ต้องมี API)  
> 2. เชื่อม GPT หรือ Gemini API ให้โมดูลรันอัตโนมัติ  
> 3. ผลลัพธ์จะออกไปที่ไหน

---

## 📋 ความเข้าใจพื้นฐาน

ระบบ W3 มีโมดูล 8 ตัวที่ตั้งชื่อตามเอเจนท์ AI ที่ช่วยสร้างโปรเจกต์นี้:

| โมดูล | บทบาท | Backend เริ่มต้น |
|-------|------|----------------|
| **BBX19** | Root Authority / Human Decision | GPT |
| **ChatGPT** | Architecture & Flow Builder | GPT |
| **Gemini** | Meta Verification & Logic Review | Gemini |
| **Grok** | Pattern Intelligence & Narrative | Gemini |
| **DeepSeek** | Logic Audit & Scalability | Gemini |
| **Copilot-Gm** | Governance & Structure Hub | GPT |
| **Cast** | Document Architect & Interpreter | GPT |
| **BBEX-Core** | Legacy Identity & Philosophy | Gemini |

> 📌 **สำคัญ:** โมดูลเหล่านี้เป็น **ตัวแทนเชิงสัญลักษณ์** (symbolic agents) ไม่ใช่ integration โดยตรงกับ API ภายนอก  
> ดูรายละเอียดเต็มที่: [`docs/reports/AGENT_MODULE_CAPABILITY_REPORT.md`](./reports/AGENT_MODULE_CAPABILITY_REPORT.md)

---

## ⚡ วิธีที่ 1: Manual Workflow (ทำได้เลย ไม่ต้องมี API)

### ขั้นตอน

```
1. เลือกโมดูลเป้าหมาย (เช่น ChatGPT)
2. สร้างไฟล์ request ใน requests/ ของโมดูล
3. ส่งคำขอให้ AI ภายนอก (เช่น ChatGPT.com หรือ Gemini.google.com)
4. วาง output ลงในโฟลเดอร์ตามสเปคของโมดูล
5. Commit เข้า repo
```

### ตัวอย่าง

```bash
# 1. สร้าง request
cat > ChatGPT/modules/ChatGPT/requests/task_$(date +%Y%m%d).md << 'EOF'
# Request: Design W3 API Spec
Date: $(date +%Y-%m-%d)
Module: ChatGPT
Task: ออกแบบ REST API spec สำหรับ W3 module registry
EOF

# 2. ถาม ChatGPT.com หรือ Gemini.google.com แล้ว copy output
# 3. บันทึกผลลัพธ์
cat > ChatGPT/modules/ChatGPT/reports/2026-05-06_api_design.md << 'EOF'
# W3 API Design
[วางผลลัพธ์จาก AI ที่นี่]
EOF

# 4. Commit
git add .
git commit -m "feat(ChatGPT): add API design report"
```

---

## 🤖 วิธีที่ 2: Automated — เชื่อม GPT/Gemini API

### ขั้นตอนที่ 1: ติดตั้ง Dependencies

```bash
pip install openai google-generativeai
```

หรือ เพิ่มใน `requirements.txt`:
```
jsonschema>=4.10.3
openai>=1.0.0
google-generativeai>=0.8.0
```

### ขั้นตอนที่ 2: ตั้งค่า Environment Variables

**สำหรับ GPT:**
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

**สำหรับ Gemini:**
```bash
# Linux/Mac
export GEMINI_API_KEY="AIza..."

# Windows PowerShell
$env:GEMINI_API_KEY = "AIza..."
```

> ⚠️ **อย่า commit API key ลงใน repo** — ใช้ `.env` file หรือ GitHub Secrets เท่านั้น

**ใช้ .env file (แนะนำ):**
```bash
# สร้าง .env ที่ root ของ repo
echo "OPENAI_API_KEY=sk-..." >> .env
echo "GEMINI_API_KEY=AIza..." >> .env

# โหลด .env
export $(cat .env | xargs)
```

ตรวจสอบว่า `.env` อยู่ใน `.gitignore` แล้ว:
```bash
grep ".env" .gitignore  # ต้องพบ .env
```

### ขั้นตอนที่ 3: รัน LLM Adapter

```bash
# รัน ChatGPT module ด้วย GPT API
python -m core.adapters.llm_adapter \
  --module ChatGPT \
  --task "ออกแบบ REST API spec สำหรับ W3 module registry"

# รัน Gemini module ด้วย Gemini API
python -m core.adapters.llm_adapter \
  --module Gemini \
  --task "ตรวจสอบความสมเหตุสมผลของ W3 module registry v2"

# กำหนด backend เอง
python -m core.adapters.llm_adapter \
  --module Grok \
  --task "วิเคราะห์ pattern ใน commit history ของ W3" \
  --backend gpt

# ใช้ system prompt
python -m core.adapters.llm_adapter \
  --module Cast \
  --task "สรุปโครงสร้าง W3 เป็นภาษาไทย" \
  --system-prompt "คุณเป็น technical writer ที่เชี่ยวชาญระบบ W3 Hybrid"

# ใช้ model เฉพาะ
python -m core.adapters.llm_adapter \
  --module ChatGPT \
  --task "design architecture" \
  --model gpt-4o
```

### ตัวอย่าง Output

```
{
  "status": "SUCCESS",
  "module": "ChatGPT",
  "backend": "gpt",
  "task": "ออกแบบ REST API spec สำหรับ W3 module registry",
  "output_file": "ChatGPT/modules/ChatGPT/reports/2026-05-06_design_REST_API.md",
  "content_preview": "# W3 Module Registry API\n\n## Overview\nThe W3 Module Registry...",
  "latency_ms": 1842,
  "time": "2026-05-06T13-00-00Z"
}

✅ Output written to: ChatGPT/modules/ChatGPT/reports/2026-05-06_design_REST_API.md
```

### ขั้นตอนที่ 4: ใช้งานใน Python Script

```python
from core.adapters.llm_adapter import run_module

# รัน ChatGPT module
result = run_module(
    module_name="ChatGPT",
    task="ออกแบบ REST API spec สำหรับ W3 module registry",
    system_prompt="คุณเป็น architect ของ W3 Hybrid System"
)

print(result["output_file"])    # path ที่บันทึกไฟล์
print(result["content_preview"])  # preview ของเนื้อหา

# รัน Gemini module
result2 = run_module(
    module_name="Gemini",
    task="ตรวจสอบความสมเหตุสมผลของ API design นี้: ...",
)
print(result2["status"])
```

---

## 🔄 Flow การทำงาน (รวม Runtime Engine)

```
User/BBX19
    │
    ▼
engine_v2.run("design")
    │
    ├── router.execution_plan("design")  ← อ่าน module-registry.json
    │       └── returns: { run_with: "ChatGPT", ... }
    │
    ├── build_context("design")  ← search memory_bus
    │
    ├── dispatch("ChatGPT", task, context)
    │       └── run_chatgpt(task, context)  ← ปัจจุบัน: stub
    │                                       ← อนาคต: เรียก llm_adapter
    │
    └── add_memory(...)  ← บันทึกผลลง memory_store.json


llm_adapter.run_module("ChatGPT", task)
    │
    ├── เลือก backend (gpt/gemini)
    ├── เรียก API จริง (OpenAI / Gemini)
    ├── รับผลลัพธ์
    └── เขียนไฟล์ → ChatGPT/modules/ChatGPT/reports/YYYY-MM-DD_task.md
```

---

## 📁 ตำแหน่ง Output ของแต่ละโมดูล

| โมดูล | ผลลัพธ์จะออกที่ |
|-------|--------------|
| BBX19 | `BBX19/status/` |
| ChatGPT | `ChatGPT/modules/ChatGPT/reports/` |
| Gemini | `Gemini/modules/Gemini/reports/` |
| Grok | `Grok/modules/Grok/reports/` |
| DeepSeek | `DeepSeek/modules/DeepSeek/reports/` |
| Copilot-Gm | `Copilot-Gm/reports/` |
| Cast | `Cast/reports/` |
| BBEX-Core | `BBEX-Core/public/reports/` |

---

## 🧪 ทดสอบว่าระบบพร้อมหรือยัง

```bash
# ทดสอบ memory bus (ไม่ต้องมี API key)
python core/memory/memory_bus.py

# ทดสอบ engine stub (ไม่ต้องมี API key)
python core/runtime/engine_v2.py

# ตรวจสอบว่า API key ตั้งค่าถูกต้อง
python -c "import os; print('GPT key set:', bool(os.environ.get('OPENAI_API_KEY'))); print('Gemini key set:', bool(os.environ.get('GEMINI_API_KEY')))"
```

---

## ❓ คำถามที่พบบ่อย

**Q: โมดูล "เรียนรู้" จากประวัติการทำงานไหม?**  
A: ในระดับ memory_bus — ใช่ ผลการทำงานทุกครั้งถูกบันทึกและค้นหาได้  
แต่ "adaptive learning" อัตโนมัติยังไม่มี — เป็นสเปคสำหรับอนาคต

**Q: การ "สื่อสารระหว่างโมดูล" ทำงานยังไง?**  
A: ปัจจุบัน — ผ่าน memory_bus (โมดูลหนึ่งบันทึก อีกตัวค้นหาอ่าน)  
อนาคต — multi-module pipeline (v0.3+)

**Q: ต้องใช้ API key ทั้งสองไหม?**  
A: ไม่จำเป็น ถ้ามีแค่ GPT key ก็รัน GPT modules ได้  
ถ้ามีแค่ Gemini key ก็รัน Gemini modules ได้  
ถ้าไม่มี key ก็ยังรันแบบ stub simulation ได้ผ่าน engine_v2

**Q: ไฟล์ผลลัพธ์อยู่ที่ไหน?**  
A: ดูตาราง "ตำแหน่ง Output" ด้านบน — แต่ละโมดูลมี `reports/` folder ของตัวเอง

---

## 📚 อ่านเพิ่มเติม

- [รายงานความสามารถโมดูลเต็ม](./reports/AGENT_MODULE_CAPABILITY_REPORT.md)
- [Architecture Map](./architecture/REDR_Structure_Map.md)  
- [Module Registry (v2)](../src/modules/registry/registry.json)

---

*อัปเดต: 2026-05-06 | W3 HB_team_BXCGICOG*
