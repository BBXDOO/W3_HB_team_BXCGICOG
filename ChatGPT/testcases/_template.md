id: T?
title: <short, explicit name>

target:
  - <component | module | entrypoint>

goal:
  - <single observable behavior to prove>

preconditions:
  - <state that must be true before run>

steps:
  1. <action>
  2. <action>

expected:
  stdout:
    contains:
      - "<expected string>"
  process:
    exit_code: 0
    min_runtime_sec: <number>

failure_conditions:
  - banner mismatch
  - process exit before min_runtime
  - panic / uncaught exception
  - non-zero exit_code

risk: L1 | L2 | L3 | L4 | L5

constraints:
  network: false
  filesystem: local
  time_limit_sec: <number>
  external_dependency: false

notes:
  - <optional, non-normative>
