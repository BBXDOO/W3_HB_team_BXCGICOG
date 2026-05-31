# modules/Codex

Central module workspace for Codex inside the W3 module registry.

Codex owns implementation execution artifacts only. It does not own source truth,
review authority, governance authority, or merge authority.

## Zones

- `requests/` — incoming implementation requests
- `plans/` — implementation plans before edits
- `patches/` — patch notes and branch summaries
- `reports/` — verification reports
- `logs/` — execution logs

## Handoff

Every completed implementation must be handed to:

1. Human Review
2. Governance Gate
3. Relevant verifier, usually Gemini or Copilot-Gm depending on risk
