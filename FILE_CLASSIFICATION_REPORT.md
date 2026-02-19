# W3 File Classification Report

**Purpose:** Analyze the repository from an outsider perspective and classify every significant file.

**Authority:** BBX19  
**Generated:** 2026-02-19  
**Classification Scheme:**
- `[PUBLIC OK]` — Safe for external/public access; no sensitive information
- `[INTERNAL ONLY]` — Team-internal; reveals operational patterns, workflows, or design intent that should not leave the team
- `[PRIVATE REQUIRED]` — Must not be publicly accessible; contains personal details, core identity, system secrets, or sensitive ledger/config data

---

## 1. Root-Level Files

| File | Classification | Reason |
|------|----------------|---------|
| `README.md` | [PUBLIC OK] | High-level overview, intentionally public-facing |
| `CHANGELOG.md` | [PUBLIC OK] | Version history for public release tracking |
| `QUICK_START.md` | [PUBLIC OK] | Public onboarding guide |
| `USER_SUMMARY.md` | [INTERNAL ONLY] | Describes internal tool usage patterns |
| `AGENT_TASKS.md` | [INTERNAL ONLY] | Reveals internal agent task assignment model |
| `BBEX_Reflection.md` | [INTERNAL ONLY] | Internal philosophical reflection on system design intent |
| `AUDIT_ARCHITECTURE.md` | [INTERNAL ONLY] | Exposes internal audit agent architecture and escalation paths |
| `AUDIT_COMPLETION_SUMMARY.md` | [INTERNAL ONLY] | Internal audit status and findings |
| `AUDIT_SYSTEM_README.md` | [INTERNAL ONLY] | Internal audit system documentation |
| `INTEGRITY_REPORT_TH.md` | [INTERNAL ONLY] | Internal integrity scan output |
| `W3_SANITY_SWEEP_REPORT.md` | [INTERNAL ONLY] | Full internal structural sweep report |
| `W3_SANITY_SWEEP_SUMMARY.md` | [INTERNAL ONLY] | Summary of internal sweep findings |
| `DTML_Report.md` | [INTERNAL ONLY] | Internal security scan results |
| `PR_Flow_Table.md` | [INTERNAL ONLY] | Exposes internal PR routing and decision logic |
| `REDR_Structure_Map.md` | [INTERNAL ONLY] | Full repository structure map for internal navigation |
| `LINE_B_GPT.md` | [INTERNAL ONLY] | Internal protocol notes and GPT interaction patterns |
| `decision_trace.md` | [INTERNAL ONLY] | Traces internal governance decisions with full reasoning |
| `executions_log.json` | [INTERNAL ONLY] | System execution audit log with event history |
| `manifesto-2.md` | [INTERNAL ONLY] | Internal philosophical manifesto — design intent document |
| `1.md` | [INTERNAL ONLY] | Raw internal notes |
| `portal.html` | [PUBLIC OK] | Public-facing HTML portal page |
| `resume_header.json` | [INTERNAL ONLY] | Contains personal identity/profile data |
| `resume_header.schema.json` | [INTERNAL ONLY] | Schema for personal profile data |

---

## 2. `BBEX-Core/` — Core Philosophy Module

| File | Classification | Reason |
|------|----------------|---------|
| `BBEX-Core/PROTOCOL_HYBRID.md` | [INTERNAL ONLY] | Hybrid access protocol for the core module |
| `BBEX-Core/private/ESSENCE.md` | [PRIVATE REQUIRED] | Explicitly restricted to BBX19 only; core personal decree and philosophy |
| `BBEX-Core/private/BBEX_CORE_IDP.md` | [PRIVATE REQUIRED] | Inner Sanctum identity document; BBX19-only; reveals philosophical foundations and personal commitments |
| `BBEX-Core/public/BBEX_CORE_IDP.md` | [INTERNAL ONLY] | Shared summary of core philosophy for team use; contains detailed internal architecture |
| `BBEX-Core/public/module.json` | [INTERNAL ONLY] | Module manifest for internal orchestration |
| `BBEX-Core/public/request_template.json` | [INTERNAL ONLY] | Internal request template revealing access protocol design |

---

## 3. `BBX19/` — Root Authority Module

