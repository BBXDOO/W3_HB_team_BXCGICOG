"""GitHub host adapter: repository-owner event -> unified human callback.

Identity comes from the event environment supplied by GitHub, not JSON fields.
Blank generated forms are never approvals and bot pushes are not admitted.
"""
import json
import os
from pathlib import Path
import subprocess

from tools import request_cycle as rc
from tools.human_callback import authority, respond
from workflows.human_callback import BASE, inside


def process_event(root, *, actor, owner, event_name, event, evidence,
                  mode=None, request=None, callback=None, checkpoint=None, event_sha=None):
    if not actor or actor != owner:
        raise ValueError('only the authenticated repository owner can submit a human callback')
    root = Path(root).resolve()
    if event_name == 'workflow_dispatch' and mode == 'prepare':
        return [respond(root, inside(root, request or ''), prepare_only=True)]
    if event_name == 'workflow_dispatch' and mode == 'apply':
        paths = [callback] if callback else []
    elif event_name == 'push':
        # Use the complete Git range; webhook commit arrays may be truncated.
        before, after = event.get('before', ''), event.get('after', '')
        if any(len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha) for sha in (before, after)) or set(before) == {'0'}:
            raise ValueError('existing branch commit range required')
        paths = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=AM', before, after,
                                         '--', BASE+'/responses/*.json'], cwd=root, text=True).splitlines()
    else:
        raise ValueError('unsupported callback event or mode')
    if not paths:
        raise ValueError('no response file selected')
    results = []
    for name in paths:
        path = inside(root, name)
        if not path.is_relative_to(inside(root, BASE+'/responses')) or path.suffix != '.json':
            raise ValueError('response must be inside callback/responses/')
        source_sha = event.get('after') if event_name == 'push' else event_sha
        if source_sha:
            if len(source_sha) != 40 or any(c not in '0123456789abcdef' for c in source_sha):
                raise ValueError('invalid event source commit')
            approved_bytes = subprocess.check_output(['git', 'show', f'{source_sha}:{name}'], cwd=root)
            if path.read_bytes() != approved_bytes:
                raise ValueError('response content changed after the authenticated event; submit the current response again')
        data = json.loads(path.read_text())
        if not data.get('decision') and data.get('kind') != 'NOTE':
            results.append({'status': 'SKIPPED', 'reason': 'blank response form', 'path': name})
            continue
        requests = []
        for candidate in (root/'requests').glob('*.md'):
            try:
                parsed = rc.parse_request(candidate)
            except ValueError:
                continue  # General Markdown documents are not callback requests.
            if parsed.get('request_id') == data.get('request_id'):
                requests.append(candidate)
        if len(requests) != 1:
            raise ValueError('response needs exactly one matching root request')
        results.append(respond(root, requests[0], data,
            authority_context=authority('BBX19', evidence), host_evidence=evidence, checkpoint=checkpoint))
    return results


def checkpoint_to_git(root):
    """Persist the callback intent remotely before any executor continuation."""
    for command in [
        ['git', 'config', 'user.name', 'w3-human-callback'],
        ['git', 'config', 'user.email', 'w3-human-callback@users.noreply.github.com'],
        ['git', 'add', '--', 'repo_events/runtime_circuit', BASE+'/responses'],
        ['git', 'commit', '-m', 'runtime: checkpoint pending human callback'],
        ['git', 'push', 'origin', 'HEAD:refactor/v0.2'],
    ]:
        subprocess.run(command, cwd=root, check=True)


def main():
    root = Path(__file__).resolve().parents[1]
    event = json.loads(Path(os.environ['CALLBACK_EVENT']).read_text())
    result = process_event(root, actor=os.environ['CALLBACK_ACTOR'], owner=os.environ['CALLBACK_OWNER'],
        event_name=os.environ['CALLBACK_EVENT_NAME'], event=event, evidence=os.environ['CALLBACK_RUN_URL'],
        mode=os.environ.get('CALLBACK_MODE'), request=os.environ.get('CALLBACK_REQUEST'),
        callback=os.environ.get('CALLBACK_FILE'), event_sha=os.environ.get('CALLBACK_EVENT_SHA'), checkpoint=lambda: checkpoint_to_git(root))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
