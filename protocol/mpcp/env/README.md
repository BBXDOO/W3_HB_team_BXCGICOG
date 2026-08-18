# MPCP ENV Boundary

Status: Active Runtime Component
Scope: `Cross-L → ENV → MPCP → Cross-L / W3DB evidence`
Canonical package: `protocol.mpcp.env`

## Responsibility

This package owns the boundary where Cross-L work meets the real execution
environment. It runs before an inbound work unit becomes an MPCP packet and
before an MPCP result is returned to another system.

It does not own the Cross-L language table, W3Lgu grammar, Condien ontology,
Modew implementation, ECS chain, or W3DB storage.

## Flow

```text
Cross-L dispatch envelope
→ validate chain/event/scope/workset
→ inspect current ENV
→ resolve language tag against available runtime or data format
→ read only declared Condien layers
→ create immutable MPCPWorkUnit
→ require a matching temporary ExecutionAgreement
→ execute a registered Modew through MPCP runtime
→ validate canonical MPCP result through ROT
→ return Cross-L contract + W3DB append candidate
```

## Public components

- `probe_environment()` observes platform and available commands. Environment
  variable values are never returned.
- `CrossLEnvironmentBoundary.ingress()` performs all checks before conversion.
- `MPCPWorkUnit.to_mpcp_packet()` is the conversion point into MPCP runtime.
- `ExecutionAgreement` binds borrowed capability to one chain, event and
  boundary. Cross-L cannot approve its own execution.
- `MPCPEnvironmentGateway.execute()` runs only a registered Modew with a
  matching agreement.
- `CrossLEnvironmentBoundary.egress()` enforces the Cross-L return contract and
  produces a non-writing W3DB evidence candidate.

## Boundary laws

1. Language is a role, not authority.
2. ENV is inspected before language/runtime selection.
3. External libraries never control MPCP flow or grammar.
4. Condien access is declared and evaluated through Condien's own access law.
5. An agreement is temporary and event-bound; a boolean flag is insufficient.
6. A missing runtime, return field or agreement becomes a visible WAIT/STOP
   result. Source truth is not discarded.
7. W3DB output from this package is an append candidate, not an implicit write.
8. Pillar construction follows architectural order; operational data flow does
   not inherit that order unless the current Paper/ENV requires it.

## W3Lgu relation

Inbound MPCP packets declare `W3LGU_PROFILE:W3Lgu-MPCP-Runtime` and outbound
returns declare `w3lgu_profile:W3Lgu-Result`. The package does not duplicate the
W3Lgu parser or freeze its future library structure.
