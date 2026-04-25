# Agent Memory Protocol

Every agent must read memory before work and write summary after work.

## Scope

Applies to: Cast, ChatGPT, Gemini, Claude, Copilot, DeepSeek, Grok, and all future W3 agents.

## Rules

### Priority Read Rule (start of session)
1. Read `Cast/context/session_summary.md` before beginning any work.
2. Restore from the latest entry:
   - latest decisions
   - unfinished tasks
   - known risks
   - last modified modules

### Mandatory Write Rule (end of session)
1. Append a new entry to `Cast/context/session_summary.md` after every productive session.
2. Never overwrite or delete previous entries.
3. Use the template defined at the top of `session_summary.md`.

### Archive Rule (overflow management)
- If `Cast/context/session_summary.md` exceeds 1000 lines:
  1. Move the oldest entries to `Cast/context/archive/session_summary_01.md`.
  2. If that archive file also exceeds 1000 lines, increment the suffix (e.g. `_02.md`).
  3. Keep the most recent entries in the main file.

## Status

protocol active: YES
