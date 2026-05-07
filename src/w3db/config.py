"""
W3DB Configuration
------------------
Reads environment variables (or falls back to safe defaults) to produce
a W3DBConfig instance.  Supports dev / test / prod environments.

Environment variable:
  W3DB_ENV   — "dev" | "test" | "prod"  (default: "dev")
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any


# ---------------------------------------------------------------------------
# Per-environment defaults
# ---------------------------------------------------------------------------

_ENV_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "dev": {
        "backend": "memory",
        "log_level": "DEBUG",
        "immutable_xiz": False,
        "max_store_size": 1000,
    },
    "test": {
        "backend": "memory",
        "log_level": "WARNING",
        "immutable_xiz": True,
        "max_store_size": 500,
    },
    "prod": {
        "backend": "memory",
        "log_level": "ERROR",
        "immutable_xiz": True,
        "max_store_size": 10000,
    },
}

_VALID_ENVS = frozenset(_ENV_DEFAULTS.keys())


@dataclass
class W3DBConfig:
    """Runtime configuration for the W3DB layer."""

    env: str = "dev"
    backend: str = "memory"
    log_level: str = "DEBUG"
    immutable_xiz: bool = False
    max_store_size: int = 1000
    extra: Dict[str, Any] = field(default_factory=dict)

    def is_immutable_xiz(self) -> bool:
        """Return True if XIZ records must not be modified after creation."""
        return self.immutable_xiz


def get_config() -> W3DBConfig:
    """
    Build a W3DBConfig from environment variables + per-env defaults.

    W3DB_ENV controls which default profile is loaded.  Individual values
    can be further overridden by additional env-vars (W3DB_LOG_LEVEL, etc.).
    """
    env_name = os.environ.get("W3DB_ENV", "dev").lower()
    if env_name not in _VALID_ENVS:
        env_name = "dev"

    defaults = _ENV_DEFAULTS[env_name].copy()

    return W3DBConfig(
        env=env_name,
        backend=os.environ.get("W3DB_BACKEND", defaults["backend"]),
        log_level=os.environ.get("W3DB_LOG_LEVEL", defaults["log_level"]),
        immutable_xiz=(
            os.environ.get("W3DB_IMMUTABLE_XIZ", str(defaults["immutable_xiz"]))
            .lower()
            in ("1", "true", "yes")
        ),
        max_store_size=int(
            os.environ.get("W3DB_MAX_STORE_SIZE", str(defaults["max_store_size"]))
        ),
    )
