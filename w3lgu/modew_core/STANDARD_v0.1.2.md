W3Lgu Standard Specification

Modew Architecture + Execution + Task System

Version: v0.1.2
Status: Draft Standard (Deployable)
Authority: BBX19
Scope: W3Lgu Core System

---

1. INTRODUCTION

Modew (Module-W) คือหน่วยประมวลผลปัญญาแบบแยกส่วน (Decoupled Cognitive Unit)
ใช้สำหรับรับข้อมูล → ประมวลผล → สร้างสถานะ → ส่งต่อ → บันทึก

มาตรฐานนี้กำหนด:

- โครงสร้าง Modew
- วงจรการทำงาน (Execution Lifecycle)
- ระบบงาน (Task System)
- การเชื่อมต่อ (Inter-Modew Communication)
- การบันทึก (Trace & Logging)

---

2. CORE PRINCIPLES

2.1 Observation Model

State ∈ {0.0, 0.5, 1.0}

State| Meaning
1.0| Active / Force / Line A
0.5| Uncertain / Observe / Line B
0.0| Stable / Passive / Line C

---

2.2 Separation of Concern

Layer| Responsibility
Modew| Process & Decision
PSP2| Routing
DTML| Validation
LRC2| Logging
REDR| Structuring

---

2.3 Deterministic + Non-Deterministic Hybrid

ระบบต้องรองรับ:

- Deterministic (0 / 1)
- Semantic Uncertainty (0.5)

---

3. MODEW STRUCTURE (REQUIRED)

{
  "registry": {
    "id": "MDW-XXXX",
    "version": "0.1.2",
    "type": "logic | perception | process",
    "name": "string"
  },

  "schema": {
    "input_type": "object",
    "required_fields": []
  },

  "properties": {},

  "logic_law": {
    "observation": "rule",
    "action": "rule"
  },

  "perception": {
    "mapping": [
      {"state": 1.0, "symbol": "▲", "color": "RED"},
      {"state": 0.5, "symbol": "●", "color": "YELLOW"},
      {"state": 0.0, "symbol": "■", "color": "GREEN"}
    ]
  }
}

---

4. EXECUTION PROTOCOL (v0.1.1)

4.1 Lifecycle

INVOKE → VALIDATE → OBSERVE → DECIDE → EMIT → LOG → IDLE

---

4.2 Execution Contract

{
  "execution": {
    "trigger": "event | interval | manual",
    "priority": "low | medium | high | critical",
    "concurrency": "allow | queue | lock",
    "retry": {
      "max": 3,
      "fallback": "state_0.5"
    }
  }
}

---

4.3 Validation (DTML)

{
  "governance": {
    "schema_check": true,
    "dtml_required": true
  }
}

---

4.4 Emission

{
  "emit": {
    "type": "event | signal",
    "resolver": "PSP2"
  }
}

---

4.5 Trace (LRC2 REQUIRED)

{
  "trace": {
    "trace_id": "auto",
    "log": true,
    "channel": "LRC2"
  }
}

---

5. TASK SYSTEM (v0.1.2)

5.1 Task Model

{
  "task": {
    "task_id": "UUID",
    "modew_id": "MDW-XXXX",
    "execution_mode": "sync | async",
    "status": "pending | running | completed | failed",
    "priority": "low | medium | high | critical",
    "created_at": "ISO8601"
  }
}

---

5.2 Task Lifecycle

CREATE → QUEUE → RUN → COMPLETE | FAIL → LOG

---

5.3 Async Behavior

Event → Task Created → Immediate Return
Task → Background Execution → Emit Result Event

---

5.4 Error Model

{
  "error": {
    "type": "validation | runtime | timeout",
    "severity": "low | high | critical",
    "recovery": "retry | fallback_0.5 | escalate"
  }
}

---

5.5 Task vs State

Task Status ≠ System State

Task = execution progress  
State = perception result

---

6. MODEW COMMUNICATION

6.1 Routing

Modew → PSP2 → Target Modew

---

6.2 Dynamic Resolution

{
  "plug": {
    "input": "dynamic",
    "output": "dynamic"
  }
}

---

6.3 Chain Execution

{
  "link": {
    "next": ["MDW-A", "MDW-B"],
    "condition": "state_based"
  }
}

---

7. EVOLUTION SYSTEM

{
  "evolution": {
    "fbd": true,
    "patch_mode": "draft",
    "requires": ["DTML", "Human"],
    "versioning": "semantic"
  }
}

---

8. MINIMUM COMPLIANCE

Modew MUST implement:

- registry
- schema
- logic_law
- execution
- trace
- task binding

---

9. FILE STANDARD

Path: /W3Lgu/modew/
Format: .json | .wgu

---

10. SYSTEM GUARANTEES

เมื่อปฏิบัติตามมาตรฐานนี้:

- ระบบสามารถ scale ได้
- รองรับ async execution
- log ไม่สูญหาย
- behavior traceable
- รองรับ uncertainty (0.5)

---

11. LIMITATIONS

- ไม่มี scheduler (future version)
- ยังไม่รองรับ external protocol เต็มรูปแบบ
- ต้องพึ่ง DTML สำหรับความปลอดภัย

---

12. FUTURE EXTENSIONS

- Scheduler System
- External Interop Layer
- Distributed Modew Network

---

FINAL NOTE

Modew ไม่ใช่เพียง module
แต่เป็นหน่วยปัญญาที่มี lifecycle, state, และ memory

---

End of Specification
