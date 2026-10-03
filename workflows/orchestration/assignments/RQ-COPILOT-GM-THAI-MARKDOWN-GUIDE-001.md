# Assignment — RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001

source_request: requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md
status: ROUTED
mutated: false
review: true

## Participants

- Primary: Copilot-Gm
- Partner / validator / activity recorder: Gemini
- Coordinator: Orchestration
- Final decision node: BBX19

## Work chain

1. Orchestration — inspect request, retain identity, route and collect evidence.
2. Copilot-Gm — create `BBX19/notes/THAI_MARKDOWN_GUIDE.md` under the one-file authority granted in the source request.
3. Gemini — cross-check syntax, renderer compatibility, links and limitations; write actual validation activity to `repo_events/`.
4. Orchestration — verify the artifact and both modules' evidence; return blockers to the responsible stage when necessary.
5. BBX19 — review and decide final closure.

## No-duplicate rule

- One source request only: `requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md`.
- Handoff documents reference the source; they do not copy or redefine its intent.
- Search for the expected artifact before creating a new file.
- A support adapter may help write the artifact but must not create a second guide or claim Primary ownership.

Each contribution must retain this `request_id`. No participant inherits another participant's authority.

