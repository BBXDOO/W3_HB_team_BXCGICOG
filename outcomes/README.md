# Outcomes Ledger

## Purpose

This directory stores **observable outcomes, impacts, and evidence** produced by the W3 system — by any module (human or AI). It is intentionally separate from `governance/` (rules) and `versions/` (snapshots) to keep observed facts independent of policy interpretation.

## Principles

- **Evidence-first** — record what was observed and where to verify it, before adding interpretation.
- **Plural ownership** — any module or human contributor may append a record; no single authority owns this ledger.
- **Admit unknowns** — it is better to record an open question than to fabricate certainty.
- **Observed facts vs. notes** — keep the `Observed` section factual; move opinions and context to `Notes`.
- **Non-judgmental** — avoid "right/wrong" framing; describe what happened and its scope.
- **Append-only** — do not edit or delete existing records; add new records to correct or supersede.

## Directory Layout

```
outcomes/
├── README.md              ← this file
├── ledger/                ← timestamped outcome records (one file per event)
│   └── _TEMPLATE__outcome-record.md
└── artifacts/             ← binary or generated evidence files referenced by records
```

## Naming Convention

Ledger files follow the pattern:

```
YYYY-MM-DD_<short-slug>.md
```

- `YYYY-MM-DD` — UTC date of the observation.
- `<short-slug>` — lowercase, hyphen-separated, ≤ 6 words (e.g. `outcomes-system-bootstrap`, `ci-failure-module-x`).

Example: `2026-02-25_outcomes-system-bootstrap.md`

## Referencing Evidence

Prefer permanent links:

| Evidence type | How to reference |
|---|---|
| Commit | GitHub permalink: `https://github.com/BBXDOO/W3_HB_team_BXCGICOG/commit/<sha>` |
| PR / Issue | `https://github.com/BBXDOO/W3_HB_team_BXCGICOG/pull/<number>` |
| File at revision | `https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/<sha>/path/to/file` |
| Command output | Paste inline or store file in `outcomes/artifacts/` and link relatively |
| External artifact | URL + retrieval timestamp |

## How to Add a Record

1. Copy `ledger/_TEMPLATE__outcome-record.md`.
2. Rename using the naming convention above.
3. Fill in all required fields; leave optional fields blank rather than omitting them.
4. Open a PR targeting `refactor/v0.2` (or the current base branch).
5. After merge, update any `[PLACEHOLDER]` evidence links with real URLs.
