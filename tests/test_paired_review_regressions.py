"""PR #322: broken-input and accountability paths identified by both reviewers."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import digest
from tools.origin_collaboration import collaborate
from tools.origin_cycle import directed_work
from tests import test_origin_operations as origin_fixtures
from tests import test_artifact_handoff as artifact_fixtures
from workflows.paired_work import PairedWork
from w3_tool_store.agent_workbench.tools.artifact_handoff import runner


class OriginReviewRegressions(unittest.TestCase):
    setUp = origin_fixtures.OriginOperationsTests.setUp
    execute = origin_fixtures.OriginOperationsTests.execute

    def report(self, result):
        self.assertTrue((self.root/result['orchestration_evidence']).is_file())
        return json.loads((self.root/result['collaboration_report']).read_bytes())

    def test_edit_bodies_and_unrecognized_fields_are_not_persisted(self):
        path = self.root/'ChatGPT/state.json'
        result = self.execute('ChatGPT', [{'action': 'edit', 'path': 'ChatGPT/state.json',
            'old': 'active', 'new': 'canary-body-9a', 'unexpected': 'canary-extra-7b',
            'expected_sha256': digest(path.read_bytes())}])
        self.assertEqual(result['status'], 'COMPLETED')
        for file in (self.root/'repo_events').rglob('*.json'):
            text = file.read_text()
            self.assertNotIn('canary-body-9a', text)
            self.assertNotIn('canary-extra-7b', text)
        intake = json.loads((self.root/result['work_start']['path']).read_bytes())
        self.assertEqual(intake['operations'][0]['action'], 'edit')

    def test_non_list_operations_still_get_failure_receipts(self):
        for value in (42, True, {'action': 'read'}):
            with self.subTest(value=value):
                result = self.execute('ChatGPT', value)
                self.assertEqual(result['status'], 'FAILED')
                self.assertTrue((self.root/result['log_path']).is_file())
                self.assertTrue((self.root/result['work_start']['path']).is_file())

    def test_all_supported_context_transports_keep_notes_and_explanations(self):
        note = {'id': 'n1', 'owner': 'ChatGPT', 'kind': 'doubt', 'meaning': 'bounded coverage'}
        exp = {'note_id': 'n1', 'owner': 'ChatGPT', 'what': 'read', 'how': 'local', 'why': 'request'}
        data = {'request_type': 'origin_file_operations', 'operations': [{'action': 'read', 'path': 'ChatGPT/state.json'}],
                'handoff_notes': [note], 'note_explanations': [exp]}
        for body in (data, {'payload': data}, {'request': data}, {'request': {'payload': data}}):
            with self.subTest(transport=list(body)):
                result = get_agent('ChatGPT').execute('transport probe', {},
                    {**body, 'authority_context': {'repo_root': str(self.root)}})
                self.assertEqual(result['status'], 'COMPLETED')
                self.assertEqual(result['handoff_notes'], [note])
                checked = collaborate(self.root, 'ChatGPT', result)
                report = self.report(checked)
                self.assertEqual(report['note_explanations'][0]['what'], 'read')
                self.assertIn(note, report['handoff_notes'])

    def test_rejected_annotations_block_with_report_and_followup(self):
        result = directed_work(self.root, 'ChatGPT', {'request_id': 'BAD-NOTES', 'source': 'BBX19',
            'payload': {'operations': [{'action': 'read', 'path': 'ChatGPT/state.json'}], 'handoff_notes': [{}]}})
        report = self.report(result)
        self.assertTrue(result['support_pending'])
        self.assertTrue(any(x['kind'] == 'invalid_annotations' for x in report['findings']))
        owner = json.loads((self.root/result['log_path']).read_bytes())
        self.assertEqual(owner['handoff_notes'], [{}])
        self.assertTrue(report['paired_review']['conflicts'])

    def test_correct_missing_receipt_review_does_not_blame_reviewer(self):
        result = self.execute('ChatGPT', [{'action': 'read', 'path': 'ChatGPT/state.json'}])
        (self.root/result['log_path']).unlink()
        checked = collaborate(self.root, 'ChatGPT', result, partner='Gemini')
        report = self.report(checked)
        self.assertTrue(checked['support_pending'])
        self.assertNotIn('reviewer_fault_note', report)
        receipt = json.loads((self.root/report['partner_receipt']).read_bytes())
        self.assertEqual(receipt['partner_result']['status'], 'REVIEW_REQUIRED')
        self.assertFalse(receipt['partner_result'].get('invalid_partner_receipt', False))

    def test_no_independent_reviewer_returns_saved_block(self):
        for profile in (self.root/'core/identity/profiles').glob('*.json'):
            if profile.name != 'ChatGPT.idp.json':
                profile.unlink()
        result = self.execute('ChatGPT', [{'action': 'read', 'path': 'ChatGPT/state.json'}])
        checked = collaborate(self.root, 'ChatGPT', result)
        report = self.report(checked)
        self.assertTrue(checked['support_pending'])
        self.assertEqual(report['replacement_pair']['status'], 'BLOCKED_NO_CAPABLE_PAIR')

    def test_read_only_invalid_input_does_not_create_owner_fault(self):
        (self.root/'ChatGPT/invalid.md').write_text('approved-by: BBX19\n')
        result = self.execute('ChatGPT', [{'action': 'read', 'path': 'ChatGPT/invalid.md'}])
        report = self.report(collaborate(self.root, 'ChatGPT', result))
        self.assertTrue(report['findings'])
        self.assertNotIn('fault_note', report)
        self.assertTrue(report['paired_review']['conflicts'])

    def test_unknown_writer_invalid_output_does_not_create_owner_fault(self):
        result = self.execute('ChatGPT', [{'action': 'create', 'path': 'ChatGPT/output.md', 'content': '# Valid\n'}])
        (self.root/'ChatGPT/output.md').write_text('approved-by: BBX19\n')
        report = self.report(collaborate(self.root, 'ChatGPT', result))
        self.assertNotIn('fault_note', report)
        self.assertTrue(any(x['kind'] == 'output_evidence_mismatch' for x in report['findings']))

    def test_tampered_owner_receipt_cannot_establish_producer_fault(self):
        result = self.execute('ChatGPT', [{'action': 'create', 'path': 'ChatGPT/output.md', 'content': '# Valid\n'}])
        path = self.root/result['log_path']
        original = json.loads(path.read_bytes())
        (self.root/'ChatGPT/output.md').write_text('approved-by: BBX19\n')
        original['operations'][0]['sha256'] = digest((self.root/'ChatGPT/output.md').read_bytes())
        path.write_text(json.dumps(original))
        report = self.report(collaborate(self.root, 'ChatGPT', result))
        self.assertNotIn('fault_note', report)
        self.assertTrue(any(x['kind'] == 'invalid_owner_receipt' for x in report['findings']))


class ExplanationReviewRegressions(unittest.TestCase):
    setUp = artifact_fixtures.ArtifactHandoffTests.setUp

    def ledger(self):
        path = self.root/'core/example.py'
        ledger = PairedWork(self.root, 'receipts', {'evidence': [{'path': 'core/example.py','sha256': digest(path.read_bytes())}]})
        note = ledger.note('Cast', 'unknown')
        return ledger, note

    def send(self, ledger):
        ledger.transfer('Cast', 'Gemini', 'BBX19', ['core/example.py'], [{'passed': True}])

    def test_explanation_added_after_last_handoff_is_not_certified(self):
        ledger, note = self.ledger()
        self.send(ledger)
        ledger.explain('Cast', note, what='read', how='AST', why='inspect')
        self.assertFalse(ledger.audit()['trace_verified'])
        self.assertFalse(ledger.audit()['note_review'][0]['explanation_attached'])
        self.send(ledger)
        self.assertTrue(ledger.audit()['trace_verified'])

    def test_explanation_omission_or_rewrite_breaks_continuity(self):
        for change in ('omit', 'rewrite'):
            with self.subTest(change=change):
                ledger, note = self.ledger()
                ledger.explain('Cast', note, what='read', how='AST', why='inspect')
                self.send(ledger)
                if change == 'omit': ledger.explanations.clear()
                else: ledger.explanations[0]['why'] = 'changed'
                self.send(ledger)
                self.assertFalse(ledger.audit()['trace_verified'])


class ArtifactReviewRegressions(unittest.TestCase):
    setUp = artifact_fixtures.ArtifactHandoffTests.setUp

    def mutate_after_cast(self, mutation):
        real_get = runner.get_agent
        cast = real_get('Cast')
        original = cast.execute
        def execute(*args, **kwargs):
            value = original(*args, **kwargs)
            mutation()
            return value
        with patch.object(cast, 'execute', side_effect=execute):
            with patch.object(runner, 'get_agent', side_effect=lambda name: cast if name == 'Cast' else real_get(name)):
                return runner.run(self.root, self.output, ['core/example.py'])

    def assert_blocked_saved(self, result):
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertTrue((self.output/'delivery.json').is_file())
        task = json.loads((self.root/result['task_snapshot']).read_bytes())
        self.assertEqual(task['status'], 'BLOCKED')
        self.assertFalse((self.output/'Gemini-result.json').exists())

    def test_missing_or_invalid_source_does_not_imply_cast_fault(self):
        for mutation in ('missing', 'invalid-python'):
            with self.subTest(mutation=mutation):
                # Separate evidence directories; source is restored before the next attempt.
                (self.root/'core/example.py').write_text('def produce(value):\n    return str(value)\n')
                self.output = self.root/'modules/ChatGPT/reports/handoffs'/mutation
                path = self.root/'core/example.py'
                result = self.mutate_after_cast(lambda: path.unlink() if mutation == 'missing' else path.write_text('def broken('))
                self.assert_blocked_saved(result)
                self.assertNotIn('fault_note', result)

    def test_request_and_rules_damage_always_leave_blocked_delivery(self):
        for filename in ('request.json', 'rules.json'):
            for damage in ('missing', 'malformed', 'changed'):
                with self.subTest(filename=filename, damage=damage):
                    self.output = self.root/'modules/ChatGPT/reports/handoffs'/(filename+'-'+damage)
                    def mutate():
                        path = self.output/filename
                        if damage == 'missing': path.unlink()
                        elif damage == 'malformed': path.write_text('{broken')
                        else: path.write_text('{}')
                    result = self.mutate_after_cast(mutate)
                    self.assert_blocked_saved(result)
                    self.assertNotIn('fault_note', result)
