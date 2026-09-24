# W3 Modules Loader

`core/modules_loader` is the Python-importable runtime adapter for W3 module
routing and identity metadata.

## Ownership

- `core/modules_loader/router.py` loads routing from the canonical
  `modules/registry.json` registry.
- `modules/<name>/module.json` is the canonical runtime manifest for a module.
- `core/modules_loader/identity/*.idp.json` contains the legacy-compatible IDP
  profiles still consumed by lifecycle review code.
- `core/modules_loader/idp-schema.json` defines the schema for those IDP files.

The former hyphenated and singular-underscore loader trees were consolidated
here so all Python imports use this valid, single package name.
