info : add...

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
