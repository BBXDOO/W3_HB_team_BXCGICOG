# W3 / MPCP Operational Structure Report

- Generated: 2026-05-09
- Scope: W3 / MPCP operational structure only
- Rule: factual only; when evidence was not found, this report uses `ยังไม่พบหลักฐาน`

## 1. Repository Structure

### 1.1 Root tree (depth 3)
```text
/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/
├── architecture/
│   ├── diagrams/
│   │   ├── file_000000001e7c72088554e0c1715f55b2.png
│   │   ├── placeholder.md
│   │   └── w3-civilization-main-map.png
│   ├── base.md
│   ├── interface-map.md
│   ├── layers.md
│   ├── overview.md
│   ├── standards.md
│   ├── system-map.md
│   └── W3_MASTER_ARCHITECTURE.md
├── BBX19/
│   ├── directives/
│   │   └── base.md
│   ├── modules/
│   │   └── BBX19/
│   ├── status/
│   │   ├── human-status.json
│   │   └── README.md
│   ├── ENTRANCE.md
│   ├── README.md
│   └── self-review.md
├── Cast/
│   ├── context/
│   │   ├── archive/
│   │   ├── protocol.md
│   │   ├── README.md
│   │   └── session_summary.md
│   ├── idp/
│   │   └── Cast.idp.json
│   ├── knowledge/
│   │   └── README.md
│   ├── modules/
│   ├── notes/
│   │   └── cast-context-notes.md
│   ├── reports/
│   │   └── RISK_REPORT.md
│   ├── requests/
│   │   └── README.md
│   ├── tasks/
│   ├── ENTRANCE.md
│   ├── module.json
│   ├── README.md
│   └── self-review.md
├── ChatGPT/
│   ├── artifacts/
│   ├── flow-lab/
│   │   └── design-stack.md
│   ├── modules/
│   │   └── ChatGPT/
│   ├── notes/
│   │   ├── design-decisions.md
│   │   ├── experiments-index.md
│   │   └── mpcp.json
│   ├── prototypes/
│   │   ├── design-bridge.md
│   │   └── live.md
│   ├── testcases/
│   │   └── test-harness.md
│   ├── ux-sim/
│   │   └── simulation-primitives.md
│   ├── ENTRANCE.md
│   ├── README.md
│   └── self-review.md
├── Copilot-Gm/
│   ├── governance/
│   │   └── repo-lock.md
│   ├── modules/
│   │   └── Copilot-Gm/
│   ├── templates/
│   ├── workspace/
│   │   ├── ci-config/
│   │   ├── drafts/
│   │   └── onboarding/
│   ├── ENTRANCE.md
│   ├── LOCKED.md
│   ├── module.json
│   ├── README.md
│   ├── repo-lock.md
│   └── self-review.md
├── core/
│   ├── adapters/
│   │   ├── __init__.py
│   │   └── llm_adapter.py
│   ├── events/
│   │   ├── event-protocol.md
│   │   └── event-schema.json
│   ├── governance/
│   │   ├── rules/
│   │   ├── decisions.md
│   │   ├── module-manifest-policy.md
│   │   ├── operating-guidelines.md
│   │   └── phase2-framework.md
│   ├── hybrid-model/
│   │   ├── responsibilities.md
│   │   └── vision.md
│   ├── logs/
│   │   ├── archive/
│   │   ├── rotations/
│   │   ├── templates/
│   │   ├── system_log.json
│   │   └── system_log.schema.json
│   ├── memory/
│   │   ├── memory_bus.py
│   │   └── memory_store.json
│   ├── module-loader/
│   │   ├── identity/
│   │   ├── idp-schema.json
│   │   ├── module-registry.json
│   │   └── router.py
│   ├── module_loader/
│   │   └── router.py
│   └── runtime/
│       ├── agents/
│       ├── engine.py
│       ├── engine_v2.py
│       └── runtime.md
├── DeepSeek/
│   ├── architecture-hints/
│   ├── meta-structure/
│   │   └── structure-map.md
│   ├── modules/
│   │   └── DeepSeek/
│   ├── notes/
│   │   └── observation-log.md
│   ├── pattern-lab/
│   ├── studio/
│   │   ├── collab/
│   │   ├── core/
│   │   ├── forge/
│   │   └── wisdom/
│   ├── ENTRANCE.md
│   ├── README.md
│   └── self-review.md
├── docs/
│   ├── architecture/
│   │   ├── AUDIT_ARCHITECTURE.md
│   │   └── REDR_Structure_Map.md
│   ├── audits/
│   │   ├── templates/
│   │   └── 2025-12-10-audit.md
│   ├── governance/
│   │   ├── decision_trace.md
│   │   ├── DECLARATION_IV.md
│   │   ├── LINE_B_GPT.md
│   │   ├── manifesto-2.md
│   │   └── PHILOSOPHY.md
│   ├── guides/
│   │   ├── AGENT_WORKSPACE_GUIDELINE.md
│   │   ├── GITHUB_PAGES_SETUP.md
│   │   ├── MODULE_USAGE_GUIDE.md
│   │   ├── PR_Flow_Table.md
│   │   └── QUICK_START.md
│   ├── reports/
│   │   ├── AGENT_MODULE_CAPABILITY_REPORT.md
│   │   ├── AGENT_WORKSPACE_AUDIT.md
│   │   ├── AUDIT_COMPLETION_SUMMARY.md
│   │   ├── AUDIT_SYSTEM_README.md
│   │   ├── W3_RUNTIME_FIX_REPORT.md
│   │   └── W3_SANITY_SWEEP_REPORT.md
│   ├── review/
│   │   ├── COMPLETION_STATUS.md
│   │   ├── MPCP_STATUS_SSOT.md
│   │   └── PR83_review_summary.md
│   ├── AGENT_RULES_AND_MEMORY.md
│   ├── agent.profile.json
│   ├── context.map.json
│   ├── GITHUB_ACTIONS_AGENT.md
│   ├── IGET_OPERATION_MODEL.md
│   ├── index.json
│   ├── index.md
│   ├── manifest.json
│   ├── modules.json
│   ├── MPCP_architecture
│   ├── protocol.md
│   ├── rules.json
│   ├── state.json
│   ├── system.json
│   ├── version.policy.json
│   └── W3_MASTER_MAP.md
├── Gemini/
│   ├── analysis-lab/
│   │   └── experiment_template.md
│   ├── dependency-map/
│   │   └── system_map.md
│   ├── logic-check/
│   │   └── validation_protocol.md
│   ├── modules/
│   │   └── Gemini/
│   ├── notes/
│   │   ├── analyst_notebook.md
│   │   └── qa-issues.md
│   ├── reports/
│   │   └── monthly_health_check.md
│   ├── risk-scan/
│   │   └── risk_register.md
│   ├── tasks/
│   │   ├── active_tasks.md
│   │   └── checkpoints.md
│   ├── tools/
│   │   └── validate_json.py
│   ├── ENTRANCE.md
│   ├── README.md
│   ├── rules.md
│   └── self-review.md
├── Grok/
│   ├── action-tracker/
│   │   └── todo.md
│   ├── insight-vault/
│   │   ├── 2025-12-01_discourse_summary.md
│   │   └── incidents.md
│   ├── interpret-lab/
│   │   └── quick-test.md
│   ├── modules/
│   │   └── Grok/
│   ├── narrative/
│   │   └── example_narrative.md
│   ├── notes/
│   │   ├── grok_self_notes.md
│   │   └── methodology-notes.md
│   ├── oncall-board/
│   │   └── emergency.md
│   ├── pattern-scan/
│   │   └── latest_scan_20251201.md
│   ├── risk-mitigation/
│   │   └── deepseek_downtime.md
│   ├── base.md
│   ├── ENTRANCE.md
│   ├── README.md
│   └── self-review.md
├── SYSTEM/
│   └── TESTS/
│       ├── EP_SIGNAL/
│       ├── mpcp/
│       └── w3db/
├── modules/
│   ├── BBEX-Core/
│   │   └── module.json
│   ├── BBX19/
│   │   └── module.json
│   ├── Cast/
│   │   └── module.json
│   ├── ChatGPT/
│   │   ├── flows/
│   │   ├── logs/
│   │   ├── reports/
│   │   ├── requests/
│   │   ├── scenarios/
│   │   └── module.json
│   ├── Copilot-Gm/
│   │   ├── governance/
│   │   └── module.json
│   ├── DeepSeek/
│   │   ├── plans/
│   │   └── module.json
│   ├── Gemini/
│   │   ├── reports/
│   │   ├── requests/
│   │   └── module.json
│   ├── Grok/
│   │   ├── patterns/
│   │   ├── requests/
│   │   ├── risk-reports/
│   │   └── module.json
│   └── registry.json
├── reports/
│   ├── cleanup_plan.md
│   ├── full_structure_audit.md
│   ├── module_health.md
│   └── registry_audit.md
├── src/
│   └── w3db/
│       ├── config.py
│       ├── flow.py
│       ├── models.py
│       └── store.py
└── tools/
    ├── run_audit.py
    ├── validate_metadata.py
    ├── validate_modules.py
    ├── w3_agent_ci.py
    └── w3run.py
```

