# protocol.files_void

Importable runtime/tool package for the W3 `File.void` concept.

Concept documents remain in `protocol/Files.void/`.
Python code lives here because dotted directory names are not importable as normal packages.

## Role

`protocol.files_void` is a bounded staging layer:

- create an unresolved File.void record
- resolve it against an ENV/lib pair
- manifest a temporary artifact representation
- copy active manifestation state
- create a persistence handoff record
- release the manifestation

It does **not** write final artifacts, mutate source truth, or approve persistence.

## Tool call

```python
from protocol.files_void import file_void_tool

result = file_void_tool(
    action="manifest",
    source_ref="BOX:CROSS_L_BLOCK",
    source_body="return {state='pass'}",
    artifact_type="lua",
    env="lua.env",
    lib="lua.lib",
    mpcp_task="manifest_cross_code",
)
```

## MPCP adapter

```python
from protocol.mpcp.adapter.file_void_tool import call_file_void_tool

result = call_file_void_tool({
    "TASK": "manifest_cross_code",
    "ACTION": "manifest",
    "SOURCE_REF": "BOX:CROSS_L_BLOCK",
    "SOURCE_BODY": "return {state='pass'}",
    "ARTIFACT_TYPE": "lua",
})
```
