# Cleanup Plan (Proposal Only — No Execution)
**Repository:** W3_HB_team_BXCGICOG  
**Date:** 2026-04-25  
**Mode:** RMB / SAFE-MAINTENANCE / NON-DESTRUCTIVE  
**Agent:** Copilot-Gm  
**Authority Required:** BBX19  

> ⚠️ **This is a recommendation document only.**  
> No files have been moved, renamed, or deleted.  
> All actions below require explicit BBX19 approval before execution.

---

## Priority Legend

| Symbol | Priority |
|--------|----------|
| 🔴 | CRITICAL — Affects runtime or registry integrity |
| 🟡 | MEDIUM — Affects consistency and discoverability |
| 🟢 | LOW — Cosmetic or organizational improvement |

---

## Plan A: Fix Typo Directory

**Priority:** 🔴 CRITICAL  
**Effort:** Low  

| Step | Action |
|------|--------|
| A1 | Move `YSTEM/TESTS/MPCP/W3_TERMS_MASTER_PAPER_v2.md` → `SYSTEM/TESTS/MPCP/W3_TERMS_MASTER_PAPER_v2.md` |
| A2 | Remove empty `YSTEM/` directory after move |

**Reason:** `YSTEM/` is a typo of `SYSTEM/` causing orphaned content.

---

## Plan B: Fix Runtime Registry Paths

**Priority:** 🔴 CRITICAL  
**Effort:** Medium  

Two options:

### Option B1 — Move module.json files to top of each module dir (recommended)

| Step | Action |
|------|--------|
| B1.1 | Copy `BBX19/modules/BBX19/module.json` → `BBX19/module.json` |
| B1.2 | Copy `ChatGPT/modules/ChatGPT/module.json` → `ChatGPT/module.json` |
| B1.3 | Copy `Gemini/modules/Gemini/module.json` → `Gemini/module.json` |
| B1.4 | Copy `Grok/modules/Grok/module.json` → `Grok/module.json` |
| B1.5 | Copy `DeepSeek/modules/DeepSeek/module.json` → `DeepSeek/module.json` |
| B1.6 | Rename+copy `Cast/modules/Cast.json` → `Cast/module.json` |
| B1.7 | Copy `BBEX-Core/public/module.json` → `BBEX-Core/module.json` |
| B1.8 | Update `src/modules/registry/registry.json` to reflect corrected paths |

### Option B2 — Update registry to match current file locations

| Step | Action |
|------|--------|
| B2.1 | Update `src/modules/registry/registry.json` `path` fields to match actual nested locations |

**Recommendation:** B1 — standardizes the pattern across all modules.

---

## Plan C: Fix Cast Module

**Priority:** 🔴 CRITICAL  
**Effort:** Low  

| Step | Action |
|------|--------|
| C1 | Rename `Cast/modules/Cast.json` → `Cast/modules/Cast/module.json` (standard nested path) |
| C2 | Create top-level `Cast/module.json` symlink or copy for registry compatibility |
| C3 | Complete 3 required trial tasks (human action) to graduate Cast from `trial` → `stable` |

---

## Plan D: Fix BBEX-Core Missing Docs

**Priority:** 🟡 MEDIUM  
**Effort:** Low  

| Step | Action |
|------|--------|
| D1 | Create `BBEX-Core/README.md` — summary of module purpose, links to public/ and private/ |
| D2 | Create `BBEX-Core/ENTRANCE.md` — entry instructions consistent with other modules |
| D3 | Create `BBEX-Core/self-review.md` — self-assessment document |
| D4 | Create `BBEX-Core/logs/` directory with `.gitkeep` |

---

## Plan E: Resolve Governance File Conflict

**Priority:** 🟡 MEDIUM  
**Effort:** Low  

| Step | Action |
|------|--------|
| E1 | Rename top-level `governance` (plain text file) → `GOVERNANCE_PRINCIPLES.md` |
| E2 | Move to `core/governance/GOVERNANCE_PRINCIPLES.md` |
| E3 | Add reference in `core/governance/README.md` |

**Reason:** A plain file named `governance` conflicts with the `core/governance/` directory pattern.

---

## Plan F: Remove Duplicate Root PNG

**Priority:** 🟡 MEDIUM  
**Effort:** Trivial  

| Step | Action |
|------|--------|
| F1 | Confirm `file_000000001e7c72088554e0c1715f55b2.png` at root == `architecture/diagrams/` copy |
| F2 | Remove root copy (`/file_000000001e7c72088554e0c1715f55b2.png`) |

**Saves:** ~1.9 MB from repo root.

---

## Plan G: Fix Spaces in Directory Names

**Priority:** 🟡 MEDIUM  
**Effort:** Medium (requires git mv)  

| Step | Old Path | New Path |
|------|----------|----------|
| G1 | `modules/DTML /` | `modules/DTML/` |
| G2 | `SYSTEM/TESTS/BBX19/ARCHITECTURE /` | `SYSTEM/TESTS/BBX19/ARCHITECTURE/` |
| G3 | `SYSTEM/TESTS/BBX19/COMMUNITY /` | `SYSTEM/TESTS/BBX19/COMMUNITY/` |
| G4 | `SYSTEM/TESTS/BBX19/GOVERNANCE /` | `SYSTEM/TESTS/BBX19/GOVERNANCE/` |
| G5 | `SYSTEM/TESTS/BBX19/LAB_RULES/CIVILIZATION /` | `SYSTEM/TESTS/BBX19/LAB_RULES/CIVILIZATION/` |
| G6 | `SYSTEM/TESTS/BBX19/SYSTEM /` | `SYSTEM/TESTS/BBX19/SYSTEM/` |

