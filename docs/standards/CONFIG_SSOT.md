# Config SSOT Mapping

## Single Source of Truth Map
- IGET scoring thresholds: `iget/config.py`
- Runtime module routing and W3-wide module registry: `modules/registry.json`
- Importable runtime routing adapter: `core/modules_loader/router.py`

## Change policy
1. Update SSOT file first.
2. Propagate derived docs/tests after.
3. Record significant config shifts in changelog/review docs.
