# W3-API Cross Proof Before v0.3

## Proof statement

W3-API is locked as a **gateway-only Cross proof** before any v0.3 movement. The `/w3/cross` route accepts an external intent, builds a traceable W3Lgu five-line packet, returns a W3DB append plan, and returns an EP_SIGNAL / RYTM preview. It does **not** execute persistence, rewrite source truth, or mutate W3DB, EP_SIGNAL, MPCP, W3Lgu, or runtime state.

**Required invariant:** `mutated:false`

## Real `/w3/cross` example request

```http
POST /w3/cross
Content-Type: application/json
```

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

## Expected response shape

`id`, `timestamp`, PX identifiers, append-envelope identifiers, and compact signal fingerprints are generated per request. The shape below is the proof contract; values marked with `...` are deterministic from runtime input or request-time identifiers.

```json
{
  "id": "<uuid>",
  "timestamp": "<utc-iso8601>Z",
  "status": "accepted",
  "w3lgu": "MEM:SOURCE:BBX19\nPATCH:MODE:cross\nLAW:TARGET:W3Lgu,CONTRACT:do/not/rewrite/source/truth\nEVENT:INTENT:align/W3Lgu/with/W3DB/and/EP_SIGNAL\nSIGNAL:STATUS:received,TRACEABLE:true",
  "signal": {
    "type": "W3_API_CROSS",
    "source": "BBX19",
    "target": "W3Lgu",
    "mode": "cross",
    "traceable": true,
    "mutated": false,
    "w3db": {
      "mode": "append_plan_only",
      "mutated": false,
      "xiz_hint": "XIZ-API-...",
      "tuf_hint": "TUF-API-...",
      "source": "BBX19",
      "target": "W3Lgu",
      "px": { "px_id": "PX-...", "relation": "w3lgu.cross_reference", "mode": "observe" },
      "append_envelope": { "append_id": "APP-PX-...", "kind": "PX", "confidence": 0.5 }
    },
    "ep_signal": {
      "mode": "preview_only",
      "mutated": false,
      "format": "BIN",
      "ep_signal": "EP_SIGNAL:...",
      "rytm": {
        "mode": "preview_only",
        "mutated": false,
        "rytm_signal": "0/...'W3_API'CROSS'-31//BIN."
      }
    },
    "references": [
      "protocol/w3lgu/RML01.md",
      "docs/integration_guide.md",
      "docs/standards/referencing_standard.md"
    ]
  }
}
```

## Generated W3Lgu five-line packet

```text
MEM:SOURCE:BBX19
PATCH:MODE:cross
LAW:TARGET:W3Lgu,CONTRACT:do/not/rewrite/source/truth
EVENT:INTENT:align/W3Lgu/with/W3DB/and/EP_SIGNAL
SIGNAL:STATUS:received,TRACEABLE:true
```

- `MEM` keeps the request source as compact continuity memory.
- `PATCH` records the gateway mode without executing runtime action.
- `LAW` carries the target plus explicit `CONTRACT` boundary.
- `EVENT` carries the user intent as the event packet.
- `SIGNAL` reports receipt and traceability only.

## W3DB append plan is plan-only

W3-API returns `signal.w3db.mode: append_plan_only` and `signal.w3db.mutated:false`. The PX anchor and append envelope show how a future approved persistence layer would append the observation, but the gateway route does not call a W3DB write path.

## EP_SIGNAL / RYTM preview is preview-only

W3-API returns `signal.ep_signal.mode: preview_only`, `signal.ep_signal.mutated:false`, and a nested `signal.ep_signal.rytm` preview with `mutated:false`. The preview is a compact trace fingerprint of the W3Lgu packet; it is not persisted as EP_SIGNAL truth.

## Gateway-only conclusion

For v0.3 readiness, W3-API remains a Cross Gateway only:

- accepts external intent;
- builds W3Lgu proof packet;
- builds W3DB append plan only;
- builds EP_SIGNAL / RYTM preview only;
- returns references for traceability;
- preserves `mutated:false` across the response.
