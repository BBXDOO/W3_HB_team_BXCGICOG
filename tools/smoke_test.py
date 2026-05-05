#!/usr/bin/env python3
"""
W3 Engine Smoke Test Runner
----------------------------
Role  : Android/Termux-friendly smoke test — boots the engine and exits after 8 seconds.
Owner : BBX19
Note  : Stdlib only.  No signals required.  Run from the repo root:
          python tools/smoke_test.py

Termux (Android) quickstart:
  pkg update && pkg install python git
  git clone https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
  cd W3_HB_team_BXCGICOG
  git checkout refactor/v0.2
  python tools/smoke_test.py
"""

import sys
import os
import time
import traceback

# ---------------------------------------------------------------------------
# Ensure repo root is on sys.path so `src.main` can be imported regardless
# of where Python is invoked from.
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import src.main as engine  # noqa: E402  (after sys.path patch)

# Duration the smoke test runs before self-exiting (seconds).
SMOKE_DURATION_SEC = 8


def run_smoke(duration_sec: int = SMOKE_DURATION_SEC) -> int:
    """
    Execute engine bootstrap, run heartbeats for *duration_sec* seconds,
    then shut down cleanly.

    Returns 0 on success, 1 on unexpected error.
    """
    engine.init_logger()
    exit_code = 0
    try:
        engine.system_check()

        cfg = engine.load_engine_config()
        modules = cfg.get("modules", ["Gemini", "Copilot-Gm", "Grok", "DeepSeek"])
        engine.simulate_module_boot(list(modules))

        # Timed heartbeat loop — exits automatically after duration_sec seconds.
        interval = int(cfg.get("heartbeat_interval_sec", 3))
        engine._log(
            f"Smoke test running for {duration_sec}s "
            f"(heartbeat every {interval}s) ..."
        )
        deadline = time.time() + duration_sec
        beat = 0
        while time.time() < deadline:
            beat += 1
            engine._log(
                f"[smoke] Heartbeat #{beat} | env={cfg.get('env')} "
                f"| version={cfg.get('version')}"
            )
            engine.log_event(
                event_type="system_heartbeat",
                level="INFO",
                source="smoke_test",
                message="smoke test heartbeat",
                metadata={"knowledge_level": "K1"},
            )
            remaining = deadline - time.time()
            time.sleep(min(interval, max(0.0, remaining)))

        engine._log("Smoke test complete.")
    except Exception as exc:
        engine.log_event(
            event_type="error",
            level="ERROR",
            source="smoke_test",
            message=str(exc),
            metadata={
                "error_code": type(exc).__name__,
                "stack_trace": traceback.format_exc(),
                "knowledge_level": "K2",
            },
        )
        engine._log(f"Smoke test error: {exc}")
        exit_code = 1
    finally:
        engine.log_event(
            event_type="shutdown",
            level="INFO",
            source="smoke_test",
            message="smoke test shutdown",
            metadata={"knowledge_level": "K1"},
        )
        engine.close_logger()
        engine._log("W3 smoke test shutdown completed.")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_smoke())