### 1.2 ChatGPT registry workspace tree (depth 3)
```text
/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/ChatGPT/
├── flows/
├── logs/
│   └── daily/
├── reports/
│   ├── 2026-05-09_w3_mpcp_operational_structure_report.md
│   └── response_2026-04-16_error-meaning.md
├── requests/
│   ├── .gitkeep
│   └── requsts.md
├── scenarios/
└── module.json
```

### 1.3 MPCP tree (depth 4)
```text
/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/
├── adapter/
│   └── w3_bridge.py
├── kernel/
│   ├── contract.py
│   ├── rot.py
│   ├── system.py
│   └── validator.py
├── lib/
│   └── pillar.py
├── modew/
│   └── base_modew.py
├── mpcp_blueprint_paper/
│   └── mpcp_blueprint_paper.md
├── mpcp_concept_paper/
│   ├── mpcp_concept_paper.md
│   └── ROT_PAPER.md
├── mpcp_lib_paper/
│   └── mpcp_lib_paper.md
├── mpcp_unified_lgu/
│   └── mpcp_unified_language_paper.md
├── orchestrator/
│   ├── flow.py
│   └── manager.py
├── runtime/
│   ├── entry.py
│   ├── executor.py
│   └── trace.py
├── schema/
│   └── pillar.schema.json
├── COLOR_STATE.md
├── COLOR_SYMBOL_PAPER.md
├── MODEW_PAPER.md
├── MPCP_ORIGIN.md
├── README.md
├── W3_TERMS_MASTER_PAPER_v2.md
└── runtime_sanity_sweep.py
```

### 1.4 Main modules
- Human/root: `BBX19`
- Root auxiliary: `BBEX-Core`
- L1/L2/L3 AI modules: `ChatGPT`, `Gemini`, `DeepSeek`, `Grok`, `Copilot-Gm`, `Cast`
- Central registry file: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`
- Task router registry: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/module-registry.json`

