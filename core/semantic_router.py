"""
Semantic Router for W3/MPCP Agents
Routes tasks based on mpcp_role and mpcp_concepts.
Logs every routing decision to W3DB.
"""

from __future__ import annotations

from typing import Optional, List, Any, TYPE_CHECKING
from datetime import datetime, timezone
import uuid

if TYPE_CHECKING:
    from core.runtime.agents.registry import RuntimeAgent
    from src.w3db.store import W3DBStore


class NoSuitableAgentError(Exception):
    """Raised when no agent matches the required role/concept."""
    pass


class RouterTracer:
    """
    Records routing decisions to W3DB as a TUF -> XIZ -> (FBD|PRX) chain.

    Use a shared W3DBStore instance to persist traces across calls.
    """

    def __init__(self, store: W3DBStore | None = None) -> None:
        from src.w3db.store import get_store
        self._store = store if store is not None else get_store()

    @staticmethod
    def _confidence_state(confidence: float) -> str:
        if confidence >= 0.75:
            return "1"
        if confidence > 0.25:
            return "0.5"
        return "0"

    def trace_success(
        self,
        task: str,
        agent_name: str,
        confidence: float,
        reason: str,
    ) -> str:
        from src.w3db.crud.tuf import create_tuf
        from src.w3db.crud.xiz import create_xiz
        from src.w3db.crud.prx import create_prx_from_tuf

        tuf = create_tuf(
            tuf_id=f"TUF-{uuid.uuid4().hex[:8]}",
            cix_id="ROUTER",
            initial="0",
            final=self._confidence_state(confidence),
            confidence=confidence,
            store=self._store,
        )
        xiz = create_xiz(
            xiz_id=f"XIZ-{uuid.uuid4().hex[:8]}",
            action=f"route_task:{task}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            result=agent_name,
            store=self._store,
            tuf_id=tuf.tuf_id,
        )
        create_prx_from_tuf(
            f"PRX-{uuid.uuid4().hex[:8]}", tuf, store=self._store
        )
        return xiz.xiz_id

    def trace_failure(
        self,
        task: str,
        reason: str,
    ) -> str:
        from src.w3db.crud.tuf import create_tuf
        from src.w3db.crud.xiz import create_xiz
        from src.w3db.crud.fbd import create_fbd
        from src.w3db.crud.prx import create_prx_from_tuf

        tuf = create_tuf(
            tuf_id=f"TUF-{uuid.uuid4().hex[:8]}",
            cix_id="ROUTER",
            initial="0",
            final="0",
            confidence=0.0,
            store=self._store,
        )
        xiz = create_xiz(
            xiz_id=f"XIZ-{uuid.uuid4().hex[:8]}",
            action=f"route_task:{task}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            result="NO_AGENT",
            store=self._store,
            tuf_id=tuf.tuf_id,
        )
        create_fbd(
            fbd_id=f"FBD-{uuid.uuid4().hex[:8]}",
            tuf_id=tuf.tuf_id,
            failure="Red",
            conditions=reason,
            store=self._store,
        )
        create_prx_from_tuf(
            f"PRX-{uuid.uuid4().hex[:8]}", tuf, store=self._store
        )
        return xiz.xiz_id


