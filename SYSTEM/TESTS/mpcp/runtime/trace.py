# mpcp/runtime/trace.py
#
# ROT-aligned trace module.
# Preserves ENV (no reduction) — per ENV LAW in ROT_PAPER.
# Tracks CAUSE → ACTION → RESULT chain.
# Provides queryable log for debugging and audit.

import datetime

_trace_log: list = []


def trace(stage: str, data, env: dict = None) -> dict:
    """
    Record one trace entry.

    Parameters
    ----------
    stage : str
        Execution stage label (e.g. "A:INPUT", "ROT:INPUT_VALID", "D:EXECUTE").
    data  : any
        Payload to record (kept as-is — no reduction per ENV LAW).
    env   : dict, optional
        Current context snapshot.  Pass the Modew/executor context so that
        every entry carries the full environment at that moment.

    Returns
    -------
    dict  The trace entry that was appended to the log.
    """
    entry = {
        "stage": stage,
        "data": data,
        "env": dict(env) if env else {},
        "time": datetime.datetime.utcnow().isoformat() + "Z",
    }
    _trace_log.append(entry)
    print(f"[MPCP][{stage}] {data}")
    return entry


def get_trace_log() -> list:
    """Return a read-only copy of the full trace log."""
    return list(_trace_log)


def clear_trace() -> None:
    """Reset the trace log.  Use with caution — clears all history."""
    global _trace_log
    _trace_log = []