### 1.5 Important paths
- Repo root: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG`
- ChatGPT workspace root: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/`
- ChatGPT registry workspace: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/ChatGPT/`
- Central docs: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/`
- Architecture docs: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/architecture/`
- Core runtime: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/runtime/`
- Core memory: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/memory/`
- MPCP runtime: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/`
- Reports root: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/reports/`
- `protocols/` root directory: `ยังไม่พบหลักฐาน` (checked repo root; no `/protocols/` directory matched)

## 2. Module Registry

### 2.1 Registry authorities
- Registry authority: `BBX19` — `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`
- Task routing registry: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/module-registry.json`
- Runtime registry type: `centralized` — `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`
- Governance merge requirements: `Copilot-Gm`, `Gemini` — `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`

### 2.2 Modules
| Module | Role | Owner | Invoke path | Input | Output | Escalation target |
|---|---|---|---|---|---|---|
| `BBX19` | `Final Authority / Vision Keeper` | `BBX19` | task keyword: `vision`; channel: `/BBX19/` | `modules/BBX19/requests/`, `modules/registry.json`, `core/governance/`, `knowledge/`, `logs/` | `modules/BBX19/logs/`, `core/governance/`, `outcomes/append_only_ledger/` | authority: `BBX19`; registry `critical_requires`: `BBX19` |
| `BBEX-Core` | `Identity / Philosophical Anchor` | `BBX19` | task keywords: `identity`, `philosophy`; channel: `/BBEX-Core/` | `modules/BBEX-Core/requests/`, `knowledge/`, `BBEX-Core/public/`, `logs/` | `modules/BBEX-Core/reflections/`, `modules/BBEX-Core/logs/`, `knowledge/philosophy/` | authority: `BBX19`; identity change requires `BBX19`, `BBEX-Core` |
| `ChatGPT` | `Architecture / Flow / Execution` | `ChatGPT` | task keywords: `design`, `architecture`, `flow`, `simulation`; channel: `/ChatGPT/` | `modules/ChatGPT/requests/`, `knowledge/`, `docs/`, `core/`, `blueprints/`, `repo_events/` | `modules/ChatGPT/flows/`, `modules/ChatGPT/scenarios/`, `modules/ChatGPT/reports/`, `modules/ChatGPT/logs/` | authority: `BBX19`; risky path in README L0: `If risky → escalate to Gemini`; merge requires `Copilot-Gm`, `Gemini` |
| `Gemini` | `Validation / Cross Check` | `Gemini` | task keywords: `verify`, `verification`, `audit`, `security`; channel: `/Gemini/` | `modules/Gemini/requests/`, `modules/ChatGPT/flows/`, `knowledge/`, `docs/`, `core/` | `modules/Gemini/reports/`, `modules/Gemini/audit/`, `modules/Gemini/logs/` | authority: `BBX19`; merge requires `Copilot-Gm`, `Gemini` |
| `Grok` | `Pattern / Signals / Insight` | `Grok` | task keywords: `pattern`, `signals`, `insight`; channel: `/Grok/` | `modules/Grok/requests/`, `decision_trace/`, `tuf_snapshots/`, `fbd_reports/`, `knowledge/`, `repo_events/` | `modules/Grok/patterns/`, `modules/Grok/risk-reports/`, `modules/Grok/insights/`, `modules/Grok/logs/` | authority: `BBX19`; `Grok/base.md` escalation: governance/branch conflict → `Copilot-Gm`, AI-module conflict → `BBX19` |
| `DeepSeek` | `Scale / Long-Term Planning` | `DeepSeek` | task keywords: `research`, `scale`, `planning`; channel: `/DeepSeek/` | `modules/DeepSeek/requests/`, `knowledge/`, `docs/`, `core/`, `blueprints/` | `modules/DeepSeek/reports/`, `modules/DeepSeek/plans/`, `modules/DeepSeek/logs/` | authority: `BBX19`; structure conflicts in `ENTRANCE.md` send to `Gemini` |
| `Copilot-Gm` | `Policy / Merge / Compliance` | `Copilot-Gm` | task keywords: `governance`, `policy`, `compliance`; channel: `/Copilot-Gm/` | `modules/Copilot-Gm/requests/`, `core/governance/`, `knowledge/`, `docs/`, `modules/registry.json` | `modules/Copilot-Gm/reports/`, `modules/Copilot-Gm/governance/`, `modules/Copilot-Gm/logs/` | authority: `BBX19`; merge review in `ENTRANCE.md`: `BBX19` final sign-off + `Gemini` validation |
| `Cast` | `Deep Reasoning / Decision Support` | `Cast` | task keywords: `reason`, `critical_reasoning`, `interpret`, `document`; channel: `/Cast/` | `modules/Cast/requests/`, `knowledge/`, `docs/`, `core/` | `modules/Cast/reports/`, `modules/Cast/artifacts/`, `modules/Cast/logs/` | authority: `BBX19`; `merge_to_main` approval required in `modules/Cast/module.json` |

### 2.3 Source files used for section 2
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/module-registry.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/BBX19/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/BBEX-Core/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/ChatGPT/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Gemini/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Grok/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/DeepSeek/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Copilot-Gm/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Cast/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/base.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/README.md`

## 3. MPCP Structure

### 3.1 MPCP in the live repository
- `README.md` in MPCP defines: `MPCP is a lightweight operational system built for clear execution, short communication, and structured control.`
- `MPCP_ORIGIN.md` defines MPCP as `Marble-patterned Concrete Pillars (MPCP)`.
- `docs/MPCP_architecture` defines: `Multi-Point Control Protocol (MPCP) architecture for the W3 Hybrid system.`

### 3.2 Responsibilities
- `README.md`: `Rot Paper defines system. Paper drives action. Modew executes. Condien carries data.`
- `README.md`: components = `Modew`, `Condien`, `Rot Paper`, `Paper`
- `MPCP_ORIGIN.md`: `Structure = คงที่`, `Meaning = ปรับตัวได้ตามบริบท`
- `COLOR_STATE.md`: color system position = `Decision Layer`

### 3.3 Runtime location
- Runtime executor: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py`
- Runtime entry: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/entry.py`
- Modew base: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/modew/base_modew.py`
- Orchestrator: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/orchestrator/manager.py`
- Adapter bridge: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/adapter/w3_bridge.py`

