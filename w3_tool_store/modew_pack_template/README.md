# W3 Plugin / Modew Pack Template

**Status:** TEMPLATE / DRAFT  
**Scope:** W3 / Modew / Plugin Pack / W3MD / MPCP / MCP / Boundary / Return Contract  
**Owner:** BBX19  

This folder is a W3-style template for packaging reusable capabilities.

It is inspired by plugin-pack structures, but it is **not copied as-is**.
W3 uses the idea as raw material to create its own pattern.

Core idea:

```text
W3 Plugin / Modew Pack
= a reusable capability bundle
= readable by human / AI / module / W3API
= bounded by boundary and return contract
= mutated:false by default
```

---

## Folder Tree

```text
w3_tool_store/modew_pack_template/
├─ README.md
├─ W3_PLUGIN_MODEW_PACK.w3md
├─ pack.json
├─ mpcp.json
├─ mcp.json
├─ skills/
│  └─ README.md
├─ agents/
│  └─ README.md
├─ commands/
│  └─ README.md
├─ hooks/
│  └─ hooks.json
├─ assets/
│  └─ README.md
├─ boundary/
│  └─ boundary.json
└─ return_contract/
   └─ return_contract.json
```

---

## Layer Meaning

```text
w3md manifest
= official W3 document / intent / scope / philosophy / reference

pack.json
= machine-readable pack identity and capability summary

skills/
= reusable ability notes or skill definitions

agents/
= agent-specific role notes

commands/
= command patterns that this pack can expose

hooks/
= before/after observation hooks, not direct mutation

assets/
= icons, diagrams, images, examples

mpcp.json / mcp.json
= bridge hints for environment/runtime/tool connection

boundary/
= what the pack may or may not do

return_contract/
= what the pack must return after being used
```

---

## Safety Lock

```text
mutated:false by default
execution_allowed:false by default
review:true by default
repo_write_allowed:false by default
direct_merge_allowed:false by default
```

---

## W3 Position

This template is not the final system.

It is a seed structure for future W3 packs such as:

```text
WE_PAPER_PACK
TABLE_X_PACK
HOSPITICATION_INTAKE_PACK
W3API_GATE_PACK
CROSS_L_PLANNER_PACK
MODEW_DYNAMIC_PACK
```

END
