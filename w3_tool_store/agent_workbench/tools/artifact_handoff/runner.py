"""One bounded work item: Cast produces; Gemini checks; owner receives.

Uses existing module executors and Orchestration transitions. The stopping point
is a verified delivery awaiting its owner's review, never a self-issued approval.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from uuid import uuid4

from core.modules_loader.router import execution_plan
from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import atomic_write
from workflows import orchestration as orc

ROOT = Path(__file__).resolve().parents[4]
RULES = {
    'schema': 'w3.artifact_review_rules/1',
    'profile': 'cast_source_inspection',
    'checks': ['artifact_hashes', 'request_and_trace_binding', 'source_hashes',
               'source_structure_matches_source', 'private_pattern_separate',
               'idp_reference', 'no_source_write'],
    'expected_stop': 'WAITING_HUMAN',
    'authority': 'technical verification only; owner review is separate',
}


def write(path, value):
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_inside(root, name):
    if not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('repository-relative evidence path required')
    path = (root/name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('evidence outside repository')
    return path.read_bytes()


def verify_artifacts(root, produced, request, rules):
    """Recompute evidence; never accept producer-supplied PASS flags."""
    root = Path(root).resolve()
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
    try:
        check('trusted_rule_profile', rules == RULES)
        artifacts = produced['artifacts']
        expected_kinds = ['w3.cast.structure_report.json', 'w3.cast.private_pattern.json']
        check('two_distinct_artifacts', len(artifacts) == 2 and
              [a['kind'] for a in artifacts] == expected_kinds and artifacts[0]['path'] != artifacts[1]['path'])
        if not checks[-1]['passed']:
            return checks
        documents = []
        for info in artifacts:
            data = read_inside(root, info['path'])
            check(info['kind']+':hash', sha(data) == info['sha256'] and len(data) == info['bytes'])
            documents.append(json.loads(data))
        report, pattern = documents
        check('request_and_trace_binding', report['request_id'] == request['request_id'] == pattern['request_id']
              and report['trace_id'] == produced['trace_id'] == pattern['trace_id'])
        check('source_paths_match_request', [r['path'] for r in report['facts']] == request['source_paths'])
        for row in report['facts']:
            data = read_inside(root, row['path'])
            check(row['path']+':source_hash', sha(data) == row['sha256'] and len(data) == row['bytes'])
            if row['path'].endswith('.py'):
                text = data.decode('utf-8')
                tree = ast.parse(text)
                symbols = [{'name': n.name, 'line': n.lineno, 'kind': type(n).__name__}
                           for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                imports = [ast.get_source_segment(text, n) for n in ast.walk(tree)
                           if isinstance(n, (ast.Import, ast.ImportFrom))]
                calls = [{'expression': ast.unparse(n.func), 'line': n.lineno}
                         for n in ast.walk(tree) if isinstance(n, ast.Call)]
                check(row['path']+':structure', row['symbols'] == symbols and row['imports'] == imports and row['calls'] == calls)
            elif row['path'].endswith('.json'):
                value = json.loads(data)
                check(row['path']+':structure', row['json_type'] == type(value).__name__ and
                      row['keys'] == (sorted(value) if isinstance(value, dict) else []))
            else:
                check(row['path']+':structure', row['headings'] ==
                      [line for line in data.decode('utf-8').splitlines() if line.startswith('#')])
        check('private_pattern_separate', pattern['source_truth'] is False and
              pattern['report_path'] == artifacts[0]['path'] and
              pattern['basis'] == [{'path': r['path'], 'sha256': r['sha256']} for r in report['facts']])
        check('idp_reference', report['idp']['version'] == '2.0' and
              sha(read_inside(root, report['idp']['path'])) == report['idp']['sha256'])
        check('no_source_write', report['source_modified'] is False and produced['source_modified'] is False)
    except (OSError, ValueError, TypeError, KeyError, SyntaxError) as exc:
        checks.append({'name': 'read_and_verify_artifacts', 'passed': False, 'reason': str(exc)})
    return checks


def run(root, output, source_paths):
    root, output = Path(root).resolve(), Path(output).resolve()
    allowed = root/'modules/ChatGPT/reports/handoffs'
    if not output.is_relative_to(allowed) or output == allowed:
        raise ValueError('output must be a new handoff evidence directory')
    output.mkdir(parents=True, exist_ok=False)  # an existing delivery is never replayed
    identifier = str(uuid4().int)
    request = {'request_id': 'RQ-ARTIFACT-HANDOFF-'+identifier,
               'intent': 'Create a source inspection report and separate private pattern; independently verify and return to owner.',
               'source_paths': source_paths, 'expected_stop': RULES['expected_stop'],
               'final_signoff_required': True, 'not_required': 'activation of every W3 system'}
    request_path, rules_path = output/'request.json', output/'rules.json'
    write(request_path, request)
    write(rules_path, RULES)
    task = orc.new_task('W3-ORC-20261102-'+identifier, 'REQUEST', 'NORMAL',
                        {'module': 'BBX19', 'tier': 0}, request,
                        source_id=request['request_id'], human_review_required=True)
    def persist():
        return orc.save(task, output/'tasks')
    def evidence(name, value):
        path = output/(name+'.json')
        write(path, value)
        return str(path.relative_to(root))
    def advance(status, actor, detail, ref=None):
        orc.advance(task, status, actor=actor, detail=detail, evidence=ref)
        persist()
    def handoff(module, job, payload):
        def notify(message):
            ref = evidence(module+'-handoff', {**message, 'input': payload,
                                               'rules_path': str(rules_path.relative_to(root))})
            return {'delivered': True, 'evidence': ref}
        orc.route(task, {'module': module, 'task': job}, actor='Orchestration', notify=notify)
        persist()
        ack = evidence(module+'-ack', {'accepted_by': 'local module executor', 'module': module,
                                      'request_id': request['request_id']})
        advance('ACKNOWLEDGED', module, 'Local executor accepted this bounded work', ack)
        advance('IN_PROGRESS', module, 'Invoke existing module executor')
    persist()
    advance('INSPECTING', 'Orchestration', 'Explicit work item and stopping condition recorded')
    advance('QUEUED', 'Orchestration', 'Cast produces; Gemini reviews; owner receives')
    handoff('Cast', 'structural_inspect', request)
    produced = get_agent('Cast').execute('structural_inspect', execution_plan('structural_inspect'),
        {'authority_context': {'repo_root': str(root)},
         'request': {'source_id': request['request_id']}, 'payload': {'source_paths': source_paths}})
    produced_ref = evidence('Cast-result', produced)
    task['mutated'] = bool(produced.get('mutated'))
    # This is an artifact review handoff requested by Cast, not approval of its
    # source changes or the use of WorkflowRuntime to bypass its review gate.
    checks = verify_artifacts(root, produced, request, RULES)
    initial = evidence('pre-review-checks', checks)
    if produced['status'] != 'COMPLETED' or not checks or not all(c['passed'] for c in checks):
        task['blocker'] = {'reason': 'Producer output cannot be verified', 'evidence': initial}
        advance('BLOCKED', 'Orchestration', 'Retain producer output and stop', initial)
        return {'status': task['status'], 'task': task, 'output': str(output.relative_to(root))}
    advance('VERIFYING', 'host-artifact-verifier', 'Verify files before handing them to reviewer', initial)
    advance('QUEUED', 'Orchestration', 'Deliver Cast review request to Gemini')
    handoff('Gemini', 'verify', {'produced_result': produced_ref, 'rules_path': str(rules_path.relative_to(root))})
    # Read persisted producer output and rules afresh at the recipient boundary.
    checks = verify_artifacts(root, json.loads(read_inside(root, produced_ref)), request,
                              json.loads(rules_path.read_bytes()))
    verdict = get_agent('Gemini').execute('verify', execution_plan('verify'),
        {'target': request['request_id'], 'checks': checks, 'evidence': produced['artifacts'],
         'event_identity': {'chain_id': task['task_id'], 'event_id': produced['trace_id'],
                            'sequence': 2, 'owner_scope': 'artifact-review'}})
    verdict_ref = evidence('Gemini-result', verdict)
    if verdict['status'] != 'COMPLETED' or verdict['decision'] != 'VERIFIED':
        task['blocker'] = {'reason': 'Technical review did not pass', 'evidence': verdict_ref}
        advance('BLOCKED', 'Gemini', 'Retain unresolved checks and stop', verdict_ref)
    else:
        advance('VERIFYING', 'Gemini', 'Independent artifact checks passed', verdict_ref)
        advance('WAITING_HUMAN', 'Orchestration', 'Expected final delivery; no more automatic work')
    delivery = {'schema': 'w3.artifact_delivery/1', 'request_id': request['request_id'],
                'task_id': task['task_id'], 'status': task['status'],
                'technical_result': 'VERIFIED' if verdict['decision'] == 'VERIFIED' else 'UNRESOLVED',
                'expected_stop_reached': task['status'] == request['expected_stop'],
                'recipient': 'BBX19', 'human_approval': None, 'automatic_continuation': False,
                'artifacts': produced['artifacts'], 'rules': str(rules_path.relative_to(root)),
                'verification': verdict_ref, 'task_snapshot': str(persist().relative_to(root)),
                'scope': 'this source report and private pattern only; not all W3 systems'}
    write(output/'delivery.json', delivery)
    return delivery


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('source_paths', nargs='+')
    args = parser.parse_args()
    print(json.dumps(run(ROOT, args.output, args.source_paths), ensure_ascii=False, indent=2))
