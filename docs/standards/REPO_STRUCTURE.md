# Repository Structure Standard

## Canonical folders
- `core/` — runtime/core logic
- `modules/` — module definitions and module-local assets
- `tools/` — operator scripts
- `docs/` — user/developer/governance docs
- `SYSTEM/TESTS/` and `iget/tests/` — test suites
- `knowledge/` — durable notes and session learnings

## Placement rules
- New operational docs go under `docs/` with a clear section folder.
- New automation scripts go under `tools/` unless they are test-only helpers.
- Module-specific artifacts remain under that module root.
