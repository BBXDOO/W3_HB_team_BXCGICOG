# RML01 — W3Lgu Runtime Minimal Law

> Reconstruction note: the requested `protocol/w3lgu/RML01.md` source file was
> not present in this checkout. This document anchors the implementation to the
> existing W3Lgu README and papers while preserving the missing concept the user
> called “กฎ 5 บรรทัด”.

## Purpose

RML01 defines the minimal W3Lgu runtime contract: one compact language unit that
humans can read, machines can parse, and W3 systems can replay without hidden
meaning.

## Reading law

1. Read left to right.
2. Read top to bottom.
3. One line is one event or one event sequence.
4. Uppercase keys are command/control fields.
5. Lowercase values are data/state unless explicitly symbolic.

## Five-line operating law

A complete W3Lgu operating unit has exactly five lines:

```text
MEM:...
PATCH:...
LAW:...
EVENT:...
SIGNAL:...
```

| Line | Role | Meaning | Must not become |
| --- | --- | --- | --- |
| 1 | `MEM` | System reserve / compact continuity memory | runtime log dump |
| 2 | `PATCH` | Training patch / protective example slot | permanent truth rewrite |
| 3 | `LAW` | Strict law zone / boundary condition | UI decoration |
| 4 | `EVENT` | Actionable event packet | hidden multi-step script |
| 5 | `SIGNAL` | Visible state/perception output | authority over truth |

## Grammar law

Canonical packets use explicit `KEY:VALUE` fields:

```text
TASK:sync,MODE:auto,ENV:mobile,STATE:ready
```

Flexible Line C input may omit commas when meaning is obvious, but normalized
output must restore explicit separators:

```text
TASK:sync MODE:auto STATE:ready
```

normalizes to:

```text
TASK:sync,MODE:auto,STATE:ready
```

## Symbol law

- `:` assigns KEY to VALUE.
- `;` separates event sequences.
- `.` ends a command/event.
- `'` splits shared-space/shared-data values.
- `,` splits raw data fields or packet pairs.

## Signal law

Signals are perception/state outputs. They are not execution authority and must
not overwrite result truth. `CONF:0.5` means observe or warn, not final success.

## Boundary law

W3Lgu normalizes structure, not truth. Adapters may enrich with traceable
metadata; runtime may emit derived signals; neither may mutate source payloads.
