# CROSS-X / W3Lgu / Condien Relation Anchor

Status: active reference  
Scope: MPCP relation guide  
Mutation: false  
Runtime: none

## Purpose

This file anchors the missing cross-reference between MPCP, Cross-X, W3Lgu,
and Condien after the protocol migration.

MPCP does not own Cross-X logic, W3Lgu runtime, or Condien implementation.
MPCP must still be able to locate them, reason about their relation, and use
existing tests as reference cases without turning the relation into execution
authority.

```text
MPCP
  ├─ references Cross-X for cross-point coordination
  ├─ references W3Lgu for packet / meaning transport
  ├─ references Condien for meaning / state / context shape
  └─ remains governed by Paper / ROT / Modew boundaries
```

## Canonical locations

```text
Cross-X logic:
  cross_x/

Cross-X W3Lgu test case:
  tests/test_cross_x_config.py

W3Lgu protocol:
  protocol/w3lgu/

W3Lgu PX / append flow:
  protocol/w3lgu/px.py
  src/w3db/append_flow.py

Condien implementation:
  src/core/condien.py

Condien / Blueprint MPCP test:
  protocol/mpcp/test_condien_blueprint.py
```

## Existing test case

`tests/test_cross_x_config.py` is the current executable anchor for the
Cross-X → W3Lgu → PX → W3DB append envelope → EP_SIGNAL preview chain.

It checks that a Cross-X plan can produce:

```text
W3-API intent
→ W3Lgu five-line packet
→ Event chain
→ PX anchor
→ W3DB append envelope
→ EP_SIGNAL preview
→ process trace
→ system audit
```

This test may be reused as a baseline case when checking whether future MPCP
adapter work still respects Cross-X and W3Lgu boundaries.

## Relation rules

### 1. Cross-X is a coordinator, not an executor

Cross-X may build a plan, chain, audit, PX anchor, append envelope, and signal
preview.

Cross-X must not execute MPCP Modew, mutate W3DB truth, or approve source truth
by itself.

```text
Cross-X = plan / coordinate / trace
MPCP    = operational structure / Modew boundary
```

### 2. W3Lgu is meaning transport, not final truth

W3Lgu carries compact meaning through a readable packet. It may produce syntax,
state, and signal-ready structure, but it must not decide final truth alone.

```text
W3Lgu = packet / meaning / event language
Truth = declaration + memory + traceable evidence
```

### 3. Condien is context shape, not storage-only data

Condien is the adaptive meaning/state/context layer used by MPCP concepts. It
is not a plain data bag.

```text
Condien = meaning / state / context / continuity / layer access
```

### 4. MPCP keeps the boundary

MPCP may reference Cross-X, W3Lgu, and Condien, but adapter work must stay
behind explicit review and governance gates.

```text
No adapter may grant itself execution authority.
No relation file may become runtime execution.
No test case may be used to bypass Paper / ROT / Modew boundaries.
```

## Safe validation commands

Use these commands to check the current relation without activating runtime
execution:

```bash
python -m pytest tests/test_cross_x_config.py tests/test_file_void_tool.py -q
python -m pytest protocol/mpcp/test_condien_blueprint.py -q
python -m compileall cross_x protocol/w3lgu src/core protocol/mpcp -q
```

## Not included here

This file intentionally does not define:

```text
MPCP adapter execution
Modew runtime call
truth mutation
W3DB persistence
approval authority
```

Those belong in separate reviewed work after the return contract and governance
boundary are stable.

## One-line summary

```text
MPCP does not contain Cross-X / W3Lgu / Condien, but it must keep a clear,
non-executing reference path to them.
```
