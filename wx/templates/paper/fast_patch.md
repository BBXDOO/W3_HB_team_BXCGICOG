---
template_id: PAPER:FAST_PATCH_V1
version: 1.0.0
scope: CROSS_L_ONLY
boundary: temp_patch
deny: truth_mutation, direct_merge, repo_write_without_review
owner: BBX19
status: active
created_at: 2026-06-12
---

# Fast Patch Paper

> Copy this template into an agent workspace before editing. Do not edit this source for a task instance.

## STEP1: CLASSIFY

```text
RYTM:ROCK
WORK_TYPE:FAST_PATCH
```

## STEP2: BUILD_WORKSET

```text
TAG_GROUP: FAST,LOW,SCRIPT,CONFIG
LANG_CANDIDATE: cpp,rust,c,assembly,bash,json
READ: ENV,trace,error_report
```

## STEP3: DISPATCH

```text
MODEW: FAST_PATCH
REVIEW: on_complete
```
