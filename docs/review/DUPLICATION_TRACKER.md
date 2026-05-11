# Duplication Tracker

## Active duplication findings

| Area | Duplicate/Overlap | Decision | Owner | Status |
|---|---|---|---|---|
| `core/module_loader/router.py` vs `core/module-loader/router.py` | Similar router behavior under different paths | Keep `core/module_loader/router.py` as canonical for runtime imports; legacy path to be deprecated in follow-up PR | platform | tracked |
| P1-P3 plan references in architecture + roadmap | Architectural summary and detailed plan overlap by design | Keep both; architecture links to roadmap detail | governance | resolved |

## Notes
- This file is the single running list for intentional/unintentional duplication.
