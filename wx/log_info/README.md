# BOX Log-Info

`requests.jsonl` and `creations.jsonl` are append-only audit surfaces for
`create`, `generate`, `borrow`, or `export` events. Reading/studying a reference
is not logged. BOX runtime code never appends these files; an authorized human
or separately reviewed tool must do so explicitly.
