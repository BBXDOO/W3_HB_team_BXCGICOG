# Hospitication Architecture

Hospitication models repository health as structural pressure, not simple style
violations. The architecture is intentionally layered to preserve W3 governance
and replay boundaries.

## Layer Responsibilities

| Layer | May Do | Must Not Do |
| --- | --- | --- |
| Observer | Read files and build immutable snapshots | Diagnose, recover, or write files |
| Analyzer | Compute burden metrics | Emit signals or apply recovery |
| Detector | Detect drift/spike/oscillation/divergence | Recommend recovery or diagnose root cause |
| Emitter | Create immutable signal envelopes | Interpret or mutate truth |
| Recovery | Produce proposals | Apply destructive changes |
| Reporter | Render Markdown/JSON | Change process or repository state |

## Determinism

Reports sort metrics, signals, and proposals. The default timestamp is fixed so
CI output is replayable; callers may pass an explicit timestamp when needed.

## Recovery Doctrine

Recovery is proposal-first. A proposal is a new derived artifact and never a
mutation of the underlying observation, detection, signal, memory, or ledger
truth.
