"""
W3DB Configuration
------------------
Loads env/integration settings with dev/test/prod defaults.

Priority (highest → lowest):
  1. Environment variables (W3DB_*)
  2. Per-environment defaults below
"""

import os
from typing import Any, Dict

# ── Per-environment defaults ──────────────────────────────────────────────────

_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "dev": {
        "store_backend": "memory",   # "memory" | "json"
        "store_path": "data/w3db",   # used only for json backend
        "log_level": "DEBUG",
        "flow_auto": True,           # automatically run relation flow on XIZ create
        "prx_scale": 2.0,            # intensity = abs(confidence - 0.5) * scale
    },
    "test": {
        "store_backend": "memory",
        "store_path": "data/w3db_test",
        "log_level": "WARNING",
        "flow_auto": True,
        "prx_scale": 2.0,
    },
    "prod": {
        "store_backend": "memory",
        "store_path": "data/w3db_prod",
        "log_level": "INFO",
        "flow_auto": True,
        "prx_scale": 2.0,
    },
}

# ── Loader ────────────────────────────────────────────────────────────────────


def load_config() -> Dict[str, Any]:
    """
    Return the active W3DB configuration dict.

    Environment variables override defaults:
      W3DB_ENV           — "dev" | "test" | "prod"  (default: "dev")
      W3DB_STORE_BACKEND — "memory" | "json"
      W3DB_STORE_PATH    — filesystem path (json backend only)
      W3DB_LOG_LEVEL     — logging level string
      W3DB_FLOW_AUTO     — "1" | "0" / "true" | "false"
      W3DB_PRX_SCALE     — float scale for PRX intensity formula
    """
    env = os.environ.get("W3DB_ENV", "dev").lower()
    if env not in _DEFAULTS:
        env = "dev"

    cfg: Dict[str, Any] = dict(_DEFAULTS[env])

    if val := os.environ.get("W3DB_STORE_BACKEND"):
        cfg["store_backend"] = val
    if val := os.environ.get("W3DB_STORE_PATH"):
        cfg["store_path"] = val
    if val := os.environ.get("W3DB_LOG_LEVEL"):
        cfg["log_level"] = val
    if val := os.environ.get("W3DB_FLOW_AUTO"):
        cfg["flow_auto"] = val.lower() in ("1", "true", "yes")
    if val := os.environ.get("W3DB_PRX_SCALE"):
        try:
            cfg["prx_scale"] = float(val)
        except ValueError:
            pass

    cfg["env"] = env
    return cfg
