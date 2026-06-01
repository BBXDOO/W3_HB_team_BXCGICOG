# W3 ENV Config

`config/` is the W3 runtime orientation map for integration-grade coordination.
It does not replace source-truth systems such as W3DB, W3Lgu, module registries,
or governance docs. It links them so agents can discover the same ecosystem
shape before building Cross-X plans.

## Files

- `environment.json` — top-level runtime status, compatibility, and philosophy
- `ecosystem.json` — systems that participate in Cross-X coordination
- `cross_system.json` — Cross-X policy, chain, and contracts
- `paths.json` — canonical paths to major subsystems
- `loader.py` — stdlib loader/validator for tests and tools

## Boundary

- Config may describe routing and policy.
- Config must not approve truth.
- Config must not replace `modules/registry.json`.
- Config must not mutate W3DB, EP_SIGNAL, MPCP, or W3Lgu runtime state.
