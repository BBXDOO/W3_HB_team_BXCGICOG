# 📦 คู่มือการใช้งานโมดูล W3
## Module Usage Guide — W3 Hybrid Runtime

> **สำหรับผู้ใช้ที่มี API key ของ GPT (OpenAI) และ Gemini พร้อมแล้ว**

---

## สารบัญ / Table of Contents

1. [ภาพรวม — โมดูลที่มีใน Registry](#1-ภาพรวม--โมดูลที่มีใน-registry)
2. [สถานะโมดูล — ใช้งานได้จริง vs. Stub](#2-สถานะโมดูล--ใช้งานได้จริง-vs-stub)
3. [วิธีใช้งานแบบ Manual (Request/Output Folders)](#3-วิธีใช้งานแบบ-manual-requestoutput-folders)
4. [วิธีใช้งาน Runtime Stub (engine.py / engine_v2.py)](#4-วิธีใช้งาน-runtime-stub-enginepy--engine_v2py)
5. [เครื่องมือ/สคริปต์ที่ใช้งานได้จริงใน repo](#5-เครื่องมือสคริปต์ที่ใช้งานได้จริงใน-repo)
6. [Quick Start — เริ่มใช้งานใน 5 นาที](#6-quick-start--เริ่มใช้งานใน-5-นาที)
7. [ตัวอย่าง Input/Output ที่คาดหวัง](#7-ตัวอย่าง-inputoutput-ที่คาดหวัง)
8. [เช็กลิสต์: สิ่งที่ต้องเพิ่มเพื่อใช้งาน Production](#8-เช็กลิสต์-สิ่งที่ต้องเพิ่มเพื่อใช้งาน-production)
9. [ข้อจำกัดปัจจุบัน](#9-ข้อจำกัดปัจจุบัน)

---

## 1. ภาพรวม — โมดูลที่มีใน Registry

ระบบ W3 มีโมดูลทั้งหมด **8 ตัว** ที่ลงทะเบียนใน `src/modules/registry/registry.json`:

| ID | ชื่อโมดูล | ประเภท | Tier | สิทธิ์ | บทบาทหลัก |
|----|-----------|--------|------|--------|-----------|
| `bbx19` | **BBX19** | human-root | ROOT | final | Root Authority / Final Decision |
| `chatgpt` | **ChatGPT** | ai-builder | L1 | advisory | Architecture & Flow Design |
| `gemini` | **Gemini** | ai-reviewer | L2 | advisory | Meta-Verification & Logic Check |
| `grok` | **Grok** | ai-pattern | L2 | advisory | Pattern Intelligence & Narrative |
| `deepseek` | **DeepSeek** | ai-scale | L1 | advisory | Logic & Scalability |
| `copilot-gm` | **Copilot-Gm** | governance-engine | L2 | review-gate | Governance & Compliance |
| `cast` | **Cast** | reasoning-core | L1 | analysis | Document Architecture & Context |
| `bbex-core` | **BBEX-Core** | legacy-core | ROOT-AUX | symbolic | Philosophical Anchor & Identity |

**Task Routing Table** (จาก `core/module-loader/module-registry.json`):

| คำสั่ง (task keyword) | โมดูลที่รับผิดชอบ |
|----------------------|------------------|
| `design`, `architecture`, `flow`, `simulation` | ChatGPT |
| `verify`, `verification`, `audit`, `security` | Gemini |
| `pattern`, `signals`, `insight` | Grok |
| `research`, `scale`, `planning` | DeepSeek |
| `governance`, `policy`, `compliance` | Copilot-Gm |
| `reason`, `critical_reasoning`, `interpret`, `document` | Cast |
| `identity`, `philosophy` | BBEX-Core |
| `vision` | BBX19 |

---

## 2. สถานะโมดูล — ใช้งานได้จริง vs. Stub

| โมดูล | Registry ✓ | module.json ✓ | Runtime Dispatch ✓ | AI API เชื่อมจริง | พร้อม Production |
|-------|:----------:|:-------------:|:-----------------:|:----------------:|:---------------:|
| BBX19 | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |
| ChatGPT | ✅ | ✅ | ✅ | ❌ stub | 🟡 เพิ่ม API call |
| Gemini | ✅ | ✅ | ✅ | ❌ stub | 🟡 เพิ่ม API call |
| Grok | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |
| DeepSeek | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |
| Copilot-Gm | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |
| Cast | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |
| BBEX-Core | ✅ | ✅ | ✅ | ❌ stub | 🔴 ยังไม่พร้อม |

> **สรุป:** ทุกโมดูล dispatch ได้ผ่าน `engine_v2.py` แต่ยังเป็น stub (คืนข้อความจำลอง)  
> โมดูลที่ต่อ API จริงได้ง่ายที่สุดคือ **ChatGPT** และ **Gemini** เพราะมี SDK พร้อม

---

## 3. วิธีใช้งานแบบ Manual (Request/Output Folders)

### โปรโตคอล L0 (Manual Invocation Protocol)

นี่คือวิธีที่ **ใช้งานได้จริงตอนนี้** โดยไม่ต้องรัน Python:

```
1. กำหนด intent ของงาน
2. สร้างไฟล์ request_XXX.md ใน /requests/ ของโมดูลเป้าหมาย
3. โมดูลผลิต output ไปที่ reports/ หรือ knowledge/
4. ถ้า risky → ส่งต่อไปยัง Gemini
5. Review → merge / revise / reject
```

### เส้นทาง Input/Output ของแต่ละโมดูล

| โมดูล | Input Paths | Output Paths |
|-------|-------------|-------------|
| **ChatGPT** | `modules/ChatGPT/requests/`<br>`knowledge/`<br>`docs/`, `core/`<br>`blueprints/`, `repo_events/` | `modules/ChatGPT/flows/`<br>`modules/ChatGPT/scenarios/`<br>`modules/ChatGPT/reports/`<br>`modules/ChatGPT/logs/daily/` |
| **Gemini** | `requests/intent`<br>`docs/MPCP_architecture`<br>`knowledge/universal_truth` | `reports/logic_analysis`<br>`logs/interaction_history`<br>`results/structural_blueprints` |
| **Grok** | `requests/`<br>`docs/`, `knowledge/`<br>`decision_trace/`, `tuf_snapshots/` | `narrative_reports/`<br>`system_observations/`<br>`connection_maps/`, `full_moon_analysis/` |
| **DeepSeek** | `requests/`<br>`docs/`, `knowledge/`, `tools/` | `reports/`, `logs/`<br>`results/`, `outcomes/` |
| **Copilot-Gm** | `requests/`<br>`docs/`, `knowledge/` | `reports/`, `logs/`, `results/` |
| **Cast** | `requests/`<br>`docs/`, `knowledge/` | `reports/`, `artifacts/`, `context/` |
| **BBEX-Core** | `knowledge/`, `logs/`<br>`core/governance/`<br>`BBEX-Core/private/` | `BBEX-Core/public/`<br>`outcomes/append_only_ledger/`<br>`knowledge/philosophy/` |

### ตัวอย่าง: สร้าง Request สำหรับ ChatGPT

```bash
# สร้างโฟลเดอร์ถ้ายังไม่มี
mkdir -p modules/ChatGPT/requests

# สร้างไฟล์ request
cat > modules/ChatGPT/requests/request_001.md << 'EOF'
# Request: System Architecture Review
Date: 2026-05-06
Requested by: BBX19

## Intent
ออกแบบ flow การรับ-ส่งข้อมูลระหว่างโมดูลใน W3

## Context
- ระบบมี 8 โมดูลที่ dispatch ได้
- ต้องการ diagram แสดงความสัมพันธ์

## Expected Output
- Flow diagram (Markdown/ASCII)
- Module interaction table
EOF
```

---

## 4. วิธีใช้งาน Runtime Stub (engine.py / engine_v2.py)

### 4.1 engine.py — Simulation Mode

ไฟล์: `core/runtime/engine.py`  
**สถานะ:** Placeholder executor (ไม่ต่อ AI จริง)

```python
# ตัวอย่างการเรียกใช้
from core.runtime.engine import run, heartbeat

# รัน task เดียว
result = run("design")
# output: {"status": "SUCCESS", "plan": {...}, "context": {...}, "output": {...}}

# ตรวจสอบสถานะ
health = heartbeat()
# output: {"engine": "ONLINE", "recent_memory": 5}
```

**ข้อจำกัด:**
- ฟังก์ชัน `simulate_agent()` คืนข้อความ placeholder เท่านั้น
- ไม่ได้เรียก OpenAI/Gemini SDK จริง

### 4.2 engine_v2.py — Dispatch Table Mode

ไฟล์: `core/runtime/engine_v2.py`  
**สถานะ:** มี dispatch table ครบ แต่ฟังก์ชัน run_* ยังเป็น stub

```python
from core.runtime.engine_v2 import run, run_many, heartbeat

# รัน task เดียว
result = run("design")
# output: {"status": "SUCCESS", "task": "design", "module": "ChatGPT",
#          "output": "ChatGPT completed: design", "latency_ms": 12}

# รัน tasks หลายอันพร้อมกัน (parallel, MAX_WORKERS=3)
results = run_many(["verify", "audit", "security"])

# ตรวจสอบสถานะ
health = heartbeat()
# output: {"engine": "ONLINE", "workers": 3, "recent_memory": 0}
```

**dispatch table ปัจจุบัน:**

```python
table = {
    "ChatGPT":    run_chatgpt,   # -> "ChatGPT completed: {task}"
    "Gemini":     run_gemini,    # -> "Gemini verified: {task}"
    "Copilot-Gm": run_copilot,   # -> "Copilot audited: {task}"
    "DeepSeek":   run_deepseek,  # -> "DeepSeek structured: {task}"
    "Grok":       run_grok,      # -> "Grok scanned: {task}"
    "Cast":       run_cast,      # -> "Cast interpreted: {task}"
    "BBEX-Core":  run_bbex,      # -> "BBEX-Core reflected: {task}"
    "BBX19":      run_bbx19,     # -> "BBX19 directed: {task}"
}
```

### 4.3 วิธีใส่ API จริงใน run_chatgpt และ run_gemini

เมื่อคุณมี API key พร้อมแล้ว ให้แก้ไขฟังก์ชันใน `core/runtime/engine_v2.py`:

#### สำหรับ ChatGPT (OpenAI):

```python
# ติดตั้ง: pip install openai
import openai

def run_chatgpt(task, context):
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are W3 ChatGPT module, an architecture expert."},
            {"role": "user", "content": f"Task: {task}\nContext: {context}"}
        ]
    )
    return response.choices[0].message.content
```

#### สำหรับ Gemini (Google):

```python
# ติดตั้ง: pip install google-generativeai
import google.generativeai as genai

def run_gemini(task, context):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"You are W3 Gemini module, a verification expert.\nTask: {task}\nContext: {context}"
    )
    return response.text
```

---

## 5. เครื่องมือ/สคริปต์ที่ใช้งานได้จริงใน repo

### 5.1 `tools/validate_modules.py` — ตรวจสอบความถูกต้องของ module.json

```bash
python tools/validate_modules.py
```

ตรวจสอบ:
- ฟิลด์บังคับครบหรือไม่ (`name`, `display_name`, `version`, `owner`, `input`, `output`, `scope`)
- รูปแบบ semver ของ `version`
- ประเภท `input`/`output` เป็น array

**ตัวอย่าง output:**
```
Running module validation...
================================================================================
MODULE VALIDATION REPORT
================================================================================

✅ VALID MODULES (8):
----------------------------------------
  • BBX19/modules/BBX19/module.json
  • Cast/module.json
  • ChatGPT/modules/ChatGPT/module.json
  ...

================================================================================
SUMMARY:
----------------------------------------
Valid Modules:    8
Invalid Modules:  0
================================================================================
```

### 5.2 `tools/run_audit.py` — รัน Audit Agents ทั้งหมด

```bash
python tools/run_audit.py
```

รันตามลำดับ:
1. **DTML** — Security Scanner (CRITICAL)
2. **REDR** — Structure Reader (HIGH)
3. **PSP2** — PR Flow Router (MEDIUM)
4. **LRC2** — System Recorder (ALWAYS-ON)
5. **BBEX CORE** — Philosophical Anchor (PASSIVE)

### 5.3 `tools/w3run.py` — CLI สำหรับเรียก engine_v2 โดยตรง

> ดู [Quick Start](#6-quick-start--เริ่มใช้งานใน-5-นาที) สำหรับวิธีใช้

```bash
# รัน task เดียว (simulation mode)
python tools/w3run.py design

# รัน tasks หลายอัน
python tools/w3run.py design verify audit

# ดู heartbeat ของ engine
python tools/w3run.py --heartbeat

# ดูรายการ task ที่รองรับ
python tools/w3run.py --list-tasks
```

### 5.4 `iget/main.py` — iGet PR Review Tool

```bash
# ต้องตั้งค่า environment variables ก่อน
export REPO="BBXDOO/W3_HB_team_BXCGICOG"
export PR="123"
export GITHUB_TOKEN="ghp_your_token"

python -m iget.main
```

> **หมายเหตุ:** ต้องติดตั้ง `requests` ก่อน (`pip install requests`) — ปัจจุบันยังไม่ได้ประกาศใน `requirements.txt`

---

## 6. Quick Start — เริ่มใช้งานใน 5 นาที

### ขั้นตอนที่ 1: ติดตั้ง dependencies

```bash
pip install -r requirements.txt
# ถ้าต้องการใช้ iget ด้วย
pip install requests
# ถ้าต้องการต่อ OpenAI API
pip install openai
# ถ้าต้องการต่อ Gemini API
pip install google-generativeai
```

### ขั้นตอนที่ 2: ตั้งค่า Environment Variables

```bash
# สำหรับ OpenAI/ChatGPT (ถ้าต้องการต่อ API จริง)
export OPENAI_API_KEY="sk-..."

# สำหรับ Gemini (ถ้าต้องการต่อ API จริง)
export GEMINI_API_KEY="AIza..."

# สำหรับ iGet PR review (optional)
export GITHUB_TOKEN="ghp_..."
export REPO="BBXDOO/W3_HB_team_BXCGICOG"
export PR="<PR number>"
```

### ขั้นตอนที่ 3: ทดสอบ Runtime (Simulation Mode)

```bash
# ทดสอบ engine_v2 ด้วย CLI tool
python tools/w3run.py design

# ทดสอบ validate_modules
python tools/validate_modules.py

# ทดสอบ engine โดยตรง
python -c "
import sys; sys.path.insert(0, '.')
from core.runtime.engine_v2 import run, heartbeat
import json
print(json.dumps(run('design'), indent=2, ensure_ascii=False))
print(json.dumps(heartbeat(), indent=2, ensure_ascii=False))
"
```

### ขั้นตอนที่ 4: สร้าง Request แบบ Manual

```bash
mkdir -p modules/ChatGPT/requests
echo "# Request: สร้าง flow diagram สำหรับระบบ\n\nDate: $(date +%Y-%m-%d)\nRequested by: BBX19\n\n## Intent\nอธิบาย..." > modules/ChatGPT/requests/request_001.md
```

---

## 7. ตัวอย่าง Input/Output ที่คาดหวัง

### 7.1 engine_v2.run("design") — Simulation Mode (ปัจจุบัน)

**Input:**
```python
run("design")
```

**Output (stub):**
```json
{
  "status": "SUCCESS",
  "task": "design",
  "module": "ChatGPT",
  "output": "ChatGPT completed: design",
  "latency_ms": 5,
  "time": "2026-05-06T10:00:00Z"
}
```

### 7.2 engine_v2.run("design") — เมื่อต่อ OpenAI API จริง

**Input:**
```python
# หลังจากเพิ่ม API call ใน run_chatgpt()
os.environ["OPENAI_API_KEY"] = "sk-..."
run("design")
```

**Output (ตัวอย่างที่คาดหวัง):**
```json
{
  "status": "SUCCESS",
  "task": "design",
  "module": "ChatGPT",
  "output": "ระบบ W3 ควรมีโครงสร้าง modular ดังนี้:\n1. Core Layer: engine_v2.py รับ task...",
  "latency_ms": 1250,
  "time": "2026-05-06T10:00:01Z"
}
```

### 7.3 engine_v2.run_many() — รัน Tasks คู่ขนาน

**Input:**
```python
run_many(["verify", "audit", "security"])
```

**Output (stub):**
```json
[
  {"status": "SUCCESS", "task": "verify", "module": "Gemini", "output": "Gemini verified: verify"},
  {"status": "SUCCESS", "task": "audit", "module": "Gemini", "output": "Gemini verified: audit"},
  {"status": "SUCCESS", "task": "security", "module": "Gemini", "output": "Gemini verified: security"}
]
```

### 7.4 tools/w3run.py -- ผ่าน CLI

```bash
$ python tools/w3run.py design
{
  "status": "SUCCESS",
  "task": "design",
  "module": "ChatGPT",
  "output": "ChatGPT completed: design",
  "latency_ms": 3,
  "time": "2026-05-06T10:00:00Z"
}
```

---

## 8. เช็กลิสต์: สิ่งที่ต้องเพิ่มเพื่อใช้งาน Production

### 🔴 Critical — ต้องทำก่อนใช้ API จริง

- [ ] **[ChatGPT]** แก้ `run_chatgpt()` ใน `core/runtime/engine_v2.py` ให้เรียก `openai.chat.completions.create()`
- [ ] **[Gemini]** แก้ `run_gemini()` ให้เรียก `google.generativeai.GenerativeModel().generate_content()`
- [ ] เพิ่ม `openai` และ `google-generativeai` ใน `requirements.txt`
- [ ] กำหนด `OPENAI_API_KEY` และ `GEMINI_API_KEY` ใน environment หรือ `.env` file

### 🟡 Medium — ควรทำเพื่อความเสถียร

- [ ] เพิ่ม error handling / retry logic ใน dispatch functions
- [ ] เพิ่ม system prompt ที่เหมาะสมสำหรับแต่ละโมดูล (อ้างอิง `module.json` แต่ละตัว)
- [ ] เพิ่ม `requests` ใน `requirements.txt` (ใช้โดย `iget/fetcher.py`)
- [ ] สร้าง `.env.example` สำหรับ environment variables

### 🟢 Low — ปรับปรุงระยะยาว

- [ ] สร้าง system prompt จาก `module.json` แต่ละตัวโดยอัตโนมัติ
- [ ] เพิ่ม streaming response สำหรับ ChatGPT และ Gemini
- [ ] เชื่อม memory bus กับ context จริง (ปัจจุบัน `core/memory/memory_bus.py` ยังเป็น stub)
- [ ] เพิ่ม rate limiting และ cost tracking

---

## 9. ข้อจำกัดปัจจุบัน

| จุด | สถานะ | หมายเหตุ |
|-----|--------|----------|
| AI dispatch | 🔴 stub | `run_chatgpt()` ฯลฯ คืนข้อความจำลอง ไม่ได้เรียก API จริง |
| Memory bus | 🔴 stub | `core/memory/memory_bus.py` ยังไม่มี persistent storage จริง |
| Authentication | 🔴 ไม่มี | ไม่มีระบบ auth สำหรับ API calls |
| `iget` dependency | 🟡 ขาด | `requests` ใช้งานได้แต่ไม่ได้ประกาศใน `requirements.txt` |
| Registry sync | 🟡 ไม่มี | `modules/registry.json` และ `src/modules/registry/registry.json` ไม่มี sync mechanism |
| CI/CD integration | 🟡 ไม่มี | `core/runtime/` ยังไม่มี entry point ที่ถูกเรียกโดย workflow |
| Schema validation | 🟢 ไม่มี | `src/modules/standards/module.schema.json` ยังไม่ได้สร้าง |

---

> **อัพเดทล่าสุด:** 2026-05-06  
> **Authority:** BBX19  
> **สร้างโดย:** GitHub Copilot (W3 documentation agent)
