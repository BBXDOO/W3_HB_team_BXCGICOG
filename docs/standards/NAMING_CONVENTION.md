---
AM_TYPE: II
ROLE: ARCHITECTURE_GUIDANCE
GROUP: BUILD
DERIVED_FROM: []
---

# Naming Convention (Repo-wide)

## Rules
- Python files/modules: `snake_case.py`
- Markdown docs: `UPPER_SNAKE_CASE.md` for canonical standards, otherwise `kebab-case.md`
- JSON/YAML config keys: `snake_case`
- Test files: `test_<unit>.py`

## Directory naming
- Runtime code: `core/`, `modules/`, `tools/`
- Documentation: `docs/`
- Experiments/sandbox: keep outside production paths and label clearly
