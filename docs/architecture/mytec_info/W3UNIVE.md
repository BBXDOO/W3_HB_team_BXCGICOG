# W3UNIVE — คู่มือเทคนิคภาษาไทยสำหรับ W3

เอกสารนี้เป็นคู่มือทางเทคนิคสำหรับการอ่าน ใช้งาน ตรวจสอบ และทดสอบระบบหลักใน repository `W3_HB_team_BXCGICOG` บน branch `refactor/v0.2`

เอกสารนี้เน้น “ทำอย่างไร ใช้ไฟล์ไหน รันคำสั่งอะไร และต้องระวังอะไร”

เอกสารนี้ไม่ใช่ philosophy paper, governance paper, หรือเอกสารประวัติศาสตร์ของ W3 และไม่แทน README, source code, protocol, registry, หรือ governance docs ใด ๆ

## 0) กติกาอ่านเอกสารนี้

- ใช้เอกสารนี้เป็น **technical handbook** สำหรับเปิด repo แล้วลงมือเช็คระบบ
- ถ้าเอกสารนี้ขัดกับ source code / protocol / registry ให้ยึด source code / protocol / registry ก่อน
- คำว่า `mutated:false` หมายถึงระบบนั้นรายงานว่า “ไม่ได้แก้ truth/runtime state”
- คำว่า `read-only` หมายถึงอ่าน/ตรวจ/ประเมิน ไม่แก้ไฟล์ ไม่ซ่อมเอง
- คำว่า `plan-only` หมายถึงสร้างแผน/trace/preview แต่ไม่ execute
- คำว่า `gateway-only` หมายถึงเป็นทางเข้า/ตัว normalize/ตัวทำ trace ไม่ใช่ executor

## 1) Repository Entry / Branch

| รายการ | ค่าใช้งาน |
|---|---|
| active base | `refactor/v0.2` |
| public branch | `main` เป็น public/stable surface ไม่ใช่ฐานพัฒนาหลัก |
| handbook path | `docs/architecture/mytec_info/W3UNIVE.md` |

คำสั่งตรวจ branch ปัจจุบัน:

```bash
git branch --show-current
git status --short
```

เอกสารที่เกี่ยวข้อง:

- [Branch Strategy](../../branch_strategy.md)
- [Public Boundary](../../public_boundary.md)
- [v0.2 → v0.3 Readiness](../../reports/V0_2_TO_V0_3_READINESS.md)

ต้องระวัง:

- อย่าใช้ config หรือ docs เป็น source truth
- อย่าให้ระบบ gateway-only กลายเป็น executor โดยไม่ผ่าน review
- อย่าให้ read-only observer กลายเป็น auto-repair

## 2) Technical Map / Quick Navigation

| System | Path | Purpose | Run/Test | Boundary |
|---|---|---|---|---|
| W3-API | [w3_api](../../../w3_api/) | Cross Gateway / normalizer / trace planner | `python -m pytest tests/test_w3_api_cross.py` | gateway-only, `mutated:false` |
| W3 local client | [tools/w3api.py](../../../tools/w3api.py), [w3](../../../w3) | local shell/Termux client + optional Markdown writer | `python tools/w3api.py --help` | local wrapper only, server remains gateway-only |
| Cross-X | [cross_x](../../../cross_x/) | cross-point coordinator | `python -m pytest tests/test_cross_x_config.py` | plan-only, non-mutating |
| W3Lgu | [protocol/w3lgu](../../../protocol/w3lgu/) | five-line packet / expression layer | `python -m pytest tests/test_w3lgu_core.py` | protocol/expression, ไม่ใช่ executor เอง |
| W3DB | [src/w3db](../../../src/w3db/) | relation flow + in-process store | ดูตัวอย่าง Python ในหัวข้อ W3DB | append/trace path, ห้าม rewrite truth |
| EP_SIGNAL:Rytm | [protocol/EP_SIGNAL](../../../protocol/EP_SIGNAL/) | signal preview / rhythm preview | `python -m pytest tests/test_ep_signal_rytm.py` | preview-only |
| Hospitication | [hospitication](../../../hospitication/) | structural health observer | `python tools/run_hospitication.py` | read-only, no auto-repair |
| G-State | [G-State Paper](../../governance/G_STATE_PAPER.md), [examples/gstate](../../../examples/gstate/) | awareness metadata | `python -m pytest tests/test_g_state_foundation.py` | awareness, not authority |
| IGET | [iget](../../../iget/), [workflow](../../../.github/workflows/iget.yml) | PR intelligence / evaluation support | `python -m iget.tests.test_iget_v8` | review support, not human replacement |
| Codex | [codex](../../../codex/) | implementation workspace / execution packet helper | `python -m pytest tests/test_codex_agent.py` | branch work, no self-merge |
| Config | [config](../../../config/) | orientation map | `python -m pytest tests/test_cross_x_config.py` | orientation only |
| Process Layer | [process_layer.py](../../../core/runtime/process_layer.py) | REDR→PSP2→DTML→LRC2 trace | `python -m pytest tests/test_process_layer.py` | plan-only trace |

