---

# ChatGPT — Test Harness & Scenario Stack (W3-HB)

📍 Path: `ChatGPT/testcases/test-harness.md`

---

## 0. Identity

- Layer: Validation & Safety
- Role: ออกแบบ test case / test flow สำหรับ W3 Hybrid Engine
- Mode: deterministic, repeatable, no narrative
- Consumer: Gemini, Copilot-Gm, Engine (src/main.py)

---

## 1. Test Taxonomy (ชนิดของเทส)

### 1.1 T0 — Sanity
> เช็คว่า “ระบบยังหายใจอยู่ไหม”

ตัวอย่าง:
- run main → expect `W3 Hybrid Engine online`
- check heartbeat loop ไม่ crash ภายใน N วินาที

### 1.2 T1 — Module Test
> ตรวจทีละ subsystem

ตัวอย่าง:
- config loader
- logger
- module loader (Gemini, Copilot-Gm, Grok, DeepSeek, ChatGPT)

### 1.3 T2 — Integration Test
> ตรวจ “เส้นเชื่อม” ระหว่าง module

ตัวอย่าง:
- boot → load-config → load-modules → write log
- error case: config แตก → logger ยังบันทึก footprint ได้

### 1.4 T3 — Regression / Guardrail
> ใช้กัน “ความพังซ้ำ” เมื่อมีการ refactor

ตัวอย่าง:
- เทส error footprint format ยังเหมือนเดิม
- เทส log schema ยังตรงกับ `core/logs/systemlogschema.json`

---

## 2. Input Contract สำหรับ ChatGPT

รูปแบบ input ที่ให้ ChatGPT ออกแบบ test:

```json
{
  "target": "module|flow|file|endpoint",
  "level": "T0|T1|T2|T3",
  "goal": "...",
  "risk": "L1-L5",
  "constraints": ["no network", "local only", "..."]
}

กติกา:

target = จุดที่อยากเทส (เช่น engine_boot, logger, config_loader)

goal = พฤติกรรมที่ต้องพิสูจน์

risk = ช่วย Gemini เลือกความเข้มของการตรวจ

constraints = เงื่อนไขสภาพแวดล้อม



---

3. Standard Test Output (สิ่งที่ ChatGPT ต้องสร้าง)

รูปแบบ output หนึ่ง test case:

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

ข้อบังคับ:

ทุกเทส ต้อง มี failure_path

ทุกเทส ต้อง ระบุ route_next (ใครตรวจต่อ)



---

4. Scenario Design Workflow

1. รับ input spec


2. ระบุ level + target ชัดเจน


3. แตกเป็น precondition / steps / expected / failure_path


4. ผูกกับ log schema / module name จริงใน W3


5. ใส่ route_next (ส่วนใหญ่ → Gemini / Copilot-Gm)


6. ตรวจ self-consistency (steps สัมพันธ์กับ expected)


7. ส่งออกเป็น YAML/JSON พร้อมใช้งาน




---

5. Example Scenarios

5.1 T0 — Engine Online

id: T0-engine-online-001
level: T0
target: engine_boot
title: "Engine prints online banner"
steps:
  - "run: python src/main.py"
expected:
  - "stdout contains 'W3 Hybrid Engine online'"
  - "process remains alive at least 3s"
failure_path:
  - "no output"
  - "process exits with non-zero code"
log:
  risk: L1
  route_next: Copilot-Gm


---

5.2 T1 — Config Loader Error Handling

id: T1-config-invalid-001
level: T1
target: config_loader
title: "Invalid JSON config is handled gracefully"
precondition:
  - "prepare malformed config file at config/settings.json"
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
  route_next: Gemini


---

5.3 T2 — Module Load Log

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
  - "log has one module_load event per module"
  - "no unknown module appears"
failure_path:
  - "missing module_load for any declared module"
  - "extra module not in config"
log:
  risk: L2
  route_next: Gemini


---

6. Integration with W3

Test spec ถูกเก็บใน ChatGPT/testcases/

Copilot-Gm:

อ่าน test spec → สร้าง test script จริง (pytest / custom runner)


Gemini:

ตรวจความครบถ้วน / risk coverage

เช็คว่า test ครอบ use-case สำคัญของ engine


Grok:

จำ pattern ของ bug ที่เคยเจอจาก failure_path


DeepSeek:

ใช้ test spec วางแผน scaling / optimization




---

7. Anti-patterns (ถือว่า FAIL)

เทสที่ “ผ่านได้” โดยไม่ทำอะไร

expected กว้างแบบตีความได้หลายแบบ

ไม่มี failure_path

ไม่มีการผูกกับ log หรือ behavior จริงในระบบ

narrative ยาว ไม่ actionable


> ถ้า test case ไม่:

actionable

reproducible

traceable ไปยัง module จริง
= FAIL

8. Definition of Done (DOD)

ชุด testcases จาก ChatGPT ถือว่า “พร้อมส่งให้เอเจนท์” เมื่อ:

ครอบคลุม T0–T2 อย่างน้อยอย่างละ 1

ทุก case มี id, level, target, steps, expected, failure_path

มี route_next ชัดเจนสำหรับแต่ละ case

สามารถแปลงเป็น test script ได้โดยไม่ต้องเดาเพิ่ม


If human can run it,
and engine can log it,
and Gemini can judge it,
→ Test Harness = PASS



---