class SemanticRouter:
    """
    Routes tasks to agents based on role or concept matching.

    Typical usage::

        router = SemanticRouter(store=my_store)
        agent = router.route("audit", required_role="validation")

    All routing decisions are logged to W3DB via the internal RouterTracer.
    """

    def __init__(
        self,
        store: W3DBStore | None = None,
        tracer: RouterTracer | None = None,
    ) -> None:
        from src.w3db.store import get_store
        self._store = store if store is not None else get_store()
        self._tracer = tracer if tracer is not None else RouterTracer(self._store)

    @property
    def tracer(self) -> RouterTracer:
        return self._tracer

    @property
    def store(self) -> Any:
        return self._store

    def route(
        self,
        task_description: str,
        required_role: str | None = None,
        concept_keywords: list[str] | None = None,
        fallback_agent: str | None = None,
    ) -> Any:
        """
        Route a task to an appropriate agent.

        Args:
            task_description: Human-readable task description (used for logging).
            required_role: Exact mpcp_role required (e.g. "validation", "governance").
            concept_keywords: Keywords to match against agent's mpcp_concepts.
            fallback_agent: Agent name to use if no match found.

        Returns:
            Agent instance (via get_agent).

        Raises:
            NoSuitableAgentError: if no agent matches and no fallback is provided.
        """
        # 1. Role-based routing
        if required_role:
            match = self._route_by_role(task_description, required_role)
            if match:
                return match

        # 2. Concept-based routing
        if concept_keywords:
            match = self._route_by_concept(task_description, concept_keywords)
            if match:
                return match

        # 3. Fallback
        if fallback_agent:
            from core.runtime.agents.registry import AGENT_TABLE, get_agent

            if fallback_agent in AGENT_TABLE:
                self._tracer.trace_success(
                    task_description, fallback_agent, 0.5, "fallback agent used",
                )
                return get_agent(fallback_agent)

        # 4. No match
        self._tracer.trace_failure(
            task_description,
            f"no agent for role={required_role} concepts={concept_keywords}",
        )
        raise NoSuitableAgentError(
            f"No suitable agent for role={required_role} concepts={concept_keywords}"
        )

    def _route_by_role(self, task: str, required_role: str) -> Any | None:
        from core.runtime.agents.registry import AGENT_TABLE, get_agent

        for name, agent_cls in AGENT_TABLE.items():
            if getattr(agent_cls, "mpcp_role", None) == required_role:
                self._tracer.trace_success(
                    task, name, 0.95, f"matched role {required_role}",
                )
                return get_agent(name)
        return None

    def _route_by_concept(self, task: str, keywords: list[str]) -> Any | None:
        from core.runtime.agents.registry import AGENT_TABLE, get_agent

        best_name: str | None = None
        best_score = 0
        for name, agent_cls in AGENT_TABLE.items():
            concepts = getattr(agent_cls, "mpcp_concepts", [])
            score = sum(
                1 for kw in keywords
                if any(kw.lower() in c.lower() for c in concepts)
            )
            if score > best_score:
                best_score = score
                best_name = name

        if best_name is not None and best_score > 0:
            confidence = min(0.7 + best_score / 10, 0.95)
            self._tracer.trace_success(
                task, best_name, confidence, f"concept match score {best_score}",
            )
            return get_agent(best_name)
        return None

    def interpret_hospitication_report(
        self,
        report_path: str,
        fallback_agent: str | None = "Cast",
    ) -> Any:
        """
        Route a Hospitication report to Gemini/Cast without mutating truth.

        The routed task explicitly instructs interpretation layers to create
        derived references only. Signals and reports remain source truth artifacts.
        """
        return self.route(
            task_description=(
                "interpret_hospitication_report "
                f"source={report_path} references=hospitication/docs/ARCHITECTURE.md "
                "policy=do_not_overwrite_signal_or_report"
            ),
            concept_keywords=[
                "validation", "interpretation", "context", "reasoning",
            ],
            fallback_agent=fallback_agent,
        )


# ---------------------------------------------------------------------------
# Module-level convenience API (backward compatible)
# ---------------------------------------------------------------------------

_DEFAULT_ROUTER: SemanticRouter | None = None


def _default_router() -> SemanticRouter:
    global _DEFAULT_ROUTER
    if _DEFAULT_ROUTER is None:
        _DEFAULT_ROUTER = SemanticRouter()
    return _DEFAULT_ROUTER


def route_task(
    task_description: str,
    required_role: str | None = None,
    concept_keywords: list[str] | None = None,
    store: Any = None,
    fallback_agent: str | None = None,
) -> Any:
    """
    Convenience function: route a task via a one-off SemanticRouter.

    If *store* is ``None``, traces go to the process-wide W3DB singleton.

    See :meth:`SemanticRouter.route` for details.
    """
    router = SemanticRouter(store=store) if store else _default_router()
    return router.route(
        task_description=task_description,
        required_role=required_role,
        concept_keywords=concept_keywords,
        fallback_agent=fallback_agent,
    )


def interpret_hospitication_report(
    report_path: str,
    store: Any = None,
    fallback_agent: str | None = "Cast",
) -> Any:
    """
    Convenience function: route a Hospitication report via a one-off router.

    If *store* is ``None``, traces go to the process-wide W3DB singleton.

    See :meth:`SemanticRouter.interpret_hospitication_report` for details.
    """
    router = SemanticRouter(store=store) if store else _default_router()
    return router.interpret_hospitication_report(
        report_path=report_path,
        fallback_agent=fallback_agent,
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.semantic_router <task> [--role R] [--concept C ...] [--fallback F]", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python -m core.semantic_router 'security audit' --role validation", file=sys.stderr)
        print("  python -m core.semantic_router 'create diagram' --concept architecture design", file=sys.stderr)
        sys.exit(1)

    task = sys.argv[1]
    role = None
    concepts = None
    fallback = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--role" and i + 1 < len(args):
            role = args[i + 1]
            i += 2
        elif args[i] == "--concept":
            concepts = []
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                concepts.append(args[i])
                i += 1
        elif args[i] == "--fallback" and i + 1 < len(args):
            fallback = args[i + 1]
            i += 2
        else:
            i += 1

    try:
        agent = route_task(task, required_role=role, concept_keywords=concepts, fallback_agent=fallback)
        print(f"Routed to: {agent.module_name} ({agent.mpcp_role})")
    except NoSuitableAgentError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
