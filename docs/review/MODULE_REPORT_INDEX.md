# Module Report Index

- Generated: 2026-05-09
- Scope: index of core W3 module reports and relationships
- Rule: factual only; when evidence is missing, use `ยังไม่พบหลักฐาน`

## 1. Purpose
This file is the navigation index for core W3 module-level operational reports.
It exists to reduce complexity in the central SSOT by separating:
- central status summary
- per-module operational detail
- cross-module navigation

## 2. Core Modules

| Module | Role | Status | Primary Function |
|---|---|---|---|
| `BBX19` | Final Authority / Vision Keeper | `ready` | root authority / final sign-off |
| `BBEX-Core` | Identity / Philosophical Anchor | `partial` | identity / philosophical anchor |
| `ChatGPT` | Architecture / Flow / Execution | `partial` | flow / prototype / execution design |
| `Gemini` | Validation / Cross Check | `ready` | validation / consistency / audit |
| `Grok` | Pattern / Signals / Insight | `partial` | pattern / narrative / hidden signal interpretation |
| `DeepSeek` | Scale / Long-Term Planning | `partial` | long-term planning / baseline architecture |
| `Copilot-Gm` | Policy / Merge / Compliance | `ready` | governance / structure / merge compliance |
| `Cast` | Deep Reasoning / Structural Adaptation / Decision Support | `partial-active` | context bridge / structural augmentation / adaptive reasoning / continuity support |

## 3. Module Report Links

| Module | Report Path | Status | Notes |
|---|---|---|---|
| `BBX19` | `modules/BBX19/reports/bbx19_operational_report.md` | `available` | operational baseline created |
| `BBEX-Core` | `modules/BBEX-Core/reflections/bbex_core_operational_report.md` | `available` | workspace path follows current module structure |
| `ChatGPT` | `modules/ChatGPT/reports/chatgpt_operational_report.md` | `available` | operational baseline created |
| `Gemini` | `modules/Gemini/reports/gemini_operational_report.md` | `available` | operational baseline created |
| `Grok` | `modules/Grok/risk-reports/grok_operational_report.md` | `available` | stored under `risk-reports/` per current workspace layout |
| `DeepSeek` | `modules/DeepSeek/plans/deepseek_operational_report.md` | `available` | stored under `plans/` to match planning role |
| `Copilot-Gm` | `modules/Copilot-Gm/reports/copilot_gm_operational_report.md` | `available` | operational baseline created |
| `Cast` | `modules/Cast/reports/cast_operational_report.md` | `available` | operational baseline created |

## 4. Cross-Module Navigation

### 4.1 Authority Path
`BBX19` �� all modules

### 4.2 Validation Path
`ChatGPT` → `Gemini`  
`Grok` → `Gemini`  
`DeepSeek` → `Gemini` (case-based)  
`Copilot-Gm` → `Gemini` (governance/config validation)

### 4.3 Governance Path
`ChatGPT` → `Copilot-Gm`  
`Grok` → `Copilot-Gm` (governance conflict)  
`Copilot-Gm` → `BBX19`

### 4.4 Context / Memory Path
`Cast` → all modules

### 4.5 Identity / Meaning Path
`BBEX-Core` → `BBX19` → system-wide interpretation anchor

## 5. Recommended Reading Order
For fast operational understanding:

1. `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.th.md`
2. `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.md`
3. `docs/review/MODULE_REPORT_INDEX.md`
4. per-module reports as needed

For governance-related work:

1. `modules/BBX19/reports/bbx19_operational_report.md`
2. `modules/Gemini/reports/gemini_operational_report.md`
3. `modules/Copilot-Gm/reports/copilot_gm_operational_report.md`

For flow / execution work:

1. `modules/ChatGPT/reports/chatgpt_operational_report.md`
2. `modules/Gemini/reports/gemini_operational_report.md`
3. `modules/Copilot-Gm/reports/copilot_gm_operational_report.md`

For context / continuity issues:

1. `modules/Cast/reports/cast_operational_report.md`
2. `modules/BBX19/reports/bbx19_operational_report.md`
3. relevant working module report

## 6. Next Build Steps
1. Keep the central SSOT short and summary-focused
2. Review cross-module inconsistencies and update module reports when evidence changes
3. Add review metadata later if needed: `reviewed_on`, `reviewed_by`, `next_review_trigger`
4. Maintain this index whenever report paths or module roles change

## 7. Related Files
- `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.md`
- `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.th.md`
- `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.json`

## 8. Evidence Base
- `modules/ChatGPT/reports/2026-05-09_w3_mpcp_operational_structure_report.md`
- `core/module-loader/module-registry.json`
- `modules/*/module.json`
- `*/ENTRANCE.md`
- `Cast/context/protocol.md`
- `core/governance/operating-guidelines.md`
