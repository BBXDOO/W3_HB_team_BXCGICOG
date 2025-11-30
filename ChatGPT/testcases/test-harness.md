# ChatGPT — Test Harness & Scenario Stack (W3-HB)

> Path: `ChatGPT/testcases/test-harness.md`  
> Layer: Validation & Safety

---

## 0. Identity

- **Layer:** Validation & Safety
- **Role:** ออกแบบ test case / test flow สำหรับ W3 Hybrid Engine  
- **Mode:** deterministic, repeatable, no narrative
- **Consumers:** Gemini, Copilot-Gm, Engine (`src/main.py`), Grok, DeepSeek

---

## 1. Test Taxonomy (ชนิดของเทส)

### 1.1 T0 — Sanity

เช็คว่า “ระบบยังหายใจอยู่ไหม”

ตัวอย่าง:

- run main → expect banner `W3 Hybrid Engine: ONLINE`
- process ไม่ crash ภายใน ≥ 3s

### 1.2 T1 — Module Test

ตรวจทีละ subsystem

ตัวอย่าง:

- `config loader`
- `logger`
- `module loader` (Gemini, Copilot-Gm, Grok, DeepSeek, ChatGPT)

### 1.3 T2 — Integration Test

ตรวจ “เส้นเชื่อม” ระหว่าง module

ตัวอย่าง:

- boot → load-config → load-modules → write log
- error case: config แหก แต่ logger ยังบันทึก footprint ได้

### 1.4 T3 — Regression / Guardrail

ใช้กัน “ความพังซ้ำ” เมื่อมีการ refactor

ตัวอย่าง:

- เทส error footprint format ยังเหมือนเดิม
- เทส log schema ยังตรงกับ `core/logs/systemlogschema.json`

---

## 2. Input Contract สำหรับ ChatGPT

รูปแบบ input ที่ให้ ChatGPT ออกแบบ test

```json
{
  "target": "module|flow|file|endpoint",
  "level": "T0|T1|T2|T3",
  "goal": "...",
  "risk": "L1-L5",
  "constraints": ["no network", "local only", "..."]
}
```

**Glossary:**

- `target` = จุดที่อยากทดสอบ (เช่น engine_boot, logger, config_loader)
- `goal` = พฤติกรรมที่ต้องพิสูจน์
- `risk` = ช่วย Gemini เลือกความเข้มข้นการตรวจ
- `constraints` = เงื่อนไขสภาพแวดล้อม

---

## 3. Standard Test Output (สิ่งที่ ChatGPT ต้องสร้าง)

รูปแบบ output หนึ่ง test case (human-readable + machine-mappable):

```yaml
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
```

**ข้อบังคับ:**

- ทุกเคส ต้องมี `failure_path`
- ทุกเคส ต้องระบุ `route_next` (ใครตรวจต่อ)

---

## 4. Scenario Design Workflow

ChatGPT ใช้ flow นี้ตอนออกแบบ test:

1. รับ input spec (JSON ด้านบน)
2. ระบุ level + target ให้ชัด
3. แตกเป็น precondition / steps / expected / failure_path
4. ผูกกับ log schema / module name จริงใน W3
5. ใส่ route_next (ส่วนใหญ่ → Gemini / Copilot-Gm)
6. ตรวจ self-consistency (steps สัมพันธ์กับ expected)
7. ส่งออกเป็น YAML/JSON พร้อมใช้งาน (แต่ในไฟล์นี้ใช้เป็น text spec เพื่ออ่านง่าย)

---

## 5. Example Scenarios

### 5.1 T0 — Engine Online

```yaml
id: T0-engine-online-001
level: T0
target: engine_boot
title: "Engine prints online banner"

steps:
  - "run: python src/main.py"

expected:
  - "stdout contains 'W3 Hybrid Engine: ONLINE'"
  - "process remains alive at least 3s"

failure_path:
  - "no output"
  - "process exits with non-zero code"

log:
  risk: L1
  route_next: Copilot-Gm
```

---

### 5.2 T1 — Config Loader Error Handling

```yaml
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
```

---

### 5.3 T2 — Module Load Log

```yaml
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
```

---

## 6. Integration with W3

**ตำแหน่งไฟล์ test spec:** `ChatGPT/testcases/`

### Copilot-Gm

- อ่าน test spec → สร้าง test script จริง (pytest / custom runner)
- รันใน CI / local
- แจ้งผลกลับ engine + BBX19

### Gemini

- ตรวจความครบถ้วน / risk coverage
- เช็คว่า test ครอบ use-case สำคัญของ engine
- review ว่า expected behavior align กับ system spec

### Grok

- จับ pattern ของ bug ที่เคยเจอจาก failure_path
- สร้าง knowledge base ของ failure signature
- ช่วยชี้ pattern anti-design

### DeepSeek

- ใช้ test spec วางแผน scaling / optimization
- วัด performance path ที่ critical
- เสนอ refactor ที่ไม่ทำลาย coverage เดิม

---

## 7. Anti-patterns (ถือว่า FAIL)

กรณีต่อไปนี้ เทสถือว่า "ใช้ไม่ได้":

- เคสที่เขียนแค่ "ผ่านได้" โดยไม่ทำอะไร
- expected กว้างแบบตีความได้หลายแบบ
- ไม่มี failure_path
- ไม่มีการผูกกับ log หรือ behavior จริงในระบบ
- narrative ยาว แต่ไม่ actionable
- route_next ไม่ชัด (ไม่รู้ใครดูต่อ)

> ถ้า test case ไม่:
> - actionable
> - reproducible
> - traceable ไปยัง module จริง
>
> ⇒ ให้ mark ว่า FAIL

---

## 8. Definition of Done (DOD)

ชุด testcases จาก ChatGPT ถือว่า "พร้อมส่งให้เอเจนท์" เมื่อ:

1. ครอบคลุม T0–T2 อย่างน้อยอย่างละ 1 เคสสำคัญ
2. ทุกเคสมี id, level, target, steps, expected, failure_path ครบ
3. มี route_next ชัดเจนสำหรับแต่ละเคส
4. สามารถแปลงเป็น test script ได้โดยไม่ต้องเดาเพิ่ม (human หรือ agent เขียน runner ได้ตรงๆ)

**เกณฑ์สุดท้าย:**

> If human can run it,
> and engine can log it,
> and Gemini can judge it,
> ⇒ Test Harness = PASS
