Name : MPCP — Modular Protocol Control Platform  
AM Ⅱ - BUILD : MPCP system architecture, operational model and boundaries  
Log time : 2026-11-22 (date only; time not recorded) ; ID : MPCP-README-001  
≡ Cr8ra - RAMS

## Body — MPCP system definition

**Scope:** This README describes only the `protocol/mpcp/` directory, its architecture, operational model, and local components. Links outside this directory are references, not an extension of its authority.

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - knowledge/philosophy/corevsstructure.md
  - protocol/mpcp/MPCP_ORIGIN.md
DOCUMENT_ID: MPCP-README-001
DOCUMENT_PATH: protocol/mpcp/README.md
SYSTEM: MPCP
STATUS: Active Runtime Foundation
```

**Preserved meaning:** Simple, bounded operational units; clear responsibility; traceable decisions; and separation of system meaning from implementation.

**Authority boundary:** Cross-L classifies language roles but cannot authorize execution. MPCP ENV prepares and scopes context; Modew execution remains subject to external authority and ROT validation. This README documents the model; it does not grant runtime, write, deployment, or approval permissions.

### Original MPCP reference — preserved operational description

MPCP is a lightweight operational system built for clear execution, short communication, and structured control.

MPCP does not depend on heavy schemas during daily use.

Instead, it uses a layered document model:

- Modew = execution units
- Condien = structured data objects
- Rot Paper = primary master paper
- Paper = short operational papers for live tasks

---

Core Philosophy

Use common standards.

Change only the method:

- reduce complexity
- reduce interpretation errors
- improve execution clarity
- keep learning cost low
- support fast operation

---

Core Components

1. Modew

Single-purpose work units.

Examples:

- Input Modew
- Process Modew
- Validation Modew
- Output Modew

Modew should be clear, limited, and reusable.

BaseModew in runtime also supports:

- run memory (history + stats)
- skill registration / usage
- capability checks for role-based execution control

---

2. Condien

Structured system data.

Examples:

- Condien.User
- Condien.Task
- Condien.Runtime
- Condien.Result

Condien stores state, values, and operational objects.

---

3. Rot Paper

Primary system paper.

Used for:

- core rules
- architecture
- boundaries
- standards
- decision principles

Rot Paper may be long and detailed.

It acts as the main reference of the system.

---

4. Paper

Short live documents attached to real tasks, events, or operations.

Used for:

- current step
- temporary rules
- task scope
- exact action request

Paper must be:

- short
- clear
- specific
- bounded

---

5. ENV Boundary

`env/` is the full Cross-L-facing boundary before data enters or leaves MPCP.

It:

- observes platform capability without exposing secret values
- consumes Cross-L language tags and worksets
- resolves available runtime/library bindings in the current ENV
- scopes Condien reads before Modew receives context
- converts accepted work into an MPCP packet
- returns an MPCP/Cross-L result contract and W3DB evidence candidate

Cross-L classifies and governs the inserted language role. MPCP does not own
the Cross-L language table and does not allow a language or library to become
authority over execution.

```text
Cross-L declaration
→ MPCP ENV inspection
→ library/runtime resolution
→ Condien scoped context
→ Modew boundary
→ ROT validation
→ Cross-L return contract
→ W3DB evidence candidate
```

Execution still requires authority outside Cross-L. Cross-L may prepare work;
it cannot approve its own execution.

Examples:

AUTH check login
BUILD fast mode
VALIDATE input only
DEPLOY test branch

---

Operational Model

Rot Paper defines system.
Paper drives action.
Modew executes.
Condien carries data.

---

Why MPCP

Traditional systems often use:

- long schemas
- complex configs
- unclear responsibility
- excessive interpretation

MPCP replaces that with:

- short operational papers
- readable structures
- controlled boundaries
- faster execution flow

---

Platform Direction

Designed for:

- Linux
- Android
- iOS
- Mobile-first systems
- Lightweight runtime environments

---

Runtime Structure

config/      runtime policy and portable capability mapping
env/         Cross-L ingress, ENV probe, Condien scope, MPCP egress
lib/         core/bridge/optional library registry and Pillar
modew/       bounded execution unit base
kernel/      contract, ROT, module relation and validation
runtime/     execution and causal trace
orchestrator/ composed Modew flow
adapter/     external system bridges

---

Status

Active Runtime Foundation



## Movement — directory map and references

### M1 — Items in `protocol/mpcp/`

| Item | Responsibility |
|---|---|
| [README.md](README.md) | This system-level AMS directory map |
| [MPCP_ORIGIN.md](MPCP_ORIGIN.md) | MPCP origin reference and lineage |
| [ROT_PAPER.md](ROT_PAPER.md), [ROT_BASELINE.md](ROT_BASELINE.md) | ROT rules and baseline references |
| [MODEW_PAPER.md](MODEW_PAPER.md), [MODEW_DYNAMIC_CAPABILITY_PAPER/](MODEW_DYNAMIC_CAPABILITY_PAPER/) | Modew concepts and capability documentation |
| [COLOR_STATE.md](COLOR_STATE.md), [COLOR_SYMBOL_PAPER.md](COLOR_SYMBOL_PAPER.md) | Color state and symbol papers |
| [CO_MODULE_LAW.md](CO_MODULE_LAW.md), [CROSS_W3LGU_CONDIEN_RELATION.md](CROSS_W3LGU_CONDIEN_RELATION.md), [EVENT_TEMPLATE_CONDIEN_BRIDGE.md](EVENT_TEMPLATE_CONDIEN_BRIDGE.md) | Module, language, and Condien relation documents |
| [THEORDERMPCP.md](THEORDERMPCP.md), [W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md](W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md), [W3_TERMS_MASTER_PAPER_v2.md](W3_TERMS_MASTER_PAPER_v2.md) | Ordering, architecture, and terminology references |
| [mpcp_pillar.md](mpcp_pillar.md) | MPCP pillar document |
| [config/](config/), [env/](env/), [lib/](lib/) | Runtime policy, ENV boundary, and library registry |
| [modew/](modew/), [kernel/](kernel/), [runtime/](runtime/) | Execution units, validation kernel, and runtime traces |
| [orchestrator/](orchestrator/), [adapter/](adapter/), [schema/](schema/) | Flow composition, external bridges, and schema definitions |
| [case_studies/](case_studies/), [mpcp_blueprint_paper/](mpcp_blueprint_paper/), [mpcp_concept_paper/](mpcp_concept_paper/), [mpcp_lib_paper/](mpcp_lib_paper/) | Local case studies and design papers |
| [mpcp_unified_lgu/](mpcp_unified_lgu/), [w3lgu_integration_paper/](w3lgu_integration_paper/) | Local language integration references |
| [__init__.py](__init__.py), [cooperative_contract.py](cooperative_contract.py), [runtime_sanity_sweep.py](runtime_sanity_sweep.py), [sandbox.py](sandbox.py) | Python entry/contract/validation/sandbox modules |
| [test_agent_mpcp_alignment.py](test_agent_mpcp_alignment.py), [test_condien_blueprint.py](test_condien_blueprint.py) | Local tests |

The entries above are an inventory, not a grant of authority. Read each component's contract before execution.

### M2 — External references

| docs.* | Text link | Relation |
|---|---|---|
| docs.ams | [Architecture Mapping Standard](../../docs/governance/AMS.md) | AM type, lineage and Gradation rules |
| docs.ams-template | [AMS README template](../../docs/box/AMS/AMS_README.txt) | Head / Body / Movement / OWNER / MAKER format |
| docs.core | [Core vs Structure](../../knowledge/philosophy/corevsstructure.md) | Origin meaning and separation of structure |
| docs.tools | [Repository tools](../../tools/README.md) | Related tooling; separate authority boundary |

---

OWNER : BBX19  
MAKER : ChatGPT / Codex — AMS structure adaptation; original MPCP reference retained
