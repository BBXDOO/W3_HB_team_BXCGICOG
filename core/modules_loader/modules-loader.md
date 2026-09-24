# W3 Modules Loader

`core/modules_loader` is the Python-importable runtime adapter for W3 module
routing. It does not own registry, manifest, or identity data.

## Ownership

- `core/modules_loader/router.py` loads routing from the canonical
  `modules/registry.json` registry.
- `modules/<name>/module.json` is the canonical runtime manifest for a module.
- `core/identity/profiles/*.idp.json` contains runtime IDP profiles.
- `core/identity/idp-schema.json` defines the IDP contract.

The former hyphenated and singular-underscore loader trees were retired so all
Python imports use this valid, single package name without coupling unrelated
data ownership to the adapter.
