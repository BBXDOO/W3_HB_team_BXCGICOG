# Cross-X Ecosystem Coordination

Cross-X is the W3 cross-system coordination layer. It exists to bring related
systems to the same cross point so W3 can improve the way work flows through the
ecosystem. It is not a bug hunt and not an execution authority.

## Chain

```text
Human / Agent intent
→ Cross-X plan
→ W3Lgu five-line packet
→ REDR / PSP2 / DTML process trace
→ PX position anchor
→ W3DB append envelope
→ EP_SIGNAL preview
→ EP_SIGNAL:Rytm pulse preview
→ Human Review + Governance Gate
```

## ENV config

The `config/` folder is the runtime orientation map:

- `config/environment.json` — top-level runtime status and compatibility
- `config/ecosystem.json` — systems that participate in Cross-X
- `config/cross_system.json` — Cross-X policy and chain
- `config/paths.json` — canonical paths for subsystem discovery
- `config/loader.py` — stdlib loader and validation helpers

Config is not source truth. It links existing truth sources and protocols.

## Guarantees

- Cross-X plans are non-mutating by default.
- PX is a pointer, not execution.
- W3DB append envelopes are append-only intents.
- EP_SIGNAL output is preview-only unless an approved adapter appends it.
- EP_SIGNAL:Rytm is a reversible pulse-cadence preview, not a new truth store.
- REDR/PSP2/DTML/LRC2 process traces are plan-only until an approved adapter persists them.
- Human Review and Governance Gate remain required.

## Example

```python
from cross_x import build_cross_x_plan

plan = build_cross_x_plan(
    source="BBX19",
    intent="align PX and W3DB append flow",
    target="W3DB",
    mode="cross",
)
print(plan.to_dict()["chain"])
```

## EP_SIGNAL:Rytm base

Cross-X now includes `EP_SIGNAL_RYTM` as the rhythm preview layer after the raw
EP_SIGNAL preview. The Rytm packet keeps the same binary digest reversible while
exposing pulse groups, verification, and W3 context tokens for humans and agents.

```text
EP_SIGNAL = compact reversible signal payload
Rytm     = readable pulse-cadence view of that payload
Cross-X  = plan-only coordinator that carries both without mutating source truth
```

The implementation lives in `protocol/EP_SIGNAL/rytm.py` and is referenced by
`cross_x/core.py` when building plan dictionaries.

## REDR / PSP2 / DTML / LRC2 base

Cross-X now carries a `process_trace` built by `core/runtime/process_layer.py`.
REDR packages the intent, PSP2 stamps/routes it, DTML emits a review signal, and
LRC2 prepares an immutable memory preview. The trace is non-mutating by default
and can be persisted only through a separately approved append adapter.
