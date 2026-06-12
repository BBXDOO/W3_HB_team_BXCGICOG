# G-State Paper — Foundation Standard

## Status

G-State is a permanent W3 foundation layer for shared operational awareness. It is designed for long-lived ecosystem use, not for a single pull request or temporary feature.

G-State is **not**:

- a runtime executor;
- a workflow engine;
- a state-machine replacement;
- a temporary project feature;
- an experimental sandbox.

G-State is:

> A shared awareness layer describing the current operational condition of the ecosystem.

It exists so Humans, Agents, Modews, Papers, Governance systems, and future modules can operate under the same environmental understanding without repeating the same instructions in every request.

## Core distinction

Paper answers:

> What should be done?

G-State answers:

> What condition are we currently operating under?

Example:

```text
TASK:create_report
```

is Paper/task intent.

```text
GSTATE:AUDIT
```

is ecosystem environment.

## Responsibilities

G-State may:

- describe ecosystem condition;
- provide operational awareness;
- expose environment intent;
- assist governance decisions;
- guide interpretation;
- help humans and agents notice limitations, dependencies, consequences, and known incompatibilities before acting.

G-State must not:

- execute tasks;
- override ROT;
- override Paper;
- override Result;
- mutate runtime directly;
- replace MPCP, Condien, Modew, W3Lgu, W3DB, EP_SIGNAL, Hospitication, or IGET;
- claim authority that belongs to Human Review, Governance Gate, registry truth, protocol truth, or source-code truth.

## Initial canonical states

These first-generation states are environment conditions, not workflow steps.

| State | Condition described | Not a command to |
|---|---|---|
| `GSTATE:BUILD` | The ecosystem is oriented toward construction, integration, or implementation. | Execute changes without review. |
| `GSTATE:AUDIT` | The ecosystem is oriented toward inspection, proof, verification, or boundary review. | Block or approve by itself. |
| `GSTATE:RESEARCH` | The ecosystem is oriented toward learning, comparison, source reading, or design discovery. | Convert exploration into runtime behavior. |
| `GSTATE:RECOVERY` | The ecosystem is oriented toward repair, rollback planning, continuity, or non-destructive restoration. | Rewrite truth history. |
| `GSTATE:MAINTENANCE` | The ecosystem is oriented toward cleanup, dependency care, tests, documentation alignment, or stability. | Hide risks or skip review. |
| `GSTATE:LEARNING` | The ecosystem is oriented toward reflection, knowledge capture, and improving future decisions. | Replace evidence with emotion or memory alone. |

A G-State can be attached to a request, report, module handoff, or governance note as awareness metadata. It does not turn that artifact into an executor.

## Integration mapping

| System | Existing responsibility | G-State relationship | Boundary |
|---|---|---|---|
| `ROT` | Law, boundary, and truth protection. | G-State can describe the operating condition under which ROT is consulted. | G-State never overrides ROT. |
| `Paper` | Declares what should be done. | G-State provides environment context around the Paper. | G-State never replaces Paper intent. |
| `Modew` | Performs a defined unit of work according to its own structure and allowed inputs. | G-State can help a Modew interpret the surrounding condition before acting. | G-State is not a Modew and does not execute Modew logic. |
| `Condien` | Meaning, context, adaptation, and interpretation layer. | G-State can provide a stable condition label that Condien may consider. | G-State does not replace Condien's meaning/context role. |
| `W3Lgu` | Compact language/protocol shape for cross-system packets and five-line law. | G-State may appear as a readable environment declaration or metadata. | G-State does not alter W3Lgu grammar or runtime contract. |
| `IGET` | Governance/intelligence evaluation and trace support. | G-State can help IGET understand the environment being evaluated. | G-State does not become an IGET score or proof by itself. |
| `Hospitication` | Read-only structural health observer and recovery proposal source. | G-State can label whether the ecosystem is in audit, recovery, maintenance, or learning condition. | G-State does not mutate health reports or recovery actions. |

## Relationship to v0.2 truth layers

- **Registry / protocol / source code = truth.**
- **Config = orientation map.**
- **Docs = explanation / public boundary / branch strategy.**

G-State belongs to the awareness/governance explanation layer until an explicitly reviewed future adapter attaches it to a runtime or registry contract. Even then, it remains an awareness layer and does not gain execution authority.

## Awareness law

**Awareness is responsibility.**

Participants should consider the current G-State before execution, especially:

- limitations;
- dependencies;
- consequences;
- known incompatibilities;
- review requirements;
- public/private boundary;
- whether the current task is build, audit, research, recovery, maintenance, or learning.

Awareness does not grant authority.

Awareness creates responsibility.

A participant who knows the ecosystem is in `GSTATE:AUDIT` should avoid acting as if it were in unrestricted build mode. A participant who knows the ecosystem is in `GSTATE:RECOVERY` should preserve evidence and avoid rewriting history. The state informs conduct; it does not approve execution.

## Future extension hooks

The following namespaces are reserved for future awareness systems. They are structural reservations only; this paper does not implement them.

| Hook | Reserved purpose |
|---|---|
| `GSTATE_META` | Metadata about provenance, timestamp, owner, confidence, compatibility, or review status. |
| `GSTATE_PROFILE` | Profiles for BFLC, ethics, relationship memory, cross-agent interpretation, or ecosystem-specific awareness posture. |
| `GSTATE_FEEDBACK` | Feedback loops for governance learning, compatibility review, human impact, and future agent cooperation. |

These hooks allow future BFLC, awareness, ethics, governance, compatibility, relationship-memory, and cross-agent understanding systems to attach without structural redesign.

## Stability rule

Design for ten years, not for the next pull request.

Structure must remain stable.

Meaning may evolve.
