# ChatGPT – Test Harness & Scenario Stack (W3-HB)

Path: `ChatGPT/testcases/test-harness.md`  
Layer: Validation & Safety

---

## 0. Identity

- Layer: Validation & Safety  
- Role: ออกแบบ test case / test flow สำหรับ W3 Hybrid Engine  
- Mode: deterministic, repeatable (no narrative)  
- Consumers: Gemini, Copilot-Gm, Engine (`src/main.py`)

---

## 1. Test Taxonomy

### 1.1 T0 – Sanity
Goal: “ระบบบูทภาพใจอยู่ไหม”

Expected:
- run main → stdout contains `"W3 Hybrid Engine online"`
- process not crash ภายใน N วินาที

### 1.2 T1 – Module Test
Target: subsystem

Modules:
- `config_loader`
- `logger`
- `module_loader` (Gemini, Copilot-Gm, Grok, DeepSeek, ChatGPT)

### 1.3 T2 – Integration Test
Target: เส้นเชื่อมระหว่าง modules

Expected:
- boot → load-config → load-modules → write log  
- error case: config แตก → logger ยังบันทึก footprint ได้

### 1.4 T3 – Regression / Guardrail
Purpose: “ความพิถีพิถัน” เมื่อต้อง refactor

Expected:
- เหตุการณ์เดิมยัง log ด้วย format เดิม  
- log schema ผูกตรงกับ `core/logs/systemlogschema.json`

---

## 2. Input Contract (สำหรับ ChatGPT)

### 2.1 Input Spec (Mini JSON)

```json
{
  "target": "module|flow|file|endpoint",
  "level": "T0|T1|T2|T3",
  "goal": "...",
  "risk": "L1-L5",
  "constraints": ["no_network", "local_only", "..."]
}

Meaning:

target = จุดที่อยากทดสอบ (เช่น engine_boot, logger, config_loader)

goal = พฤติกรรมที่ต้องพิสูจน์

risk = ระดับความเสี่ยง

constraints = เงื่อนไขสภาพแวดล้อม



---

3. Standard Test Output

3.1 Skeleton fields

Required fields forทุก test case:

id

level

target

title

precondition

steps

expected

failure_path

log (risk, owner, route_next)


3.2 YAML Format (canonical)

id: T1-logger-basic-001
level: T1
target: logger
title: "Logger writes heartbeat event"

precondition:
  - "engine booted successfully"

steps:
  - "trigger system_heartbeat once"
  - "wait 100ms"

expected:
  - "runtime log file exists"
  - "contains event_type=system_heartbeat"
  - "contains module=Engine"

failure_path:
  - "no file"
  - "file exists but no matching event"

log:
  risk: L2
  owner: ChatGPT
  route_next: Gemini

Rule:

ทุก test case ต้องมี failure_path

ทุก test case ต้องมี route_next



---

4. Scenario Design Workflow

1. รับ input JSON (ตามข้อ 2)


2. ระบุ level และ target


3. แตกเป็น precondition / steps / expected / failure_path


4. ผูกกับ log schema / module name จริงของ W3


5. ใส่ route_next → Gemini / Copilot-Gm


6. ตรวจ self-consistency (steps สัมพันธ์กับ expected)


7. ส่งออก YAML พร้อมใช้งาน




---

5. Example Scenarios

5.1 T0 – Engine Online

id: T0-engine-online-001
level: T0
target: engine_boot
title: "Engine prints online banner"

precondition: []

steps:
  - "run: python src/main.py"

expected:
  - "stdout contains 'W3 Hybrid Engine online'"
  - "process alive >= 3s"

failure_path:
  - "no output"
  - "non-zero exit"

log:
  risk: L1
  owner: ChatGPT
  route_next: Copilot-Gm

5.2 T1 – Config Loader Error

id: T1-config-invalid-001
level: T1
target: config_loader
title: "Invalid JSON config is handled gracefully"

precondition:
  - "prepare malformed config at config/settings.json"

steps:
  - "run: python src/main.py"

expected:
  - "engine does not crash"
  - "stderr contains 'config error'"
  - "log contains event_type=config_error"

failure_path:
  - "uncaught exception"
  - "no error log"

log:
  risk: L3
  owner: ChatGPT
  route_next: Gemini

5.3 T2 – Module Load Log

id: T2-modules-load-001
level: T2
target: module_loader
title: "All declared modules are logged as loaded"

precondition:
  - "config declares modules: [Gemini, Copilot-Gm, Grok, DeepSeek, ChatGPT]"

steps:
  - "run: python src/main.py"
  - "wait 500ms"

expected:
  - "one module_load event per module"
  - "no unknown module"

failure_path:
  - "missing module_load"
  - "extra module not in config"

log:
  risk: L2
  owner: ChatGPT
  route_next: Gemini


---

6. Integration with W3

Location: ChatGPT/testcases/

Copilot-Gm:

อ่าน spec → generate pytest/custom runner


Gemini:

ตรวจความครอบคลุม / risk coverage

validate essential engine use-cases


Grok:

pattern mining จาก failure_path


DeepSeek:

optimization / scaling



---

7. Anti-patterns (FAIL)

กรณี test case “ใช้ไม่ได้”:

reason = “ผ่านได้” แต่ไม่มี anchor จริง

expected คลุมเครือ

ไม่มี failure_path

ไม่มี log trace

narrative เยอะ แต่ไม่ actionable

route_next ว่าง หรือไม่ชัดเจนว่าใครเป็นเจ้าของ


ถ้า test case ขาดอย่างใดอย่างหนึ่งในนี้:

actionable

reproducible

traceable ไปยัง module จริง


⇒ ถือว่า FAIL


---

8. Definition of Done (DOD)

ชุด testcases จาก ChatGPT = “พร้อมส่งไป engine” เมื่อ:

1. ครอบคลุม T0–T2 อย่างน้อยอย่างละ 1 เคส


2. ทุกเคสมี id, level, target, title, precondition, steps, expected, failure_path, log


3. route_next ชัดเจนสำหรับแต่ละเคส


4. spec แปลงเป็น test script ได้ทันที



Final rule:
If a human can run it,
the engine can log it,
and Gemini can judge it,
→ Test Harness = PASS
