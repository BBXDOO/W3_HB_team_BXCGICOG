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

### เส้นทางอ่าน AMS / RAMS

1. **AM:I** เริ่มที่ [MPCP Origin](MPCP_ORIGIN.md) เพื่ออ่านเจตนาของระบบ
2. **AM:II** อ่าน [ROT Baseline](ROT_BASELINE.md) และ [Blueprint](mpcp_blueprint_paper/README.md) เพื่อดูการแปลงเจตนาเป็นกฎและแบบงาน
3. **AM:III** เปิด [Runtime](runtime/README.md) เพื่อดูจุดรัน และ [กรณีทดสอบ](case_studies/README.md) เพื่อดูหลักฐานตามขอบเขตที่ทดสอบ
4. ใช้ **M1** เดินลงไปที่ไฟล์หรือ README ลูก ใช้ **M2** กลับไปยังเอกสารแม่และต้นทาง แล้วตาม `DERIVED_FROM` จนถึง AM:I รหัสในแผนผังใช้ลำดับชื่อไฟล์จาก Git แบบไบต์ และนับเฉพาะไฟล์นามสกุลเดียวกันหรือโฟลเดอร์ระดับเดียวกัน

ใช้ [4 Groups](../../docs/box/AMS/Group_4.md) อ่านจุดประสงค์ของเอกสารตาม BUILD, OBSERVE, LEARN หรือ CONTINUE แล้วใช้ AM Type อ่านระดับความหมาย

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
| [README.md](README.md) · `≡ Cd8ra - mpcp` | This system-level AMS directory map |
| [MPCP_ORIGIN.md](MPCP_ORIGIN.md) · `≡ Cd7mc - mpcp` | MPCP origin reference and lineage |
| [ROT_PAPER.md](ROT_PAPER.md) · `≡ Cd10rt - mpcp`, [ROT_BASELINE.md](ROT_BASELINE.md) · `≡ Cd9rt - mpcp` | ROT rules and baseline references |
| [MODEW_PAPER.md](MODEW_PAPER.md) · `≡ Cd6md - mpcp`, [MODEW_DYNAMIC_CAPABILITY_PAPER/](MODEW_DYNAMIC_CAPABILITY_PAPER/README.md) · `≡ Cf1md - mpcp` | Modew concepts and capability documentation |
| [COLOR_STATE.md](COLOR_STATE.md) · `≡ Cd1cl - mpcp`, [COLOR_SYMBOL_PAPER.md](COLOR_SYMBOL_PAPER.md) · `≡ Cd2cl - mpcp` | Color state and symbol papers |
| [CO_MODULE_LAW.md](CO_MODULE_LAW.md) · `≡ Cd3c_ - mpcp`, [CROSS_W3LGU_CONDIEN_RELATION.md](CROSS_W3LGU_CONDIEN_RELATION.md) · `≡ Cd4co - mpcp`, [EVENT_TEMPLATE_CONDIEN_BRIDGE.md](EVENT_TEMPLATE_CONDIEN_BRIDGE.md) · `≡ Cd5ee - mpcp` | Module, language, and Condien relation documents |
| [THEORDERMPCP.md](THEORDERMPCP.md) · `≡ Cd11te - mpcp`, [W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md](W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md) · `≡ Cd12w_ - mpcp`, [W3_TERMS_MASTER_PAPER_v2.md](W3_TERMS_MASTER_PAPER_v2.md) · `≡ Cd13w_ - mpcp` | Ordering, architecture, and terminology references |
| [mpcp_pillar.md](mpcp_pillar.md) · `≡ Cd14mc - mpcp` | MPCP pillar document |
| [config/](config/README.md) · `≡ Cf4cn - mpcp`, [env/](env/README.md) · `≡ Cf5ev - mpcp`, [lib/](lib/README.md) · `≡ Cf7lb - mpcp` | Runtime policy, ENV boundary, and library registry |
| [modew/](modew/README.md) · `≡ Cf8md - mpcp`, [kernel/](kernel/README.md) · `≡ Cf6kr - mpcp`, [runtime/](runtime/README.md) · `≡ Cf14rn - mpcp` | Execution units, validation kernel, and runtime traces |
| [orchestrator/](orchestrator/README.md) · `≡ Cf13oc - mpcp`, [adapter/](adapter/README.md) · `≡ Cf2aa - mpcp`, [schema/](schema/README.md) · `≡ Cf15sh - mpcp` | Flow composition, external bridges, and schema definitions |
| [case_studies/](case_studies/README.md) · `≡ Cf3cs - mpcp`, [mpcp_blueprint_paper/](mpcp_blueprint_paper/README.md) · `≡ Cf9mc - mpcp`, [mpcp_concept_paper/](mpcp_concept_paper/README.md) · `≡ Cf10mc - mpcp`, [mpcp_lib_paper/](mpcp_lib_paper/README.md) · `≡ Cf11mc - mpcp` | Local case studies and design papers |
| [mpcp_unified_lgu/](mpcp_unified_lgu/README.md) · `≡ Cf12mc - mpcp`, [w3lgu_integration_paper/](w3lgu_integration_paper/README.md) · `≡ Cf16wl - mpcp` | Local language integration references |
| [__init__.py](__init__.py) · `≡ Cc1_i - mpcp`, [cooperative_contract.py](cooperative_contract.py) · `≡ Cc2co - mpcp`, [runtime_sanity_sweep.py](runtime_sanity_sweep.py) · `≡ Cc3rn - mpcp`, [sandbox.py](sandbox.py) · `≡ Cc4sn - mpcp` | Python entry/contract/validation/sandbox modules |
| [test_agent_mpcp_alignment.py](test_agent_mpcp_alignment.py) · `≡ Cc5ts - mpcp`, [test_condien_blueprint.py](test_condien_blueprint.py) · `≡ Cc6ts - mpcp` | Local tests |

The entries above are an inventory, not a grant of authority. Read each component's contract before execution.

### M2 — External references

| docs.* | Text link | Relation |
|---|---|---|
| docs.ams | [Architecture Mapping Standard](../../docs/governance/AMS.md) | AM type, lineage and Gradation rules |
| docs.ams-template | [AMS README template](../../docs/box/AMS/AMS_README.txt) | Head / Body / Movement / OWNER / MAKER format |
| docs.core | [Core vs Structure](../../knowledge/philosophy/corevsstructure.md) | Origin meaning and separation of structure |
| docs.tools | [Repository tools](../../tools/README.md) | Related tooling; separate authority boundary |
| docs.wx-box | [wx / BOX / CN-Fold](../../wx/references/cn_fold_to_wx_box_mapping.md) | ตัวอย่างส่งต่องานข้ามพื้นที่ |
| docs.handoff | [ChatGPT context handoff](../../modules/ChatGPT/reports/WX_BOX_AMS_GRADATION_LIBRARY_X_CN_FOLD_HANDOFF_TH.md) | หลักฐานที่ใช้ค้น wx, BOX, CN-Fold และข้อจำกัดข้อมูล Library-X |
| docs.migration | [AMS migration request](../../requests/RQ-AMS-MIGRATION-A001.md) | ขอบเขตงานนำ AMS ไปใช้ |
| docs.lineage-review | [ผลตรวจสายอ้างอิง PR #339](../../docs/reports/AMS_LINEAGE_REVIEW_PR339_TH.md) | จุดที่ยืนยันสายแล้วและจุดรอหลักฐาน |

---

OWNER : BBX19  
MAKER : ChatGPT / Codex — AMS structure adaptation; original MPCP reference retained
