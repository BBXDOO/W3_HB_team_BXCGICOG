"""
W3DB — in-process storage layer for the W3 relation flow.

Public surface:
  config  — environment / integration settings
  models  — data-class definitions (XIZ, TUF, FBD, WHB, PRX)
  store   — shared in-memory store instance
  flow    — run_flow() orchestrator
  crud    — per-domain CRUD helpers

Execution flow (per spec):
  INPUT -> XIZ -> PROCESS -> TUF -> FBD -> WHB -> PRX
"""

from src.w3db.config import W3DBConfig, get_config  # noqa: F401
from src.w3db.models import XIZ, TUF, FBD, WHB, PRX  # noqa: F401
from src.w3db.store import W3DBStore, get_store  # noqa: F401
from src.w3db.flow import run_flow  # noqa: F401
