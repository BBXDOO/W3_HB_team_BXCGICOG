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
        self.assertTrue(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES, json.loads((self.output/'source-baseline.json').read_text()))))
        with self.assertRaises(FileExistsError):
            run(self.root, self.output, ['core/example.py'])

    def test_content_tamper_and_current_source_change_are_rejected(self):
        _, produced, request = self.produce()
        info = produced['artifacts'][0]
        path = self.root/info['path']
        original = path.read_bytes()
        path.write_bytes(original+b' ')
        self.assertFalse(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES, json.loads((self.output/'source-baseline.json').read_text()))))
        path.write_bytes(original)
        (self.root/'core/example.py').write_text('def changed():\n    return 42\n')
        self.assertFalse(all(c['passed'] for c in verify_artifacts(self.root, produced, request, RULES, json.loads((self.output/'source-baseline.json').read_text()))))

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

class ArtifactBoundaryRegressionTests(ArtifactHandoffTests):
    def baseline(self):
        return json.loads((self.output/'source-baseline.json').read_bytes())

    def test_aliases_cannot_supply_both_artifacts(self):
        _, produced, request = self.produce()
        report = produced['artifacts'][0]['path']
        (self.root/'modules/Cast/symlink-report.json').symlink_to(self.root/report)
        for alias in ('./'+report, 'modules/Cast/same-report.json', 'modules/Cast/symlink-report.json'):
            if alias.endswith('same-report.json'):
                (self.root/alias).hardlink_to(self.root/report)
            produced['artifacts'][1]['path'] = alias
            checks = verify_artifacts(self.root, produced, request, RULES, self.baseline())
            self.assertFalse(next(c['passed'] for c in checks if c['name'] == 'two_distinct_artifacts'))

    def test_unrelated_idp_and_wrong_canonical_identity_are_rejected(self):
        _, produced, request = self.produce()
        info = produced['artifacts'][0]
        path = self.root/info['path']
        report = json.loads(path.read_bytes())
        report['idp']['path'] = 'core/example.py'
        report['idp']['sha256'] = hashlib.sha256((self.root/'core/example.py').read_bytes()).hexdigest()
        data = json.dumps(report).encode()
        path.write_bytes(data)
        info.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        checks = verify_artifacts(self.root, produced, request, RULES, self.baseline())
        self.assertFalse(next(c['passed'] for c in checks if c['name'] == 'idp_reference'))

    def test_producer_cannot_rewrite_source_and_claim_read_only(self):
        from unittest.mock import patch
        from w3_tool_store.agent_workbench.tools.artifact_handoff import runner
        real_get_agent = runner.get_agent
        cast = real_get_agent('Cast')
        original_execute = cast.execute
        def changed(*args, **kwargs):
            (self.root/'core/example.py').write_text('def changed():\n    return 1\n')
            return original_execute(*args, **kwargs)
        with patch.object(cast, 'execute', side_effect=changed):
            with patch.object(runner, 'get_agent', side_effect=lambda name: cast if name == 'Cast' else real_get_agent(name)):
                delivery = run(self.root, self.output, ['core/example.py'])
        self.assertEqual(delivery['status'], 'BLOCKED')
        self.assertNotIn('fault_note', delivery)  # baseline proves a change, not its author
        self.assertTrue((self.output/'delivery.json').is_file())

    def test_recipient_rejects_changed_or_malformed_envelope_with_full_report(self):
        from unittest.mock import patch
        from w3_tool_store.agent_workbench.tools.artifact_handoff import runner
        original_write = runner.write
        def tamper(path, value):
            original_write(path, value)
            if path.name == 'Gemini-ack.json':
                (self.output/'Cast-result.json').write_text('{broken')
        with patch.object(runner, 'write', side_effect=tamper):
            delivery = run(self.root, self.output, ['core/example.py'])
        self.assertEqual(delivery['status'], 'BLOCKED')
        self.assertEqual(delivery['technical_result'], 'UNRESOLVED')
        self.assertTrue((self.output/'delivery.json').is_file())
        self.assertFalse((self.output/'Gemini-result.json').exists())
        self.assertNotIn('fault_note', delivery)  # no unsupported attribution

    def test_duplicate_paths_are_normalized_before_dispatch(self):
        delivery = run(self.root, self.output, ['core/example.py', 'core/example.py'])
        self.assertEqual(delivery['technical_result'], 'VERIFIED')
        self.assertTrue(delivery['paired_review']['trace_verified'])
        self.assertEqual(json.loads((self.output/'request.json').read_bytes())['source_paths'], ['core/example.py'])

    def test_valid_but_substituted_envelope_is_rejected(self):
        from unittest.mock import patch
        from w3_tool_store.agent_workbench.tools.artifact_handoff import runner
        original_write = runner.write
        def substitute(path, value):
            original_write(path, value)
            if path.name == 'Gemini-ack.json':
                result_path = self.output/'Cast-result.json'
                result = json.loads(result_path.read_bytes())
                result['substituted_at_receive'] = True
                original_write(result_path, result)
        with patch.object(runner, 'write', side_effect=substitute):
            delivery = run(self.root, self.output, ['core/example.py'])
        self.assertEqual(delivery['status'], 'BLOCKED')
        checks = json.loads((self.root/delivery['checks']).read_bytes())
        self.assertFalse(next(c['passed'] for c in checks if c['name'] == 'producer_envelope_unchanged'))

    def test_clear_forged_report_writes_producer_fault_note(self):
        from unittest.mock import patch
        from w3_tool_store.agent_workbench.tools.artifact_handoff import runner
        real_get_agent = runner.get_agent
        cast = real_get_agent('Cast')
        original_execute = cast.execute
        def forge(*args, **kwargs):
            result = original_execute(*args, **kwargs)
            info = result['artifacts'][0]
            report_path = self.root/info['path']
            report = json.loads(report_path.read_bytes())
            report['facts'][0]['symbols'] = []
            data = json.dumps(report).encode()
            report_path.write_bytes(data)
            info.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
            return result
        with patch.object(cast, 'execute', side_effect=forge):
            with patch.object(runner, 'get_agent', side_effect=lambda name: cast if name == 'Cast' else real_get_agent(name)):
                delivery = run(self.root, self.output, ['core/example.py'])
        self.assertEqual(delivery['status'], 'BLOCKED')
        self.assertTrue((self.root/delivery['fault_note']).is_file())
        self.assertTrue(delivery['fault_note'].startswith('modules/Cast/notes/'))
