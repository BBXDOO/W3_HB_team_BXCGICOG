# W3-API — Cross Gateway

W3-API is the external/agent gateway into the W3 ecosystem. It is intentionally a
**cross gateway**, not a normal CRUD API and not a replacement for W3Lgu, MPCP,
W3DB, EP_SIGNAL, or IGET.

```text
External / AI Agent
        ↓
      W3-API
        ↓
W3Lgu / MPCP / W3DB / EP_SIGNAL / IGET
```

## First endpoint

`POST /w3/cross`

The endpoint:

1. accepts an external intent,
2. converts it into a five-line W3Lgu packet,
3. creates W3DB and EP_SIGNAL trace plans/previews,
4. returns a traceable signal response,
5. does **not** mutate W3DB, MPCP, EP_SIGNAL, IGET, or runtime state.

## Request

```json
{
  "source": "BBX19",
  "intent": "align W3Lgu with W3DB and EP_SIGNAL",
  "target": "W3Lgu",
  "mode": "cross",
  "payload": {
    "contract": "do not rewrite source truth"
  }
}
```

## Response shape

```json
{
  "id": "...",
  "timestamp": "...Z",
  "status": "accepted",
  "w3lgu": "MEM:...\nPATCH:...\nLAW:...\nEVENT:...\nSIGNAL:...",
  "signal": {
    "type": "W3_API_CROSS",
    "traceable": true,
    "mutated": false
  }
}
```

## Local run

```bash
uvicorn w3_api.main:app --reload
```

## Design rule

W3-API normalizes and routes intent. It does not overwrite source truth. Any
future write integration should append derived W3DB records through a reviewed
adapter and keep references back to this gateway signal.

## BOX-assisted Cross-L planning

`POST /w3/cross/plan` accepts the optional boolean
`include_box_suggestion`. When true, the response may include a registered
`suggested_template` from `wx/registry/template_registry.json`. The default is
false, so existing callers retain the original response shape.

```json
{
  "px": "1,1",
  "include_box_suggestion": true
}
```

This is a reference lookup only: no template is copied, no log is appended, no
runtime is executed, and `execution_allowed`/`mutated` remain false.