| File | Classification | Reason |
|------|----------------|---------|
| `BBX19/ENTRANCE.md` | [PUBLIC OK] | Module entry point overview |
| `BBX19/README.md` | [PUBLIC OK] | Module public documentation |
| `BBX19/directives/base.md` | [INTERNAL ONLY] | Internal directives and operating base rules |
| `BBX19/self-review.md` | [INTERNAL ONLY] | Internal self-assessment reveals thinking patterns |
| `BBX19/status/human-status.json` | [PRIVATE REQUIRED] | Contains personal status data for BBX19 (the human founder) |
| `BBX19/modules/BBX19/module.json` | [INTERNAL ONLY] | Module registry and internal metadata |
| `BBX19/modules/BBX19/idp/INDEX.md` | [INTERNAL ONLY] | Index of all identity cards; reveals team structure |
| `BBX19/modules/BBX19/idp/BBX19-IDP.md` | [PRIVATE REQUIRED] | Contains personal details: work constraints (รพ.), financial constraints, device limitations — should never be public |
| `BBX19/modules/BBX19/idp/ChatGPT-IDP.md` | [INTERNAL ONLY] | Internal AI module identity card |
| `BBX19/modules/BBX19/idp/Copilot-Gm-IDP.md` | [INTERNAL ONLY] | Internal AI module identity card |
| `BBX19/modules/BBX19/idp/DeepSeek-IDP.md` | [INTERNAL ONLY] | Internal AI module identity card |
| `BBX19/modules/BBX19/idp/Gemini-IDP.md` | [INTERNAL ONLY] | Internal AI module identity card |
| `BBX19/modules/BBX19/idp/Grok-IDP.md` | [INTERNAL ONLY] | Internal AI module identity card |
| `BBX19/modules/BBX19/context/chatgpt_context.json` | [INTERNAL ONLY] | Internal AI context configuration |
| `BBX19/modules/BBX19/context/chatgpt_context2.json` | [INTERNAL ONLY] | Internal AI context configuration |

---

## 4. `architecture/` — System Architecture

| File | Classification | Reason |
|------|----------------|---------|
| `architecture/overview.md` | [PUBLIC OK] | Intentionally designed as a "safe abstract"; contains only high-level component names |
| `architecture/system-map.md` | [INTERNAL ONLY] | Full operational flow: User → Module → Log → Merge → State; helps reverse-engineer how the system executes |
| `architecture/interface-map.md` | [INTERNAL ONLY] | Exposes inter-module interface connections |
| `architecture/layers.md` | [INTERNAL ONLY] | L0–L3 layer architecture; exposes authority hierarchy |
| `architecture/base.md` | [INTERNAL ONLY] | Base architecture reference |
| `architecture/standards.md` | [INTERNAL ONLY] | Internal standards for system design |
| `architecture/diagrams/placeholder.md` | [PUBLIC OK] | Placeholder only; no sensitive content |

---

## 5. `blueprints/` — Abstract System Blueprints

| File | Classification | Reason |
|------|----------------|---------|
| `blueprints/abstract/overview.md` | [PUBLIC OK] | High-level overview; intentionally abstract |
| `blueprints/abstract/root-model-abstract.md` | [PUBLIC OK] | Explicitly designed as a "safe version" with sensitive logic hidden |
| `blueprints/abstract/ecosystem-outline.md` | [INTERNAL ONLY] | More detailed ecosystem structure than the public overview |
| `blueprints/abstract/blueprints/NETWORK.md` | [INTERNAL ONLY] | Network blueprint reveals internal topology concepts |
| `blueprints/abstract/blueprints/W3CON.md` | [INTERNAL ONLY] | W3 connection blueprint; reveals design intent |

---

## 6. `branding/` — Brand Assets

| File | Classification | Reason |
|------|----------------|---------|
| `branding/guidelines/brand-guideline.md` | [PUBLIC OK] | Public brand guideline |
| `branding/guidelines/color-palette.md` | [PUBLIC OK] | Public color palette |
| `branding/guidelines/usage-rules.md` | [PUBLIC OK] | Public usage rules |
| `branding/logo/*` | [PUBLIC OK] | Public logo assets |
| `branding/icons/*` | [PUBLIC OK] | Public icon assets |

---

## 7. `core/` — Core System

