[ต้นฉบับ](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/repo_events/IDP_TEMPLATE.V3_TEST.md)

info : add...

(ข้อมูล: เพิ่มเติม...)

ORIGIN:
  source: W3-PR-30
  source_type: identity-backup
  source_status: historical
  inheritance: selective

IDENTITY_CONTINUITY:
  identity_core: stable
  capability_profile: current
  operational_context: renewable
  historical_character: reference-only

RESTORE:
  strategy: current-state-first
  fallback: historical-identity-reference
  resume_pointer: docs/operations/resume_header.json
  schema: docs/operations/resume_header.schema.json

WORK_STATE:
  task_id: <current-task>
  state: <state>
  last_action: <last-confirmed-action>
  next_action: <next-action>
  evidence: <reference>

VERSION_LINEAGE:
  origin: PR-30/Soul-Manifest
  predecessor: IDP-v2
  current: IDP-v3
