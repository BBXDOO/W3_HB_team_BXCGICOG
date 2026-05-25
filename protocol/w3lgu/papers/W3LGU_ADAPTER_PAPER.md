# W3Lgu Adapter Paper

## Goal
Define how external inputs become W3Lgu without bloating runtime or losing intent.

## Adapter roles
- **input adapter**: human text, UI form, or API payload into line form
- **module adapter**: one module contract to another module contract
- **MPCP adapter**: W3Lgu packet to MPCP execution packet
- **environment adapter**: adds ENV hints for device, power, or network constraints

## Rules
- adapters normalize structure, not meaning
- adapters may enrich context only with traceable metadata
- adapters must leave a readable packet behind
- adapters should prefer additive repair over destructive rewrite

## ENV-aware adapter example
Input:
```txt
run sync now
```

Adapted:
```txt
TASK:sync,INTENT:run_now,ENV:mobile,CHANNEL:text
```

## MPCP bridge example
```txt
TASK:sync,STATE:ready
```
→
```txt
CAUSE:sync,state:ready,error:
```

The bridge should preserve MPCP-required fields while keeping a matching W3Lgu view for humans.

## Line C support
Adapters operate on Line C when they need to balance strict parsing with adaptive interpretation.
They should accept imperfect input, then output a clean packet rather than pushing ambiguity deeper into runtime.
