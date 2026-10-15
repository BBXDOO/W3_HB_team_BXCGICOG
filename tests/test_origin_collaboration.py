import json
import unittest
from tests import test_origin_operations as origin_fixtures
from tools.origin_cycle import directed_work, periodic_work
from tools.origin_collaboration import validate_repair_selection
from core.runtime.agents.origin_operations import digest


class CollaborationTests(unittest.TestCase):
    setUp = origin_fixtures.OriginOperationsTests.setUp
    def test_missing_partner_uses_orchestration_receipt(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'PAIR', 'source': 'BBX19',
            'payload': {'partner': 'NotInstalled', 'operations': [
                {'action': 'create', 'path': 'ChatGPT/paired.txt', 'content': 'real'}]}})
        self.assertEqual(result['partner'], 'Orchestration')
        self.assertTrue((self.root / result['orchestration_evidence']).is_file())

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
