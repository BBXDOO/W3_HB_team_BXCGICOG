# Duplication Tracker

## Active duplication findings

| Area | Duplicate/Overlap | Decision | Owner | Status |
|---|---|---|---|---|
| Module loader runtime adapters | The hyphenated and singular-underscore loaders duplicated routing behavior | Consolidated into `core/modules_loader/router.py`; routing data remains canonical in `modules/registry.json` | platform | resolved |
| P1-P3 plan references in architecture + roadmap | Architectural summary and detailed plan overlap by design | Keep both; architecture links to roadmap detail | governance | resolved |

## Notes
- This file is the single running list for intentional/unintentional duplication.