### 3.4 Interfaces
- Input parser in `runtime/executor.py`: `TASK:value,KEY:value`
- Output formatter in `runtime/executor.py`: `STATE:<state>,COLOR:<color>,SYM:<symbol>`
- Optional system field in `kernel/system.py`: `SYSTEM`
- W3 bridge stub in `adapter/w3_bridge.py`: `execute_with_w3(task)`

### 3.5 Protocol docs
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/MPCP_ORIGIN.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/COLOR_STATE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/COLOR_SYMBOL_PAPER.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/MODEW_PAPER.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/mpcp_concept_paper/ROT_PAPER.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/W3_TERMS_MASTER_PAPER_v2.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/MPCP_architecture`

### 3.6 Dependency map
- `runtime/executor.py` imports:
  - `mpcp.runtime.trace.trace`
  - `mpcp.kernel.contract.MPCPContract`
  - `mpcp.kernel.rot.MPCPRot`
  - `mpcp.kernel.system.validate_system_context`
- `runtime/entry.py` imports:
  - `mpcp.runtime.executor.run`
  - `mpcp.runtime.executor.register`
  - `mpcp.runtime.executor.to_mpcp_output`
  - `mpcp.modew.base_modew.BaseModew`
- `orchestrator/manager.py` imports:
  - `mpcp.runtime.executor.run`
  - `mpcp.kernel.contract.VALID_STATES`
- `runtime_sanity_sweep.py` imports:
  - `mpcp.kernel.contract`
  - `mpcp.kernel.rot`
  - `mpcp.runtime.executor`
  - `mpcp.runtime.trace`
  - `mpcp.modew.base_modew`

## 4. Runtime Architecture

### 4.1 Local / cloud split
| Area | Evidence |
|---|---|
| Local runtime | `docs/W3_MASTER_MAP.md`: `Termux = Local Runtime Engine`; `core/runtime/engine.py`; `core/runtime/engine_v2.py`; `protocol/mpcp/runtime/executor.py` |
| Cloud source/version layer | `docs/W3_MASTER_MAP.md`: `GitHub = Version Truth / Source Authority`; `.github/workflows/w3_agent_ci.yml`; `docs/GITHUB_ACTIONS_AGENT.md` |
| Public web surface | `README.md` GitHub Pages URL; `docs/manifest.json`; `docs/index.html`; `docs/sw.js`; `docs/mirror.policy.json` |
| Public/private split | `docs/mirror.policy.json` |

### 4.2 Active services / executors / workflows
- W3 runtime engine: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/runtime/engine.py`
- W3 runtime engine v2: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/runtime/engine_v2.py`
- Runtime CLI: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/tools/w3run.py`
- Runtime agent registry: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/runtime/agents/registry.py`
- MPCP orchestrator: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/orchestrator/manager.py`
- W3 Agent CI workflow: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/.github/workflows/w3_agent_ci.yml`
- IGET PR governance unit: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/iget/README.md`

### 4.3 APIs
- OpenAI adapter: `core/adapters/llm_adapter.py` (`OPENAI_API_KEY`, `call_gpt`)
- Gemini adapter: `core/adapters/llm_adapter.py` (`GEMINI_API_KEY`, `call_gemini`)
- Manual external AI workflow: `docs/QUICK_START_MODULES.md` (`ChatGPT.com`, `Gemini.google.com`)

### 4.4 Bots / agents
- Registered runtime agents: `BBX19`, `BBEX-Core`, `ChatGPT`, `Gemini`, `Grok`, `DeepSeek`, `Copilot-Gm`, `Cast` — `core/runtime/runtime.md`, `core/agents.json`, `core/runtime/agents/*.py`
- Governance PR assistant: `IGET` — `iget/README.md`, `docs/IGET_OPERATION_MODEL.md`

### 4.5 Databases / persistence / vector stores
| Category | Evidence |
|---|---|
| JSON shared memory | `core/memory/memory_bus.py`, `core/memory/memory_store.json` |
| Session log | `Cast/context/session_summary.md`, `knowledge/SESSION_LOG.md` |
| In-process W3DB store | `src/w3db/store.py` (`W3DBStore`), `src/w3db/flow.py` |
| Future memory sources | `architecture/W3_MASTER_ARCHITECTURE.md`: future sources = `W3DB`, `Vector memory`, `Team trust memory` |
| SQL/files layer | `docs/W3_MASTER_MAP.md`: `SQL / Files = Structured Persistence Layer` |
| Vector store runtime path | `ยังไม่พบหลักฐาน` for a dedicated vector-store implementation path in repo root, `core/`, `src/`, `SYSTEM/TESTS/` |

### 4.6 Orchestration layer
- Task router: `core/module-loader/router.py`
- Task registry: `core/module-loader/module-registry.json`
- Runtime dispatch: `core/runtime/engine_v2.py`
- Runtime flow note: `core/runtime/runtime.md`
- MPCP flow manager: `protocol/mpcp/orchestrator/manager.py`
- Event protocol: `core/events/event-protocol.md`

