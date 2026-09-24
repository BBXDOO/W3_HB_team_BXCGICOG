# W3 Modules Loader

`core/modules_loader` is the Python-importable runtime adapter for W3 module
routing. It does not own W3-IDP profiles or their schema.

## Ownership

- `core/modules_loader/router.py` loads routing from the canonical
  `modules/registry.json` registry.
- `modules/<name>/module.json` is the canonical runtime manifest for a module.
- `core/identity/profiles/*.idp.json` contains runtime-compatible IDP
  projections for consumers that require identity/context metadata.
- `core/identity/idp-schema.json` preserves the runtime IDP schema during
  migration.
- Human/session IDP cards and their lineage remain under
  `BBX19/modules/BBX19/idp/`.

The former hyphenated and singular-underscore loader trees were consolidated
into this importable package. Identity data is deliberately kept outside the
loader so routing, module manifests, and IDP/context identity do not collapse
into one ownership boundary.

Historical reports may retain their original paths as evidence.
