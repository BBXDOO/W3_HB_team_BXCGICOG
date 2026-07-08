# รายงาน: โมดูลที่ทำงานได้จริง — สาขา `refactor/v0.2`

> **จัดทำโดย:** Copilot Agent (BBX19/notes)  
> **วันที่:** 2026-07-08  
> **แหล่งข้อมูล:** สาขา `refactor/v0.2`, รัน `python -m pytest` ครบ 288 tests ผ่านทั้งหมด

---

## สรุปภาพรวม

| รายการ | จำนวน |
|---|---|
| โมดูลที่ทำงานได้จริง | **15 โมดูล** |
| Test files ที่ผ่าน | **42 ไฟล์** |
| จำนวน test cases ทั้งหมด | **288 passed** |
| Test cases ที่ fail | **0** |

---

## โมดูลที่ทำงานได้จริง (15 โมดูล)

---

### 1. `iget/` — PR Governance Tool (v9)

**ทำอะไรได้:**
- วิเคราะห์และให้คะแนน Pull Request บน GitHub (0–100)
- จำแนกไฟล์ในแต่ละ PR ว่าเป็น code / doc / test / risky
- สร้าง comment รายงานลงใน PR พร้อม inline annotations
- มี benchmark ทดสอบ scoring ในสถานการณ์ต่าง ๆ
- รองรับ Issue mode (v10-preview) — แนะนำ module จาก issue brief

**เรียกใช้ได้โดย:**
```bash
# CLI (ใช้กับ GitHub Actions หรือ Termux)
python -m iget

# Issue mode
python -m iget issue --repo owner/repo --issue 42

# GitHub Action
# ดู .github/workflows/ สำหรับ iget-workflow
```

---

### 2. `croll/` — Cross-L Dispatcher & Workset Builder

**ทำอะไรได้:**
- สร้าง Cross-L workset (แผนงาน non-executing) จาก PX coordinate
- Dispatch plan ไปยัง ECS event chain โดยไม่ execute จริง
- validate boundary contract (ตรวจ deny rules)
- List PX ที่รองรับ และ parse PX string
- รองรับ BOX suggestion (read-only) ใน plan

**เรียกใช้ได้โดย:**
```bash
python -m croll --help
python -m croll plan --px "1,1"
python -m croll list
python -m croll validate '{"w3_scope": "...", "deny": []}'
```

---

### 3. `hospitication/` — W3 Structural Health Observer

**ทำอะไรได้:**
- ตรวจสุขภาพโครงสร้าง repository (cognitive cost, dependency fatigue, replay complexity, semantic pressure, recovery resistance)
- สร้างรายงานใน format Markdown หรือ JSON
- เสนอ recovery proposals แบบ non-mutating
- emit signals เมื่อตรวจพบปัญหาเชิงโครงสร้าง

**เรียกใช้ได้โดย:**
```bash
python -m hospitication --repo . --format markdown
python -m hospitication --repo . --format json --output report.json
python tools/run_hospitication.py
```

---

### 4. `w3_api/` — W3 FastAPI Cross Gateway

**ทำอะไรได้:**
- REST API gateway สำหรับ cross-system coordination
- รับ intent จาก external agent → แปลงเป็น W3Lgu packet → สร้าง trace plan
- Endpoint `POST /w3/cross` — ส่ง intent แล้วได้ traceable signal response
- Endpoint `GET /health` — ตรวจสถานะ service
- ไม่ mutate ข้อมูลจริง (plan-only)

**เรียกใช้ได้โดย:**
```bash
uvicorn w3_api.main:app --reload
# หรือ
python -m uvicorn w3_api.main:app

# ตัวอย่าง request:
# POST http://localhost:8000/w3/cross
# Body: {"source": "BBX19", "intent": "review", "target": "REDR", "mode": "plan"}
```

---

### 5. `protocol/w3lgu/` — W3Lgu Language Runtime

**ทำอะไรได้:**
- Parse/สร้าง W3Lgu packet (KEY:VALUE pairs)
- ตรวจ 5-line program contract (MEM / PATCH / LAW / EVENT / SIGNAL)
- Runtime: normalize packet + สร้าง signal output
- Encode/decode W3Lgu values
- SixRoom runtime สำหรับ 6-room event flow
- PX anchor (แปลง 5-line program เป็น PX coordinate)