| File | Classification | Reason |
|------|----------------|---------|
| `core/guardrails.md` | [INTERNAL ONLY] | Defines internal operational guardrails |
| `core/versioning.md` | [INTERNAL ONLY] | Internal versioning strategy |
| `core/decisions/DR-001.md` | [INTERNAL ONLY] | Formal decision record; reveals architectural decision-making process |
| `core/governance/README.md` | [INTERNAL ONLY] | Governance index |
| `core/governance/awareness-baseline.md` | [INTERNAL ONLY] | Exposes internal awareness thresholds and cognitive baseline |
| `core/governance/compass.md` | [INTERNAL ONLY] | Internal directional compass for decision-making |
| `core/governance/decisions.md` | [INTERNAL ONLY] | Internal governance decision log |
| `core/governance/operating-guidelines.md` | [INTERNAL ONLY] | Full internal operational rules; exposes communication channels and override hierarchy |
| `core/governance/phase2-framework.md` | [INTERNAL ONLY] | Internal roadmap and phase planning |
| `core/governance/policies.md` | [INTERNAL ONLY] | Internal governance policies |
| `core/hybrid-model/README.md` | [INTERNAL ONLY] | Hybrid model documentation |
| `core/hybrid-model/insights.md` | [INTERNAL ONLY] | Internal operational insights |
| `core/hybrid-model/responsibilities.md` | [INTERNAL ONLY] | Module responsibility matrix |
| `core/hybrid-model/system-foundations.md` | [INTERNAL ONLY] | Team composition and system capability map |
| `core/hybrid-model/vision.md` | [INTERNAL ONLY] | Internal vision document; reveals design intent |
| `core/logs/system_log.json` | [INTERNAL ONLY] | System activity log |
| `core/logs/simulation_test_01.json` | [INTERNAL ONLY] | Simulation test output; reveals test scenarios |
| `core/logs/system_log.schema.json` | [INTERNAL ONLY] | Log schema; reveals data model |
| `core/logs/systemlogschema.json` | [INTERNAL ONLY] | Duplicate log schema |
| `core/logs/templates/log_entry.md` | [INTERNAL ONLY] | Log entry template |
| `core/logs/rotations/rotation_policy.md` | [INTERNAL ONLY] | Log rotation policy |
| `core/logs/guardrails.md` | [INTERNAL ONLY] | Log guardrails |
| `core/logs/versioning.md` | [INTERNAL ONLY] | Log versioning policy |
| `core/standards/README.md` | [INTERNAL ONLY] | Internal standards index |
| `core/templates/log_entry.md` | [INTERNAL ONLY] | Template for internal logging |
| `core/vault/w3_internal_ledger.json` | [PRIVATE REQUIRED] | Internal resource/credit ledger; exposes service cost model and system economic structure |

---

## 8. `docs/` — Documentation Layer

| File | Classification | Reason |
|------|----------------|---------|
| `docs/index.html` | [PUBLIC OK] | Public-facing HTML page |
| `docs/index.md` | [PUBLIC OK] | Public documentation index |
| `docs/index.json` | [PUBLIC OK] | Public document index |
| `docs/protocol.md` | [PUBLIC OK] | Public interaction protocol |
| `docs/manifesto-3.md` | [INTERNAL ONLY] | Team manifesto; reveals internal values and operational intent |
| `docs/context.map.json` | [INTERNAL ONLY] | Maps internal context scopes and load policies; exposes AI audience segmentation |
| `docs/modules.json` | [INTERNAL ONLY] | Module registry; exposes full module list and metadata |
| `docs/state.json` | [INTERNAL ONLY] | Live system state; exposes operational mode and alert level |
| `docs/mirror.policy.json` | [INTERNAL ONLY] | Defines public/private split policy; reveals what is intentionally hidden |
| `docs/blank-template.md` | [PUBLIC OK] | Empty template |
| `docs/sample-report.md` | [PUBLIC OK] | Example report with no sensitive content |
| `docs/audit-checklist.md` | [INTERNAL ONLY] | Internal audit process checklist |
| `docs/audits/2025-12-10-audit.md` | [INTERNAL ONLY] | Internal audit record |
| `docs/audits/templates/blank-template.md` | [PUBLIC OK] | Empty template |
| `docs/announcement/announcement-3.md` | [PUBLIC OK] | Official public announcement |
| `docs/review/COMPLETION_STATUS.md` | [INTERNAL ONLY] | Internal PR review completion status |
| `docs/review/PR83_MANUAL_STEPS.md` | [INTERNAL ONLY] | Internal PR review steps; exposes review workflow |
| `docs/review/PR83_review_summary.md` | [INTERNAL ONLY] | Internal PR review summary |
| `docs/agent.profile.json` | [PRIVATE REQUIRED] | Explicitly marked private in `mirror.policy.json`; defines AI agent behavior profiles and context scopes |
| `docs/rules.json` | [PRIVATE REQUIRED] | Explicitly marked private in `mirror.policy.json`; defines authority model, boundaries, and token policy |
| `docs/system.json` | [PRIVATE REQUIRED] | Explicitly marked private in `mirror.policy.json`; exposes system name, owner, operation mode, and AI behavior config |
| `docs/snapshot.json` | [PRIVATE REQUIRED] | Explicitly marked private in `mirror.policy.json`; system baseline snapshot |
| `docs/version.policy.json` | [PRIVATE REQUIRED] | Explicitly marked private in `mirror.policy.json`; internal versioning policy and update rules |

