"""Evidence-led, resumable coordination of explicit local runtime stages.

The host owns verifiers, support adapters and authenticated human decisions.
Module `next` is advisory and never authorizes another execution.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
from typing import Callable
from uuid import uuid4

from core.modules_loader.router import execution_plan
from core.runtime import engine_v2
from workflows import orchestration as orc


class WorkflowRuntime:
    def __init__(self, directory: Path, *, verifier: Callable,
                 runner=None, authority_context=None):
        if not callable(verifier):
            raise ValueError('trusted verifier must be callable')
        self.directory = Path(directory)
        self.verifier = verifier
        self.runner = runner or engine_v2.run
        self.authority_context = deepcopy(authority_context or {})

    @staticmethod
    def _stage(stage):
        if not isinstance(stage, dict) or not isinstance(stage.get('task'), str):
            raise ValueError('stage.task must be a registered task name')
        if not isinstance(stage.get('request', {}), dict):
            raise ValueError('stage.request must be an object')
        normalized = deepcopy(stage)
        module = execution_plan(stage['task'])['run_with']
        if stage.get('module', module) != module:
            raise ValueError('stage module does not match registry route')
        normalized.update(module=module, request=deepcopy(stage.get('request', {})))
        try:
            json.dumps(normalized, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise ValueError('stage must be JSON serializable') from exc
        return normalized

    def _evidence(self, task, kind, value):
        orc.validate(task)
        # Serialize before creating a file, so malformed results leave no partial JSON.
        encoded = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
        folder = self.directory / task['task_id']
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f'{kind}-{uuid4().hex}.json'
        with path.open('x', encoding='utf-8') as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        return str(path.resolve())

    def _save(self, task):
        orc.save(task, self.directory / 'tasks')
        return task

    def _block(self, task, reason, evidence):
        task['blocker'] = {'reason': reason, 'evidence': evidence}
        orc.advance(task, 'BLOCKED', actor='Orchestration', detail=reason, evidence=evidence)
        return self._save(task)

    def _prepare(self, task, stages):
        orc.validate(task)
        if task['status'] != 'RECEIVED' or 'runtime_circuit' in task or not isinstance(stages, list) or not stages:
            raise ValueError('new task and nonempty explicit stage list required')
        normalized = [self._stage(stage) for stage in stages]
        ref = self._evidence(task, 'pipeline', {'stages': normalized})
        task['evidence'].append({'at': orc.timestamp(), 'actor': 'pipeline-plan', 'ref': ref})
        task['runtime_circuit'] = {
            'version': 1, 'stages': normalized, 'index': 0, 'effective_stage': None,
            'result_ref': None, 'previous_result_ref': None, 'verified': False,
        }
        self._save(task)

    @staticmethod
    def _state(task):
        orc.validate(task)
        state = task.get('runtime_circuit')
        if not isinstance(state, dict):
            raise ValueError('saved circuit state required; reconcile older task snapshots first')
        return state

    def _verify(self, task, stage, result):
        try:
            verdict = self.verifier(deepcopy(stage), deepcopy(result))
            if not isinstance(verdict, dict) or type(verdict.get('passed')) is not bool:
                verdict = {'passed': False, 'reason': 'verifier must return a boolean passed field'}
            json.dumps(verdict, allow_nan=False)
        except Exception as exc:
            verdict = {'passed': False, 'reason': str(exc)}
        return verdict, self._evidence(task, 'verification', verdict)

    def execute_stage(self, task, stage):
        """Execute the current saved stage; never replay interrupted IN_PROGRESS work."""
        normalized = self._stage(stage)
        if 'runtime_circuit' not in task:
            self._prepare(task, [normalized])
        state = self._state(task)
        expected = state['stages'][state['index']]
        if normalized != expected:
            raise ValueError('execution must use the original stage parameters')
        job, module = expected['task'], expected['module']
        if task['status'] not in {'RECEIVED', 'QUEUED', 'RETURNED'}:
            raise ValueError('stage requires RECEIVED, QUEUED or RETURNED; reconcile interrupted work')
        if task['status'] == 'RETURNED' and task['destination'] != {'module': module, 'task': job}:
            raise ValueError('support must return to original stage')
        if state['effective_stage'] is None:
            effective = deepcopy(expected)
            if state['previous_result_ref']:
                previous = json.loads(Path(state['previous_result_ref']).read_text(encoding='utf-8'))
                effective['request'].setdefault('payload', previous.get('agent_result', {}))
            else:
                effective['request'].setdefault('payload', deepcopy(task['payload']))
            state['effective_stage'] = effective
        effective = state['effective_stage']
        if task['status'] == 'RECEIVED':
            orc.advance(task, 'INSPECTING', actor='Orchestration', detail='explicit stage inspected')
            orc.advance(task, 'QUEUED', actor='Orchestration', detail='stage ready')
        if task['status'] == 'RETURNED':
            orc.advance(task, 'IN_PROGRESS', actor=module, detail='resuming original stage after support')
        else:
            def notify(handoff):
                ref = self._evidence(task, 'handoff', {**handoff, 'stage': effective})
                return {'delivered': True, 'evidence': ref}
            orc.route(task, {'module': module, 'task': job}, actor='Orchestration', notify=notify)
            ack = self._evidence(task, 'ack', {'module': module, 'task': job,
                                             'accepted_by': 'local runtime bridge'})
            orc.advance(task, 'ACKNOWLEDGED', actor='local-runtime',
                        detail='local invocation accepted; not an external AI acknowledgement', evidence=ack)
            orc.advance(task, 'IN_PROGRESS', actor=module, detail='executor starting')
        state['verified'] = False
        state['result_ref'] = None
        self._save(task)  # durable intent before executor side effects
        request = deepcopy(effective['request'])
        request.update(task_id=task['task_id'], source_id=task.get('source_id'))
        request.setdefault('source', task['origin']['module'])
        # target is the work subject, e.g. W3API; the registry chooses executor.
        try:
            result = self.runner(job, request, authority_context=deepcopy(self.authority_context))
            if not isinstance(result, dict) or not isinstance(result.get('status'), str):
                raise ValueError('runner must return a result object with status')
            if not isinstance(result.get('agent_result', {}), dict) or not isinstance(result.get('result_validation', {}), dict):
                raise ValueError('invalid runtime result envelope')
            json.dumps(result, allow_nan=False)
        except Exception as exc:
            result = {'status': 'FAILED', 'error': str(exc)}
        ref = self._evidence(task, 'result', result)
        state['result_ref'] = ref
        task['evidence'].append({'at': orc.timestamp(), 'actor': 'runtime-result', 'ref': ref})
        agent = result.get('agent_result', {})
        task['mutated'] = task['mutated'] or bool(agent.get('mutated'))
        self._save(task)
        if result['status'] not in {'COMPLETED', 'ACTIVE', 'REVIEW_REQUIRED', 'REVIEW', 'STOP'}:
            return self._block(task, 'executor did not produce a usable result', ref)
        if result.get('result_validation', {}).get('status') != 'valid':
            return self._block(task, 'runtime result contract requires review', ref)
        if result['status'] in {'REVIEW_REQUIRED', 'REVIEW', 'STOP'} or agent.get('review'):
            task['human_review_required'] = True
            orc.advance(task, 'VERIFYING', actor=module, detail='result needs human review', evidence=ref)
            orc.advance(task, 'WAITING_HUMAN', actor='Orchestration', detail='review gate', evidence=ref)
            return self._save(task)
        verdict, verification = self._verify(task, effective, result)
        if not verdict['passed']:
            return self._block(task, 'stage postcondition not verified', verification)
        state['verified'] = True
        orc.advance(task, 'VERIFYING', actor='trusted-verifier',
                    detail='stage postcondition verified', evidence=verification)
        return self._save(task)

    def run(self, task, stages):
        """Start a validated explicit pipeline and stop at the first unresolved stage."""
        self._prepare(task, stages)
        return self.continue_work(task)

    def continue_work(self, task):
        """Continue the saved plan after review or support, without skipping stages.

        Load a task JSON snapshot and use this method after restarting the host.
        Interrupted IN_PROGRESS work is not replayed; reconcile its side effects.
        """
        state = self._state(task)
        while task['status'] in {'RECEIVED', 'QUEUED', 'RETURNED', 'VERIFYING'}:
            if task['status'] != 'VERIFYING':
                self.execute_stage(task, state['stages'][state['index']])
            if task['status'] != 'VERIFYING':
                return task
            if not state['verified']:
                raise ValueError('current stage must pass its verifier before continuing')
            if task['human_review_required'] and not task.get('human_approval'):
                orc.advance(task, 'WAITING_HUMAN', actor='Orchestration', detail='human review of verified stage')
                return self._save(task)
            if state['index'] == len(state['stages']) - 1:
                orc.advance(task, 'COMPLETED', actor='Orchestration', detail='all explicit stages verified')
                return self._save(task)
            state.update(index=state['index'] + 1, previous_result_ref=state['result_ref'],
                         result_ref=None, effective_stage=None, verified=False)
            orc.advance(task, 'QUEUED', actor='Orchestration', detail='next explicit stage')
            self._save(task)
        if task['status'] in {'IN_PROGRESS', 'ROUTED', 'ACKNOWLEDGED', 'ASSISTING', 'INSPECTING'}:
            raise ValueError('interrupted work requires reconciliation; refusing automatic replay')
        return task

    def assist(self, task, *, kind, name, handler):
        """Call a host-selected adapter and preserve its result before returning."""
        self._state(task)
        def isolated(context):
            result = handler(deepcopy(context))
            if not isinstance(result, dict) or type(result.get('resolved')) is not bool or not isinstance(result.get('evidence'), str) or not result['evidence'].strip():
                raise ValueError('support must return resolved and a nonempty evidence reference')
            ref = self._evidence(task, 'support', result)
            return {**result, 'evidence': ref}
        orc.assist(task, kind=kind, name=name, actor='Orchestration', handler=isolated)
        return self._save(task)

    def review_stage(self, task, stage, *, human, evidence):
        """Authenticate human in the host, then recheck the exact executed stage."""
        state = self._state(task)
        if task['status'] != 'WAITING_HUMAN':
            raise ValueError('task must be waiting for human review')
        if self._stage(stage) != state['stages'][state['index']]:
            raise ValueError('review must use the original stage parameters')
        if not isinstance(human, str) or not human.strip() or not isinstance(evidence, str) or not evidence.strip():
            raise ValueError('human identity and review evidence required')
        result = json.loads(Path(state['result_ref']).read_text(encoding='utf-8'))
        if result['status'] not in {'COMPLETED', 'ACTIVE'} or result.get('result_validation', {}).get('status') != 'valid':
            raise ValueError('unresolved or stopped execution must be corrected before approval')
        verdict, checked = self._verify(task, state['effective_stage'], result)
        if not verdict['passed']:
            task['evidence'].append({'at': orc.timestamp(), 'actor': 'failed-review-verifier', 'ref': checked})
            self._save(task)
            raise ValueError('reviewed stage postcondition not verified')
        if task['blocker'] is not None:
            raise ValueError('unresolved blocker must be addressed before review')
        state['verified'] = True
        orc.advance(task, 'VERIFYING', actor='trusted-verifier',
                    detail='reviewed stage postcondition verified', evidence=checked)
        orc.approve(task, human=human, evidence=evidence)
        return self._save(task)

    def revise_stage(self, task, *, request, actor, evidence):
        """Record a host-authorized request correction, keeping job and owner fixed.

        This queues a retry; it does not execute it or approve its result. The host
        must reconcile any prior side effects before authorizing such a retry.
        """
        state = self._state(task)
        if task['status'] not in {'WAITING_HUMAN', 'BLOCKED'}:
            raise ValueError('only unresolved stages may be revised')
        if not isinstance(actor, str) or not actor.strip() or not isinstance(evidence, str) or not evidence.strip():
            raise ValueError('revision actor and evidence required')
        original = state['stages'][state['index']]
        revised = self._stage({**original, 'request': request})
        ref = self._evidence(task, 'revision', {
            'original': original, 'revised': revised, 'actor': actor, 'evidence': evidence,
            'previous_result_ref': state['result_ref'],
        })
        if task['status'] == 'BLOCKED':
            orc.advance(task, 'WAITING_HUMAN', actor=actor,
                        detail='host authorized request correction', evidence=ref)
        state['stages'][state['index']] = revised
        state.update(effective_stage=None, result_ref=None, verified=False)
        task['blocker'] = None
        orc.advance(task, 'QUEUED', actor=actor, detail='revised current stage queued', evidence=ref)
        return self._save(task)
