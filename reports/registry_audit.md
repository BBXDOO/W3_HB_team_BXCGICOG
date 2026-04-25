# Registry Consistency Audit
**Repository:** W3_HB_team_BXCGICOG  
**Date:** 2026-04-25  
**Mode:** RMB / SAFE-MAINTENANCE  
**Agent:** Copilot-Gm  

---

## Overview

Two registry files exist in this repository:

| Registry | Path | Version | Role |
|----------|------|---------|------|
| Central Registry | `modules/registry.json` | 0.4.0 | Module routing, trust scores, coordination |
| Runtime Registry | `src/modules/registry/registry.json` | 2.0.0 | Path-based module loading for runtime |

Both must be audited for consistency against the actual folder structure.

---

## Section 1: Central Registry (`modules/registry.json` v0.4.0)

### Modules Listed

| Name | Channel | Folder Exists | Status |
|------|---------|---------------|--------|
| BBX19 | `/BBX19/` | ✅ YES | Consistent |
| BBEX-Core | `/BBEX-Core/` | ✅ YES | Consistent |
| ChatGPT | `/ChatGPT/` | ✅ YES | Consistent |
| Gemini | `/Gemini/` | ✅ YES | Consistent |
| Grok | `/Grok/` | ✅ YES | Consistent |
| DeepSeek | `/DeepSeek/` | ✅ YES | Consistent |
| Copilot-Gm | `/Copilot-Gm/` | ✅ YES | Consistent |
| Cast | `/Cast/` | ✅ YES | Consistent |

### Issues Found in Central Registry

| Field | Issue |
|-------|-------|
| `memory.decisions` | Points to `"/core/governance/decisions.md"` ✅ exists |
| `memory.logs` | Points to `"/logs/"` ✅ exists |
| `memory.knowledge` | Points to `"/knowledge/"` ✅ exists |
| `memory.outcomes` | Points to `"/outcomes/"` ✅ exists |
| **Missing modules** | None — all 8 are registered |
| **Ghost modules** | None detected |
| **Path conflicts** | None between channel paths |

**Assessment:** Central registry is internally consistent. All channels map to existing folders. ✅

---

## Section 2: Runtime Registry (`src/modules/registry/registry.json` v2.0.0)

### Module Path Reference Check

The runtime registry uses `path` field pointing to module.json files. Each is checked against actual filesystem:

| Module ID | Declared Path | Actual module.json Location | Match? |
|-----------|--------------|----------------------------|--------|
| `bbx19` | `/BBX19/module.json` | `BBX19/modules/BBX19/module.json` | ❌ MISMATCH |
| `chatgpt` | `/ChatGPT/module.json` | `ChatGPT/modules/ChatGPT/module.json` | ❌ MISMATCH |
| `gemini` | `/Gemini/module.json` | `Gemini/modules/Gemini/module.json` | ❌ MISMATCH |
| `grok` | `/Grok/module.json` | `Grok/modules/Grok/module.json` | ❌ MISMATCH |
| `deepseek` | `/DeepSeek/module.json` | `DeepSeek/modules/DeepSeek/module.json` | ❌ MISMATCH |
| `copilot-gm` | `/Copilot-Gm/module.json` | `Copilot-Gm/module.json` | ✅ MATCH |
| `cast` | `/Cast/module.json` | `Cast/modules/Cast.json` | ❌ MISMATCH (wrong name + path) |
| `bbex-core` | `/BBEX-Core/module.json` | `BBEX-Core/public/module.json` | ❌ MISMATCH |

**Summary:** 7 of 8 runtime registry path references are broken. Only `copilot-gm` matches.

---

## Section 3: Module Loader Registry (`core/module-loader/module-registry.json`)

A third registry exists at `core/module-loader/module-registry.json`. It contains a simple name list:

```json
{
  "modules": ["BBX19", "ChatGPT", "Gemini", "DeepSeek", "Grok", "Copilot-Gm", "BBEX-Core", "Cast"]
}
```

| Module | In modules/registry.json | In src registry | In module-loader |
|--------|--------------------------|-----------------|------------------|
| BBX19 | ✅ | ✅ | ✅ |
| ChatGPT | ✅ | ✅ | ✅ |
| Gemini | ✅ | ✅ | ✅ |
| Grok | ✅ | ✅ | ✅ |
| DeepSeek | ✅ | ✅ | ✅ |
| Copilot-Gm | ✅ | ✅ | ✅ |
| Cast | ✅ | ✅ | ✅ |
| BBEX-Core | ✅ | ✅ | ✅ |

All three registries agree on which modules exist. ✅

---

## Section 4: Missing Modules

> **None.** All 8 expected modules have directories and are listed in all registries.

---

## Section 5: Ghost Modules

> **None detected.** No registry entry refers to a non-existent folder.

---

## Section 6: Path Conflicts

| Conflict Type | Detail |
|---------------|--------|
| Two registries for same scope | `modules/registry.json` (coordination) and `src/modules/registry/registry.json` (runtime) both claim to be authoritative. No sync mechanism found. |
| Runtime paths broken | `src` registry paths point to `/{MODULE}/module.json` but 7 of 8 files are not there |
| Cast filename mismatch | Registry expects `module.json`; actual file is `Cast.json` |
| BBEX-Core depth mismatch | Registry expects root-level module.json; actual is inside `/public/` |
| Output path alias | Multiple module.json files reference `outcomes/append_only_ledger/` but actual dir is `outcomes/ledger/` |

---

## Section 7: Registry Version Conflict

| Field | Central Registry | Runtime Registry |
|-------|-----------------|-----------------|
| Version | 0.4.0 | 2.0.0 |
| Updated | 2026-04-25 (health sync) | 2026-02-20 |
| Schema | None declared | `/src/modules/standards/module.schema.json` |
| Schema file exists | N/A | ❌ `src/modules/standards/module.schema.json` NOT FOUND |

The runtime registry references a schema file that does not exist.

---

## Section 8: Recommendations

| Priority | Action |
|----------|--------|
| 🔴 HIGH | Standardize all module.json to `{MODULE}/module.json` top-level path |
| 🔴 HIGH | Rename `Cast/modules/Cast.json` → `Cast/module.json` |
| 🔴 HIGH | Update `src/modules/registry/registry.json` to reflect actual paths |
| 🟡 MED | Create or document sync mechanism between both registries |
| 🟡 MED | Create missing schema `src/modules/standards/module.schema.json` OR remove reference |
| 🟡 MED | Standardize `outcomes/append_only_ledger/` vs `outcomes/ledger/` across all module.json |
| 🟢 LOW | Consolidate `core/module-loader/module-registry.json` into main registry |

---

## Final Registry Health Score

| Registry | Status |
|----------|--------|
| `modules/registry.json` | ✅ CONSISTENT |
| `src/modules/registry/registry.json` | ❌ 7/8 PATHS BROKEN |
| `core/module-loader/module-registry.json` | ✅ CONSISTENT (name-only) |

**Overall Registry Health: ⚠️ WARNING**  
Core registry intact. Runtime registry paths are misaligned with filesystem.

---

*Generated by Copilot-Gm | W3 Registry Audit 2026-04-25*
