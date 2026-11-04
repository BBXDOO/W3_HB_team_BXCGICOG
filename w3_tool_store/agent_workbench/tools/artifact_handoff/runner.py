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
from workflows.paired_work import PairedWork, record_fault, replacement

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
    if not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts or '.git' in Path(name).parts:
        raise ValueError('repository-relative evidence path required')
    path = (root/name).resolve()
    if not path.is_relative_to(root):
        raise ValueError('evidence outside repository')
    return path.read_bytes()


def verify_artifacts(root, produced, request, rules, baseline=None):
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
              [a['kind'] for a in artifacts] == expected_kinds and not (root/artifacts[0]['path']).samefile(root/artifacts[1]['path']))
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
        check('source_paths_match_request', [r['path'] for r in report['facts']] == list(dict.fromkeys(request['source_paths'])))
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
        canonical_idp = 'core/identity/profiles/Cast.idp.json'
        idp_data = read_inside(root, canonical_idp)
        idp = json.loads(idp_data)
        check('idp_reference', report['idp']['path'] == canonical_idp and
              report['idp']['version'] == idp.get('version') == '2.0' and idp.get('module') == 'Cast' and
              sha(idp_data) == report['idp']['sha256'])
        if baseline is not None:
            check('host_source_baseline', baseline == {p: sha(read_inside(root, p)) for p in baseline})
        check('no_source_write', baseline is not None and report['source_modified'] is False and produced['source_modified'] is False)
    except (OSError, ValueError, TypeError, KeyError, SyntaxError, IndexError, AttributeError) as exc:
        checks.append({'name': 'read_and_verify_artifacts', 'passed': False, 'reason': str(exc)})
    return checks


