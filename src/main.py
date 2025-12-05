"""
W3 Hybrid Engine Entry Point
----------------------------
Role  : System bootstrap + runtime loop
Owner : BBX19
Note  : Stdlib only. No async. Safe to run before full modules are ready.
"""

import json
import os
import sys
import time
import signal
import traceback
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, IO

# --- Runtime flags ---
_running = True

# --- Log file handle ---
_log_file: Optional[IO[str]] = None


# ---------- Runtime Logging (JSON) ----------

def _get_log_dir() -> str:
    """Get the log directory path relative to the repository root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return os.path.join(repo_root, "logs", "engine")


def init_logger() -> None:
    """Initialize the JSON log file for runtime events."""
    global _log_file
    log_dir = _get_log_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "runtime.log")
    _log_file = open(log_path, "a", encoding="utf-8")


def close_logger() -> None:
    """Flush and close the log file handle."""
    global _log_file
    if _log_file is not None:
        _log_file.flush()
        _log_file.close()
        _log_file = None


def log_event(
    event_type: str,
    level: str,
    source: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a runtime event in JSON format (JSONL style).

    Each log entry is written as a single JSON line.
    """
    global _log_file
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "source": source,
        "message": message,
    }
    if metadata is not None:
        event["metadata"] = metadata

    if _log_file is not None:
        _log_file.write(json.dumps(event) + "\n")
        _log_file.flush()


# ---------- Utilities ----------

def _log(message: str) -> None:
    """Simple structured logger for engine runtime (console output)."""
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{ts}] [W3-ENGINE] {message}", flush=True)


def _set_signal_handlers() -> None:
    """Register signal handlers for graceful shutdown."""
    def handle_signal(signum, frame):
        global _running
        _log(f"Received signal {signum}. Scheduling shutdown...")
        _running = False

    signal.signal(signal.SIGINT, handle_signal)   # Ctrl+C
    try:
        signal.signal(signal.SIGTERM, handle_signal)
    except AttributeError:
        # SIGTERM may not exist on some platforms (e.g. Windows in limited envs)
        pass


# ---------- Config Layer ----------

def _fallback_config() -> Dict[str, Any]:
    """Fallback config when core.config_loader is not available yet."""
    return {
        "env": "dev",
        "version": "0.2",
        "heartbeat_interval_sec": 3,
        "modules": ["Gemini", "Copilot-Gm", "Grok", "DeepSeek"],
    }


def load_engine_config() -> Dict[str, Any]:
    """
    Try to load config from core.config_loader.load_config().
    If not available, use internal fallback.
    """
    try:
        from core.config_loader import load_config  # type: ignore
        cfg = load_config()
        if not isinstance(cfg, dict):
            _log("Config loader returned non-dict. Using fallback config.")
            return _fallback_config()
        _log("Config loaded from core.config_loader.")
        return cfg
    except Exception as exc:  # noqa: BLE001
        _log(f"Config loader unavailable or failed ({exc}). Using fallback.")
        return _fallback_config()


# ---------- Module Boot Simulation ----------

def simulate_module_boot(mod_names: List[str]) -> Dict[str, str]:
    """
    Simulate loading of core AI modules.

    Returns mapping: module_name -> status string.
    """
    status: Dict[str, str] = {}
    for name in mod_names:
        # future: replace with real health checks / connector calls
        _log(f"Bootstrapping module: {name} ...")
        time.sleep(0.2)
        status[name] = "READY"
        _log(f"Module {name}: READY")
        log_event(
            event_type="module_load",
            level="INFO",
            source="engine",
            message=f"Module {name} ready",
            metadata={"module": name, "knowledge_level": "K1"},
        )
    return status


# ---------- Heartbeat Loop ----------

def heartbeat_loop(interval_sec: int, context: Dict[str, Any]) -> None:
    """
    Core engine loop.

    Emits heartbeat until _running is set to False by signal handler.
    """
    _log(f"Entering heartbeat loop (interval={interval_sec}s). Press Ctrl+C to stop.")

    beat = 0
    while _running:
        beat += 1
        _log(
            f"Heartbeat #{beat} | env={context.get('env')} "
            f"| version={context.get('version')}"
        )
        log_event(
            event_type="system_heartbeat",
            level="INFO",
            source="engine",
            message="W3 engine heartbeat",
            metadata={"knowledge_level": "K1"},
        )
        time.sleep(interval_sec)

    _log("Heartbeat loop terminated.")


# ---------- System Check ----------

def system_check() -> None:
    """Run basic online check before entering main loop."""
    _log("Running system check...")
    python_ver = sys.version.split()[0]
    _log(f"Python runtime: {python_ver}")
    _log("W3 Hybrid Engine: ONLINE.")
    log_event(
        event_type="system_heartbeat",
        level="INFO",
        source="engine",
        message="W3 engine heartbeat",
        metadata={"knowledge_level": "K1"},
    )


# ---------- Main ----------

def main() -> None:
    _set_signal_handlers()
    init_logger()
    system_check()

    # 1) Load configuration
    config = load_engine_config()

    # 2) Simulate module loading
    modules = config.get(
        "modules",
        ["Gemini", "Copilot-Gm", "Grok", "DeepSeek"],
    )
    module_status = simulate_module_boot(list(modules))

    ready_modules = [m for m, s in module_status.items() if s == "READY"]
    _log(f"All modules READY: {', '.join(ready_modules)}")

    # 3) Start heartbeat loop
    interval = int(config.get("heartbeat_interval_sec", 3))
    try:
        heartbeat_loop(interval, config)
    except KeyboardInterrupt:
        # Fallback in case signal handler isn't triggered in some environments
        _log("KeyboardInterrupt received. Shutting down engine...")
    except Exception as exc:
        # Log error event for exceptions in main loop
        log_event(
            event_type="error",
            level="ERROR",
            source="engine",
            message=str(exc),
            metadata={
                "error_code": type(exc).__name__,
                "stack_trace": traceback.format_exc(),
                "knowledge_level": "K2",
            },
        )
        raise
    finally:
        log_event(
            event_type="shutdown",
            level="INFO",
            source="engine",
            message="W3 engine shutdown",
            metadata={"knowledge_level": "K1"},
        )
        close_logger()
        _log("W3 Hybrid Engine shutdown completed.")


if __name__ == "__main__":
    main()
