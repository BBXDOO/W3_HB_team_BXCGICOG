# W3 Referencing Standard

This standard keeps W3 integration artifacts traceable without mutating source
truth. Every derived observation, interpretation, or recovery proposal should
link back to its source artifact through explicit references.

## Reference formats

- **Relative path**: use repository-relative paths for files in this repo, e.g.
  `hospitication/docs/ARCHITECTURE.md`.
- **Permalink**: use immutable external URLs only when the source is outside the
  repository.
- **W3DB ID**: reference generated W3DB records by their domain ID, e.g.
  `XIZ-EP-...`, `TUF-HOSP-...`, or `PRX-LAYER-...`.

## Required `references` field

Integration payloads that derive meaning from another artifact should include a
`references` field containing a list of relative paths, W3DB IDs, or permalinks.
This field is required for:

- Layer separation violations.
- Hospitication recovery proposals.
- Semantic-router interpretation tasks.
- EP_SIGNAL and Hospitication W3DB bridge outputs when serialized.

## Non-mutation rule

References point backward to source truth. They do not authorize overwriting the
source signal, report, ledger entry, or W3DB record. Interpretation may create a
new derived artifact with references; it must not replace the referenced truth.
