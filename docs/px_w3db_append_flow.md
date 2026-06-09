# PX / W3DB Append Flow

PX is a small position-exchange layer for W3 cross-system work. It gives W3Lgu,
W3-API, MPCP, EP_SIGNAL, Hospitication, and W3DB a shared way to point at a
source meaning without rewriting that source.

## Contract

`protocol/w3lgu/px.py` defines `PXAnchor`:

- `source` — where the meaning came from
- `target` — where the meaning is being routed
- `subject` — compact intent/task summary
- `relation` — why the pointer exists
- `payload` — source snapshot for traceability
- `references` — relative paths back to governing docs

PX is immutable. It is a pointer, not a command.

## Append Flow

`src/w3db/append_flow.py` defines an append envelope and result:

1. Build an immutable `AppendEnvelope`.
2. Derive deterministic XIZ/TUF/FBD/WHB/PRX IDs.
3. Append through the existing W3DB `run_flow` API.
4. If already appended and idempotency is enabled, return the existing trace IDs.

The append flow never deletes or rewrites existing W3DB records.

## W3-API Use

`w3_api/adapters/w3db_adapter.py` now includes a PX append plan in the
`POST /w3/cross` response. The gateway still does not persist state by default;
it returns the exact envelope that a later approved persistence layer can append.

## Governance

- PX does not diagnose.
- PX does not execute.
- PX does not approve truth.
- W3DB append writes are observation records only.
- Protocol mutation still requires Human Review and Governance Gate.
