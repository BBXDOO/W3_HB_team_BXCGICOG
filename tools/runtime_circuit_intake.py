"""Root request -> saved Orchestration circuit -> registered executors -> checked artifacts.

Executors and verifiers are Python callbacks supplied by the trusted host, not
import strings, commands, approval flags or provider settings from a request.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from core.runtime import engine_v2
from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import atomic_write
from core.runtime.capabilities import log_analysis
from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime


def task_id(request_id):
    number = int(hashlib.sha256(request_id.encode()).hexdigest()[:24], 16)
    return f'W3-ORC-1-{number}'


def parse_spec(request, *, flows=None):
    matches = re.findall(r'^```w3-circuit\s*\n(.*?)^```\s*$', request['_request_text'], re.S | re.M)
    if len(matches) != 1:
        raise ValueError('runtime_circuit request needs exactly one w3-circuit JSON block')
    spec = json.loads(matches[0])
    if not isinstance(spec, dict):
        raise ValueError('w3-circuit must be an object')
    if 'workflow' in spec:
        if 'stages' in spec or set(spec) - {'workflow', 'input'}:
            raise ValueError('use workflow/input or explicit stages')
        if flows is None:
            from tools.orchestration_support import default_flows
            flows = default_flows()
        spec = {'stages': flows.plan(spec['workflow'], spec.get('input', {}))}
    if not isinstance(spec.get('stages'), list) or not spec['stages']:
        raise ValueError('w3-circuit stages must be a nonempty list')
    return spec


def _inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('artifact or source path escapes repository')
    return path


def log_report_checks(agent, root):
    """Check recorded output against its immutable input; no caller-supplied PASS."""
    artifacts = agent.get('artifacts', [])
    reports = [item for item in artifacts if item.get('kind') == 'w3.lrc2.log_analysis.json']
    checks = []
    if len(reports) != 1:
        return [{'name': 'single_analysis_report', 'passed': False}]
    try:
        info = reports[0]
        path = _inside(root, info['path'])
        data = path.read_bytes()
        report = json.loads(data)
        records, _ = log_analysis.load_records({'source_file': report['source']}, root)
        expected = log_analysis.analyze(records, **report['settings'])
        checks = [
            {'name': 'report_sha256', 'passed': hashlib.sha256(data).hexdigest() == info['sha256']},
            {'name': 'input_sha256', 'passed': hashlib.sha256(log_analysis.canonical(records)).hexdigest() == report['source_sha256']},
            {'name': 'source_record_count', 'passed': report['records_total'] == len(records)},
            {'name': 'analysis_matches_source', 'passed': all(report[key] == value for key, value in expected.items())},
            {'name': 'trace_matches_execution', 'passed': report['trace_id'] == agent['trace_id']},
            {'name': 'task_identity_matches', 'passed': report['task_id'] == agent['details']['identity']['chain_id']},
        ]
    except (OSError, KeyError, TypeError, ValueError) as exc:
        checks.append({'name': 'read_report_and_source', 'passed': False, 'reason': str(exc)})
    return checks


def make_runtime(root, *, executors=None, verifiers=None):
    """Keep all existing module executors; host callbacks can extend any role."""
    root = Path(root).resolve()
    def lrc2(job, plan, context):
        if job == 'log_analysis':
            return log_analysis.execute(job, plan, context, repo_root=root)
        return get_agent('LRC2').execute(job, plan, context)
    def gemini(job, plan, context):
        previous = context.get('payload', {})
        if isinstance(previous, dict) and previous.get('capability') == 'log_analysis':
            checks = log_report_checks(previous, root)
            context = deepcopy(context)
            context['payload'] = {'checks': checks, 'evidence': previous.get('artifacts', [])}
            outcome = get_agent('Gemini').execute(job, plan, context)
            outcome.update(capability='source_artifact_verification',
                           checked_agent_result=previous)
            return outcome
        return get_agent('Gemini').execute(job, plan, context)
    handlers = {'LRC2': lrc2, 'Gemini': gemini, **(executors or {})}
    policies = dict(verifiers or {})
    def runner(job, request, *, authority_context=None):
        return engine_v2.run(job, request, authority_context=authority_context, executors=handlers)
    def verify(stage, result):
        if stage['task'] in policies:
            return policies[stage['task']](deepcopy(stage), deepcopy(result))
        agent = result.get('agent_result', {})
        capability = agent.get('capability')
        if capability == 'adopted_document_result':
            from tools.document_creation_flow import _document_checks
            try:
                artifact = _inside(root, agent['artifact_path'])
                checks = _document_checks(artifact.read_text(), artifact, agent['artifact_sha256'])
                source = json.loads(_inside(root, agent['source_receipt']).read_text())['runtime_result']
                checks.append({'name': 'existing_receipt_matches_artifact', 'passed':
                    source.get('artifact_path') == agent['artifact_path'] and
                    source.get('artifact_sha256') == agent['artifact_sha256'] and
                    source.get('gemini_result', {}).get('status') == 'COMPLETED'})
            except (OSError, ValueError, KeyError, TypeError) as exc:
                checks = [{'name': 'existing_document_verification', 'passed': False, 'reason': str(exc)}]
        elif capability == 'log_analysis':
            checks = log_report_checks(agent, root)
        elif capability == 'source_artifact_verification':
            # Recompute on continuation too, so stale/tampered evidence cannot
            # be accepted merely because an earlier Gemini stamp said VERIFIED.
            checks = log_report_checks(agent['checked_agent_result'], root)
            checks.append({'name': 'gemini_verified', 'passed': agent.get('decision') == 'VERIFIED'})
        else:
            return {'passed': False, 'reason': f'No context/outcome verifier registered for {capability or stage["task"]}'}
        return {'passed': bool(checks) and all(check['passed'] is True for check in checks), 'checks': checks}
    return WorkflowRuntime(root / 'repo_events/runtime_circuit', runner=runner, verifier=verify, reference_root=root)


def run_request(*, request, repo_root, target_module=None, executors=None, verifiers=None):
    root = Path(repo_root).resolve()
    rid = str(request['request_id'])
    request_digest = hashlib.sha256(request['_request_text'].encode()).hexdigest()
    circuit = make_runtime(root, executors=executors, verifiers=verifiers)
    snapshot = circuit.directory / 'tasks' / f'{task_id(rid)}.json'
    if snapshot.exists():
        task = json.loads(snapshot.read_text(encoding='utf-8'))
        orc.validate(task)
        if task.get('source_id') != rid or task['payload'].get('request_sha256') != request_digest:
            raise ValueError('request identity/content changed; revise explicitly or use a new request_id')
        circuit.continue_work(task)
    else:
        spec = parse_spec(request)
        # Fully validate every requested route before input snapshots or execution.
        stages = [WorkflowRuntime._stage(stage) for stage in spec['stages']]
        if target_module and stages[0]['module'] != target_module:
            raise ValueError('target_module must match the first explicit stage')
        for stage in stages:
            transport = stage['request']
            if any(key in transport for key in ('authority_context', 'approved', 'governance_approved')):
                raise ValueError('authority cannot be granted from request data')
            transport.setdefault('request_text', request['_request_text'])
            transport.setdefault('_request_file', request['_request_file'])
            transport.setdefault('intent', rid)
        # Freeze a live log file once, before runtime memory adds its own result.
        for stage in stages:
            payload = stage['request'].get('payload', {})
            if stage['task'] == 'log_analysis' and isinstance(payload, dict) and 'source_file' in payload:
                records, source = log_analysis.load_records(payload, root)
                data = log_analysis.canonical(records) + b'\n'
                digest = hashlib.sha256(data).hexdigest()
                path = _inside(root, f'repo_events/runtime_circuit/inputs/{digest}.json')
                if path.exists() and path.read_bytes() != data:
                    raise ValueError('immutable input snapshot was modified')
                if not path.exists():
                    atomic_write(path, data)
                payload.update(source_file=str(path.relative_to(root)), original_source=source)
        task = orc.new_task(task_id(rid), 'REQUEST', str(request.get('priority') or 'NORMAL'),
                            {'module': str(request.get('requester') or 'requests/'), 'tier': 0},
                            {'request_id': rid, 'source_request': request['_request_file'],
                             'request_sha256': request_digest}, source_id=rid,
                            human_review_required=bool(request.get('final_signoff_required', True)))
        from workflows.human_callback import ensure_intent
        ensure_intent(circuit, task, request)
        circuit.run(task, stages, review_policy="final")
    if task['status'] in {'WAITING_HUMAN', 'BLOCKED'}:
        from workflows.human_callback import prepare
        prepare(circuit, task, request)
    results = [json.loads(_inside(root, item['ref']).read_text(encoding='utf-8'))
               for item in task['evidence'] if item['actor'] == 'runtime-result']
    artifacts = []
    seen = set()
    for result in results:
        for artifact in result.get('artifacts', []):
            key = (artifact.get('path'), artifact.get('sha256'))
            if key[0] and key not in seen:
                seen.add(key)
                artifacts.append(artifact)
    return {'status': task['status'], 'task': 'runtime_circuit',
            'module': task.get('destination', {}).get('module') if task.get('destination') else None,
            'output': f"Request {rid}: {task['status']}; {len(results)} executor result(s), {len(artifacts)} file artifact(s).",
            'agent_result': results[-1].get('agent_result', {}) if results else {},
            'stage_results': results, 'artifacts': artifacts, 'mutated': task['mutated'],
            'orchestration_evidence': str(snapshot.relative_to(root)),
            'review': task['status'] not in {'COMPLETED', 'REJECTED', 'CANCELLED'},
            'closed': task['status'] in {'COMPLETED', 'REJECTED', 'CANCELLED'},
            'callback_path': task['payload'].get('human_cycle', {}).get('response_path') if task['status'] in {'WAITING_HUMAN', 'BLOCKED'} else None,
            'intent_id': task['payload'].get('human_cycle', {}).get('intent', {}).get('intent_id'),
            'trace_id': results[-1].get('trace_id') if results else None, 'time': engine_v2.now(),
            'circuit_revision': hashlib.sha256(log_analysis.canonical(task)).hexdigest()}


def main():
    import argparse
    from tools import request_cycle as rc
    parser = argparse.ArgumentParser(description='Run or explicitly review a saved W3 runtime circuit')
    parser.add_argument('--request', required=True, help='repository-relative root request Markdown')
    parser.add_argument('--review', action='store_true', help='record an authenticated host review, then continue')
    parser.add_argument('--human', help='reviewer identity supplied by the trusted calling environment')
    parser.add_argument('--evidence', help='reference to the actual human decision')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path = _inside(root, args.request)
    request = rc.parse_request(path)
    if request.get('request_type') != 'runtime_circuit':
        parser.error('request_type must be runtime_circuit')
    if args.review:
        if not args.human or not args.evidence:
            parser.error('--review requires --human and --evidence')
        from tools.human_callback import review_request
        result = review_request(root, path, human=args.human, evidence=args.evidence)
        print(json.dumps(result, ensure_ascii=False))
        return
    print(json.dumps(rc.process(path), ensure_ascii=False))


if __name__ == '__main__':
    main()
