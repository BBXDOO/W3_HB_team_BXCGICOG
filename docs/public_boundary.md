# W3 Public Boundary

This document defines what may safely face the public and what should remain inside active W3HBT development. It is an orientation guide, not a replacement for source-code, registry, or protocol truth.

## Boundary principle

W3 can be open and welcoming without exposing unfinished operational internals. Public space should explain purpose, philosophy, stable entry points, and approved releases. Active integration space may contain drafts, cross-system experiments, agent workspaces, and review-only coordination artifacts.

## Content labels

| Label | Meaning | Default location |
|---|---|---|
| `PUBLIC` | Safe for README, GitHub Pages, and public announcements | `main`, approved release snapshots |
| `INTERNAL` | Active development, cross-system coordination, or operational detail | `refactor/v0.2`, implementation branches |
| `REVIEW` | Potentially public but requires Human Review first | PRs, release candidates |
| `EXPERIMENTAL` | Prototype or learning artifact; not a promise of stable behavior | feature branches, module workspaces |

## Public-safe material

The public boundary may include:

- High-level W3 philosophy and welcome text.
- Stable project map and navigation.
- Approved module names and non-sensitive roles.
- Public documentation for using released features.
- GitHub Pages / PWA assets that do not expose private operational state.
- Release notes after Human Review and Governance Gate approval.

## Keep internal by default

Keep these inside active development unless explicitly approved:

- Draft governance decisions and unresolved disputes.
- Raw agent requests, private workspace notes, and unfinished analysis.
- Operational internals that could confuse public users if read out of context.
- Credentials, tokens, secrets, private API keys, environment-specific endpoints, or private account details.
- Unreviewed Cross-X plans that touch W3DB, MPCP, EP_SIGNAL, PX, W3Lgu, or module registries.
- Any file that could be interpreted as source truth before review.

## Relationship to truth layers

- **Registry / protocol / source code = truth.**
- **Config = orientation map.**
- **Docs = explanation and governance memory.**

Public docs should never claim a behavior that the registry, protocol, or source code does not support. Config should never be used to override source truth; it should point humans and agents toward the correct systems, paths, and defaults.

## Public release flow

```text
Active work on refactor/v0.2
  -> reviewed PRs
  -> release candidate / public summary
  -> Human Review
  -> Governance Gate
  -> approved public update
  -> main / GitHub Pages when appropriate
```

The `main` branch is treated as a public-facing stable surface, not the daily integration target.

## Public boundary checklist

Before moving content public, verify:

- It is understandable without private context.
- It does not expose secrets or private operational details.
- It does not overstate experimental runtime behavior.
- It matches registry, protocol, and source-code truth.
- It has passed Human Review and Governance Gate when it affects governance, identity, protocol, or cross-system behavior.
