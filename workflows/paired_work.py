"""Host-owned paired handoffs. Notes are carried, never silently discharged.

This is a receipt protocol, not a fixed route or authority to repair source files.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from uuid import uuid4

from core.runtime.agents.origin_operations import atomic_write


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def fingerprint(data):
    return hashlib.sha256(data).hexdigest()


def inside(root, name):
    raw = Path(name)
    path = (root/raw).resolve()
    if raw.is_absolute() or '..' in raw.parts or '.git' in raw.parts or not path.is_relative_to(root):
        raise ValueError('paired evidence must remain inside repository')
    return path


class PairedWork:
    def __init__(self, root, folder, start):
        self.root = Path(root).resolve()
        self.folder = inside(self.root, folder)
        self.start = deepcopy(start)
        self.events, self.notes, self.explanations = [], [], []

    def note(self, owner, meaning, *, kind='doubt', evidence=None):
        if kind not in {'doubt', 'error'}:
            raise ValueError('note kind must be doubt or error')
        note = {'id': uuid4().hex, 'owner': owner, 'kind': kind,
                'meaning': meaning, 'evidence': deepcopy(evidence), 'status': 'OPEN'}
        self.notes.append(note)
        return note['id']

    def carry(self, notes, explanations=()):
        for note in notes:
            if (not isinstance(note, dict) or not all(note.get(k) for k in ('id', 'owner', 'meaning'))
                    or note.get('kind') not in {'doubt', 'error'}):
                raise ValueError('malformed carried note')
            existing = next((n for n in self.notes if n['id'] == note['id']), None)
            if existing is not None and existing != note:
                raise ValueError('carried note rewritten')
            if existing is None:
                self.notes.append(deepcopy(note))
        for explanation in explanations:
            self.explain(explanation['owner'], explanation['note_id'],
                         what=explanation['what'], how=explanation['how'], why=explanation['why'])

    def explain(self, owner, note_id, *, what, how, why):
        if not any(n['id'] == note_id and n['owner'] == owner for n in self.notes):
            raise ValueError('only responsible participant may explain this note')
        if not all(isinstance(v, str) and v.strip() for v in (what, how, why)):
            raise ValueError('what, how and why are required')
        self.explanations.append({'note_id': note_id, 'owner': owner, 'what': what,
                                  'how': how, 'why': why, 'verified': False})

    def transfer(self, sender, reviewer, recipient, evidence, checks):
        if not sender or not reviewer or sender == reviewer:
            raise ValueError('sender and reviewer must be different participants')
        if not checks or any(not isinstance(c.get('passed'), bool) for c in checks):
            raise ValueError('explicit pre-send checks required')
        refs = []
        for name in evidence:
            data = inside(self.root, name).read_bytes()
            refs.append({'path': name, 'sha256': fingerprint(data)})
        event = {'schema': 'w3.paired_handoff/1', 'sequence': len(self.events),
                 'sender': sender, 'reviewer': reviewer, 'recipient': recipient,
                 'start': self.start, 'parent': deepcopy(self.events[-1]) if self.events else None,
                 'evidence': refs, 'checks': deepcopy(checks), 'notes': deepcopy(self.notes),
                 'explanations': deepcopy(self.explanations),
                 'accepted': all(c['passed'] for c in checks)}
        path = self.folder/(str(len(self.events))+'-'+uuid4().hex+'.json')
        atomic_write(path, encoded(event))
        ref = {'path': str(path.relative_to(self.root)), 'sha256': fingerprint(path.read_bytes())}
        # Recipient boundary reads the actual persisted envelope and evidence again.
        received = json.loads(inside(self.root, ref['path']).read_bytes())
        if received != event or fingerprint(inside(self.root, ref['path']).read_bytes()) != ref['sha256']:
            raise ValueError('recipient received a different paired envelope')
        for item in received['evidence']:
            if fingerprint(inside(self.root, item['path']).read_bytes()) != item['sha256']:
                raise ValueError('recipient evidence differs from sender evidence')
        self.events.append(ref)
        return ref

    def audit(self):
        failures, previous, known_notes = [], None, {}
        for index, ref in enumerate(self.events):
            try:
                data = inside(self.root, ref['path']).read_bytes()
                event = json.loads(data)
                if (fingerprint(data) != ref['sha256'] or event['parent'] != previous
                        or event['sequence'] != index or event['start'] != self.start
                        or event['sender'] == event['reviewer']):
                    raise ValueError('broken paired receipt or ancestry')
                for item in event['evidence']:
                    if fingerprint(inside(self.root, item['path']).read_bytes()) != item['sha256']:
                        raise ValueError('handoff evidence changed: '+item['path'])
                current = {n['id']: n for n in event['notes']}
                if any(current.get(k) != v for k, v in known_notes.items()):
                    raise ValueError('earlier note omitted or rewritten')
                known_notes = current
                previous = ref
            except (OSError, ValueError, KeyError, TypeError) as exc:
                failures.append({'receipt': ref, 'reason': str(exc)})
        if known_notes != {n['id']: n for n in self.notes}:
            failures.append({'reason': 'final notes differ from last handoff'})
        for item in self.start.get('evidence', []):
            try:
                if fingerprint(inside(self.root, item['path']).read_bytes()) != item['sha256']:
                    raise ValueError('starting evidence changed')
            except (OSError, ValueError, KeyError) as exc:
                failures.append({'start': item, 'reason': str(exc)})
        return {'schema': 'w3.paired_audit/1', 'start': self.start,
                'receipts': deepcopy(self.events), 'notes': deepcopy(self.notes),
                'explanations': deepcopy(self.explanations), 'failures': failures,
                'note_review': [{'id': n['id'], 'owner': n['owner'],
                    'disposition': 'ERROR_RETAINED' if n['kind'] == 'error' else 'CARRIED',
                    'explanation_attached': any(e['note_id'] == n['id'] for e in self.explanations)} for n in self.notes],
                'explanation_requests': [{'note_id': n['id'], 'owner': n['owner'], 'fields': ['what', 'how', 'why']}
                    for n in self.notes if not any(e['note_id'] == n['id'] for e in self.explanations)],
                'trace_verified': bool(self.events) and bool(self.start.get('evidence')) and not failures,
                'all_handoffs_accepted': bool(self.events) and not failures and all(
                    json.loads(inside(self.root, ref['path']).read_bytes())['accepted'] for ref in self.events),
                'conflicts': [n for n in self.notes if n['kind'] == 'error'],
                'explanation_policy': 'responsible owner may append what/how/why; claims do not clear evidence failures'}


def record_fault(root, module, report_ref, errors):
    """Host writes only the accountable unit's own notes; never overwrites history."""
    from core.runtime.agents.origin_operations import ORIGINS, OriginFiles
    root = Path(root).resolve()
    if module in ORIGINS:
        fs = OriginFiles(module, {'repo_root': str(root)})
        path = fs.path(module+'/notes/'+uuid4().hex+'.json')
        fs.require(path, 'create')
        if not path.is_relative_to(root/module/'notes'):
            raise ValueError('fault notes directory redirected')
    elif module == 'Cast':
        path = inside(root, 'modules/Cast/notes/'+uuid4().hex+'.json')
        if not path.is_relative_to(root/'modules/Cast/notes'):
            raise ValueError('fault notes directory redirected')
    else:
        raise ValueError('no known owned notes area for participant')
    atomic_write(path, encoded({'schema': 'w3.paired_fault/1', 'owner': module,
                               'full_report': report_ref, 'errors': errors,
                               'purpose': 'retain for self-improvement; no automatic source repair'}))
    return str(path.relative_to(root))


def replacement(root, owner, reviewer, paths):
    """Orchestration selects an available review adapter, excluding the old pair.

    Selection does not rerun failed work or certify the proposed new participant.
    """
    from tools.orchestration_support import default_catalog
    from core.runtime.agents.origin_operations import ORIGINS
    authority = {'repo_root': str(root), 'origin_scopes': {
        m: [{'path': p, 'operations': ['read']} for p in paths] for m in ORIGINS}}
    candidate, rejected = default_catalog(root, authority_context=authority).select(
        'file_review', kind='SPECIALIST', owner=owner,
        exclude=['origin-review:'+reviewer], request={'paths': paths})
    return {'selected_by': 'Orchestration', 'sender': owner,
            'reviewer': candidate.module if candidate else None,
            'status': 'SELECTED_AWAITING_RETRY' if candidate else 'BLOCKED_NO_CAPABLE_PAIR',
            'rejected': rejected, 'automatic_retry': False}
