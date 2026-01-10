# RISK LEVEL POLICY (BINDING)

## L1 — SMOKE
- purpose: boot / existence check
- runtime: very short
- autorun: YES
- merge_block: NO
- destructive: NO

## L2 — BASIC REGRESSION
- purpose: core behavior stable
- runtime: short
- autorun: YES
- merge_block: NO
- destructive: NO

## L3 — FUNCTIONAL GUARANTEE
- purpose: logic correctness
- runtime: medium
- autorun: CONDITIONAL
- merge_block: YES (if fail)
- destructive: NO

## L4 — STRESS / EDGE
- purpose: boundary / stress
- runtime: long
- autorun: NO
- merge_block: YES
- destructive: POSSIBLE

## L5 — DESTRUCTIVE / CHAOS
- purpose: failure mode validation
- runtime: long / unstable
- autorun: NEVER
- merge_block: YES
- destructive: YES

## DECISION MATRIX
- L1–L2 fail → warn
- L3 fail → block merge
- L4–L5 fail → block + manual review

## RULES
- risk field is mandatory
- risk controls execution, not documentation
- undefined risk = BLOCKER