## 3) Setup พื้นฐาน

ติดตั้ง dependency จากไฟล์ repo:

```bash
python -m pip install -r requirements.txt
```

ถ้าจะรัน FastAPI ผ่าน ASGI server ให้ติดตั้ง `uvicorn` เพิ่มก่อน:

```bash
python -m pip install uvicorn
python -m uvicorn w3_api.main:app --reload
```

> หมายเหตุ: `uvicorn` เป็นคำสั่งสำหรับเปิด FastAPI app แบบ local server ถ้าเครื่องยังไม่มีให้ติดตั้งก่อนใช้งาน

## 4) W3-API / Cross Gateway

Path หลัก:

- [w3_api/](../../../w3_api/)
- [w3_api/main.py](../../../w3_api/main.py)
- [w3_api/router.py](../../../w3_api/router.py)
- [w3_api/models.py](../../../w3_api/models.py)
- [w3_api/adapters/](../../../w3_api/adapters/)
- [W3-API Cross Proof](../../reports/W3_API_CROSS_PROOF.md)

หน้าที่:

- รับ external/agent intent
- normalize เป็น W3Lgu five-line packet
- สร้าง W3DB append plan
- สร้าง EP_SIGNAL / RYTM preview
- ตอบกลับ trace ที่ตรวจสอบได้

Boundary:

- `gateway-only`
- `mutated:false`
- ไม่ใช่ runtime executor
- ไม่เขียน W3DB จริงจาก endpoint นี้
- ไม่ mutate EP_SIGNAL, MPCP, W3Lgu, หรือ runtime state

Endpoints:

```text
GET /health
GET /w3/health
POST /w3/cross
```

ตัวอย่าง request:

```json
{
  "source": "BBX19",
  "intent": "align W3Lgu with W3DB and EP_SIGNAL",
  "target": "W3Lgu",
  "mode": "cross",
  "payload": {
    "contract": "do not rewrite source truth"
  }
}
```

รูปแบบ response ที่ควรเห็น:

```json
{
  "id": "<uuid>",
  "timestamp": "<utc>Z",
  "status": "accepted",
  "w3lgu": "MEM:...\nPATCH:...\nLAW:...\nEVENT:...\nSIGNAL:...",
  "signal": {
    "type": "W3_API_CROSS",
    "traceable": true,
    "mutated": false,
    "w3db": {
      "mode": "append_plan_only",
      "mutated": false
    },
    "ep_signal": {
      "mode": "preview_only",
      "mutated": false
    }
  }
}
```

ตรวจ health:

```bash
python tools/w3api.py --health
```

เรียก `/w3/cross` ผ่าน local client/wrapper:

```bash
python tools/w3api.py --source termux --intent review --target W3 --mode cross --focus system
```

ถ้าต้องการเขียน Markdown ลงเครื่อง ให้ wrapper เขียนไฟล์เอง ไม่ใช่ server เขียน:

```bash
python tools/w3api.py --source termux --intent review --target W3 --mode cross --write-md docs/generated/w3-cross-review.md
```

