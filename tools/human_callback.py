"""Unified human reply CLI for existing W3 runtime requests.

Host authentication is explicit: local CLI is a trusted operator boundary;
GitHub Actions maps only the repository owner to BBX19.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from tools import request_cycle as rc
from tools.runtime_circuit_intake import make_runtime, task_id
from workflows import human_callback as callback_flow


def authority(principal, evidence, *, actor=None, delegation_evidence=None):
    if principal != 'BBX19':
        raise ValueError('host principal must be BBX19')
    if not evidence or (actor and actor != 'BBX19' and not delegation_evidence):
        raise ValueError('decision provenance and explicit delegation evidence required')
    return {'authority': 'BBX19', 'authority_class': 'DELEGATED_CREATOR' if actor and actor != 'BBX19' else 'CREATOR_ORIGIN',
            'verified': True, 'verified_by': actor or principal, 'delegation_evidence': delegation_evidence}


def respond(root, path, callback=None, *, authority_context=None, host_evidence=None,
            prepare_only=False, runtime=None, checkpoint=None):
    """Serialize response application and publication under the existing lock."""
    root = Path(root).resolve()
    path = callback_flow.inside(root, str(path))
    request = rc.parse_request(path)
    rid = str(request['request_id'])
    with rc._file_lock(rc.REQUEST_LOCK_DIR / f'{rc.safe_id(rid)}.circuit.lock'):
        runtime = runtime or make_runtime(root)
        snapshot = runtime.directory/'tasks'/f'{task_id(rid)}.json'
        if not snapshot.is_file():
            if request.get('request_type') == 'runtime_circuit':
                raise ValueError('run the assignment once before responding')
            from tools.human_callback_legacy import adopt
            task = adopt(root, request, runtime)
        else:
            task = json.loads(snapshot.read_text())
        if task['payload']['request_sha256'] != hashlib.sha256(request['_request_text'].encode()).hexdigest():
            raise ValueError('source request changed; preserve original or revise explicitly')
        if prepare_only:
            response_path = callback_flow.prepare(runtime, task, request)
            rc._process(path)
            return {'status': task['status'], 'callback_path': response_path}
        if callback is None:
            raise ValueError('callback required')
        # Older snapshots can be brought into the same intent cycle without
        # granting approval or changing their previously executed stages.
        callback_flow.ensure_intent(runtime, task, request)
        applied = callback_flow.apply(runtime, task, callback,
                              authority_context=authority_context, host_evidence=host_evidence, checkpoint=checkpoint)
        # After action persistence, root audit can be retried without replaying
        # the same callback. HOLD/REVIEW remain at their current gate.
        audit = rc._process(path)
        return {**applied, 'audit': audit}


def reconcile_response(root, path, callback_id, *, outcome, authority_context, host_evidence):
    root = Path(root).resolve()
    path = callback_flow.inside(root, str(path))
    request = rc.parse_request(path)
    rid = str(request['request_id'])
    with rc._file_lock(rc.REQUEST_LOCK_DIR / f'{rc.safe_id(rid)}.circuit.lock'):
        runtime = make_runtime(root)
        task = json.loads((runtime.directory/'tasks'/f'{task_id(rid)}.json').read_text())
        if task['payload']['request_sha256'] != hashlib.sha256(request['_request_text'].encode()).hexdigest():
            raise ValueError('source request changed')
        result = callback_flow.reconcile_callback(runtime, task, callback_id, outcome=outcome,
                    authority_context=authority_context, host_evidence=host_evidence)
        return {**result, 'audit': rc._process(path)}


def review_request(root, path, *, human: str, evidence: str):
    """Compatibility entry point: --review uses the same BBEX/BBX19 pipeline."""
    if human != 'BBX19':
        raise ValueError('use --human BBX19; delegated operators use tools.human_callback with explicit delegation evidence')
    root = Path(root).resolve()
    request = rc.parse_request(path)
    rid = str(request['request_id'])
    with rc._file_lock(rc.REQUEST_LOCK_DIR / f'{rc.safe_id(rid)}.circuit.lock'):
        runtime = make_runtime(root)
        task = json.loads((runtime.directory/'tasks'/f'{task_id(rid)}.json').read_text())
        if task['payload']['request_sha256'] != hashlib.sha256(request['_request_text'].encode()).hexdigest():
            raise ValueError('source request changed')
        response_path = callback_flow.prepare(runtime, task, request)
        if response_path is None:
            raise ValueError('task is not waiting for response')
        form = json.loads(callback_flow.inside(root, response_path).read_text())
        callback = {key: form[key] for key in ('schema', 'request_id', 'binding')}
        callback.update(kind='DECISION', decision='APPROVE', reason='Explicit --review of the current request result',
                        annotations=['Accept only this request result; preserve remaining system capability goals.'], evidence=[evidence])
        applied = callback_flow.apply(runtime, task, callback, authority_context=authority('BBX19', evidence), host_evidence=evidence)
        return {**applied, 'audit': rc._process(path)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--run', action='store_true', help='run an assignment and prepare a response if needed')
    action.add_argument('--prepare', action='store_true')
    action.add_argument('--apply', metavar='CALLBACK_JSON')
    action.add_argument('--reconcile', metavar='CALLBACK_ID')
    parser.add_argument('--outcome', choices=['APPLIED', 'NOT_APPLIED'])
    parser.add_argument('--human', help='principal authenticated by trusted calling environment')
    parser.add_argument('--evidence', help='actual human decision provenance, e.g. comment or workflow run URL')
    parser.add_argument('--actor', help='delegate identity if different from BBX19')
    parser.add_argument('--delegation-evidence')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    path = callback_flow.inside(root, args.request)
    if args.run:
        result = rc.process(path)
    elif args.prepare:
        result = respond(root, path, prepare_only=True)
    else:
        if not args.human or not args.evidence:
            parser.error('--apply requires --human and --evidence supplied by the trusted host')
        if args.reconcile:
            result = reconcile_response(root, path, args.reconcile, outcome=args.outcome,
                authority_context=authority(args.human, args.evidence, actor=args.actor, delegation_evidence=args.delegation_evidence),
                host_evidence=args.evidence)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        callback = json.loads(callback_flow.inside(root, args.apply).read_text())
        result = respond(root, path, callback,
            authority_context=authority(args.human, args.evidence, actor=args.actor,
                                        delegation_evidence=args.delegation_evidence), host_evidence=args.evidence)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
