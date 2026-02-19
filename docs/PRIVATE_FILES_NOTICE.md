> ⚠️ **[PRIVATE REQUIRED]** — The following files in this `docs/` directory are designated **private** per `mirror.policy.json` and must NOT be mirrored to the public GitHub Pages site or shared externally:

| File | Reason |
|------|--------|
| `agent.profile.json` | AI agent behavior profiles and context scope definitions |
| `rules.json` | Authority model, boundary rules, token policy |
| `system.json` | System owner, operation mode, AI behavior configuration |
| `snapshot.json` | Baseline system state snapshot |
| `version.policy.json` | Internal versioning rules and update authority |

**Public files** (safe to mirror): `index.json`, `index.md`, `protocol.md`, `context.map.json`, `state.json`

See `mirror.policy.json` for the authoritative split.  
**Authority:** BBX19