ใช้ shell wrapper ที่ root repo ได้เช่นกัน:

```bash
./w3 --health
./w3 --source termux --intent review --target W3 --mode cross --focus system
```

ทดสอบ:

```bash
python -m pytest tests/test_w3_api_cross.py
python -m pytest tests/test_w3api_tools.py
```

## 5) Cross-X

Path หลัก:

- [cross_x/](../../../cross_x/)
- [cross_x/core.py](../../../cross_x/core.py)
- [docs/cross_x_ecosystem.md](../../cross_x_ecosystem.md)

หน้าที่:

- เป็น cross-point coordinator
- สร้างแผนรวม W3-API intent → W3Lgu packet → PX anchor → W3DB append envelope → EP_SIGNAL preview
- ดึง process layer REDR→PSP2→DTML→LRC2 มาเป็น trace

Boundary:

- `plan-only`
- non-mutating
- ไม่ persist W3DB
- ไม่ mutate EP_SIGNAL
- ไม่ execute MPCP
- ไม่ approve truth

ตัวอย่างเรียกจาก Python:

```python
from cross_x.core import CrossXRequest, build_cross_x_plan

plan = build_cross_x_plan(
    CrossXRequest(
        source="BBX19",
        intent="check cross-system alignment",
        target="W3-API",
        mode="observe",
    )
)
print(plan.to_dict()["mutated"])
```

ผลลัพธ์ที่ควรเห็น:

```text
False
```

ทดสอบ:

```bash
python -m pytest tests/test_cross_x_config.py
```

## 6) W3Lgu

Path หลัก:

- [protocol/w3lgu/](../../../protocol/w3lgu/)
- [protocol/w3lgu/core.py](../../../protocol/w3lgu/core.py)
- [protocol/w3lgu/parser.py](../../../protocol/w3lgu/parser.py)
- [protocol/w3lgu/px.py](../../../protocol/w3lgu/px.py)
- [protocol/w3lgu/RML01.md](../../../protocol/w3lgu/RML01.md)

ใช้งานใน repo นี้แบบเทคนิค:

- เป็น compact language / packet / expression layer
- W3-API ใช้สร้าง five-line packet
- Cross-X ใช้ packet เพื่อทำ PX anchor และ append envelope
- validator ใช้ตรวจ packet shape

Five-line packet ที่พบใน W3-API:

```text
MEM:SOURCE:BBX19
PATCH:MODE:cross
LAW:TARGET:W3Lgu,CONTRACT:do/not/rewrite/source/truth
EVENT:INTENT:align/W3Lgu/with/W3DB/and/EP_SIGNAL
SIGNAL:STATUS:received,TRACEABLE:true
```

Boundary:

- เป็นภาษา/packet/protocol shape
- อย่าใช้เป็นข้ออ้างให้ execute หรือ mutate truth เอง

ทดสอบ:

```bash
python -m pytest tests/test_w3lgu_core.py
```

## 7) W3DB

Path หลัก:

- [src/w3db/](../../../src/w3db/)
- [src/w3db/config.py](../../../src/w3db/config.py)
- [src/w3db/models.py](../../../src/w3db/models.py)
- [src/w3db/store.py](../../../src/w3db/store.py)
- [src/w3db/flow.py](../../../src/w3db/flow.py)
- [src/w3db/crud/](../../../src/w3db/crud/)
- `SYSTEM/TESTS/w3db/` — path not found / verify required

Flow ทางเทคนิค:

```text
INPUT -> XIZ -> PROCESS -> TUF -> FBD -> WHB -> PRX
```

คำอธิบายแบบใช้งาน:

| ส่วน | ใช้ทำอะไร |
|---|---|
| `XIZ` | เก็บ input event เป็น record เริ่มต้นและควร immutable หลังสร้าง |
| `TUF` | เก็บ observation state / confidence |
| `FBD` | เก็บ boundary / failure detail |
| `WHB` | เก็บ IF → THEN patch / rule view |
| `PRX` | เก็บ perception output จาก TUF |

