# W3DB — Setup & Usage Guide

## Overview

`src/w3db` is the in-process storage layer for the **W3 relation flow**.
It implements the full execution pipeline defined in
`knowledge/W3MEMORIEA/W3memoriea.md`:

```
INPUT -> XIZ -> PROCESS (full run) -> TUF -> FBD -> WHB -> PRX
```

---

## Directory Structure

```
src/w3db/
├── __init__.py          # package — re-exports public API
├── config.py            # env/integration config  (dev / test / prod)
├── models.py            # dataclasses: XIZ, TUF, FBD, WHB, PRX
├── store.py             # in-memory CRUD store + singleton get_store()
├── flow.py              # run_flow() — full pipeline orchestrator
└── crud/
    ├── __init__.py
    ├── xiz.py           # CRUD helpers for XIZ domain
    ├── tuf.py           # CRUD helpers for TUF domain
    ├── fbd.py           # CRUD helpers for FBD domain
    ├── whb.py           # CRUD helpers for WHB domain
    └── prx.py           # CRUD helpers for PRX domain

SYSTEM/TESTS/w3db/
├── __init__.py
├── test_crud.py         # 44 unit tests for all domain CRUD
└── test_flow.py         # 65 integration tests for relation flow
```

---

## Environment Variables

| Variable              | Default    | Description                              |
|-----------------------|------------|------------------------------------------|
| `W3DB_ENV`            | `dev`      | Environment profile: `dev`, `test`, `prod` |
| `W3DB_BACKEND`        | `memory`   | Storage backend (`memory` only for now)   |
| `W3DB_LOG_LEVEL`      | `DEBUG`    | Log level                                |
| `W3DB_IMMUTABLE_XIZ`  | `false`    | `true` → XIZ records cannot be updated   |
| `W3DB_MAX_STORE_SIZE` | `1000`     | Max records per domain (advisory)        |

### Prod profile (applied automatically when `W3DB_ENV=prod`)

```bash
export W3DB_ENV=prod
export W3DB_IMMUTABLE_XIZ=true
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full relation flow

```python
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore

store = W3DBStore()          # isolated store for this session
result = run_flow(
    input_event="Patient arrived — BP 140/90",
    cix_id="CIX-001",
    confidence=0.72,         # 0.0–1.0: drives TUF state + PRX perception
    store=store,
)

# Compact perception output (OPD Dashboard view)
print(result["output"])
```

**Example output:**
```json
{
  "cix": "CIX-001",
  "xiz": "XIZ-A1B2C3D4",
  "tuf": { "id": "TUF-...", "initial": "0.5", "final": "0.5", "confidence": 0.72 },
  "fbd": { "id": "FBD-...", "failure": "Yellow", "impact": "Boundary within limits" },
  "whb": { "id": "WHB-...", "condition": "IF final_state=0.5 AND confidence=0.72", "action": "THEN OBSERVE — boundary approached, monitor closely" },
  "prx": { "id": "PRX-...", "symbol": "◆", "color": "BLUE", "intensity": 0.44 }
}
```

### 3. Use individual CRUD helpers

```python
from src.w3db.store import W3DBStore
from src.w3db.crud.xiz import create_xiz, read_xiz, update_xiz, delete_xiz

store = W3DBStore()
xiz = create_xiz("XIZ-001", action="Checked patient", timestamp="2026-01-01T00:00:00Z", store=store)
xiz = update_xiz("XIZ-001", result="Stable", store=store)
print(read_xiz("XIZ-001", store=store).to_dict())
```

---

## Running the Tests

```bash
# CRUD unit tests (44 checks)
python SYSTEM/TESTS/w3db/test_crud.py

# Relation flow integration tests (65 checks)
python SYSTEM/TESTS/w3db/test_flow.py

# Full repo CI
python tools/w3_agent_ci.py
```

---

## Data Models

### XIZ — Execution Trace

| Field       | Type    | Notes                              |
|-------------|---------|------------------------------------|
| `xiz_id`    | str     | Primary key                        |
| `action`    | str     | Description of action taken        |
| `timestamp` | str     | ISO-8601                           |
| `result`    | str     | Outcome text                       |
| `tuf_id`    | str?    | FK → TUF (set automatically by flow)|
| `immutable` | bool    | If True, record cannot be updated  |

### TUF — Process State Snapshot

| Field        | Type  | Notes                              |
|--------------|-------|------------------------------------|
| `tuf_id`     | str   | Primary key                        |
| `cix_id`     | str?  | FK → CIX identity                  |
| `initial`    | str   | `"0"` / `"0.5"` / `"1"` (obs only)|
| `final`      | str   | `"0"` / `"0.5"` / `"1"` (obs only)|
| `confidence` | float | `[0.0, 1.0]`                       |
| `resolution` | str   | Resolution note                    |
| `note`       | str   | Free text                          |

### FBD — Failed Boundary Detection

| Field             | Type | Notes                          |
|-------------------|------|--------------------------------|
| `fbd_id`          | str  | Primary key                    |
| `tuf_id`          | str  | FK → TUF                       |
| `first_deviation` | str  | First detected deviation       |
| `failure_point`   | str  | Location of failure            |
| `failure`         | str  | `Red`/`Yellow`/`Green`/`Blue`  |
| `conditions`      | str  | Boundary conditions            |
| `impact`          | str  | Impact assessment              |
| `line3_patch`     | str  | IF→THEN from WHB               |

### WHB — Contextual Law (Line 3)

| Field       | Type | Notes                    |
|-------------|------|--------------------------|
| `law_id`    | str  | Primary key              |
| `fbd_id`    | str  | FK → FBD                 |
| `condition` | str  | `"IF ..."` clause        |
| `action`    | str  | `"THEN ..."` clause      |

### PRX — Perception Output (derived only)

| Field       | Type  | Notes                         |
|-------------|-------|-------------------------------|
| `prx_id`    | str   | Primary key                   |
| `tuf_id`    | str   | FK → TUF                      |
| `symbol`    | str   | `▲` / `●` / `■` / `◆`        |
| `color`     | str   | `RED`/`YELLOW`/`GREEN`/`BLUE` |
| `intensity` | float | `abs(confidence-0.5)*scale`   |
| `scale`     | float | Multiplier (default: 2.0)     |

---

## Perception Mapping (COLOR & SYMBOL)

| Confidence | Symbol | Color  | Meaning             |
|:----------:|--------|--------|---------------------|
| 1.0        | ▲      | RED    | FORCE / SYSTEM      |
| 0.5        | ●      | YELLOW | UNCERTAIN / HUMAN   |
| 0.0        | ■      | GREEN  | STABLE / RESULT     |
| other      | ◆      | BLUE   | EXTERNAL (in-between)|

**Intensity formula:** `abs(confidence - 0.5) * scale`

---

## Design Rules (from W3 spec)

- **Process must complete** — no mid-run interruption (`no_interrupt`).
- **State is observation only** — `0 / 0.5 / 1` is for learning, not deciding.
- **XIZ is immutable after creation** in `test`/`prod` environments.
- **Action must answer:** "Why is this action taken based on observed reality?"
- **PRX is derived only** — it is the visual signaling output, not a decision node.