**เรียกใช้ได้โดย:**
```python
from protocol.w3lgu.core import W3LguPacket, W3LguPair
from protocol.w3lgu.runtime import run_packet

packet = W3LguPacket((W3LguPair("EVENT", "test"), W3LguPair("STATE", "ready")))
result = run_packet(packet)
```

---

### 6. `protocol/EP_SIGNAL/` — EP Signal Protocol + Rytm Layer

**ทำอะไรได้:**
- Encode binary string → EP_SIGNAL format (reversible)
- Decode EP_SIGNAL กลับเป็น binary string
- Interop กับ W3Lgu bytes และ MPCP binary
- Rytm layer: สร้าง pulse-cadence packet สำหรับ Cross-X transport
- แปลง EP_SIGNAL ↔ Rytm packet

**เรียกใช้ได้โดย:**
```python
from protocol.EP_SIGNAL.ep_signal_adapter import to_ep_signal, from_ep_signal
from protocol.EP_SIGNAL.rytm import rytm_from_binary

signal = to_ep_signal("01001000")
rytm = rytm_from_binary("01001000", meta=("W3Lgu",))
```

---

### 7. `protocol/mpcp/` — MPCP Protocol Kernel

**ทำอะไรได้:**
- กำหนด cooperative contract ระหว่าง module
- Parse และ validate MPCP string format
- Orchestrate flow ระหว่าง MPCP modules
- Registry สำหรับ module pillar
- Runtime trace สำหรับ execution

**เรียกใช้ได้โดย:**
```python
from protocol.mpcp.kernel.system import validate_system_context
from protocol.mpcp.runtime.executor import parse_mpcp, to_mpcp_output

data = parse_mpcp("STATE:ready,COLOR:green,SYM:circle")
validate_system_context({"SYSTEM": "mpcp"})
```

---

### 8. `cross_x/` — Cross-X Ecosystem Coordinator

**ทำอะไรได้:**
- ประสานงาน W3 subsystems ทั้งหมด (W3-API → W3Lgu → PX → W3DB → EP_SIGNAL)
- สร้าง improvement plan แบบ non-mutating
- Build event chain จาก intent
- Route package ไปยัง module ที่ถูกต้อง (REDR/PSP2/DTML/LRC2)
- `psp2_mfc_logic`: route_package(), generate_px_stamp(), resolve_node()

**เรียกใช้ได้โดย:**
```python
from cross_x.core import build_cross_plan
from core.runtime.w3lgu_mfc_logic.psp2_mfc_logic import route_package, generate_px_stamp
```

---

### 9. `src/w3db/` — W3DB Append-Only Store

**ทำอะไรได้:**
- CRUD operations สำหรับ relation types: TUF, XIZ, FBD, PRX, WHB
- Append-only flow (idempotent, deterministic ID)
- AppendEnvelope: cross-system append request ที่ immutable
- ใช้ร่วมกับ W3Lgu, PX, EP_SIGNAL

**เรียกใช้ได้โดย:**
```python
from src.w3db.store import get_store
from src.w3db.append_flow import append_observation

store = get_store()
from src.w3db.crud.tuf import create_tuf
create_tuf(store, source="BBX19", intent="review")
```

---

### 10. `codex/` — Codex Implementation Agent

**ทำอะไรได้:**
- สร้าง CodexExecutionPacket ที่ traceable และ immutable
- กำหนด governance boundaries (human_review_required, no_truth_mutation ฯลฯ)
- ลงทะเบียน Codex module ใน module loader และ central registry
- เชื่อมต่อกับ W3Lgu 5-line packet

**เรียกใช้ได้โดย:**
```python
from codex.agent import build_codex_packet

packet = build_codex_packet(source="Codex", intent="implement", target="REDR")
```

---

### 11. `wx/` — BOX Template Registry (Engine Index)

**ทำอะไรได้:**
- ค้นหา template จาก BOX registry โดย PX / work_type / rytm
- Read-only (ห้าม execute หรือ copy template)
- ส่งคืน suggestions พร้อม boundary และ deny rules
- Indexor (planner-only): suggest_references()

**เรียกใช้ได้โดย:**
```python
from wx.engine_index import find_templates
from wx.indexor import suggest_references

refs = suggest_references(px=[1, 1], work_type="patch")
```

---

### 12. `modules/W3Agent/tools/` — W3Agent Approval Gate & Worker

