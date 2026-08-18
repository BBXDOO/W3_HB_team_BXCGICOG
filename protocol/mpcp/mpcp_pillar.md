# mpcp — Pillar Architecture (Marble-patterned Concrete Model)

## 1. Purpose
This document defines the structural model used in mpcp to represent
processing units (Modew) using a "pillar architecture".

The pillar represents a complete execution unit:
- Input
- Process
- Context
- Output

---

## 2. Core Concept

A pillar is composed of:

| Layer | Meaning |
|------|--------|
| Base (pile/pier) | Data / Memory / Storage |
| Body (pillar/post) | Processing logic |
| Inner pattern (marble) | Context / meaning / adaptive behavior |
| Top (capital) | Output / decision |

This model separates:
- Structure (concrete)
- Meaning (marble pattern)

---

## 3. Construction Order and Semantic Layers (A–F)

A–F are six named meaning layers inside the same pillar. During construction,
they are placed in architectural order A→F so the structure becomes complete.
This order grants no layer higher authority or special importance; every layer
exists because its capability and meaning are required by the structure.

After construction reaches the operational phase, A–F are not a mandatory data
pipeline. Work may enter, read, update, or leave through the layer related to
its present meaning, Paper, boundary and ENV.

Runtime work uses separately named operations such as receive, validate,
route, process and return. A Paper/Modew may select the operations needed for
the current ENV without changing the identity of the A–F layers.

Canonical rule:

```text
construction: A → B → C → D → E → F
operation: select related layer(s) by meaning / task / ENV
authority: no layer is inherently special
```

---

## 4. Structural Components

### 4.1 Language & Representation
- W3Lgu rules
- Markdown structure
- Line indentation
- Symbol system

### 4.2 Data Structures
- Memory table
- Grid table
- Column / Row system
- Library

### 4.3 Runtime Layer
- Tools
- Environment
- Layer meaning
- Adhesion (connection between layers)

### 4.4 Object System
- Object
- Completion level
- Modew (processing unit)
- Merging

### 4.5 Signal System
- Color system (state)
- Data format for reading values

---

## 5. Context Layer (Marble Pattern)

The inner pattern of the pillar represents:

- Context awareness
- Adaptive interpretation
- Non-static behavior

This allows the same structure to produce different outputs
based on context.

---

## 6. Extension Model (Wall Lamp)

External components (e.g. "wall lamp") represent:

- Optional objects
- Additional capabilities
- Non-core extensions

Properties:
- Do not modify the core pillar
- Attach externally
- Provide extra behavior

Examples:
- Option object
- Property arrangement layer

---

## 7. Merging

Multiple pillars can be combined:

Modew A + Modew B + Modew C → System

This enables:
- Modular system construction
- Independent scaling
- Reusable execution units

---

## 8. Mapping to mpcp

| Concept | mpcp Equivalent |
|--------|----------------|
| Pillar | Modew |
| Marble pattern | Condien |
| A–F | Semantic layers in one pillar |
| Wall lamp | Optional module |
| Merging | System composition |

---

## 9. System Capabilities

This architecture enables:

- Modular execution units
- Context-aware processing
- Clear operation tracing without turning A–F into step numbers
- Memory-aware execution continuity (history + task/role stats)
- Skill-based extension per modew role
- Capability-gated execution boundaries
- Easy debugging
- Scalable system composition
- Separation of logic and meaning

---

## 10. Summary

The pillar model defines a complete execution structure where:

- Structure = stable (concrete)
- Meaning = adaptive (marble)
- Operations = explicit and independent from A–F identity
- Extension = external (lamp)

This forms the foundation for mpcp runtime and W3Lgu mapping.