def run(root, output, source_paths):
    root, output = Path(root).resolve(), Path(output).resolve()
    allowed = root/'modules/ChatGPT/reports/handoffs'
    if not output.is_relative_to(allowed) or output == allowed:
        raise ValueError('output must be a new handoff evidence directory')
    output.mkdir(parents=True, exist_ok=False)  # an existing delivery is never replayed
    source_paths = list(dict.fromkeys(source_paths))
    identifier = str(uuid4().int)
    request = {'request_id': 'RQ-ARTIFACT-HANDOFF-'+identifier,
               'intent': 'Create a source inspection report and separate private pattern; independently verify and return to owner.',
               'source_paths': source_paths, 'expected_stop': RULES['expected_stop'],
               'final_signoff_required': True, 'not_required': 'activation of every W3 system'}
    request_path, rules_path = output/'request.json', output/'rules.json'
    write(request_path, request)
    write(rules_path, RULES)
    baseline = {}
    for path in dict.fromkeys([*source_paths, 'core/identity/profiles/Cast.idp.json']):
        try:
            baseline[path] = sha(read_inside(root, path))
        except (OSError, ValueError):
            baseline[path] = None
    write(output/'source-baseline.json', baseline)
    pair = PairedWork(root, str((output/'paired').relative_to(root)),
                      {'request_id': request['request_id'], 'evidence': [
                          {'path': str(p.relative_to(root)), 'sha256': sha(p.read_bytes())}
                          for p in (request_path, rules_path, output/'source-baseline.json')]})
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
        pair.transfer('Orchestration', 'host-artifact-verifier', module,
                      [str(request_path.relative_to(root)), str(rules_path.relative_to(root))],
                      [{'name': 'request_and_rules', 'passed': json.loads(request_path.read_bytes()) == request and json.loads(rules_path.read_bytes()) == RULES}])
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
    try:
        produced = get_agent('Cast').execute('structural_inspect', execution_plan('structural_inspect'),
            {'authority_context': {'repo_root': str(root)},
             'request': {'source_id': request['request_id']}, 'payload': {'source_paths': source_paths}})
    except (OSError, ValueError, TypeError, KeyError) as exc:
        produced = {'status': 'FAILED', 'artifacts': [], 'reason': str(exc)}
    produced_ref = evidence('Cast-result', produced)
    task['mutated'] = bool(produced.get('mutated'))
    # This is an artifact review handoff requested by Cast, not approval of its
    # source changes or the use of WorkflowRuntime to bypass its review gate.
    produced_hash = sha(read_inside(root, produced_ref))
    checks = verify_artifacts(root, produced, request, RULES, baseline)
    initial = evidence('pre-review-checks', checks)
    def blocked(reason, check_ref, accountable=None):
        task['blocker'] = {'reason': reason, 'evidence': check_ref}
        if task['status'] != 'BLOCKED':
            advance('BLOCKED', 'Orchestration', reason, check_ref)
        pair.note(accountable or 'Orchestration', reason, kind='error', evidence=check_ref)
        pair.transfer(accountable or 'Orchestration', 'host-artifact-verifier', 'Orchestration',
                      [check_ref], [{'name': 'delivery_valid', 'passed': False}])
        delivery = {'schema': 'w3.artifact_delivery/1', 'status': 'BLOCKED',
                    'request_id': request['request_id'], 'technical_result': 'UNRESOLVED',
                    'expected_stop_reached': False, 'human_approval': None,
                    'automatic_continuation': False, 'artifacts': produced.get('artifacts', []),
                    'failure': reason, 'checks': check_ref, 'paired_review': pair.audit(),
                    'task_snapshot': str(persist().relative_to(root)),
                    'replacement_pair': replacement(root, 'Cast', 'Gemini', [produced_ref])}
        write(output/'delivery.json', delivery)
        if accountable:
            try:
                delivery['fault_note'] = record_fault(root, accountable,
                    str((output/'delivery.json').relative_to(root)), delivery['paired_review']['conflicts'])
            except (OSError, ValueError) as exc:
                delivery['fault_note_error'] = str(exc)
        write(output/'delivery.json', delivery)
        return delivery
    if produced.get('status') != 'COMPLETED' or not checks or not all(c['passed'] for c in checks):
        return blocked('Producer output cannot be verified', initial,
                       'Cast' if produced.get('status') == 'COMPLETED' and
                       not any(c['name'] == 'host_source_baseline' and not c['passed'] for c in checks) else None)
    report = json.loads(read_inside(root, produced['artifacts'][0]['path']))
    for unknown in report.get('unknowns', []):
        pair.note('Cast', str(unknown), evidence=produced['artifacts'][0]['path'])
    pair.transfer('Cast', 'host-artifact-verifier', 'Gemini', [produced_ref, initial], checks)
    advance('VERIFYING', 'host-artifact-verifier', 'Verify files before handing them to reviewer', initial)
    advance('QUEUED', 'Orchestration', 'Deliver Cast review request to Gemini')
    handoff('Gemini', 'verify', {'produced_result': produced_ref, 'rules_path': str(rules_path.relative_to(root))})
    # Bind the recipient to the exact envelope seen before sending.
    try:
        received_bytes = read_inside(root, produced_ref)
        received = json.loads(received_bytes)
        checks = verify_artifacts(root, received, request, json.loads(rules_path.read_bytes()), baseline)
        checks.append({'name': 'producer_envelope_unchanged', 'passed': sha(received_bytes) == produced_hash})
    except (OSError, ValueError, TypeError) as exc:
        return blocked('Recipient input unreadable: '+str(exc),
                       evidence('recipient-checks', [{'name': 'recipient_input', 'passed': False, 'reason': str(exc)}]))
    if not checks or not all(c['passed'] for c in checks):
        return blocked('Recipient evidence changed or invalid', evidence('recipient-checks', checks))
    try:
        verdict = get_agent('Gemini').execute('verify', execution_plan('verify'),
            {'target': request['request_id'], 'checks': checks, 'evidence': received['artifacts'],
             'event_identity': {'chain_id': task['task_id'], 'event_id': received['trace_id'],
                                'sequence': 2, 'owner_scope': 'artifact-review'}})
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return blocked('Reviewer execution failed: '+str(exc), evidence('reviewer-error', {'reason': str(exc)}))
    if not isinstance(verdict, dict):
        return blocked('Reviewer returned invalid format', evidence('reviewer-error', {'reason': 'object required'}), 'Gemini')
    verdict_ref = evidence('Gemini-result', verdict)
    final_checks = verify_artifacts(root, received, request, RULES, baseline)
    try:
        final_checks.append({'name': 'producer_envelope_unchanged', 'passed': sha(read_inside(root, produced_ref)) == produced_hash})
    except (OSError, ValueError) as exc:
        final_checks.append({'name': 'producer_envelope_unchanged', 'passed': False, 'reason': str(exc)})
    if verdict.get('status') != 'COMPLETED' or verdict.get('decision') != 'VERIFIED' or not all(c['passed'] for c in final_checks):
        return blocked('Technical review did not pass', evidence('final-checks', final_checks))
    for unknown in produced.get('unknowns', []):
        pair.note('Cast', str(unknown), evidence=produced_ref)
    pair.transfer('Cast', 'Gemini', 'Orchestration', [produced_ref, verdict_ref], final_checks)
    pair.transfer('Orchestration', 'Gemini', 'BBX19', [produced_ref, verdict_ref], final_checks)
    audit = pair.audit()
    if not audit['trace_verified']:
        return blocked('Backward trace failed', evidence('trace-failures', audit))
    advance('VERIFYING', 'Gemini', 'Independent artifact checks passed', verdict_ref)
    advance('WAITING_HUMAN', 'Orchestration', 'Expected final delivery; no more automatic work')
    delivery = {'schema': 'w3.artifact_delivery/1', 'request_id': request['request_id'],
                'task_id': task['task_id'], 'status': task['status'],
                'technical_result': 'VERIFIED' if verdict['decision'] == 'VERIFIED' else 'UNRESOLVED',
                'expected_stop_reached': task['status'] == request['expected_stop'],
                'recipient': 'BBX19', 'human_approval': None, 'automatic_continuation': False,
                'paired_review': audit, 'artifacts': received['artifacts'], 'rules': str(rules_path.relative_to(root)),
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