## 5. Agent Flow

### 5.1 Human → module flow
- `README.md` L0 protocol:
  1. `Human defines intent.`
  2. `Create request_XXX.md under target module /requests/.`
  3. `Module produces output to reports/ or knowledge/.`
  4. `If risky → escalate to Gemini.`
  5. `story → merge / revise / rej`
- `core/events/event-protocol.md` event example:
  - `source: Human`
  - `target_module: ChatGPT`

### 5.2 Runtime invoke flow
- `docs/QUICK_START_MODULES.md`:
  - `engine_v2.run("design")`
  - `router.execution_plan("design")`
  - `build_context("design")`
  - `dispatch("ChatGPT", task, context)`
  - `add_memory(...)`
- `core/runtime/runtime.md`:
  - `Event → Router + IDP → Context Memory → Agent Module → Result + Memory Log`
- `protocol/mpcp/runtime/executor.py`:
  - `A (parse) → ROT input check → B (resolve) → C (inject) → D (execute) → ROT output check → E (return)`

### 5.3 Verification flow
- `README.md`: `If risky → escalate to Gemini`
- `ChatGPT/ENTRANCE.md`: success criteria include `ต้องผ่าน validation ของ Gemini` and `ต้องผ่าน sign-off ของ BBX19`
- `Gemini/tasks/checkpoints.md`: `ถ้าไม่มี checkpoint → ห้าม merge`
- `Copilot-Gm/ENTRANCE.md`: public-ready files must be checked by `Gemini`

### 5.4 Merge / reject / hold flow
- `README.md`: `Human → Module → Human Review → Merge`
- `README.md`: conflict escalation = `Grok → Gemini → Copilot-Gm → BBX19`
- `core/governance/operating-guidelines.md`: `No direct commit to main`
- `core/governance/operating-guidelines.md`: `PR must be reviewed by at least 1 AI engine`
- `docs/guides/PR_Flow_Table.md`: statuses = `HOLD`, `REVIEW`, `DROP`; final merge decisions rest with `BBX19`
- `docs/GITHUB_ACTIONS_AGENT.md`: exit code `1` blocks PR `if branch protection is enabled`

## 6. Governance Sources

### 6.1 Source-of-truth files
- Repo/module source of truth: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/registry.json`
- Task routing source of truth: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/module-registry.json`
- MPCP status SSOT: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/review/MPCP_STATUS_SSOT.md`
- Chat/context entry point: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/index.json`
- Core rule file: `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/governance/rules/w3_ruleset.yml`

### 6.2 Protocol priority
- `docs/protocol.md`: `Follow external context`
- `docs/index.json`: `This file is the single entry point. Do not embed full context in chat.`
- `docs/context.map.json`: core files load `always`; operations load `on_demand`; protocol loads `reference_only`
- `docs/agent.profile.json`: `no_guess_without_evidence: true`; missing evidence response = `ยังไม่พบหลักฐาน`

### 6.3 Authoritative docs
- `docs/protocol.md`
- `docs/index.json`
- `docs/system.json`
- `docs/rules.json`
- `docs/state.json`
- `docs/context.map.json`
- `docs/agent.profile.json`
- `docs/review/MPCP_STATUS_SSOT.md`
- `docs/W3_MASTER_MAP.md`
- `architecture/W3_MASTER_ARCHITECTURE.md`

## 7. Context System

### 7.1 Memory model
- Shared memory API: `core/memory/memory_bus.py`
- Shared memory store: `core/memory/memory_store.json`
- Session continuity protocol: `Cast/context/protocol.md`
- Session continuity log: `Cast/context/session_summary.md`
- Session template/log: `knowledge/SESSION_LOG.md`

### 7.2 Persistence model
- `core/memory/memory_store.json`: JSON records array on disk
- `memory_bus.py`: `Persistent lightweight memory store`
- `Cast/context/session_summary.md`: append-only per productive session
- `knowledge/SESSION_LOG.md`: `1 session = 1 record`
- `src/w3db/store.py`: in-memory `W3DBStore`

### 7.3 Session/context boundaries
- `docs/index.md`: `Context lives outside the chat`; `Chat is used for execution only`
- `docs/protocol.md`: `Operate by reference only`
- `Cast/context/protocol.md`: read memory before work and write summary after work
- `knowledge/SESSION_LOG.md`: session template boundary = one session per record

### 7.4 Context loading rules
- `docs/index.json`: `load_policy: reference_only`, `priority: always`
- `docs/context.map.json`:
  - `core` files (`index.json`, `system.json`, `rules.json`) → `always`
  - `operations` files (`modules.json`, `state.json`) → `on_demand`
  - `protocol.md` → `reference_only`
  - `index.md` beacon → `optional`
- `docs/agent.profile.json`: `assume_external_context`, `no_context_replication`
- `BBX19/modules/BBX19/context/chatgpt_context.json`: `If context lost, require IDP before work`

## 8. Active Branch State

### 8.1 Current checked-out branch
- Local branch: `copilot/create-chatgpt-report`
- Local HEAD at time of evidence collection: `f497f8c3db5766adf0e280ceafeb28599a6fccdc`

### 8.2 Branch declarations and examples
- `README.md`: `🚫 DO NOT TOUCH: main`
- `README.md` link section names active working branch: `refactor/v0.2`
- GitHub branch list examples returned by API:
  - `main`
  - `copilot/create-chatgpt-report`
  - `copilot/w3-agent`
  - `feature/validate-json-ajv2020`
  - `revert-170-claude/create-runtime-for-mpcp-system`
  - `BBXDOO-patch-1`

