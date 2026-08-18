# File.void

```txt
┌──────────────────────────────────────────────┐
│ File.void                                    │
├──────────────────────────────────────────────┤
│ [/]                                          │
│ unresolved transmissive state                │
│                                              │
│ env : [File.void + lib]                      │
│                                              │
│ persist  → preserve source continuity        │
│ transfer → runtime transmission              │
│ resolve  → contextual resolution             │
│ manifest → temporary artifact emergence      │
│ return   → restore unresolved state          │
│                                              │
│ [/] : ~ {manifest}                           │
│                                              │
│ env : [File.void + pdf.lib]                  │
│ → temporary PDF manifestation                │
│ → source remains unresolved                  │
│                                              │
│ :/ SAVE → persist manifestation externally   │
│ :/ COPY → duplicate manifestation state      │
│                                              │
│ File.void does not store artifacts.          │
│ It preserves the ability for form to emerge. │
└──────────────────────────────────────────────┘
```

## Runtime package

Concept docs stay in `protocol/Files.void/` because `File.void` is the W3 concept name.
The importable Python tool lives in `protocol/files_void/`.

```python
from protocol.files_void import file_void_tool

result = file_void_tool(
    action="manifest",
    source_ref="BOX:CROSS_L_BLOCK",
    source_body="return {state='pass'}",
    env="lua.env",
    lib="lua.lib",
    artifact_type="lua",
    mpcp_task="manifest_cross_code",
)
```

## MPCP / Blueprint adapter

MPCP or Blueprint-style contexts can call File.void through:

```python
from protocol.mpcp.adapter.file_void_tool import call_file_void_tool, build_file_void_operation
```

- `call_file_void_tool(context)` accepts KEY:VALUE-style context dictionaries.
- `build_file_void_operation(action)` returns an operation callback compatible with `protocol.mpcp.lib.Pillar`.

## Boundary contract

- File.void is a staging / manifestation layer only.
- File.void may manifest, copy, release, or create a persistence handoff record.
- File.void must not write final storage directly.
- `:/ SAVE` means `persist_handoff`, not direct write.
- `[/] != artifact` remains an invariant.
- Source truth must remain unchanged.
