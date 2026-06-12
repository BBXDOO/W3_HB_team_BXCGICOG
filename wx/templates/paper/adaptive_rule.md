---
template_id: PAPER:ADAPTIVE_RULE_V1
version: 1.0.0
scope: CROSS_L_ONLY
boundary: observe
deny: truth_mutation, file_write, network, merge
owner: BBX19
status: active
created_at: 2026-06-12
---

# Adaptive Rule Paper

> Copy this template into an agent workspace before editing. BOX only recommends this source.

## STEP1: CLASSIFY

```text
RYTM:JAZZ
WORK_TYPE:ADAPTIVE_RULE
```

## STEP2: BUILD_WORKSET

```text
TAG_GROUP: SCRIPT,GEN,CONFIG,DOC
BOUNDARY: observe
```

## STEP3: DISPATCH

```text
MODEW: Adapter
REVIEW: on_uncertain
```
