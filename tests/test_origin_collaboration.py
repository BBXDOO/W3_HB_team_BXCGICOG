import json
import unittest
from tests import test_origin_operations as origin_fixtures
from tools.origin_cycle import directed_work, periodic_work
from tools.origin_collaboration import validate_repair_selection
from core.runtime.agents.origin_operations import digest


class CollaborationTests(unittest.TestCase):
    setUp = origin_fixtures.OriginOperationsTests.setUp
    def test_periodic_exception_is_recorded_before_next_module_runs(self):
        from unittest.mock import patch
        from core.runtime.agents.origin_operations import ORIGINS
        from tools.origin_cycle import periodic_results
        visited = []
        def work(root, module, now=None):
            if visited:
                receipts = list((root / 'repo_events/origin_agents' / ORIGINS[0] / 'reports').glob('*_FAILURE.json'))
                self.assertEqual(len(receipts), 1)
            visited.append(module)
            if module == ORIGINS[0]:
                raise RuntimeError('host stopped after a possible partial write')
            return {'module': module, 'status': 'NOT_DUE'}
        with patch('tools.origin_cycle.periodic_work', side_effect=work):
            results = periodic_results(self.root, now=self.now)
        self.assertEqual(visited, list(ORIGINS))
        failure = json.loads((self.root / results[0]['failure_evidence']).read_text())
        self.assertEqual(failure['status'], 'FAILED')
        self.assertTrue(failure['partial_writes_possible'])
        self.assertFalse(failure['retried_in_this_run'])
        self.assertEqual([item['status'] for item in results[1:]], ['NOT_DUE'] * (len(ORIGINS) - 1))

    def test_periodic_stops_if_failure_cannot_be_recorded(self):
        from unittest.mock import patch
        from tools.origin_cycle import periodic_results
        with patch('tools.origin_cycle.periodic_work', side_effect=RuntimeError('host error')) as work:
            with patch('tools.origin_cycle.atomic_write', side_effect=OSError('storage unavailable')):
                with self.assertRaises(OSError):
                    periodic_results(self.root, now=self.now)
        self.assertEqual(work.call_count, 1)

    def test_structural_review_without_partner_persists_report_and_returns_support(self):
        from tools.origin_collaboration import collaborate
        from core.runtime.agents import get_agent
        result = get_agent('ChatGPT').execute('scoped review', {}, {
            'request_type': 'origin_review',
            'authority_context': {'repo_root': str(self.root)}})
        checked = collaborate(self.root, 'ChatGPT', result, structural=True)
        report = json.loads((self.root / checked['collaboration_report']).read_text())
        task = json.loads((self.root / checked['orchestration_evidence']).read_text())
        self.assertTrue(report['structural'])
        self.assertIn('IGET', report['participants'])
        self.assertEqual(checked['partner'], 'Orchestration')
        self.assertFalse(checked['support_pending'])
        self.assertEqual(task['status'], 'COMPLETED')
        self.assertEqual(json.loads((self.root / 'ChatGPT/state.json').read_text()), {'active': True})

    def test_all_due_origins_without_partner_persist_structural_round(self):
        from core.runtime.agents.origin_operations import ORIGINS
        from tools.origin_cycle import load_state
        reviewed = self.root / 'core/runtime/agents/reviewed.py'
        reviewed.parent.mkdir(parents=True)
        reviewed.write_text('pass\n')
        for module in ORIGINS:
            with self.subTest(module=module):
                path = self.root / 'core/identity/profiles' / (module + '.idp.json')
                profile = json.loads(path.read_text())
                profile.setdefault('integration', {})['paired_modules'] = []
                profile['file_capabilities']['review_paths'] = ['core/runtime/agents/reviewed.py']
                profile['file_capabilities']['scopes'].append({
                    'path': 'core/runtime/agents', 'operations': ['read']})
                path.write_text(json.dumps(profile))
                result = periodic_work(self.root, module, now=self.now, force=True)
                state = load_state(self.root, module)
                self.assertTrue(result['structural_review'])
                self.assertTrue((self.root / state['last_report']).is_file())
                self.assertEqual(state['last_review'], '2026-10-09T00:00:00Z')
                self.assertFalse(result['support_pending'])

    def test_missing_partner_selects_capable_replacement_and_records_receipt(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'PAIR', 'source': 'BBX19',
            'payload': {'partner': 'NotInstalled', 'operations': [
                {'action': 'create', 'path': 'ChatGPT/paired.txt', 'content': 'real'}]}})
        self.assertNotIn(result['partner'], ('Orchestration', 'ChatGPT', 'NotInstalled'))
        task = json.loads((self.root / result['orchestration_evidence']).read_text())
        receipt = json.loads((self.root / task['route'][0]['notification']).read_text())
        self.assertEqual(receipt['requested_partner'], 'NotInstalled')
        self.assertEqual(receipt['partner_selection']['selected'], result['partner'])
        self.assertEqual(receipt['partner_result']['capability'], 'origin_review')
        self.assertTrue(receipt['partner_result']['evidence'])

    def test_structural_round_has_iget_and_waits_for_selection(self):
        path = self.root / 'core/identity/profiles/ChatGPT.idp.json'
        profile = json.loads(path.read_text())
        profile['file_capabilities']['review_paths'] = ['architecture/missing.py']
        profile['file_capabilities']['scopes'].append({'path': 'architecture', 'operations': ['read']})
        path.write_text(json.dumps(profile))
        result = periodic_work(self.root, 'ChatGPT', force=True)
        report = json.loads((self.root / result['collaboration_report']).read_text())
        self.assertIn('IGET', report['participants'])
        self.assertIn('Orchestration', report['participants'])
        self.assertEqual(result['interval_days'], 7)
        self.assertFalse((self.root / 'architecture/missing.py').exists())
        self.assertEqual(report['repair_status'], 'WAITING_BBX19_SELECTION')
        selection = {'report_path': result['collaboration_report'],
                     'report_sha256': digest((self.root / result['collaboration_report']).read_bytes()),
                     'paths': ['architecture/missing.py']}
        repaired = directed_work(self.root, 'ChatGPT', {'request_id': 'SELECTED', 'source': 'BBX19',
            'payload': {'structural_repair': True, 'repair_selection': selection, 'operations': [
                {'action': 'create', 'path': 'architecture/missing.py', 'content': 'pass\n'}]}})
        self.assertEqual(repaired['status'], 'COMPLETED')
        self.assertTrue((self.root / 'architecture/missing.py').is_file())

    def test_repair_cannot_run_without_report_selection(self):
        with self.assertRaises(ValueError):
            directed_work(self.root, 'ChatGPT', {'request_id': 'REPAIR', 'source': 'BBEX',
                'payload': {'structural_repair': True, 'operations': [
                    {'action': 'create', 'path': 'ChatGPT/fix.txt', 'content': 'no'}]}})
        self.assertFalse((self.root / 'ChatGPT/fix.txt').exists())

    def test_structural_defect_repeats_once_then_resolves_to_fifteen_days(self):
        path = self.root / 'core/identity/profiles/ChatGPT.idp.json'
        profile = json.loads(path.read_text())
        profile['file_capabilities']['review_paths'] = ['architecture/missing.py']
        profile['file_capabilities']['scopes'].append({'path': 'architecture', 'operations': ['read']})
        path.write_text(json.dumps(profile))
        first = periodic_work(self.root, 'ChatGPT', force=True)
        again = periodic_work(self.root, 'ChatGPT', force=True)
        self.assertEqual(len(again['finding_tracking']), 1)
        self.assertEqual(again['finding_tracking'][0]['occurrences'], 2)
        self.assertEqual(again['interval_days'], 7)
        target = self.root / 'architecture/missing.py'
        target.parent.mkdir()
        target.write_text('pass\n')
        fixed = periodic_work(self.root, 'ChatGPT', force=True)
        self.assertEqual(fixed['interval_days'], 15)
        self.assertEqual(fixed['finding_tracking'][0]['status'], 'RESOLVED')
        report = json.loads((self.root / fixed['collaboration_report']).read_text())
        self.assertTrue(report['unknowns'])
        self.assertEqual(report['iget']['signal']['color'], 'yellow')
        self.assertTrue(report['iget']['proof']['trace'])
        self.assertFalse(report['findings'])

    def test_old_blanket_circuit_finding_does_not_lock_schedule(self):
        from tools.origin_cycle import write_state, load_state
        state = load_state(self.root, 'ChatGPT')
        state['findings'] = [{'kind': 'circuit_verification_required', 'path': 'ChatGPT/state.json'}]
        write_state(self.root, 'ChatGPT', state)
        result = periodic_work(self.root, 'ChatGPT', force=True)
        self.assertEqual(result['interval_days'], 15)
        self.assertFalse(result['finding_tracking'])

    def test_removing_defective_path_from_scope_keeps_weekly_followup(self):
        path = self.root / 'core/identity/profiles/ChatGPT.idp.json'
        profile = json.loads(path.read_text())
        profile['file_capabilities']['review_paths'] = ['architecture/absent.py']
        profile['file_capabilities']['scopes'].append({'path': 'architecture', 'operations': ['read']})
        path.write_text(json.dumps(profile))
        periodic_work(self.root, 'ChatGPT', force=True)
        profile['file_capabilities']['review_paths'] = ['ChatGPT/state.json']
        path.write_text(json.dumps(profile))
        result = periodic_work(self.root, 'ChatGPT', force=True)
        self.assertEqual(result['interval_days'], 7)
        self.assertEqual(result['finding_tracking'][0]['status'], 'NOT_RECHECKED')

    def test_existing_architecture_permission_needs_no_repair_report(self):
        profile_path = self.root / 'core/identity/profiles/ChatGPT.idp.json'
        profile = json.loads(profile_path.read_text())
        profile['file_capabilities']['scopes'].append({'path': 'docs/architecture', 'operations': ['create', 'read']})
        profile_path.write_text(json.dumps(profile))
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'ORDINARY', 'source': 'BBX19',
            'payload': {'operations': [{'action': 'create', 'path': 'docs/architecture/new.md', 'content': '# Design\n'}]}})
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertTrue((self.root / 'docs/architecture/new.md').exists())
        self.assertFalse(result['support_pending'])

    def test_orchestration_uses_existing_tools_and_records_support_return(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'TOOLS', 'source': 'BBX19',
            'payload': {'operations': [{'action': 'create', 'path': 'ChatGPT/note.md', 'content': '# Real note\n'}]}})
        task = json.loads((self.root / result['orchestration_evidence']).read_text())
        events = [entry['event'] for entry in task['history']]
        self.assertIn('ASSISTING', events)
        self.assertIn('RETURNED', events)
        support = json.loads((self.root / result['support_evidence']).read_text())
        tools = {entry['tool'] for entry in support['tools_used']}
        self.assertIn('tools/validate_metadata.py', tools)
        self.assertIn('tools/check_portable_paths.py', tools)
        self.assertTrue(support['resolved'])

    def test_failed_owner_work_remains_blocked_with_diagnostics(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'BLOCKED', 'source': 'BBX19',
            'payload': {'operations': [{'action': 'read', 'path': 'ChatGPT/absent.txt'}]}})
        self.assertEqual(result['status'], 'FAILED')
        self.assertTrue(result['support_pending'])
        task = json.loads((self.root / result['orchestration_evidence']).read_text())
        self.assertEqual(task['status'], 'BLOCKED')
        support = json.loads((self.root / result['support_evidence']).read_text())
        self.assertTrue(support['owner_reason'])
        self.assertFalse(support['resolved'])
        self.assertTrue(support['next_steps'])

    def test_tool_finding_creates_followup_without_rewriting_owner_output(self):
        content = 'approved-by: BBX19\n'
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'METADATA', 'source': 'BBX19',
            'payload': {'operations': [{'action': 'create', 'path': 'ChatGPT/note.md', 'content': content}]}})
        self.assertEqual((self.root / 'ChatGPT/note.md').read_text(), content)
        self.assertTrue(result['support_pending'])
        from tools.origin_cycle import load_state
        self.assertEqual(len(load_state(self.root, 'ChatGPT')['followups']), 1)

    def test_support_checks_final_state_after_create_move_delete(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'FINAL-STATES', 'source': 'BBX19',
            'payload': {'operations': [
                {'action': 'create', 'path': 'ChatGPT/first.txt', 'content': 'value'},
                {'action': 'move', 'path': 'ChatGPT/first.txt', 'destination': 'ChatGPT/last.txt',
                 'expected_sha256': digest(b'value')},
                {'action': 'delete', 'path': 'ChatGPT/last.txt', 'expected_sha256': digest(b'value')}]}})
        self.assertFalse(result['support_pending'])
        support = json.loads((self.root / result['support_evidence']).read_text())
        checks = [item for item in support['checks'] if item['check'] == 'final_file_state']
        self.assertEqual(len(checks), 2)
        self.assertTrue(all(item['actual_sha256'] is None for item in checks))

    def test_support_detects_changed_artifact_without_claiming_completion(self):
        from tools.origin_collaboration import collaborate
        from core.runtime.agents import get_agent
        result = get_agent('ChatGPT').execute('create', {}, {'payload': {
            'request_type': 'origin_file_operations', 'operations': [
                {'action': 'create', 'path': 'ChatGPT/file.txt', 'content': 'original'}]},
            'authority_context': {'repo_root': str(self.root)}})
        (self.root / 'ChatGPT/file.txt').write_text('changed')
        check = collaborate(self.root, 'ChatGPT', result)
        self.assertTrue(check['support_pending'])
        support = json.loads((self.root / check['support_evidence']).read_text())
        self.assertEqual(support['findings'][0]['kind'], 'output_evidence_mismatch')

