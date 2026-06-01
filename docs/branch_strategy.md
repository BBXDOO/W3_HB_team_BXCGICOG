# W3 Branch Strategy

This document defines how W3 keeps active development safe while the public surface remains calm. It is an orientation guide for humans and agents; it does not replace registry, protocol, or source-code truth.

## Operating principle

**Registry / protocol / source code = truth.**

**Config = orientation map.**

Docs explain the operating model, but implementation authority stays in the registered runtime, protocol contracts, and reviewed source code.

## Branch roles

| Branch / pattern | Role | Rule |
|---|---|---|
| `refactor/v0.2` | Active W3HBT integration base | Target PRs here while ecosystem work is in progress. |
| `work`, `codex/*`, `feature/*` | Implementation branches | Build small, test, and open PRs into `refactor/v0.2`. |
| `release/*` | Public snapshot candidate | Use only after Human Review and Governance Gate approval. |
| `main` | Public-facing stable surface | Do not use for active integration work; update only through approved public release flow. |

## Truth hierarchy

1. **Registry truth** — module registries define discoverable roles, routing, and ownership.
2. **Protocol truth** — W3Lgu, PX, EP_SIGNAL, W3DB append contracts define cross-system language and boundaries.
3. **Source-code truth** — executable code and tests define current behavior.
4. **Config orientation** — `config/` maps paths, modes, runtime defaults, and cross-system routing hints.
5. **Docs orientation** — documents explain intent, process, and public/private boundaries.

If these disagree, fix the lowest-risk orientation layer first, then update tests and source only through review.

## PR path

```text
Human intent
  -> request / plan
  -> implementation branch
  -> tests + trace evidence
  -> PR into refactor/v0.2
  -> Human Review
  -> Governance Gate
  -> merge or revise
```

No AI self-merge. No bypassing Human Review. No bypassing Governance Gate.

## Cross-system change rule

Any change that crosses W3-API, Cross-X, W3Lgu, PX, W3DB, EP_SIGNAL, Hospitication, IGET, or module registries must be treated as a **Cross-X ecosystem change**.

For Cross-X changes:

- Start in `observe` or `plan` mode unless a human explicitly approves execution.
- Preserve source truth; do not rewrite W3DB, MPCP, EP_SIGNAL, or protocol history.
- Prefer append-only envelopes and deterministic IDs.
- Include tests for idempotency, traceability, and non-mutation.
- Update `config/` only as an orientation map for paths, systems, and defaults.

## Minimal Definition of Done

A branch is ready for review when:

- The intent is clear and scoped.
- Runtime/protocol/source changes are covered by tests.
- Config changes only orient the system and do not claim authority.
- Docs explain human impact and boundary changes.
- Cross-system flows remain traceable and append-only where persistence is needed.
- The PR states what was tested and what still requires human judgment.
