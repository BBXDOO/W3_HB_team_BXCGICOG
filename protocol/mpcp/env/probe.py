"""Portable, read-only environment detection for MPCP."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from typing import Any, Mapping

from ..config import MPCPConfig, load_config
from .models import EnvironmentSnapshot


def _safe_hints(hints: Mapping[str, Any] | None) -> dict[str, Any]:
    """Keep operational hints while redacting common credential fields."""
    safe: dict[str, Any] = {}
    for key, value in (hints or {}).items():
        name = str(key)
        lowered = name.lower()
        if any(marker in lowered for marker in ("secret", "token", "password", "api_key", "credential")):
            safe[name] = "<redacted>"
        else:
            safe[name] = value
    return safe


def _in_container() -> bool:
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", "r", encoding="utf-8") as handle:
            text = handle.read().lower()
    except OSError:
        return False
    return any(marker in text for marker in ("docker", "containerd", "kubepods", "podman"))


def probe_environment(
    *,
    hints: Mapping[str, Any] | None = None,
    config: MPCPConfig | None = None,
) -> EnvironmentSnapshot:
    """Observe the host without exposing environment-variable values."""

    active = config or load_config()
    prefix = os.environ.get("PREFIX", "")
    termux = "com.termux" in prefix or "termux" in prefix.lower()
    system = platform.system().lower() or os.name
    mobile = termux or system in {"android", "ios"}

    command_names = {
        command
        for commands in active.language_runtime.values()
        for command in commands
    }
    commands = {
        command: resolved
        for command in sorted(command_names)
        if (resolved := shutil.which(command)) is not None
    }
    variable_names = tuple(
        name for name in active.allowed_variable_names if name in os.environ
    )
    return EnvironmentSnapshot(
        platform=system,
        platform_release=platform.release(),
        architecture=platform.machine() or "unknown",
        python=".".join(str(item) for item in sys.version_info[:3]),
        mobile=mobile,
        termux=termux,
        container=_in_container(),
        commands=commands,
        variable_names=variable_names,
        hints=_safe_hints(hints),
    )
