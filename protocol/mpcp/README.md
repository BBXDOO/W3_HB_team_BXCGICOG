README.md

MPCP

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

---

Owner

BBX19