---

## 9. `Hybrid-Management-Model/`

| File | Classification | Reason |
|------|----------------|---------|
| `Hybrid-Management-Model/team-doctrine.md` | [INTERNAL ONLY] | Operational doctrine; exposes decision-making philosophy and escalation model |
| `Hybrid-Management-Model/system-self-state.md` | [INTERNAL ONLY] | System self-assessment state; reveals current operational awareness |

---

## 10. `knowledge/` — Knowledge Base

| File | Classification | Reason |
|------|----------------|---------|
| `knowledge/README.md` | [INTERNAL ONLY] | Knowledge base overview |
| `knowledge/_rules.md` | [INTERNAL ONLY] | Internal rules for knowledge base usage |
| `knowledge/rules.md` | [INTERNAL ONLY] | Internal operational rules |
| `knowledge/patterns.md` | [INTERNAL ONLY] | Exposes observed operational patterns |
| `knowledge/memory_bank.json` | [PRIVATE REQUIRED] | System memory storage; designed to accumulate sensitive context over time |
| `knowledge/narratives/origin.md` | [INTERNAL ONLY] | Origin story; reveals design thinking and founding intent |
| `knowledge/apps_manual/INDEX.md` | [INTERNAL ONLY] | Internal app manual index |
| `knowledge/apps_manual/android/github.md` | [INTERNAL ONLY] | Internal usage guide for GitHub Android app |
| `knowledge/knowledge/index.md` | [INTERNAL ONLY] | Inner knowledge index |

---

## 11. `logs/` — System Logs

| File | Classification | Reason |
|------|----------------|---------|
| `logs/daily/2025-12-10.context.md` | [INTERNAL ONLY] | Daily operational context log |
| `logs/observations/2025-12-10-observe-01.md` | [INTERNAL ONLY] | Internal observation record |
| `logs/logs-usage/logs-usage.md` | [INTERNAL ONLY] | Documents how logging is used internally |

---

## 12. AI Module Directories (ChatGPT, DeepSeek, Gemini, Grok, Copilot-Gm)