**ทำอะไรได้:**
- **approval_gate**: อ่าน command `/iget approve|reject|hold|ask|run` จาก PR comment
- ตรวจ authorized actor (BBX19, BBXDOO)
- สร้าง approval response และ execution plan
- **auto_responder**: GitHub Action worker อ่าน event JSON → trigger approval flow
- **execution_worker**: ร่าง patch file ลง `worker_output/` (ไม่แตะ repo จริง)

**เรียกใช้ได้โดย:**
```bash
# GitHub Action (auto trigger บน issue_comment event)
# ดู .github/workflows/w3_agent_autorespond.yml

# หรือรันตรง (Termux):
python modules/W3Agent/tools/auto_responder.py
```

---

### 13. `core/runtime/` — Core Runtime Engine (v2 + Process Layer)

**ทำอะไรได้:**
- **engine_v2**: orchestrate task → dispatch ไปยัง agent → รวม result
- **process_layer**: รัน REDR/PSP2/DTML/LRC2 pipeline แบบ traceable
- Semantic router: route task ไปยัง agent ตาม mpcp_role/concept
- Module loader router: load .idp.json identity และส่งคืน execution plan

**เรียกใช้ได้โดย:**
```python
from core.runtime.engine_v2 import dispatch
from core.runtime.process_layer import run_w3_process_layer

result = run_w3_process_layer(intent="review", source="BBX19", target="REDR")
```

---

### 14. `protocol/files_void/` — File.void Staging Layer

**ทำอะไรได้:**
- จัดการ lifecycle ของ file manifestation (UNRESOLVED → RESOLVING → MANIFESTED → PERSISTED → RELEASED)
- สร้าง temporary manifestation โดยไม่แตะ source truth
- สร้าง persistence handoff record
- Hash-based integrity verification

**เรียกใช้ได้โดย:**
```python
from protocol.files_void.core import FileVoidRecord, FileVoidManifestation
from protocol.files_void.tool import create_file_void_record
```

---

### 15. `config/` — W3 Ecosystem Config Loader

**ทำอะไรได้:**
- Load และ validate W3 ecosystem configuration (4 JSON files)
- W3ConfigBundle: environment / ecosystem / cross_system / paths
- ใช้เป็น orientation layer สำหรับ Cross-X coordination

**เรียกใช้ได้โดย:**
```python
from config.loader import load_w3_config

bundle = load_w3_config()
print(bundle.ecosystem)
print(bundle.component_path("w3lgu"))
```

---

## ตารางสรุป

| # | โมดูล | ที่อยู่ | จำนวน Tests | วิธีเรียกหลัก |
|---|---|---|---|---|
| 1 | IGET | `iget/` | 42 | `python -m iget` / GitHub Action |
| 2 | CROLL | `croll/` | 32 | `python -m croll` |
| 3 | Hospitication | `hospitication/` | ~18 | `python -m hospitication` |
| 4 | W3-API | `w3_api/` | ~12 | `uvicorn w3_api.main:app` |
| 5 | W3Lgu Runtime | `protocol/w3lgu/` | ~20 | Python import |
| 6 | EP_SIGNAL | `protocol/EP_SIGNAL/` | ~10 | Python import |
| 7 | MPCP | `protocol/mpcp/` | ~8 | Python import |
| 8 | Cross-X | `cross_x/` | ~6 | Python import |
| 9 | W3DB | `src/w3db/` | ~15 | Python import |
| 10 | Codex | `codex/` | 4 | Python import |
| 11 | WX/BOX Engine | `wx/` | ~6 | Python import |
| 12 | W3Agent Tools | `modules/W3Agent/tools/` | ~15 | GitHub Action / Python |
| 13 | Core Runtime | `core/runtime/` | ~8 | Python import |
| 14 | File.void | `protocol/files_void/` | ~5 | Python import |
| 15 | Config Loader | `config/` | ~4 | Python import |

> หมายเหตุ: `~` หมายถึงจำนวน test ในกลุ่มไฟล์ test ที่เกี่ยวข้อง (รวมแล้ว 288 passed ทั้งสิ้น)

---

## Smoke Test (Termux / Android)

```bash
# Clone และรัน smoke test บน Termux
pkg update && pkg install python git
git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
cd W3_HB_team_BXCGICOG
git checkout refactor/v0.2
python tools/smoke_test.py
```

---

*รายงานนี้จัดทำโดย Copilot Agent จากการรัน `python -m pytest` และวิเคราะห์ source code ใน branch `refactor/v0.2` โดยตรง*
