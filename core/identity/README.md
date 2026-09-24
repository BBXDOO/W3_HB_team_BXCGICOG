# W3 Runtime Identity Profiles

This directory is the canonical home for runtime-compatible W3 IDP data.
Identity contracts are independent from module routing and therefore do not
belong to the `core.modules_loader` adapter.

- `idp-schema.json` preserves the W3-IDP v1 contract during migration.
- `profiles/<module>.idp.json` contains one runtime identity profile per module;
  some transitional profiles predate the complete v1 schema and remain
  runtime-readable while their contract upgrade is handled separately.
- `core.modules_loader` resolves tasks and module manifests from `modules/`.
- Runtime components that require full IDP metadata read it from `profiles/`.

Historical reports may retain paths that were valid when those reports were
created. Active runtime code and configuration must use this directory.