### 8.3 Protected branches
- GitHub branch API returned `protected: false` for all returned branches, including `main`
- `REPORT_REPO_AUDIT_FULL.txt`: `The single biggest risk is the unprotected main branch`

### 8.4 Unstable zones
- `REPORT_REPO_AUDIT_FULL.txt`: `main branch that has drifted behind active development`
- `REPORT_REPO_AUDIT_FULL.txt`: `duplicate workflows`, `untested runtime code`, `18 dead branches`
- `Gemini/notes/qa-issues.md`: active issue `Agent workspace content gap`
- `Cast/context/session_summary.md`: `no automated enforcement exists yet`

### 8.5 Experimental zones
- `protocol/mpcp/README.md`: `Status: Active Experimental Build`
- `DeepSeek/ENTRANCE.md`: `Skeleton Edition`, `Phase-1`
- `DeepSeek/notes/observation-log.md`: `ยังไม่เปิด full meta-scan`
- `protocol/EP_SIGNAL/README.md`: `experimental system design`, `Build experimental protocol layer for future systems`

## 9. Existing AI Systems

### 9.1 Internal agents and systems
- Runtime agents: `BBX19`, `BBEX-Core`, `ChatGPT`, `Gemini`, `Grok`, `DeepSeek`, `Copilot-Gm`, `Cast` — `core/runtime/runtime.md`, `core/runtime/agents/*.py`
- IGET governance assistant — `iget/README.md`, `docs/IGET_OPERATION_MODEL.md`
- MPCP runtime/orchestrator — `protocol/mpcp/runtime/*.py`, `protocol/mpcp/orchestrator/*.py`
- W3 memory core — `core/memory/memory_bus.py`
- W3DB — `src/w3db/*.py`

### 9.2 External AI systems declared in repo
- OpenAI / GPT backend — `core/adapters/llm_adapter.py`, `docs/QUICK_START_MODULES.md`
- Google Gemini backend — `core/adapters/llm_adapter.py`, `docs/QUICK_START_MODULES.md`
- Manual external use paths — `docs/QUICK_START_MODULES.md`: `ChatGPT.com`, `Gemini.google.com`

### 9.3 Responsibility overlaps documented in module entrances
- `ChatGPT` ↔ `Gemini`: flow/prototype → validation
- `Grok` ↔ `Gemini`: insight/narrative → validation
- `DeepSeek` ↔ `Gemini`: architecture / logic conflict review
- `ChatGPT` ↔ `Copilot-Gm`: prototype/flow → repo structure / templates
- `Grok` ↔ `Copilot-Gm`: narrative/system insight → repo mapping
- `Cast` ↔ all agents: session memory / context bridge via `Cast/context/protocol.md`

## 10. Constraints

### 10.1 Forbidden behaviors
- `ChatGPT/modules/ChatGPT/boundaries.md` forbids:
  - impersonating humans
  - human decision replacement for life/safety/finance
  - emotional manipulation persona
  - intentional information distortion
  - overriding governance / Copilot-Gm / human authority
  - storing personal data outside system context
- `docs/rules.json` boundaries:
  - `no_autonomous_scope_expansion`
  - `no_hidden_assumptions`
  - `report_uncertainty_explicitly`
- `README.md` rules:
  - `No AI merge`
  - `No persona`
  - `Every critical insight -> logged`

### 10.2 Hard rules
- `core/governance/rules/w3_ruleset.yml`:
  - `RULE-001 module_validity` (`error`)
  - `RULE-002 metadata_approval_reason` (`error`)
  - `RULE-003 python_syntax` (`error`)
  - `RULE-004 json_schema_valid` (`warn`)
  - `RULE-005 no_orphan_schemas` (`warn`)
- `core/governance/operating-guidelines.md`:
  - `No direct commit to main`
  - `PR must be reviewed by at least 1 AI engine`
  - `BBX19 exclusive override`

### 10.3 Termination / halt conditions
- `protocol/mpcp/kernel/contract.py`: valid halt states include `STOP`, `fail`, `block`
- `protocol/mpcp/kernel/rot.py`: halt states must include `error`
- `protocol/mpcp/runtime/executor.py`: unknown modew returns `MODEW_NOT_FOUND:<task>` with state `STOP`
- `docs/agent.profile.json`: when evidence is missing, response = `ยังไม่พบหลักฐาน`

### 10.4 Escalation rules
- `README.md`: `Grok → Gemini → Copilot-Gm → BBX19`
- `ChatGPT/ENTRANCE.md`: conflict with `DeepSeek` or `Gemini` → `flow-resolution meeting`
- `Gemini/ENTRANCE.md`: conflict with `DeepSeek` or `ChatGPT` → `validation meeting`
- `Grok/ENTRANCE.md`: conflict with `DeepSeek` or `Gemini` → `insight-resolution meeting`
- `DeepSeek/ENTRANCE.md`: pattern conflict → `Gemini`
- `Grok/base.md`: governance/branch conflict → `Copilot-Gm`; AI-module conflict → `BBX19`

## 11. Current Problems

### 11.1 Known instability
- `REPORT_REPO_AUDIT_FULL.txt`:
  - `18 dead branches`
  - `duplicate workflows`
  - `untested runtime code`
  - `main branch that has drifted behind active development`
  - `unprotected main branch`
- `Gemini/notes/qa-issues.md`: `Agent workspace content gap` (severity `HIGH`)
- `Gemini/notes/qa-issues.md`: `Cast session_summary.md — single contributor` (severity `MEDIUM`)

