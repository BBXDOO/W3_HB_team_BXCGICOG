# W3DB Setup Guide

## Overview

W3DB is the in-process database layer for the W3 execution model.  It implements
the five-domain relation flow described in `knowledge/W3MEMORIEA/W3memoriea.md`:

```
INPUT → XIZ → (PROCESS) → TUF → FBD → WHB → PRX
```

| Domain | File | Purpose |
|--------|------|---------|
| XIZ | `.xiz` | Immutable execution trace |
| TUF | `.tuf` | Process state snapshot (observation) |
| FBD | `.fbd` | Failed boundary detection |
| WHB | `.whb` | Contextual law / LINE 3 patch |
| PRX | `.prx` | Derived perception output |

---

## Environment Variables

| Variable | Default | Values | Purpose |
|----------|---------|--------|---------|
| `W3DB_ENV` | `dev` | `dev`, `test`, `prod` | Active environment |
| `W3DB_STORE_BACKEND` | `memory` | `memory` | Storage backend |
| `W3DB_STORE_PATH` | `data/w3db` | any path | JSON backend path (future) |
| `W3DB_LOG_LEVEL` | `DEBUG` | `DEBUG`, `INFO`, `WARNING` | Log verbosity |
| `W3DB_FLOW_AUTO` | `1` | `1`/`0`, `true`/`false` | Auto-run flow on XIZ create |
| `W3DB_PRX_SCALE` | `2.0` | float | PRX intensity scale |

Load the config in code:

```python
from src.w3db.config import load_config
cfg = load_config()
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the flow (programmatic)

```python
from src.w3db.flow import run_flow_from_input

result = run_flow_from_input(
    cix_id="CIX-001",
    action="Checked patient",
    result="Stable",
    confidence=0.72,   # 0.0–1.0; drives TUF state + PRX intensity
)

print(result.state)               # 0.5 (uncertain)
print(result.deviation_detected)  # True → FBD + WHB were created
print(result.prx["symbol"])       # ●
print(result.prx["color"])        # YELLOW
```

### 3. Access individual domains

```python
from src.w3db.crud import xiz, tuf, fbd, whb, prx

all_xiz = xiz.list_all()
one_tuf = tuf.read("TUF-001")
fbd.update("FBD-001", impact="critical")
```

---

## State Mapping

| Confidence Range | TUF State | PRX Symbol | PRX Color | Meaning |
|-----------------|-----------|-----------|-----------|---------|
| ≥ 0.8 | 1.0 | ▲ | RED | Force / True |
| 0.4 – 0.8 | 0.5 | ● | YELLOW | Uncertain |
| < 0.4 | 0.0 | ■ | GREEN | Stable / Result |

`intensity = abs(confidence - 0.5) × scale`

---

## Running Tests

```bash
# CRUD unit tests
python SYSTEM/TESTS/w3db/test_crud.py

# Flow integration tests
python SYSTEM/TESTS/w3db/test_flow.py

# Full CI suite
python tools/w3_agent_ci.py
```

---

## Relation Flow Rules

1. **Process must complete** — no interrupts mid-run.
2. **State ≠ Decision** — TUF state values (0 / 0.5 / 1) are for observation only.
3. **Failure = Boundary** — any state ≠ 1.0 triggers FBD + WHB creation.
4. **XIZ is immutable** — once written, an execution trace cannot be updated.
5. **PRX is derived only** — perception output is always computed from TUF; never set directly.
6. **Action must answer "why"** — WHB law captures the reason behind each corrective action.

---

## Source Layout

```
src/w3db/
├── __init__.py       — package docstring
├── config.py         — environment / integration config loader
├── models.py         — XIZ, TUF, FBD, WHB, PRX dataclasses
├── store.py          — in-memory dict store (reset_store for tests)
├── flow.py           — relation flow engine (run_flow / run_flow_from_input)
└── crud/
    ├── __init__.py
    ├── xiz.py        — create / read / list_all / list_by_tuf
    ├── tuf.py        — create / read / update / list_all / list_by_cix
    ├── fbd.py        — create / read / update / list_all / list_by_tuf
    ├── whb.py        — create / read / update / list_all / list_by_fbd
    └── prx.py        — create / read / list_all / list_by_tuf

SYSTEM/TESTS/w3db/
├── test_crud.py      — per-domain CRUD unit tests
└── test_flow.py      — end-to-end relation flow integration tests
```
