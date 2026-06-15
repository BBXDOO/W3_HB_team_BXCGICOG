# Cross-X

Cross-X is the W3 ecosystem cross-point coordinator.

It is **not** a bug hunter. It gathers the relevant systems at one cross point so
W3 can improve the working method:

```text
Intent
→ W3-API shape
→ W3Lgu five-line packet
→ E-CS immutable event handoffs
→ PX position pointer
→ W3DB append envelope
→ EP_SIGNAL preview
→ Human Review / Governance Gate
```

Default behavior is plan-only and non-mutating. Cross-X does not execute MPCP,
persist W3DB records, mutate EP_SIGNAL payloads, or approve source truth.

W3Lgu packets carry the E-CS `CHAIN_ID`, planned event state, and an explicit
`EXECUTE_ALLOWED:false` signal. E-CS then expands the configured system order
into traceable records; it coordinates handoffs but does not run the systems.

## Code

- `cross_x/core.py` — immutable request/plan contracts and `build_cross_x_plan`
- `cross_x/event_chain.py` — immutable E-CS event and chain contracts
- `config/cross_system.json` — Cross-X ecosystem policy
- `config/ecosystem.json` — participating systems
- `config/paths.json` — canonical subsystem paths
