"""
Semantic Router for W3/MPCP Agents
Routes tasks based on mpcp_role and mpcp_concepts.
Logs every routing decision to W3DB.
"""

from typing import Optional, List, Dict, Any
from core.runtime.agents.registry import AGENT_TABLE, get_agent
from src.w3db.store import W3DBStore
from src.w3db.crud.xiz import create_xiz
from src.w3db.crud.fbd import create_fbd
from src.w3db.crud.prx import create_prx_from_tuf
from src.w3db.crud.tuf import create_tuf
import datetime
import uuid


class NoSuitableAgentError(Exception):
    """Raised when no agent matches the required role/concept."""
    pass


def _create_routing_trace(
    store: W3DBStore,
    task: str,
    selected_agent: str,
    confidence: float,
    reason: str,
    failed: bool = False
) -> str:
    """Internal: record routing decision to W3DB and return XIZ id."""
    tuf = create_tuf(
        tuf_id=f"TUF-{uuid.uuid4().hex[:8]}",
        cix_id="ROUTER",
        initial="0",
        final=str(confidence),
        confidence=confidence,
        store=store
    )
    xiz = create_xiz(
        xiz_id=f"XIZ-{uuid.uuid4().hex[:8]}",
        action=f"route_task:{task}",
        timestamp=datetime.datetime.utcnow().isoformat(),
        result=selected_agent if not failed else "NO_AGENT",
        store=store,
        tuf_id=tuf.tuf_id
    )
    if failed:
        create_fbd(
            fbd_id=f"FBD-{uuid.uuid4().hex[:8]}",
            tuf_id=tuf.tuf_id,
            failure="Red",
            conditions=reason,
            store=store
        )
    else:
        # optional: log success as green FBD or skip
        pass
    # create PRX from TUF (perception)
    prx = create_prx_from_tuf(f"PRX-{uuid.uuid4().hex[:8]}", tuf, store=store)
    return xiz.xiz_id


def route_task(
    task_description: str,
    required_role: Optional[str] = None,
    concept_keywords: Optional[List[str]] = None,
    store: Optional[W3DBStore] = None,
    fallback_agent: Optional[str] = None
) -> Any:
    """
    Route a task to an appropriate agent based on role or concept keywords.

    Args:
        task_description: Human-readable task description (used for logging)
        required_role: Exact mpcp_role required (e.g. "validation", "governance")
        concept_keywords: List of keywords to match against agent's mpcp_concepts
        store: W3DBStore instance (if None, routing is still performed but no logs)
        fallback_agent: Agent name to use if no match found (default: raises error)

    Returns:
        Agent instance (from AGENT_TABLE)

    Raises:
        NoSuitableAgentError: if no agent matches and no fallback provided
    """
    if store is None:
        store = W3DBStore()  # ephemeral, not persisted

    # 1. Role-based routing
    if required_role:
        for name, agent in AGENT_TABLE.items():
            if getattr(agent, "mpcp_role", None) == required_role:
                _create_routing_trace(
                    store, task_description, name, confidence=0.95,
                    reason=f"matched role {required_role}"
                )
                return agent
        # fallback: if role not found, try concept matching later
        pass

    # 2. Concept-based routing
    if concept_keywords:
        best_agent = None
        best_score = 0
        for name, agent in AGENT_TABLE.items():
            concepts = getattr(agent, "mpcp_concepts", [])
            score = sum(1 for kw in concept_keywords if any(kw.lower() in c.lower() for c in concepts))
            if score > best_score:
                best_score = score
                best_agent = agent
                best_name = name
        if best_agent and best_score > 0:
            _create_routing_trace(
                store, task_description, best_name, confidence=0.7 + (best_score/10),
                reason=f"concept match score {best_score}"
            )
            return best_agent

    # 3. Fallback
    if fallback_agent and fallback_agent in AGENT_TABLE:
        _create_routing_trace(
            store, task_description, fallback_agent, confidence=0.5,
            reason="fallback agent used"
        )
        return AGENT_TABLE[fallback_agent]

    # 4. No match
    _create_routing_trace(
        store, task_description, "NONE", confidence=0.0,
        reason=f"no agent for role={required_role} concepts={concept_keywords}",
        failed=True
    )
    raise NoSuitableAgentError(
        f"No suitable agent for role={required_role} concepts={concept_keywords}"
    )
