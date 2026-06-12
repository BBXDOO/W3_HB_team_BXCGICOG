# BOX Registries

Registries are the machine-readable reference source of truth. Template order
is meaningful: when a caller asks for one suggestion, Engine-Index returns the
first active match in registry order. IDs must be unique and every registered
source path must remain repository-relative and exist under this repository.

`template_registry.schema.json` supplies the portable JSON contract, while
`wx.engine_index` also validates source paths and required front matter.