| File Pattern | Classification | Reason |
|------|----------------|---------|
| `*/ENTRANCE.md` | [PUBLIC OK] | Entry point overview; intentionally accessible |
| `*/README.md` | [PUBLIC OK] | Module public documentation |
| `*/self-review.md` | [INTERNAL ONLY] | Internal self-assessment; reveals thinking patterns and weaknesses |
| `*/modules/*/module.json` | [INTERNAL ONLY] | Internal module manifests |
| `ChatGPT/flow-lab/*` | [INTERNAL ONLY] | Internal design flow documents |
| `ChatGPT/prototypes/*` | [INTERNAL ONLY] | Internal prototype designs |
| `ChatGPT/testcases/*` | [INTERNAL ONLY] | Internal test harness |
| `ChatGPT/ux-sim/*` | [INTERNAL ONLY] | Internal UX simulation primitives |
| `ChatGPT/modules/ChatGPT/boundaries.md` | [INTERNAL ONLY] | Exposes module operational boundaries |
| `DeepSeek/studio/core/meta-architecture-map.md` | [INTERNAL ONLY] | Internal architecture map; helps reverse-engineer system |
| `DeepSeek/studio/core/pattern-hub.md` | [INTERNAL ONLY] | Internal pattern recognition hub |
| `DeepSeek/studio/core/anomaly-radar.md` | [INTERNAL ONLY] | Internal anomaly detection design |
| `DeepSeek/studio/core/consciousness-feed.md` | [INTERNAL ONLY] | Internal cognitive feed design |
| `DeepSeek/studio/wisdom/philosophy-manifesto/*` | [INTERNAL ONLY] | Internal ethical framework and philosophy |
| `DeepSeek/studio/wisdom/narrative-core/origin-story.md` | [INTERNAL ONLY] | Internal narrative revealing system origins |
| `DeepSeek/studio/collab/*` | [INTERNAL ONLY] | Internal collaboration protocols |
| `DeepSeek/studio/forge/*` | [INTERNAL ONLY] | Internal integration design patterns |
| `DeepSeek/meta-structure/structure-map.md` | [INTERNAL ONLY] | Internal structural map |
| `Gemini/dependency-map/system_map.md` | [INTERNAL ONLY] | Full system dependency map; directly enables architecture reverse-engineering |
| `Gemini/logic-check/validation_protocol.md` | [INTERNAL ONLY] | Internal validation logic |
| `Gemini/risk-scan/risk_register.md` | [INTERNAL ONLY] | Internal risk register; exposes known system vulnerabilities |
| `Gemini/reports/monthly_health_check.md` | [INTERNAL ONLY] | Internal health metrics |
| `Gemini/notes/analyst_notebook.md` | [INTERNAL ONLY] | Internal analyst notes |
| `Gemini/tasks/active_tasks.md` | [INTERNAL ONLY] | Internal task tracking |
| `Gemini/tasks/checkpoints.md` | [INTERNAL ONLY] | Internal milestone checkpoints |
| `Gemini/tools/validate_json.py` | [INTERNAL ONLY] | Internal validation tooling |
| `Grok/base.md` | [INTERNAL ONLY] | Grok base configuration and escalation rules |
| `Grok/insight-vault/*` | [INTERNAL ONLY] | Internal insights and incident records |
| `Grok/pattern-scan/*` | [INTERNAL ONLY] | Internal pattern scan results |
| `Grok/risk-mitigation/*` | [INTERNAL ONLY] | Internal risk mitigation plans |
| `Grok/oncall-board/emergency.md` | [INTERNAL ONLY] | Internal on-call emergency procedures |
| `Grok/action-tracker/todo.md` | [INTERNAL ONLY] | Internal action items |
| `Grok/notes/grok_self_notes.md` | [INTERNAL ONLY] | Internal self-reflection notes |
| `Grok/narrative/example_narrative.md` | [INTERNAL ONLY] | Internal narrative template |
| `Grok/interpret-lab/quick-test.md` | [INTERNAL ONLY] | Internal interpretation test |
| `Copilot-Gm/LOCKED.md` | [INTERNAL ONLY] | Governance lock documentation |
| `Copilot-Gm/governance/repo-lock.md` | [INTERNAL ONLY] | Repository lock governance rules |
| `Copilot-Gm/repo-lock.md` | [INTERNAL ONLY] | Duplicate repo lock rules |

---

## 13. `tools/` — Operational Tooling

| File | Classification | Reason |
|------|----------------|---------|
| `tools/README.md` | [INTERNAL ONLY] | Tool usage documentation |
| `tools/run_audit.py` | [INTERNAL ONLY] | Audit orchestrator; reveals full audit pipeline |
| `tools/dtml_security_scanner.py` | [INTERNAL ONLY] | Security scanner logic; exposes what patterns are checked |
| `tools/redr_structure_reader.py` | [INTERNAL ONLY] | Structure reader; exposes internal parsing approach |
| `tools/psp2_pr_router.py` | [INTERNAL ONLY] | PR routing logic; exposes merge decision workflow |
| `tools/lrc2_recorder.py` | [INTERNAL ONLY] | Log recorder; exposes logging architecture |
| `tools/bbex_core_anchor.py` | [INTERNAL ONLY] | Core anchor tool for BBEX philosophy module |
| `tools/memory_manager.py` | [INTERNAL ONLY] | Memory management; exposes knowledge storage patterns |
| `tools/file_integrity_check.py` | [INTERNAL ONLY] | File integrity tool |
| `tools/file_integrity_report.txt` | [INTERNAL ONLY] | File integrity scan output |
| `tools/send_integrity_report.py` | [INTERNAL ONLY] | Report sending mechanism; may expose communication channels |
| `tools/validate_json_schemas.py` | [INTERNAL ONLY] | JSON schema validation tool |
| `tools/validate_metadata.py` | [INTERNAL ONLY] | Metadata validation tool |
| `tools/validate_modules.py` | [INTERNAL ONLY] | Module validation tool |
| `tools/validate_runtime_log.py` | [INTERNAL ONLY] | Runtime log validation tool |