ตัวอย่างรัน flow จาก Python:

```bash
python - <<'PY'
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore

store = W3DBStore()
result = run_flow(
    input_event="technical handbook smoke check",
    cix_id="CIX-HANDBOOK",
    confidence=0.5,
    store=store,
)
print(result["output"])
PY
```

Boundary:

- W3DB เป็น trace/memory path
- W3-API ปัจจุบันส่งกลับ append plan เท่านั้น ไม่เขียน W3DB จาก gateway
- append-only ควรใช้เฉพาะจุดที่ได้รับอนุมัติแล้ว

ทดสอบที่พบใน repo:

```bash
python -m pytest tests/test_px_w3db_append_flow.py
```

คำสั่งที่ผู้ใช้ระบุแต่ path ยังไม่พบใน repo นี้:

```bash
# ตรวจสอบ path ก่อนใช้งาน
python SYSTEM/TESTS/w3db/test_crud.py
python SYSTEM/TESTS/w3db/test_flow.py
```

## 8) EP_SIGNAL / RYTM

Path หลัก:

- [protocol/EP_SIGNAL/](../../../protocol/EP_SIGNAL/)
- [protocol/EP_SIGNAL/ep_signal_adapter.py](../../../protocol/EP_SIGNAL/ep_signal_adapter.py)
- [protocol/EP_SIGNAL/rytm.py](../../../protocol/EP_SIGNAL/rytm.py)

หน้าที่:

- EP_SIGNAL เป็น perception/signal layer
- RYTM เป็น preview format ที่ช่วยแสดง rhythm/fingerprint ของ signal
- W3-API และ Cross-X ใช้เป็น preview ไม่ใช่ mutation

Boundary:

- `preview_only`
- `mutated:false`
- ไม่ persist เป็น source truth เองจาก gateway

ทดสอบ:

```bash
python -m pytest tests/test_ep_signal_rytm.py
```

## 9) Hospitication

Path หลัก:

- [hospitication/](../../../hospitication/)
- [hospitication/analysis/](../../../hospitication/analysis/)
- [hospitication/cli.py](../../../hospitication/cli.py)
- [tools/run_hospitication.py](../../../tools/run_hospitication.py)

หน้าที่:

- read-only structural health observer
- ตรวจ / evaluate / propose
- ไม่ auto-repair
- ไม่ลบไฟล์
- ไม่ rewrite truth

analysis modules ที่มี:

- [cognitive_cost.py](../../../hospitication/analysis/cognitive_cost.py)
- [dependency_fatigue.py](../../../hospitication/analysis/dependency_fatigue.py)
- [recovery_resistance.py](../../../hospitication/analysis/recovery_resistance.py)
- [replay_complexity.py](../../../hospitication/analysis/replay_complexity.py)
- [semantic_pressure.py](../../../hospitication/analysis/semantic_pressure.py)

รันแบบ concise runner:

```bash
python tools/run_hospitication.py
```

ผลลัพธ์ที่ควรเห็น:

```text
status:completed
mutated:false
observation:not repair
warnings_risks:
recommendations:
boundary:Hospitication observes/evaluates/proposes only; no auto-repair
```

รัน CLI report:

```bash
python -m hospitication.cli --repo . --format markdown
python -m hospitication.cli --repo . --format json --timestamp 2026-06-01T00:00:00Z
```

ทดสอบ:

```bash
python -m pytest tests/test_hospitication_runner.py
python -m pytest tests/test_hospitication_core.py tests/test_hospitication_cli.py
```

## 10) G-State

Path หลัก:

- [docs/governance/G_STATE_PAPER.md](../../governance/G_STATE_PAPER.md)
- [examples/gstate/](../../../examples/gstate/)
- [notes/gstate/W3_ORGANIZATIONAL_CULTURE_LINK.md](../../../notes/gstate/W3_ORGANIZATIONAL_CULTURE_LINK.md)

หน้าที่:

- shared awareness metadata
- บอกสภาพแวดล้อมที่กำลังทำงานอยู่
- attach ได้กับ request, handoff, report, note

