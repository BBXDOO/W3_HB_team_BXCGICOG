# Cross-X Ecosystem Coordination

Cross-X is the W3 cross-system coordination layer. It exists to bring related
systems to the same cross point so W3 can improve the way work flows through the
ecosystem. It is not a bug hunt and not an execution authority.

## Chain

```text
Human / Agent intent
→ Cross-X plan
→ W3Lgu five-line packet
→ PX position anchor
→ W3DB append envelope
→ EP_SIGNAL preview
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