---

## 14. `src/` — Source Code

| File | Classification | Reason |
|------|----------------|---------|
| `src/main.py` | [INTERNAL ONLY] | Main source entry point |

---

## 15. `.github/` — Repository Configuration

| File | Classification | Reason |
|------|----------------|---------|
| `.github/CODEOWNERS` | [INTERNAL ONLY] | Exposes team ownership model |
| `.github/PULL_REQUEST_TEMPLATE.md` | [PUBLIC OK] | Standard PR template |
| `.github/ISSUE_TEMPLATE/decision-request.md` | [INTERNAL ONLY] | Reveals internal decision-request workflow |
| `.github/workflows/static.yml` | [PUBLIC OK] | Standard static site deploy workflow |
| `.github/workflows/validate-json.yml` | [INTERNAL ONLY] | Internal JSON validation pipeline |

---

## 16. `versions/` — Release Snapshots

| File | Classification | Reason |
|------|----------------|---------|
| `versions/v0.1/README.md` | [PUBLIC OK] | Public version documentation |
| `versions/v0.1/CHANGELOG.md` | [PUBLIC OK] | Public changelog |
| `versions/v0.1/modules/*.json` | [INTERNAL ONLY] | Module version snapshots; reveal internal module configuration at specific points in time |

---

## Summary by Classification

### [PRIVATE REQUIRED] — 11 files
These files **must not** remain publicly accessible. They contain personal data, secret configuration, or inner-sanctum philosophy restricted to BBX19:

1. `BBEX-Core/private/ESSENCE.md`
2. `BBEX-Core/private/BBEX_CORE_IDP.md`
3. `BBX19/modules/BBX19/idp/BBX19-IDP.md` ← personal details (employer, finances, device)
4. `BBX19/status/human-status.json`
5. `core/vault/w3_internal_ledger.json`
6. `docs/agent.profile.json`
7. `docs/rules.json`
8. `docs/system.json`
9. `docs/snapshot.json`
10. `docs/version.policy.json`
11. `knowledge/memory_bank.json`

### [INTERNAL ONLY] — ~100 files
Operational patterns, decision logs, module configs, architecture maps. Safe for team members but should not be shared publicly. Key files for architecture reverse-engineering:
- `architecture/system-map.md` — full execution flow
- `Gemini/dependency-map/system_map.md` — system dependency map
- `DeepSeek/studio/core/meta-architecture-map.md` — meta architecture
- `core/governance/operating-guidelines.md` — authority hierarchy
- `Hybrid-Management-Model/team-doctrine.md` — operational doctrine
- `decision_trace.md` — decision reasoning
- `docs/mirror.policy.json` — reveals the public/private split itself

### [PUBLIC OK] — ~30 files
Intentionally public: README files, ENTRANCE files, branding assets, abstract blueprints, public announcements, and docs explicitly mirrored to GitHub Pages.

---

## Recommended Actions

1. **Move `docs/agent.profile.json`, `docs/rules.json`, `docs/system.json`, `docs/snapshot.json`, `docs/version.policy.json`** to a private channel or local-only store as declared in `docs/mirror.policy.json`.
2. **Review `BBX19/modules/BBX19/idp/BBX19-IDP.md`** — personal details (healthcare employment, financial constraints, device type) should be removed from any public-facing repository.
3. **Review `BBX19/status/human-status.json`** — personal status data should not be in a public git history.
4. **Consider moving `BBEX-Core/private/`** to a separate private repository or encrypted local store, as the current `/private/` folder designation provides no actual access restriction in a public GitHub repo.
5. **`core/vault/w3_internal_ledger.json`** — even though it uses "W3_Credits" (not real currency), the service cost model and system structure it reveals should be kept private.
6. **Add `[INTERNAL ONLY]` or `[PRIVATE REQUIRED]` headers** to files in `docs/`, `core/vault/`, and `BBEX-Core/private/` to signal their access level within the team.

---

*This report was generated as part of the W3 repository analysis per the problem statement requirement to classify all files by exposure level.*
