"""Real local support adapters and a CLI for saved Orchestration circuits."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from uuid import uuid4

from core.runtime.agents.origin_operations import OriginFiles, ORIGINS, atomic_write
from core.runtime.agents import get_agent
from tools.check_portable_paths import path_problems, case_collisions
from tools.validate_metadata import validate_file
from workflows.support_catalog import Adapter, SupportCatalog, FlowCatalog, tool_inventory


def inside(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError('support path escapes repository')
    return path


def default_flows():
    flows = FlowCatalog()
    flows.register('log_analysis', [
        {'id': 'analyze', 'task': 'log_analysis', 'module': 'LRC2'},
        {'id': 'validate', 'after': ['analyze'], 'task': 'verify', 'module': 'Gemini'},
    ])
    flows.register('system_inspection', [
        {'id': 'inspect', 'task': 'design', 'module': 'ChatGPT'},
        {'id': 'verify', 'after': ['inspect'], 'task': 'verify', 'module': 'Gemini'},
    ])
    return flows


def default_catalog(root, *, authority_context=None):
    root = Path(root).resolve()
    authority = deepcopy(authority_context or {})
    # Authority supplied by host only. A request cannot widen an Origin's scope.
    authority['repo_root'] = str(root)
    catalog = SupportCatalog()
    def diagnostic(capability, context):
        paths = context['request'].get('paths')
        if not isinstance(paths, list) or not paths or any(not isinstance(p, str) or not p for p in paths):
            raise ValueError('explicit nonempty paths required')
        records, findings = [], []
        for value in paths:
            path = inside(root, value)
            if not path.is_file():
                raise ValueError('support input must be an existing file')
            data = path.read_bytes()
            errors = path_problems(value) if capability == 'portable_paths' else validate_file(str(path))
            records.append({'path': value, 'sha256': hashlib.sha256(data).hexdigest()})
            findings.extend({'path': value, 'reason': error} for error in errors)
        if capability == 'portable_paths':
            findings.extend({'reason': reason} for reason in case_collisions(paths))
        report = {'capability': capability, 'inputs': records, 'findings': findings,
                  'task_id': context['task_id'], 'resolved': not findings,
                  'coverage': 'path portability' if capability == 'portable_paths' else 'approval metadata'}
        path = inside(root, f'repo_events/orchestration_support/{uuid4().hex}.json')
        atomic_write(path, (json.dumps(report, ensure_ascii=False, indent=2)+'\n').encode())
        return {'resolved': not findings, 'mutated': True, 'report': str(path.relative_to(root)),
                'report_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'diagnostics': report}
    def diagnostic_verifier(context, result):
        path = inside(root, result['report'])
        data = path.read_bytes()
        report = json.loads(data)
        valid = (hashlib.sha256(data).hexdigest() == result['report_sha256']
                 and report == result['diagnostics'] and report['task_id'] == context['task_id']
                 and report['capability'] == context['selection']['capability']
                 and [item['path'] for item in report['inputs']] == context['request']['paths'])
        for item in report['inputs']:
            valid &= hashlib.sha256(inside(root, item['path']).read_bytes()).hexdigest() == item['sha256']
        # Recompute substantive checks, not just adapter-reported PASS.
        paths = context['request']['paths']
        if report['capability'] == 'portable_paths':
            errors = [error for p in paths for error in path_problems(p)] + case_collisions(paths)
        else:
            errors = [error for p in paths for error in validate_file(str(inside(root, p)))]
        return {'passed': bool(valid and not errors and not report['findings'])}
    for capability, name in [('portable_paths', 'tools/check_portable_paths.py'),
                             ('approval_metadata', 'tools/validate_metadata.py')]:
        catalog.register(Adapter(name, 'TOOL', frozenset({capability}),
                                 lambda c, cap=capability: diagnostic(cap, c), diagnostic_verifier,
                                 available=lambda n=name: inside(root, n).is_file()))
    for module in ORIGINS:
        def available(m=module):
            OriginFiles(m, authority)
            return True
        def accepts(request, m=module):
            paths = request.get('paths')
            if not isinstance(paths, list) or not paths:
                return False
            fs = OriginFiles(m, authority)
            for value in paths:
                fs.require(fs.path(value), 'read')
            return True
        def review(context, m=module):
            paths = context['request'].get('paths')
            if not isinstance(paths, list) or not paths:
                raise ValueError('explicit review paths required')
            result = get_agent(m).execute('Orchestration paired file review', {},
                      {'request_type': 'origin_review', 'review_paths': paths,
                       'authority_context': deepcopy(authority)})
            return {'resolved': result.get('status') == 'COMPLETED',
                    'mutated': True, 'agent_result': result}
        def verify(context, result, m=module):
            agent = result['agent_result']
            # Re-read using the same host scope and recompute syntax/bytes.
            actual = OriginFiles(m, authority).review(context['request']['paths'])
            receipt = json.loads(inside(root, agent['log_path']).read_text())
            return {'passed': agent.get('module') == m and agent.get('status') == 'COMPLETED'
                    and all(receipt.get(k) == v for k, v in agent.items())
                    and not actual['findings'] and bool(actual['evidence'])
                    and actual['evidence'] == agent.get('evidence')}
        catalog.register(Adapter(f'origin-review:{module}', 'SPECIALIST', frozenset({'file_review'}),
                                 review, verify, module=module, available=available, accepts=accepts))
    return catalog


def main():
    import argparse
    from tools import request_cycle as rc
    from tools.runtime_circuit_intake import make_runtime, task_id
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--request', help='root runtime_circuit request path')
    parser.add_argument('--capability')
    parser.add_argument('--kind', choices=['TOOL', 'SPECIALIST'])
    parser.add_argument('--preferred')
    parser.add_argument('--paths', nargs='+')
    parser.add_argument('--continue', dest='resume', action='store_true', help='explicitly retry original stage after verified support')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    catalog = default_catalog(root)
    if args.list or args.inventory:
        data = tool_inventory(root, catalog) if args.inventory else [
            {'name': a.name, 'kind': a.kind, 'module': a.module, 'capabilities': sorted(a.capabilities)}
            for a in catalog.adapters.values()]
        print(json.dumps(data, ensure_ascii=False, indent=2)); return
    if not args.request or not args.capability or not args.paths:
        parser.error('--request, --capability and --paths required')
    request = rc.parse_request(inside(root, args.request))
    if request.get('request_type') != 'runtime_circuit':
        parser.error('saved runtime_circuit request required')
    rid = str(request['request_id'])
    with rc._file_lock(rc.REQUEST_LOCK_DIR / f'{rc.safe_id(rid)}.circuit.lock'):
        runtime = make_runtime(root)
        task = json.loads((runtime.directory/'tasks'/f'{task_id(rid)}.json').read_text())
        if task['payload']['request_sha256'] != hashlib.sha256(request['_request_text'].encode()).hexdigest():
            raise ValueError('request changed since saved execution')
        catalog.support(runtime, task, args.capability, request={'paths': args.paths},
                        kind=args.kind, preferred=args.preferred,
                        owner=task['destination']['module'], request_type=request['request_type'])
        if args.resume and task['status'] == 'RETURNED':
            runtime.continue_work(task)
        print(json.dumps({'status': task['status'], 'task_id': task['task_id'], 'support': task['support']}, ensure_ascii=False))
    # Publish current audit without triggering an implicit retry when RETURNED.
    if task['status'] != 'RETURNED':
        rc.process(inside(root, args.request))


if __name__ == '__main__':
    main()
