"""Host-owned capability selection, workflow recipes and verified support.

AM III / BUILD + CONTINUE. Names in request data never import executable code.
"""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from workflows import orchestration as orc


@dataclass(frozen=True)
class Adapter:
    name: str
    kind: str
    capabilities: frozenset[str]
    handler: Callable
    verifier: Callable
    module: str | None = None
    available: Callable = lambda: True
    request_types: frozenset[str] = frozenset()
    accepts: Callable = lambda request: True


class SupportCatalog:
    def __init__(self):
        self.adapters = {}

    def register(self, adapter):
        if (not isinstance(adapter, Adapter) or adapter.kind not in {'TOOL', 'SPECIALIST'}
                or not adapter.name or not adapter.capabilities
                or not all(isinstance(c, str) and c for c in adapter.capabilities)
                or not all(callable(c) for c in (adapter.handler, adapter.verifier, adapter.available, adapter.accepts))
                or (adapter.kind == 'SPECIALIST' and not adapter.module)):
            raise ValueError('named capability adapter, verifier and availability callback required')
        if adapter.name in self.adapters:
            raise ValueError('duplicate adapter')
        self.adapters[adapter.name] = adapter

    def select(self, capability, *, kind=None, preferred=None, owner=None, request_type=None, exclude=(), request=None):
        candidates, reasons = [], []
        if preferred and not any(a.name == preferred or a.module == preferred for a in self.adapters.values()):
            reasons.append({'adapter': preferred, 'reason': 'not registered'})
        for entry in self.adapters.values():
            reason = None
            if capability not in entry.capabilities or (kind and entry.kind != kind):
                continue
            if entry.name in exclude or (owner and entry.module == owner):
                reason = 'excluded or same as owner'
            elif entry.request_types and request_type not in entry.request_types:
                reason = 'request type not supported'
            else:
                try:
                    if entry.available() is not True:
                        reason = 'unavailable'
                    elif entry.accepts(deepcopy(request or {})) is not True:
                        reason = 'input or scope not supported'
                except Exception:
                    reason = 'availability or input/scope check failed'
            if reason:
                reasons.append({'adapter': entry.name, 'reason': reason})
            else:
                candidates.append(entry)
        candidates.sort(key=lambda entry: (entry.name != preferred and entry.module != preferred, entry.name))
        return (candidates[0] if candidates else None), reasons

    def support(self, runtime, task, capability, *, request=None, kind=None, preferred=None,
                owner=None, request_type=None):
        """Call one selected adapter; persist intent before effects via runtime.assist.

        A failed/uncertain invocation is never retried with another adapter here.
        RETURNED means verified support, not completion of the owner's task.
        """
        runtime._ready(task)
        if task['status'] != 'BLOCKED' or not task.get('blocker'):
            raise ValueError('recorded blocker required')
        entry, rejected = self.select(capability, kind=kind, preferred=preferred,
                                      owner=owner, request_type=request_type, request=request)
        selection = {'capability': capability, 'preferred': preferred, 'owner': owner,
                     'selected': entry.name if entry else None, 'rejected': rejected}
        ref = runtime._evidence(task, 'support-selection', selection)
        task['evidence'].append({'at': orc.timestamp(),
                                 'actor': 'support-selection', 'ref': ref})
        runtime._save(task)
        if entry is None:
            return task  # blocker remains; absence of an executor is not success
        def invoke(_):
            context = {'task_id': task['task_id'], 'source_id': task.get('source_id'),
                       'payload': deepcopy(task['payload']), 'blocker': deepcopy(task['blocker']),
                       'destination': deepcopy(task.get('destination')), 'request': deepcopy(request or {}),
                       'stage': deepcopy(task['runtime_circuit'].get('effective_stage')),
                       'selection': deepcopy(selection)}
            raw = entry.handler(deepcopy(context))
            # Keep actual side effects visible even when the verifier fails.
            if not isinstance(raw, dict):
                raise ValueError('support adapter must return an object')
            try:
                verdict = entry.verifier(deepcopy(context), deepcopy(raw))
                passed = isinstance(verdict, dict) and verdict.get('passed') is True
            except Exception as exc:
                verdict, passed = {'passed': False, 'reason': str(exc)}, False
            receipt = {'adapter': entry.name, 'module': entry.module, 'capability': capability,
                       'owner': owner, 'result': raw, 'verification': verdict}
            return {**raw, 'resolved': raw.get('resolved') is True and passed,
                    'evidence': ref, 'selection': selection, 'verification': verdict,
                    'support_receipt': receipt}
        return runtime.assist(task, kind=entry.kind, name=entry.name, handler=invoke)


class FlowCatalog:
    """Trusted recipes ordered by dependencies, independent of module tier."""
    def __init__(self):
        self.recipes = {}

    def register(self, name, steps):
        from workflows.runtime_circuit import WorkflowRuntime
        if not isinstance(name, str) or not name or name in self.recipes or not isinstance(steps, list) or not steps:
            raise ValueError('unique workflow name and steps required')
        pending = deepcopy(steps)
        ids = [s.get('id') for s in pending]
        if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
            raise ValueError('unique step ids required')
        ordered, done = [], set()
        while pending:
            ready = [s for s in pending if isinstance(s.get('after', []), list) and set(s.get('after', [])) <= done]
            if not ready:
                raise ValueError('missing dependency or workflow cycle')
            for step in ready:
                stage = WorkflowRuntime._stage({k: v for k, v in step.items() if k not in {'id', 'after'}})
                ordered.append(stage)
                done.add(step['id'])
                pending.remove(step)
        self.recipes[name] = ordered

    def plan(self, name, request):
        if name not in self.recipes or not isinstance(request, dict):
            raise ValueError('unknown workflow or invalid input')
        stages = deepcopy(self.recipes[name])
        # Only first step receives initial payload; later stages receive predecessor output.
        stages[0]['request'].update(deepcopy(request))
        return stages


def tool_inventory(root, catalog=None):
    """Discover source files for host registration; never import scanned scripts."""
    root = Path(root).resolve()
    return [{'path': str(p.relative_to(root)), 'registered': catalog is not None and str(p.relative_to(root)) in catalog.adapters}
            for p in sorted((root / 'tools').rglob('*.py'))
            if p.resolve().is_relative_to(root / 'tools') and '__pycache__' not in p.parts]


def register_repository_tool(catalog, root, path, capabilities, handler, verifier, **options):
    """Register any repository tool through an explicit trusted Python adapter."""
    root = Path(root).resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root / 'tools') or not target.is_file():
        raise ValueError('existing tool within tools/ required')
    name = str(target.relative_to(root))
    catalog.register(Adapter(name, 'TOOL', frozenset(capabilities), handler, verifier,
                             available=lambda: target.is_file(), **options))
