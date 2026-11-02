import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from w3_tool_store.agent_workbench.tools.artifact_handoff.runner import run, verify_artifacts, RULES


class ArtifactHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, text in {
            'modules/Cast/module.json': json.dumps({'file_access': {'read': ['core/', 'modules/Cast/']}}),
            'core/identity/profiles/Cast.idp.json': json.dumps({'module': 'Cast', 'version': '2.0'}),
            'core/example.py': 'def produce(value):\n    return str(value)\n',
        }.items():
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.output = self.root/'modules/ChatGPT/reports/handoffs/test'

    def produce(self):
        delivery = run(self.root, self.output, ['core/example.py'])
        produced = json.loads((self.output/'Cast-result.json').read_text())
        request = json.loads((self.output/'request.json').read_text())
        return delivery, produced, request

    def test_real_handoff_stops_at_declared_owner_review_with_trace(self):
        delivery, produced, request = self.produce()
        self.assertTrue(delivery['expected_stop_reached'])
        self.assertEqual(delivery['technical_result'], 'VERIFIED')
        self.assertEqual(delivery['status'], 'WAITING_HUMAN')
        self.assertIsNone(delivery['human_approval'])
        task = json.loads((self.root/delivery['task_snapshot']).read_text())
        self.assertEqual([r['destination']['module'] for r in task['route']], ['Cast', 'Gemini'])
        self.assertEqual(task['source_id'], request['request_id'])
        self.assertIsNone(task['human_approval'])
        self.assertTrue(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES)))
        with self.assertRaises(FileExistsError):
            run(self.root, self.output, ['core/example.py'])

    def test_content_tamper_and_current_source_change_are_rejected(self):
        _, produced, request = self.produce()
        info = produced['artifacts'][0]
        path = self.root/info['path']
        original = path.read_bytes()
        path.write_bytes(original+b' ')
        self.assertFalse(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES)))
        path.write_bytes(original)
        (self.root/'core/example.py').write_text('def changed():\n    return 42\n')
        self.assertFalse(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES)))

    def test_forged_structure_fails_even_with_updated_artifact_hash(self):
        _, produced, request = self.produce()
        info = produced['artifacts'][0]
        path = self.root/info['path']
        data = json.loads(path.read_bytes())
        data['facts'][0]['symbols'] = []
        encoded = json.dumps(data).encode()
        path.write_bytes(encoded)
        info.update(sha256=hashlib.sha256(encoded).hexdigest(), bytes=len(encoded))
        checks = verify_artifacts(self.root, produced, request, RULES)
        self.assertFalse(next(c['passed'] for c in checks if c['name'].endswith(':structure')))

    def test_rules_cannot_be_replaced_with_caller_pass_flags(self):
        _, produced, request = self.produce()
        self.assertFalse(all(c['passed'] for c in verify_artifacts(self.root, produced, request, {'passed': True})))

    def test_forged_json_inventory_is_rejected_with_matching_file_hash(self):
        run(self.root, self.output, ['core/identity/profiles/Cast.idp.json'])
        produced = json.loads((self.output/'Cast-result.json').read_text())
        request = json.loads((self.output/'request.json').read_text())
        info = produced['artifacts'][0]
        path = self.root/info['path']
        report = json.loads(path.read_bytes())
        report['facts'][0]['keys'] = ['invented']
        data = json.dumps(report).encode()
        path.write_bytes(data)
        info.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        checks = verify_artifacts(self.root, produced, request, RULES)
        self.assertFalse(next(c['passed'] for c in checks if c['name'].endswith(':structure')))

    def test_missing_producer_input_stops_with_blocked_evidence(self):
        result = run(self.root, self.output, ['core/missing.py'])
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertTrue((self.output/'Cast-result.json').is_file())
        self.assertFalse((self.output/'Gemini-result.json').exists())

    def test_output_cannot_be_placed_outside_handoff_area(self):
        with self.assertRaises(ValueError):
            run(self.root, self.root/'outside', ['core/example.py'])


if __name__ == '__main__':
    unittest.main()
