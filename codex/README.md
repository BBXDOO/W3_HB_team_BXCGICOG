# Codex — Implementation Agent / Repo Executor

Codex is the W3 implementation agent workspace. Its job is to turn approved
intent and architecture into code, tests, documentation, commits, and PR-ready
changes while preserving W3 source-truth boundaries.

## Role

Codex may execute implementation work on a branch:

- inspect repository structure
- create or update production code
- add tests and deterministic checks
- update documentation
- prepare commits and PR descriptions
- create adapter or gateway layers when cross-system work is needed

Codex does **not** approve truth, merge its own PR, or bypass governance.

## Governance Gate

Every Codex change must remain reviewable and pass:

1. Human Review
2. Governance Gate
3. Existing protocol boundaries
4. Tests / CI checks

## Cross-system policy

Codex treats W3 cross-system work as adapter/gateway work by default:

- W3Lgu: generate trace packets or adapters, not new runtime law without review
- MPCP: bridge through documented adapter contracts only
- W3DB: propose append records; never overwrite source truth
- EP_SIGNAL: encode/decode previews; never mutate original payloads
- IGET: repair tests and CI through branch commits

## Files

- `codex/modules.json` — Codex workspace manifest and boundaries
- `codex/agent.py` — importable helper for deterministic execution packets
- `modules/Codex/module.json` — central module registry entry format
- `core/module-loader/identity/Codex.idp.json` — loader identity profile
- `BBX19/modules/BBX19/idp/IDP-V2.0/Codex-IDP.md` — IDP v2.0 orientation capsule

## Example

```python
from codex import build_execution_packet

packet = build_execution_packet("implement W3-API gateway")
print(packet.w3lgu)
```

The packet is a trace artifact. It does not mutate W3DB, MPCP, EP_SIGNAL, or
any runtime truth store.