ไม่ใช่:

- executor
- workflow engine
- state-machine replacement
- task approver
- governance authority

ตัวอย่างไฟล์ `.gstate`:

| File | State |
|---|---|
| [build.gstate](../../../examples/gstate/build.gstate) | `GSTATE:BUILD` |
| [audit.gstate](../../../examples/gstate/audit.gstate) | `GSTATE:AUDIT` |
| [research.gstate](../../../examples/gstate/research.gstate) | `GSTATE:RESEARCH` |
| [recovery.gstate](../../../examples/gstate/recovery.gstate) | `GSTATE:RECOVERY` |
| [maintenance.gstate](../../../examples/gstate/maintenance.gstate) | `GSTATE:MAINTENANCE` |
| [learning.gstate](../../../examples/gstate/learning.gstate) | `GSTATE:LEARNING` |

ตัวอย่างการใช้แบบเอกสาร:

```text
GSTATE:AUDIT
CONDITION:ecosystem oriented toward inspection, proof, verification, and boundary review
```

Boundary:

- G-State เป็น awareness
- ไม่ให้ authority
- ไม่ override ROT / Paper / Result / source code / protocol / registry

ทดสอบ:

```bash
python -m pytest tests/test_g_state_foundation.py
```

## 11) IGET

Path หลัก:

- [iget/](../../../iget/)
- [.github/workflows/iget.yml](../../../.github/workflows/iget.yml)
- [iget/tests/test_iget_v8.py](../../../iget/tests/test_iget_v8.py)

หน้าที่:

- PR intelligence / evaluation support
- ช่วยตรวจ governance / semantic state / proof trace
- ไม่แทน Human Review
- ไม่แทน Governance Gate

รัน smoke suite:

```bash
python -m iget.tests.test_iget_v8
```

รัน pipeline local:

```bash
python -m iget.main
```

ต้องระวัง:

- `iget.main` อาจต้องการ env เช่น `GITHUB_TOKEN`, `REPO`, `PR` เมื่อใช้งานกับ GitHub workflow
- workflow ใช้ Python 3.11 และรัน `python -m iget.tests.test_iget_v8`

## 12) Codex Workspace

Path หลัก:

- [codex/](../../../codex/)
- [codex/agent.py](../../../codex/agent.py)
- [codex/modules.json](../../../codex/modules.json)
- [modules/Codex/module.json](../../../modules/Codex/module.json)
- [core/module-loader/identity/Codex.idp.json](../../../core/module-loader/identity/Codex.idp.json)

directories ที่พบ:

- `codex/requests/`
- `codex/reports/`
- `codex/logs/`
- `codex/modules/`
- `codex/notes/`

หน้าที่:

- implementation workspace / agent execution package
- สร้าง execution packet
- ช่วยทำ branch-local code/test/docs/PR artifacts

Boundary:

- Codex ไม่ใช่ source truth โดยตัวเอง
- ไม่ self-merge
- ไม่ bypass Human Review หรือ Governance Gate

ตัวอย่าง Python:

```python
from codex import build_execution_packet

packet = build_execution_packet("implement reviewed W3 task")
print(packet.w3lgu)
```

ทดสอบ:

```bash
python -m pytest tests/test_codex_agent.py
```

## 13) Config / Registry / Runtime

Config paths:

- [config/](../../../config/)
- [config/environment.json](../../../config/environment.json)
- [config/ecosystem.json](../../../config/ecosystem.json)
- [config/cross_system.json](../../../config/cross_system.json)
- [config/paths.json](../../../config/paths.json)
- [config/loader.py](../../../config/loader.py)

Registry paths:

- [modules/registry.json](../../../modules/registry.json)
- [core/module-loader/module-registry.json](../../../core/module-loader/module-registry.json)

Runtime paths:

- [core/runtime/](../../../core/runtime/)
- [core/runtime/agents/](../../../core/runtime/agents/)
- [core/runtime/process_layer.py](../../../core/runtime/process_layer.py)

Config ใช้ทำอะไร:

