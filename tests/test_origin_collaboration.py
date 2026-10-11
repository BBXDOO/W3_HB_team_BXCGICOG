import json
import unittest
from tests.test_origin_operations import OriginOperationsTests
from tools.origin_cycle import directed_work, periodic_work
from tools.origin_collaboration import validate_repair_selection
from core.runtime.agents.origin_operations import digest


class CollaborationTests(unittest.TestCase):
    setUp = OriginOperationsTests.setUp
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
