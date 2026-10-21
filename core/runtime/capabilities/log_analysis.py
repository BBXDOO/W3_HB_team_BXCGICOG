"""LRC2 log analysis over supplied records: explicit rules, evidence and sample sizes."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import uuid

from core.runtime.agents.origin_operations import atomic_write

REPO_ROOT = Path(__file__).resolve().parents[3]
CATEGORIES = {
    'success': {'COMPLETED', 'SUCCESS', 'SUCCEEDED', 'PASS'},
    'failure': {'FAILED', 'ERROR', 'FAIL'},
    'blocked': {'BLOCKED', 'STOP'},
    'review': {'REVIEW', 'REVIEW_REQUIRED', 'WAITING_HUMAN'},
    'pending': {'ACTIVE', 'WAIT', 'STANDBY', 'QUEUED', 'RECEIVED', 'IN_PROGRESS'},
    'cancelled': {'CANCELLED', 'REJECTED'},
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode('utf-8')


def load_records(payload, root):
    if not isinstance(payload, dict):
        raise ValueError('log analysis payload must be an object')
    if 'records' in payload and 'source_file' in payload:
        raise ValueError('choose records or source_file, not both')
    if 'records' in payload:
        records = payload['records']
        origin = 'request.records'
    elif isinstance(payload.get('source_file'), str):
        path = (root / payload['source_file']).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError('source_file must be an existing file within the repository')
        text = path.read_text(encoding='utf-8')
        if path.suffix == '.jsonl':
            records = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            data = json.loads(text)
            records = data.get('records') if isinstance(data, dict) else data
        origin = str(path.relative_to(root.resolve()))
    else:
        raise ValueError('provide log records or a repository source_file')
    if not isinstance(records, list) or any(not isinstance(row, dict) for row in records):
        raise ValueError('log records must be a list of objects')
    canonical(records)
    return records, origin


def normalize(row, index):
    content = row.get('content', {})
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except ValueError:
            content = {}
    content = content if isinstance(content, dict) else {}
    status = row.get('status') or content.get('status')
    tags = row.get('tags', [])
    if not status and isinstance(tags, list):
        status = 'FAILED' if 'error' in tags else 'COMPLETED' if 'success' in tags else None
    status = str(status or 'UNKNOWN').upper()
    category = next((name for name, values in CATEGORIES.items() if status in values), 'unknown')
    signature = row.get('error_code') or row.get('error') or content.get('error_code') or content.get('error')
    # Group only explicit error evidence, not guessed semantic similarities.
    signature = re.sub(r'\s+', ' ', str(signature)).strip()[:200] if signature else None
    stamp = row.get('timestamp') or row.get('time') or content.get('time')
    try:
        parsed = datetime.fromisoformat(str(stamp).replace('Z', '+00:00'))
        epoch = parsed.timestamp() if parsed.tzinfo is not None else None
    except (ValueError, TypeError, OverflowError):
        epoch = None
    return {'ref': str(row.get('id') or row.get('event_id') or f'input:{index}'),
            'input_index': index, 'module': str(row.get('module') or row.get('source') or content.get('module') or 'unknown'),
            'task': str(row.get('task') or row.get('topic') or content.get('task') or 'unknown'),
            'status': status, 'category': category, 'error_signature': signature,
            'timestamp': stamp, 'epoch': epoch}


def analyze(records, *, min_samples=20, window_size=20):
    if type(min_samples) is not int or min_samples < 1 or type(window_size) is not int or window_size < 1:
        raise ValueError('min_samples and window_size must be positive integers')
    rows = [normalize(row, i) for i, row in enumerate(records)]
    groups = defaultdict(list)
    for row in rows:
        groups[(row['module'], row['task'])].append(row)
    patterns = []
    summaries = []
    for (module, task), members in sorted(groups.items()):
        chronological = all(row['epoch'] is not None for row in members)
        ordered = sorted(members, key=lambda row: (row['epoch'], row['input_index'])) if chronological else members
        window = ordered[-window_size:]
        categories = Counter(row['category'] for row in members)
        stack = peak = 0
        for row in window:
            stack = stack + 1 if row['category'] in {'failure', 'blocked'} else 0
            peak = max(peak, stack)
        risk_score = sum({'failure': 2, 'blocked': 1, 'review': 0.5}.get(row['category'], 0) for row in window)
        successes, failures = categories['success'], categories['failure']
        n = successes + failures
        rate = successes / n if n else None
        estimate = {'method': 'historical_frequency', 'sample_count': n, 'minimum_samples': min_samples,
                    'value': None, 'wilson_95_interval': None, 'state': 'insufficient_comparable_outcomes',
                    'assumption': 'future outcomes are comparable to this module/task history; not established by this calculation'}
        if n >= min_samples:
            z = 1.959963984540054
            denom = 1 + z*z/n
            center = (rate + z*z/(2*n))/denom
            half = z * math.sqrt(rate*(1-rate)/n + z*z/(4*n*n))/denom
            estimate.update(value=rate, wilson_95_interval=[max(0., center-half), min(1., center+half)],
                            state='conditional_estimate')
        summaries.append({'module': module, 'task': task, 'records': len(members),
                          'categories': dict(sorted(categories.items())), 'outcome_successes': successes,
                          'outcome_failures': failures, 'observed_success_rate': rate,
                          'success_estimate': estimate,
                          'risk_window': {'records': len(window), 'order': 'timestamp' if chronological else 'input_order',
                                          'advisory_score': risk_score, 'current_adverse_streak': stack,
                                          'maximum_adverse_streak': peak,
                                          'record_refs': [row['ref'] for row in window]}})
        errors = defaultdict(list)
        for row in members:
            if row['category'] in {'failure', 'blocked'} and row['error_signature']:
                errors[row['error_signature']].append(row['ref'])
        for signature, refs in sorted(errors.items()):
            if len(refs) > 1:
                patterns.append({'module': module, 'task': task, 'signature': signature,
                                 'count': len(refs), 'record_refs': refs})
    return {'algorithm': 'lrc2-explicit-log-analysis-v1', 'classification': 'provisional_rule_based',
            'records_total': len(rows), 'categories': dict(sorted(Counter(row['category'] for row in rows).items())),
            'groups': summaries, 'repeated_error_patterns': patterns,
            'unknown_record_refs': [row['ref'] for row in rows if row['category'] == 'unknown'],
            'limitations': ['Categories describe recorded statuses, not unobserved task quality.',
                            'Risk weights are advisory: failure=2, blocked=1, review=0.5.',
                            'Historical frequency is not a validated predictor of future success.']}


def execute(task, plan, context, *, repo_root=None):
    root = Path(repo_root or REPO_ROOT).resolve()
    request = context.get('request', {})
    payload = context.get('payload', {})
    records, origin = load_records(payload, root)
    if not records:
        raise ValueError('no log records supplied; analysis has no observations')
    report = analyze(records, min_samples=payload.get('min_samples', 20), window_size=payload.get('window_size', 20))
    trace = str(context.get('trace_id') or uuid.uuid4().hex)
    digest = hashlib.sha256(canonical(records)).hexdigest()
    report.update(source=origin, original_source=payload.get('original_source', origin), source_sha256=digest,
                  settings={'min_samples': payload.get('min_samples', 20), 'window_size': payload.get('window_size', 20)},
                  task_id=request.get('task_id'), trace_id=trace)
    directory = root / 'modules/LRC2/reports/log_analysis'
    directory = directory.resolve()
    if not directory.is_relative_to(root):
        raise ValueError('LRC2 report directory escapes repository')
    name = re.sub(r'[^A-Za-z0-9_-]', '', trace)[:80] or uuid.uuid4().hex
    path = directory / f'{name}.json'
    if path.exists():
        raise ValueError('analysis trace already has a report; reconcile instead of overwriting')
    data = canonical(report) + b'\n'
    atomic_write(path, data)
    return {'contract_version': '1.0', 'status': 'COMPLETED', 'module': 'LRC2', 'task': task,
            'capability': 'log_analysis', 'trace_id': trace, 'action': 'analyze_recorded_log_patterns',
            'confidence': 0.0, 'input_type': 'log_records', 'decision': 'analysis_report_created',
            'reason': 'Computed classifications, exact repeated error signatures and conditional historical estimates from supplied records.',
            'next': [], 'standby': ['Gemini'], 'mutated': True, 'traceable': True, 'review': False,
            'summary': f"Analyzed {len(records)} records in {len(report['groups'])} module/task groups; created a source-linked report.",
            'details': {'identity': {'chain_id': request.get('task_id') or f'LRC2-{trace}',
                                     'event_id': trace, 'package_id': f'LRC2-ANALYSIS-{digest[:20]}'},
                        'records_total': len(records), 'source_sha256': digest,
                        'confidence_scope': 'predictive confidence is not measured'},
            'artifacts': [{'path': str(path.relative_to(root)), 'sha256': hashlib.sha256(data).hexdigest(),
                           'bytes': len(data), 'kind': 'w3.lrc2.log_analysis.json'}]}