---

## Plan H: Move Misplaced Root Files

**Priority:** 🟢 LOW  
**Effort:** Low  

| Step | File | Proposed New Location |
|------|------|-----------------------|
| H1 | `init_test.ts` | `SYSTEM/TESTS/init_test.ts` |
| H2 | `requirements.txt` | `src/requirements.txt` (or document purpose) |
| H3 | `resume_header.json` | `meta/resume_header.json` |
| H4 | `resume_header.schema.json` | `meta/resume_header.schema.json` |
| H5 | `executions_log.json` | `logs/executions_log.json` |
| H6 | `portal.html` | `docs/portal.html` |
| H7 | `REPORT_REPO_AUDIT_FULL.txt` | `docs/audits/REPORT_REPO_AUDIT_FULL.txt` |
| H8 | `1.md` | Review content; rename descriptively or archive to `docs/audits/` |

---

## Plan I: Remove Structural Ghosts

**Priority:** 🟢 LOW  
**Effort:** Trivial  

| Step | Action |
|------|--------|
| I1 | Remove `Gemini/Gemini/` (empty nested self-directory) |
| I2 | Review `knowledge/knowledge/` — consolidate into `knowledge/` or rename to `knowledge/content/` |
| I3 | Remove `blueprints/abstract/overview/placeholder.md` — `overview.md` file serves same purpose |

---

## Plan J: Fix Output Path Aliases in module.json

**Priority:** 🟢 LOW  
**Effort:** Medium (edit 5+ files)  

Multiple module.json files reference `outcomes/append_only_ledger/` but actual dir is `outcomes/ledger/`.

| Step | Action |
|------|--------|
| J1 | Update `BBX19/modules/BBX19/module.json` — change `outcomes/append_only_ledger/` → `outcomes/ledger/` |
| J2 | Update `BBEX-Core/public/module.json` — same fix |
| J3 | Audit other module.json files for same mismatch |

---

## Plan K: Consolidate Duplicate Documentation

**Priority:** 🟢 LOW  
**Effort:** High (requires content review)  

| Duplication | Proposed Resolution |
|-------------|---------------------|
| `QUICK_START.md` (root) vs `docs/QUICK_START.md` | Keep `docs/QUICK_START.md`; add redirect note in root version |
| `manifesto-2.md` vs `docs/manifesto-3.md` | Archive `manifesto-2.md` to `docs/audits/` |
| `core/logs/system_log.schema.json` vs `core/logs/systemlogschema.json` | Confirm which is canonical; remove duplicate |
| 6+ audit report files at root | Move all to `docs/audits/` |

---

## Plan L: Archive Legacy Content

**Priority:** 🟢 LOW  
**Effort:** Medium  

| Step | Content | Action |
|------|---------|--------|
| L1 | `versions/v0.1/` | Already in versions — add README explaining this is snapshot archive |
| L2 | `Hybrid-Management-Model/` | Review; if superseded by `core/hybrid-model/`, move to `docs/audits/` |
| L3 | `SYSTEM/TESTS/MPCP/` docs | Review if superseded by W3Lgu standard; archive if so |
| L4 | Old daily log entries | No action needed; maintain as historical record |

---

## Plan M: Create Missing Runtime Schema

**Priority:** 🟡 MEDIUM  
**Effort:** Low  

| Step | Action |
|------|--------|
| M1 | Create `src/modules/standards/module.schema.json` OR remove reference from `src/modules/registry/registry.json` |

Currently the runtime registry declares a schema that does not exist, breaking schema validation tools.

---

## Execution Order (If Approved)

If BBX19 approves execution, recommended order:

```
1. Plan A  — Fix YSTEM typo
2. Plan C  — Fix Cast module.json
3. Plan B  — Fix runtime registry paths
4. Plan E  — Fix governance file conflict
5. Plan D  — Add BBEX-Core missing docs
6. Plan G  — Fix spaces in directory names
7. Plan F  — Remove duplicate PNG
8. Plan M  — Create missing schema
9. Plan J  — Fix output path aliases
10. Plan H  — Move misplaced root files
11. Plans I, K, L — Cleanup ghosts, docs, legacy
```

---

## Estimated Impact

| Plan | Files Affected | Risk | Requires Human Review |
|------|---------------|------|----------------------|
| A | 1 file move, 1 dir delete | Low | Yes |
| B | 7 file copies + 1 registry update | Medium | Yes |
| C | 1 rename + 1 new file | Low | Yes |
| D | 4 new files | Low | Yes |
| E | 1 rename + 1 move | Low | Yes |
| F | 1 file delete | Low | Yes |
| G | 6 dir renames | Medium | Yes |
| H | 8 file moves | Low | Yes |
| I | 2-3 removals | Low | Yes |
| J | 2-3 file edits | Low | Yes |
| K | Content review | High | Yes |
| L | Content review | Medium | Yes |
| M | 1 new file | Low | No (can auto-generate) |

---

*Generated by Copilot-Gm | W3 Cleanup Plan 2026-04-25 | PROPOSAL ONLY — NO EXECUTION*