### 11.2 Hallucination points documented in repo
- `protocol/mpcp/MPCP_ORIGIN.md`: `นี่คือจุดที่ GPT ตีความผิดบ่อยที่สุดครับ`
- `protocol/mpcp/MPCP_ORIGIN.md`: `❌ A→F ≠ ลำดับความสำคัญ`
- `protocol/mpcp/MPCP_ORIGIN.md`: `❌ Structure ≠ Meaning`
- `docs/agent.profile.json`: `no_guess_without_evidence: true`
- `BBX19/modules/BBX19/context/chatgpt_context.json`: `no hallucination`

### 11.3 Orchestration gaps
- `Gemini/notes/qa-issues.md`: `ไม่มีหลักฐานว่า rules เหล่านั้นถูก enforce จริง`
- `Cast/context/session_summary.md`: `no automated enforcement exists yet`
- `docs/guides/AGENT_WORKSPACE_GUIDELINE.md`: anti-pattern `ENTRANCE.md ที่ไม่เคยถูก execute`
- `docs/reports/AGENT_WORKSPACE_AUDIT.md`: `ไม่มี cross-agent knowledge flow ที่วัดได้`

### 11.4 Protocol drift points
- `protocol/mpcp/MPCP_ORIGIN.md`: `ถ้า AI หรือระบบใดตีความว่า structure = meaning นั่นคือ drift`
- `docs/index.md`: externalized context exists `to reduce token usage, prevent context drift`
- `Gemini/tasks/checkpoints.md`: `pattern drift จาก Grok`
- `Copilot-Gm/self-review.md`: `commit drift: …`

## 12. Desired ChatGPT Role

### 12.1 Exact allowed scope
- `modules/ChatGPT/module.json`: scope = `architecture`
- `ChatGPT/ENTRANCE.md`: flow design, prototype creation, scenario-test, module interaction experiments
- `ChatGPT-IDP.md`: responsibilities = `design flow & blueprint`, `produce ≤10 line system summaries`, `verify JSON / logic`, `support module-pair operations`, `produce actionable execution steps`
- `ChatGPT/modules/ChatGPT/boundaries.md`: can analyze system structure, design simulations/test scenarios, draft schema/spec/protocol drafts, analyze non-human risk, provide technical options

### 12.2 Exact forbidden scope
- `ChatGPT/modules/ChatGPT/boundaries.md` section `เรื่องที่ต้อง “ถามมนุษย์เท่านั้น”`
- `ChatGPT/modules/ChatGPT/boundaries.md` section `เรื่องที่ “ห้ามแตะเด็ดขาด”`
- `docs/rules.json`: `no_autonomous_scope_expansion`
- `README.md`: `No AI merge`

### 12.3 Expected outputs
- `modules/ChatGPT/module.json`: outputs = `modules/ChatGPT/flows/`, `modules/ChatGPT/scenarios/`, `modules/ChatGPT/reports/`, `modules/ChatGPT/logs/`
- `ChatGPT/ENTRANCE.md` expected outputs:
  - `flow-lab/*.md`
  - `prototypes/*.md`
  - `testcases/*.md`
  - `ux-sim/*.md`
  - `notes/design-decisions.md`
  - `artifacts/flow-master.md`

### 12.4 Interaction mode
- `ChatGPT/modules/ChatGPT/boundaries.md` modes:
  - `RESTORATION MODE`
  - `SIMULATION MODE`
  - `OBSERVER MODE`
  - `EXECUTION SUPPORT`
- `docs/system.json` interaction style:
  - tone `direct`
  - verbosity `low`
  - focus `action_over_theory`
- `docs/protocol.md`: `Execution-first`, `Minimal verbosity`, `Actionable output only`

## 13. Available Interfaces

| Interface | Evidence |
|---|---|
| Slack | `ยังไม่พบหลักฐาน` in `docs/`, `architecture/`, `core/`, root README, module entrances |
| GitHub | `.github/workflows/w3_agent_ci.yml`; `docs/GITHUB_ACTIONS_AGENT.md`; `README.md` GitHub Pages URL; `architecture/W3_MASTER_ARCHITECTURE.md` current inputs = `GitHub Pull Requests` |
| MCP / MPCP | `protocol/mpcp/`; `docs/MPCP_architecture`; `runtime/executor.py` MPCP parser/output formatter |
| APIs | `core/adapters/llm_adapter.py`; `docs/QUICK_START_MODULES.md` |
| Filesystem | `modules/*/requests/`, `modules/*/reports/`, `core/memory/memory_store.json`, `Cast/context/session_summary.md` |
| Web panels | `docs/index.html`; `docs/manifest.json`; `docs/sw.js`; `README.md` GitHub Pages instructions |
| Dashboards | `architecture/W3_MASTER_ARCHITECTURE.md` current surfaces include `Notion dashboards`; `docs/W3_MASTER_MAP.md` lists `Notion = Human Dashboard / Visual Control` |

## 14. Execution Policy

### 14.1 Autonomous allowed?
- `modules/registry.json`: runtime `autonomous_ready: true`
- `modules/ChatGPT/module.json`: `self_directed: true`
- `docs/state.json`: `operation_mode: NORMAL`; `active_focus: build_and_stabilize`

### 14.2 Approval required?
- `modules/ChatGPT/module.json`: approval required for `core_changes`, `registry_update`, `governance_docs`
- `ChatGPT/modules/ChatGPT/boundaries.md`: `Human Review ก่อน Merge`
- `core/governance/operating-guidelines.md`: PR must be reviewed by at least 1 AI engine; `BBX19 exclusive override`
- `Copilot-Gm/ENTRANCE.md`: governance changes require `PR + 1 reviewer (BBX19)`; ready files require `Gemini` validation

