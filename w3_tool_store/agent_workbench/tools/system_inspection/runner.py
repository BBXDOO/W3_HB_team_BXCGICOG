"""Bounded host inspection: independent real test suites, durable evidence.

This is an audit circuit, not a newly invented production pipeline between
the seven systems. Request JSON cannot supply commands, imports or grants.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from uuid import uuid4
import xml.etree.ElementTree as ET

from core.runtime.agents.origin_operations import atomic_write

CATALOG = (
    ('MPCP', 'protocol/mpcp/runtime/README.md', ('tests/test_mpcp_agent_sandbox.py', 'tests/test_mpcp_paper_runtime.py', 'tests/test_mpcp_condien_equipment.py')),
    ('E-CS', 'ecs/event_chain_system.py', ('tests/test_ecs_native_inspection.py', 'tests/test_event_chain.py')),
    ('W3Lgu', 'core/runtime/w3lgu_mfc_logic/psp2_mfc_logic.py', ('tests/test_w3lgu_mfc_logic.py', 'tests/test_w3lgu_operational.py')),
    ('Cross-X', 'cross_x/core.py', ('tests/test_cross_x_config.py',)),
    ('CROLL', 'croll/contracts.py', ('croll/test_contracts.py', 'croll/test_cross_l_dispatcher.py')),
    ('Table-X', 'croll/table_x.py', ('croll/test_table_x.py',)),
    ('PX', 'protocol/w3lgu/px.py', ('tests/test_px_w3db_append_flow.py',)),
)
BASE = 'repo_events/system_inspections'
LIMITATIONS = [
    'Executes the listed repository regression/contract tests on isolated copies with test inputs.',
    'Does not prove one production request traverses all seven systems or authorize deployment.',
    'A failed, skipped or unavailable suite does not certify the health of that system.',
    'Inspection completion and system health are separate; unresolved findings remain open.',
]


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('inspection path escapes repository')
    return path


def write_json(path, value):
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode())


def file_hash(root, name):
    path = inside(root, name)
    return digest(path.read_bytes()) if path.is_file() else None


def junit_counts(path):
    tree = ET.parse(path).getroot()
    suites = [tree] if tree.tag == 'testsuite' else tree.findall('testsuite')
    if not suites:
        raise ValueError('no test suite evidence')
    return {key: sum(int(s.get(key, '0')) for s in suites)
            for key in ('tests', 'failures', 'errors', 'skipped')}


def classify(exit_code, counts):
    if counts is None or counts['tests'] <= 0:
        return 'BLOCKED'
    if counts['failures'] or counts['errors'] or exit_code != 0:
        return 'FAIL'
    if counts['skipped']:
        return 'PARTIAL'
    return 'PASS'


def copy_source(root, target):
    """Writable test copy; never copy other run evidence or dependency installs."""
    ignored = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv'}
    def ignore(folder, names):
        dropped = set(names) & ignored
        if Path(folder).resolve() == (root / 'repo_events').resolve():
            dropped.add('system_inspections')
        if Path(folder).resolve() == (root / 'w3_tool_store').resolve():
            dropped.add('xrea')  # upstream prototype is not used by these suites
        if Path(folder).resolve() == (root / 'w3_tool_store/agent_workbench').resolve():
            dropped.add('runs')
        return dropped
    # Dereferencing source symlinks could copy data outside the repository.
    shutil.copytree(root, target, ignore=ignore, symlinks=True)
    for link in target.rglob('*'):
        if link.is_symlink():
            link.unlink()
    # MPCP's existing sandbox uses git ls-files/rev-parse for its input inventory.
    # Give the copy its own local Git context, never the host's .git or hooks.
    # This revision identifies the copied protocol/src, not the source commit.
    if (target / 'protocol').is_dir() and (target / 'src').is_dir():
        subprocess.run(['git', 'init', '-q'], cwd=target, capture_output=True, check=True, timeout=20)
        git = ['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false']
        subprocess.run([*git, 'add', '--force', '--', 'protocol', 'src'], cwd=target,
                       capture_output=True, check=True, timeout=30)
        subprocess.run([*git, '-c', 'user.name=W3 inspection snapshot',
                        '-c', 'user.email=inspection@localhost', 'commit', '-q', '--allow-empty',
                        '-m', 'isolated protocol/src test snapshot'], cwd=target,
                       capture_output=True, check=True, timeout=30)


def run_suite(root, folder, system, entry, tests, *, timeout=180):
    """A failure belongs to this row; the caller can inspect the next system."""
    started = time.monotonic()
    row = {'system': system, 'entry_point': entry, 'tests': list(tests),
           'status': 'BLOCKED', 'started_at': now(), 'exit_code': None,
           'counts': None, 'reason': '', 'elapsed_seconds': 0,
           'input_hashes': {p: file_hash(root, p) for p in (entry, *tests)},
           'input_kind': 'repository test inputs on isolated source copy',
           'git_context': 'temporary local protocol/src snapshot; not the source commit',
           'recipient': 'pytest subprocess in isolated workspace'}
    log = folder / 'pytest.log'
    xml = folder / 'junit.xml'
    folder.mkdir(parents=True, exist_ok=False)
    missing = [p for p, value in row['input_hashes'].items() if value is None]
    try:
        if missing:
            raise ValueError('missing entry point or suite: ' + ', '.join(missing))
        if importlib.util.find_spec('pytest') is None:
            raise ValueError('pytest is not installed in the inspection host')
        with tempfile.TemporaryDirectory(prefix='w3-inspection-') as temporary:
            sandbox = Path(temporary) / 'repository'
            copy_source(root, sandbox)
            if any(file_hash(sandbox, p) != value for p, value in row['input_hashes'].items()):
                raise ValueError('copied inspection inputs differ from source')
            command = [sys.executable, '-m', 'pytest', *tests, '-q',
                       '-o', 'addopts=', '--junitxml=' + str(xml)]
            row['command'] = command
            env = dict(os.environ)
            # Python always imports the isolated source, never the host checkout.
            env['PYTHONPATH'] = str(sandbox)
            env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
            with log.open('wb') as stream:
                process = subprocess.Popen(command, cwd=sandbox, env=env,
                                           stdout=stream, stderr=subprocess.STDOUT,
                                           start_new_session=(os.name == 'posix'))
                try:
                    row['exit_code'] = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    if os.name == 'posix':
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    process.wait()
                    row['status'] = 'TIMEOUT'
                    row['reason'] = f'suite exceeded {timeout} seconds; isolated process stopped'
            if row['status'] != 'TIMEOUT':
                try:
                    row['counts'] = junit_counts(xml)
                except (OSError, ValueError, ET.ParseError) as exc:
                    row['reason'] = f'cannot verify collected test outcomes: {exc}'
                row['status'] = classify(row['exit_code'], row['counts'])
                row['reason'] = row['reason'] or ('listed checks passed' if row['status'] == 'PASS'
                                                 else 'see pytest.log and junit.xml for the first failing handoff/check')
    except Exception as exc:
        row['status'] = 'BLOCKED'
        row['reason'] = f'{type(exc).__name__}: {exc}'
    if not log.exists():
        log.write_text(row['reason'] + '\n', encoding='utf-8')
    row['source_unchanged'] = all(file_hash(root, p) == value for p, value in row['input_hashes'].items())
    if not row['source_unchanged']:
        row.update(status='BLOCKED', reason='source input changed during inspection; result not accepted')
    row['elapsed_seconds'] = round(time.monotonic() - started, 3)
    row['finished_at'] = now()
    row['evidence'] = [{'path': str(p.relative_to(root)), 'sha256': digest(p.read_bytes())}
                       for p in (log, xml) if p.is_file()]
    return row


def summary_status(rows):
    return 'PASS' if len(rows) == len(CATALOG) and all(r['status'] == 'PASS' for r in rows) else 'PARTIAL'


def execute(root, context):
    root = Path(root).resolve()
    payload = context.get('payload', {})
    if payload != {'inspection': 'w3_systems_v1'}:
        raise ValueError('fixed inspection profile required; request cannot select commands or paths')
    run_id = uuid4().hex
    folder = inside(root, f'{BASE}/runs/{run_id}')
    folder.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'w3.system_inspection/1', 'run_id': run_id,
              'task_id': context['request'].get('task_id'), 'source_id': context['request'].get('source_id'),
              'started_at': now(), 'finished_at': None, 'inspection_state': 'IN_PROGRESS',
              'coverage': 'listed regression and native contract checks; isolated test execution',
              'limitations': LIMITATIONS, 'systems': [], 'overall': 'PARTIAL', 'blockers': []}
    path = folder / 'report.json'
    reference = str(path.relative_to(root))
    def checkpoint():
        write_json(path, report)
        write_json(inside(root, f'{BASE}/latest.json'), {
            'report': reference, 'overall': report['overall'],
            'inspection_state': report['inspection_state'], 'updated_at': now(),
            'finished_at': report['finished_at'], 'blockers': report['blockers']})
    checkpoint()
    for system, entry, tests in CATALOG:
        item = run_suite(root, folder / system, system, entry, tests)
        report['systems'].append(item)
        if item['status'] != 'PASS':
            blocker = folder / 'blockers' / f'{system}.md'
            blocker.parent.mkdir(exist_ok=True)
            blocker.write_text(f"# {system} — {item['status']}\n\n{item['reason']}\n\n"
                               + '\n'.join(f"- {e['path']}" for e in item['evidence'])
                               + '\n\nติดตามแก้เฉพาะเรื่องนี้; การตรวจระบบถัดไปไม่ใช่หลักฐานว่าระบบนี้หายแล้ว\n', encoding='utf-8')
            report['blockers'].append(str(blocker.relative_to(root)))
        # Persist each row before inspecting the next system, including failures.
        checkpoint()
    report.update(inspection_state='FINISHED', finished_at=now(), overall=summary_status(report['systems']))
    checkpoint()
    lines = ['# ผลตรวจระบบ W3', '', f"- ผลรวม: **{report['overall']}**", '- ขอบเขต: รันชุดทดสอบที่ระบุในสำเนาแยก',
             '- ไม่ใช่การรับรอง production chain ทั้งเจ็ดระบบ', '', '| ระบบ | ผล | ทดสอบ | เหตุผล |', '|---|---|---:|---|']
    for row in report['systems']:
        lines.append(f"| {row['system']} | {row['status']} | {(row['counts'] or {}).get('tests', 0)} | {row['reason'].replace('|', '/').replace(chr(10), ' ')} |")
    lines += ['', '## เรื่องที่รอติดตาม', *[f'- [{p.split(chr(47))[-1]}]({p.removeprefix(str(folder.relative_to(root)) + chr(47))})' for p in report['blockers']],
              '', 'ดู report.json และ log รายระบบประกอบ ข้อมูลทดสอบไม่ใช่ข้อมูล production']
    (folder / 'REPORT_TH.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return {'contract_version': '1.0', 'module': 'ChatGPT', 'task': 'design', 'status': 'COMPLETED',
            'capability': 'system_inspection', 'review': False, 'traceable': True, 'mutated': True,
            'summary': f"Inspected {len(report['systems'])} systems; listed_checks={report['overall']}; {len(report['blockers'])} separate follow-ups. Not a production chain certification.",
            'artifacts': [{'path': reference, 'sha256': digest(path.read_bytes()), 'kind': 'w3.system_inspection.json'}]}


def report_checks(root, agent):
    """Verifier reads persisted logs/XML and recomputes each row's outcome."""
    root = Path(root).resolve()
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
    try:
        artifacts = agent.get('artifacts', [])
        if len(artifacts) != 1 or artifacts[0].get('kind') != 'w3.system_inspection.json':
            raise ValueError('one inspection report required')
        info = artifacts[0]
        path = inside(root, info['path'])
        if not path.is_relative_to(inside(root, BASE + '/runs')):
            raise ValueError('report outside inspection evidence area')
        data = path.read_bytes()
        report = json.loads(data)
        check('report_hash', digest(data) == info['sha256'])
        check('finished_with_declared_scope', report['inspection_state'] == 'FINISHED' and report['limitations'] == LIMITATIONS)
        rows = report['systems']
        check('all_systems_accounted_for', [r['system'] for r in rows] == [s[0] for s in CATALOG])
        check('overall_matches_outcomes', report['overall'] == summary_status(rows))
        for row, (system, entry, tests) in zip(rows, CATALOG):
            check(system + ':catalog', row['entry_point'] == entry and row['tests'] == list(tests))
            check(system + ':inputs_unchanged', row['source_unchanged'] and
                  row['input_hashes'] == {p: file_hash(root, p) for p in (entry, *tests)})
            evidence = row['evidence']
            check(system + ':evidence', bool(evidence) and all(
                inside(root, e['path']).is_relative_to(path.parent) and
                digest(inside(root, e['path']).read_bytes()) == e['sha256'] for e in evidence))
            if row['exit_code'] is not None:
                counts = junit_counts(path.parent / system / 'junit.xml') if row['counts'] is not None else None
                check(system + ':outcome', counts == row['counts'] and classify(row['exit_code'], counts) == row['status'])
            else:
                check(system + ':blocked_reason', row['status'] in {'BLOCKED', 'TIMEOUT'} and bool(row['reason']))
            if row['status'] != 'PASS':
                reference = str((path.parent / 'blockers' / (system + '.md')).relative_to(root))
                check(system + ':separate_followup', reference in report['blockers'] and inside(root, reference).is_file())
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        checks.append({'name': 'read_inspection_evidence', 'passed': False, 'reason': str(exc)})
    return checks