- บอก orientation map
- บอกระบบที่เข้าร่วม Cross-X
- บอก path สำคัญ
- validate ให้ tests/tools อ่าน ecosystem shape เดียวกัน

Config ไม่ใช้ทำอะไร:

- ไม่ approve truth
- ไม่ override registry
- ไม่ mutate W3DB / EP_SIGNAL / MPCP / W3Lgu

Process layer:

| Layer | Technical role | Boundary |
|---|---|---|
| REDR | package request/intent | ไม่ mutate truth |
| PSP2 | route/stamp | ไม่ mutate truth |
| DTML | decision/risk review | ไม่ approve เอง |
| LRC2 | log/memory preview | ไม่เขียน memory ถาวรโดยไม่ผ่าน gate |

ทดสอบ:

```bash
python -m pytest tests/test_process_layer.py
python -m pytest tests/test_cross_x_config.py
```

## 14) Testing รวมคำสั่งที่พบใน repo

ติดตั้ง dependency:

```bash
python -m pip install -r requirements.txt
```

ทดสอบ G-State:

```bash
python -m pytest tests/test_g_state_foundation.py
```

ทดสอบ Hospitication runner:

```bash
python -m pytest tests/test_hospitication_runner.py
python tools/run_hospitication.py
```

ทดสอบ W3-API:

```bash
python -m pytest tests/test_w3_api_cross.py
```

ทดสอบ Cross-X / process layer:

```bash
python -m pytest tests/test_cross_x_config.py
python -m pytest tests/test_process_layer.py
```

ทดสอบ W3Lgu / PX / W3DB append / EP_SIGNAL:

```bash
python -m pytest tests/test_w3lgu_core.py
python -m pytest tests/test_px_w3db_append_flow.py
python -m pytest tests/test_ep_signal_rytm.py
```

ทดสอบ Codex:

```bash
python -m pytest tests/test_codex_agent.py
```

ทดสอบ IGET:

```bash
python -m iget.tests.test_iget_v8
```

เครื่องมือ CI/agent ที่มีใน `tools/`:

```bash
python tools/w3_agent_ci.py
python tools/run_hospitication.py
python tools/w3api.py --health
```

ทดสอบเอกสาร branch/public boundary:

```bash
python -m pytest tests/test_branch_public_docs.py
```

## 15) Quick “เปิด repo แล้วเริ่มตรวจ” workflow

1. ตรวจ branch และ working tree

```bash
git branch --show-current
git status --short
```

2. ติดตั้ง dependencies

```bash
python -m pip install -r requirements.txt
```

3. รันชุด test หลักที่เกี่ยวกับ handbook นี้

```bash
python -m pytest tests/test_g_state_foundation.py tests/test_hospitication_runner.py tests/test_w3_api_cross.py tests/test_w3api_tools.py tests/test_cross_x_config.py tests/test_process_layer.py
```

4. รัน Hospitication แบบ read-only

```bash
python tools/run_hospitication.py
```

5. ถ้าจะเปิด W3-API local server

```bash
python -m pip install uvicorn
python -m uvicorn w3_api.main:app --reload
```

6. ตรวจ proof docs ก่อนแก้ architecture

- [W3-API Cross Proof](../../reports/W3_API_CROSS_PROOF.md)
- [G-State Paper](../../governance/G_STATE_PAPER.md)
- [v0.2 → v0.3 Readiness](../../reports/V0_2_TO_V0_3_READINESS.md)

## 16) ข้อควรระวังสำคัญ

- W3-API เป็น `gateway-only` อย่าใช้เป็น executor
- Cross-X เป็น `plan-only` อย่าใช้เป็น mutating workflow engine
- Hospitication เป็น `read-only` observer อย่าใช้เป็น auto-repair
- G-State เป็น awareness metadata อย่าใช้เป็น authority
- Config เป็น orientation map อย่าใช้เป็น source truth
- Registry / protocol / source code คือจุดตรวจ truth หลัก
- ถ้า path หรือ command ไม่พบ ให้หยุดและตรวจ repo ก่อน ไม่ควรเดาแทนระบบ
