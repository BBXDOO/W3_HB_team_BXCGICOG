# Handoff — Gemini

request_id: RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001
source_request: requests/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001.md
from: orchestration
to: Gemini
role: partner_validator_and_activity_recorder
reason: cross-check Markdown accuracy and preserve execution evidence
authority_scope: verify/report only; record actual activity in repo_events; do not replace Primary ownership
status: ROUTED
mutated: false
review: true

Expected contribution:

- Verify `BBX19/notes/THAI_MARKDOWN_GUIDE.md` after an artifact exists.
- Separate CommonMark, GFM, HTML/CSS fallback and renderer-specific behavior.
- Check internal links and examples without inventing successful rendering.
- Write `repo_events/RQ-COPILOT-GM-THAI-MARKDOWN-GUIDE-001_GEMINI_VALIDATION.md` only after real validation.
- Return disagreements, limitations and evidence to Orchestration.

Gemini must not mark the request completed or perform BBX19 final sign-off.