### 14.3 Write permissions
- `modules/ChatGPT/module.json` write paths:
  - `modules/ChatGPT/flows/`
  - `modules/ChatGPT/scenarios/`
  - `modules/ChatGPT/reports/`
  - `modules/ChatGPT/logs/`
- `core/adapters/llm_adapter.py` writes output to configured module output paths

### 14.4 Deployment permissions
- `README.md` GitHub Pages setup uses `main` branch + `/docs`
- `docs/GITHUB_ACTIONS_AGENT.md` documents workflow runs and artifact uploads
- Dedicated deployment permission policy file for ChatGPT module: `ยังไม่พบหลักฐาน`

## 15. Directory Map

### 15.1 Requested directories
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/architecture/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/reports/`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocols/` → `ยังไม่พบหลักฐาน`

### 15.2 ChatGPT map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/ENTRANCE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/flow-lab/design-stack.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/prototypes/design-bridge.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/prototypes/live.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/testcases/test-harness.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/ux-sim/simulation-primitives.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/notes/design-decisions.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/notes/experiments-index.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/notes/mpcp.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/modules/ChatGPT/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/ChatGPT/modules/ChatGPT/requests/task001.md`

### 15.3 Gemini map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/ENTRANCE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/analysis-lab/experiment_template.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/dependency-map/system_map.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/logic-check/validation_protocol.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/notes/qa-issues.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/tasks/active_tasks.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/tasks/checkpoints.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Gemini/modules/Gemini/module.json`

### 15.4 DeepSeek map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/ENTRANCE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/meta-structure/structure-map.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/notes/observation-log.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/studio/core/meta-architecture-map.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/DeepSeek/modules/DeepSeek/module.json`

### 15.5 Grok map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/ENTRANCE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/base.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/insight-vault/incidents.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/pattern-scan/latest_scan_20251201.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/risk-mitigation/deepseek_downtime.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Grok/modules/Grok/module.json`

### 15.6 Copilot-Gm map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/ENTRANCE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/LOCKED.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/repo-lock.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/governance/repo-lock.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/workspace/onboarding/checklist.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/modules/Copilot-Gm/reports/.gitkeep`

### 15.7 Docs / architecture / reports map
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/index.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/system.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/rules.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/state.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/protocol.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/context.map.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/review/MPCP_STATUS_SSOT.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/architecture/W3_MASTER_ARCHITECTURE.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/architecture/system-map.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/reports/module_health.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/reports/registry_audit.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/reports/full_structure_audit.md`

## 16. Existing Protocol Files

### 16.1 Manifest
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/manifest.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/governance/module-manifest-policy.md`

### 16.2 Governance
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/governance/operating-guidelines.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/governance/rules/w3_ruleset.yml`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/AGENT_RULES_AND_MEMORY.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/governance/decision_trace.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Copilot-Gm/ENTRANCE.md`

### 16.3 Invocation
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/protocol.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/README.md` (Module Invocation Protocol L0)
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/events/event-protocol.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/module-registry.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/router.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/tools/w3run.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/runtime/executor.py`

### 16.4 Memory
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/memory/memory_bus.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/memory/memory_store.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Cast/context/protocol.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/Cast/context/session_summary.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/knowledge/SESSION_LOG.md`

### 16.5 Audit
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/.github/workflows/w3_agent_ci.yml`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/GITHUB_ACTIONS_AGENT.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/tools/w3_agent_ci.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/tools/run_audit.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/iget/README.md`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/docs/guides/PR_Flow_Table.md`

### 16.6 Module contracts
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/BBX19/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/BBEX-Core/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/ChatGPT/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Gemini/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Grok/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/DeepSeek/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Copilot-Gm/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/modules/Cast/module.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/module-loader/idp-schema.json`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/protocol/mpcp/kernel/contract.py`
- `/home/runner/work/W3_HB_team_BXCGICOG/W3_HB_team_BXCGICOG/core/events/event-schema.json`

## 17. Current Operational Objective

### 17.1 Current active milestone / focus
- `docs/state.json`: `active_focus = build_and_stabilize`
- `README.md` roadmap:
  - `v0.2 → normalize modules`
  - `v0.3 → activate test runners`
  - `v0.4 → CI for knowledge flows`
- `DeepSeek/ENTRANCE.md`: `Phase-1`
- `DeepSeek/notes/observation-log.md`: `Phase-1 baseline observation`

### 17.2 Current critical tasks
- `Gemini/tasks/active_tasks.md`:
  - analyze latest `src/` structure and update dependency map
  - validate `metadata-schema.yaml`
  - daily logs watch
  - build automated test script for logic check
  - monthly risk report
- `README.md` immediate roadmap items in `W3_MASTER_MAP.md`:
  - naming standard
  - separate core/runtime/control folders
  - G-State prototype
  - Notion ↔ local files bridge
  - memory sync

### 17.3 Blocked systems / blocked flows
- `Gemini/tasks/checkpoints.md`: `ถ้าไม่มี checkpoint → ห้าม merge`
- `Gemini/notes/qa-issues.md`: persistent memory not working across all agents
- `REPORT_REPO_AUDIT_FULL.txt`: unprotected `main` branch; cleanup required before `v0.3`
- `ChatGPT/ENTRANCE.md`: no merge for flow without test-case; no prototype use without simulation

### 17.4 Expected next phase
- `README.md`: next named phase after `v0.2` is `v0.3 → activate test runners`
- `REPORT_REPO_AUDIT_FULL.txt`: `v0.3 goal ("activate test runners")`
- `DeepSeek/notes/observation-log.md`: next step = `start cross-module dependency analysis` when enough ChatGPT flow-lab patterns exist
