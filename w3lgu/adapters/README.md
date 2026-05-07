# W3Lgu Adapters

Purpose: keep W3Lgu lightweight while translating external or cross-layer input into one language contract.

## Scope
- UI input adapter
- module bridge adapter
- MPCP bridge adapter
- environment adapter

## Rule
Structure ≠ meaning.
Adapters normalize format, but must not overwrite intent unless policy explicitly requires it.

## Example
`ENV:mobile,INPUT:text,TASK:ping`
→ `TASK:ping,ENV:mobile,CHANNEL:ui`
