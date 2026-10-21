"""Explicit, evidence-led bridge from Orchestration to local runtime executors.

The host supplies a bounded stage list, trusted verifier, and any support adapter.
Module `next` is advisory: it never grants another execution or authority.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Callable
from uuid import uuid4

from core.modules_loader.router import execution_plan
from core.runtime import engine_v2
from workflows import orchestration as orc


class WorkflowRuntime:
    def __init__(self, directory: Path, *, verifier: Callable,
                 runner=None, authority_context=None):
        self.directory = Path(directory)
        self.verifier = verifier
        self.runner = runner or engine_v2.run
        self.authority_context = deepcopy(authority_context or {})

    def _evidence(self, task, kind, value):
        orc.validate(task)
        folder = self.directory / task['task_id']
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f'{kind}-{uuid4().hex}.json'
        with path.open('x', encoding='utf-8') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
        return str(path.resolve())

    def _save(self, task):
        orc.save(task, self.directory / 'tasks')
        return task

    def _block(self, task, reason, evidence):
        task['blocker'] = {'reason': reason, 'evidence': evidence}
        orc.advance(task, 'BLOCKED', actor='Orchestration', detail=reason, evidence=evidence)
        return self._save(task)

    def execute_stage(self, task, stage):
        """Run one explicit stage; RETURNED retries only the original job.

        IN_PROGRESS after a host crash is deliberately not replayed: the host
        must reconcile side effects before arranging any retry.
        """
        orc.validate(task)
        job = stage['task']
        plan = execution_plan(job)  # validate before delivery or state changes
        module = plan['run_with']
        if stage.get('module', module) != module:
            raise ValueError('stage module does not match registry route')
        if task['status'] == 'RECEIVED':
            orc.advance(task, 'INSPECTING', actor='Orchestration', detail='explicit stage inspected')
            orc.advance(task, 'QUEUED', actor='Orchestration', detail='stage ready')
        if task['status'] == 'RETURNED':
            if task['destination'] != {'module': module, 'task': job}:
                raise ValueError('support must return to original stage')
            orc.advance(task, 'IN_PROGRESS', actor=module, detail='resuming after support')
        elif task['status'] == 'QUEUED':
            def notify(handoff):
                ref = self._evidence(task, 'handoff', handoff)
                return {'delivered': True, 'evidence': ref}
            orc.route(task, {'module': module, 'task': job}, actor='Orchestration', notify=notify)
            ack = self._evidence(task, 'ack', {'module': module, 'task': job,
                                             'accepted_by': 'local runtime bridge'})
            orc.advance(task, 'ACKNOWLEDGED', actor='local-runtime',
                        detail='local invocation accepted; not an external AI acknowledgement', evidence=ack)
            orc.advance(task, 'IN_PROGRESS', actor=module, detail='executor starting')
        else:
            raise ValueError('stage requires RECEIVED, QUEUED or RETURNED')
        self._save(task)  # durable intent before executor side effects
        request = deepcopy(stage.get('request', {}))
        request.update(task_id=task['task_id'], source_id=task.get('source_id'),
                       source=task['origin']['module'], target=module)
        # Transport correlation only; this cannot supply trusted authority.
        try:
            result = self.runner(job, request, authority_context=self.authority_context)
        except Exception as exc:
            result = {'status': 'FAILED', 'error': str(exc)}
        ref = self._evidence(task, 'result', result)
        task['evidence'].append({'at': orc.timestamp(), 'actor': 'runtime-result', 'ref': ref})
        self._save(task)
        agent = result.get('agent_result', {})
        task['mutated'] = task['mutated'] or bool(agent.get('mutated'))
        validation = result.get('result_validation', {})
        if validation.get('status') != 'valid':
            return self._block(task, 'runtime result contract requires review', ref)
        if result['status'] in {'REVIEW_REQUIRED', 'REVIEW', 'STOP'} or agent.get('review'):
            task['human_review_required'] = True
            orc.advance(task, 'VERIFYING', actor=module, detail='result needs human review', evidence=ref)
            orc.advance(task, 'WAITING_HUMAN', actor='Orchestration', detail='review gate', evidence=ref)
            return self._save(task)
        if result['status'] not in {'COMPLETED', 'ACTIVE'}:
            return self._block(task, 'executor did not produce a usable result', ref)
        # ACTIVE can finish a narrowly defined stage only when the trusted
        # verifier establishes its actual postcondition (e.g. a saved log).
        try:
            verdict = self.verifier(deepcopy(stage), deepcopy(result))
        except Exception as exc:
            verdict = {'passed': False, 'reason': str(exc)}
        verification = self._evidence(task, 'verification', verdict)
        if not isinstance(verdict, dict) or verdict.get('passed') is not True:
            return self._block(task, 'stage postcondition not verified', verification)
        orc.advance(task, 'VERIFYING', actor='trusted-verifier',
                    detail='stage postcondition verified', evidence=verification)
        return self._save(task)

    def run(self, task, stages):
        """Execute an explicit finite pipeline; stop at the first unresolved stage."""
        orc.validate(task)
        if task['status'] != 'RECEIVED' or not stages:
            raise ValueError('new task and nonempty explicit stages required')
        # Reject unknown or mismatched routes before doing any work.
        for stage in stages:
            module = execution_plan(stage['task'])['run_with']
            if stage.get('module', module) != module:
                raise ValueError('stage module does not match registry route')
        plan_ref = self._evidence(task, 'pipeline', {'stages': stages})
        task['evidence'].append({'at': orc.timestamp(), 'actor': 'pipeline-plan', 'ref': plan_ref})
        self._save(task)
        for index, stage in enumerate(stages):
            stage = deepcopy(stage)
            prior = next((item['ref'] for item in reversed(task['evidence'])
                          if item['actor'] == 'runtime-result'), None)
            if prior:
                previous = json.loads(Path(prior).read_text(encoding='utf-8'))
                stage.setdefault('request', {}).setdefault('payload', previous.get('agent_result', {}))
            self.execute_stage(task, stage)
            if task['status'] != 'VERIFYING':
                return task
            if index + 1 < len(stages):
                # Only this bridge's verified stage may authorize continuation.
                orc.advance(task, 'QUEUED', actor='Orchestration', detail='next explicit stage')
                self._save(task)
        if task['human_review_required']:
            orc.advance(task, 'WAITING_HUMAN', actor='Orchestration', detail='final human review')
        else:
            orc.advance(task, 'COMPLETED', actor='Orchestration', detail='all explicit stages verified')
        return self._save(task)

    def assist(self, task, *, kind, name, handler):
        """Run a host-selected support adapter; caller explicitly resumes afterwards."""
        orc.assist(task, kind=kind, name=name, actor='Orchestration', handler=handler)
        return self._save(task)

    def review_stage(self, task, stage, *, human, evidence):
        """Trusted host records human review, but still verifies the postcondition.

        Returns VERIFYING; host may close a final stage or queue the next explicit
        stage. Human identity must be authenticated by the calling environment.
        """
        if task['status'] != 'WAITING_HUMAN':
            raise ValueError('task must be waiting for human review')
        if task['destination']['task'] != stage['task']:
            raise ValueError('review must refer to current stage')
        ref = next(item['ref'] for item in reversed(task['evidence'])
                   if item['actor'] == 'runtime-result')
        result = json.loads(Path(ref).read_text(encoding='utf-8'))
        if result['status'] not in {'COMPLETED', 'ACTIVE'}:
            raise ValueError('unresolved or stopped execution must be corrected before approval')
        verdict = self.verifier(deepcopy(stage), deepcopy(result))
        if not isinstance(verdict, dict) or verdict.get('passed') is not True:
            raise ValueError('reviewed stage postcondition not verified')
        if not isinstance(human, str) or not human.strip() or not isinstance(evidence, str) or not evidence.strip():
            raise ValueError('human identity and review evidence required')
        checked = self._evidence(task, 'verification', verdict)
        orc.advance(task, 'VERIFYING', actor='trusted-verifier',
                    detail='reviewed stage postcondition verified', evidence=checked)
        orc.approve(task, human=human, evidence=evidence)
        return self._save(task)
