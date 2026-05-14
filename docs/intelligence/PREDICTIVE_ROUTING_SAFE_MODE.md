# Predictive Routing — Safe Mode

## Objective
Route tasks/PR reviews to likely module owners with confidence scoring.

## Rules
- Rule-based first; no opaque model decisions.
- Confidence < 0.7 => fallback to manual review queue.
- Log all route decisions with reason tags.

## Output format
- `target_module`
- `confidence`
- `reasons[]`
- `fallback_triggered`
