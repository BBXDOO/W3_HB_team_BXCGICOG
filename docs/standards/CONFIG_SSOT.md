# Config SSOT Mapping

## Single Source of Truth Map
- IGET scoring thresholds: `iget/config.py`
- Runtime module routing (legacy runtime path): `core/module_loader/module-registry.json`
- W3-wide module registry: `modules/registry.json`

## Change policy
1. Update SSOT file first.
2. Propagate derived docs/tests after.
3. Record significant config shifts in changelog/review docs.
