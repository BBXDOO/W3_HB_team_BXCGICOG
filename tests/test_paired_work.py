import json
import tempfile
import unittest
from pathlib import Path

from workflows.paired_work import PairedWork, fingerprint, record_fault, replacement


class PairedWorkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'start.json').write_text('{"intent":"bounded work"}')
        self.start = {'evidence': [{'path': 'start.json', 'sha256': fingerprint((self.root/'start.json').read_bytes())}]}
        self.pair = PairedWork(self.root, 'receipts', self.start)
        self.checks = [{'name': 'file_verified', 'passed': True}]

    def send(self):
        return self.pair.transfer('Cast', 'Gemini', 'Orchestration', ['start.json'], self.checks)

    def test_notes_survive_all_handoffs_even_after_explanation(self):
        note_id = self.pair.note('Cast', 'Limited coverage', evidence='start.json')
        self.send()
        self.pair.explain('Cast', note_id, what='inspect source', how='AST', why='bounded task')
        self.pair.transfer('Orchestration', 'Gemini', 'BBX19', ['start.json'], self.checks)
        audit = self.pair.audit()
        self.assertTrue(audit['trace_verified'])
        self.assertEqual(len(audit['notes']), 1)
        self.assertEqual(audit['notes'][0]['status'], 'OPEN')
        self.assertFalse(audit['explanations'][0]['verified'])
        for ref in audit['receipts']:
            self.assertEqual(json.loads((self.root/ref['path']).read_bytes())['notes'], audit['notes'])

    def test_self_review_and_foreign_explanation_are_rejected(self):
        with self.assertRaises(ValueError):
            self.pair.transfer('Cast', 'Cast', 'BBX19', ['start.json'], self.checks)
        note = self.pair.note('Cast', 'Explain this')
        with self.assertRaises(ValueError):
            self.pair.explain('Gemini', note, what='x', how='y', why='z')

    def test_corrupt_receipt_missing_receipt_and_changed_start_fail_audit(self):
        ref = self.send()
        path = self.root/ref['path']
        original = path.read_bytes()
        path.write_bytes(b'not json')
        self.assertFalse(self.pair.audit()['trace_verified'])
        path.unlink()
        self.assertFalse(self.pair.audit()['trace_verified'])
        path.write_bytes(original)
        (self.root/'start.json').write_text('{}')
        self.assertFalse(self.pair.audit()['trace_verified'])

    def test_error_note_cannot_be_erased_by_explanation(self):
        note = self.pair.note('Cast', 'Wrong format', kind='error')
        self.pair.explain('Cast', note, what='bad report', how='wrong schema', why='mistake')
        self.send()
        self.assertEqual(len(self.pair.audit()['conflicts']), 1)

    def test_note_rewrite_is_rejected_on_next_receive(self):
        self.pair.carry([{'id': 'n', 'owner': 'Cast', 'meaning': 'unknown', 'kind': 'doubt'}])
        with self.assertRaises(ValueError):
            self.pair.carry([{'id': 'n', 'owner': 'Cast', 'meaning': 'all clear', 'kind': 'doubt'}])

    def test_fault_note_stays_in_owned_area_and_retains_prior_notes(self):
        first = record_fault(self.root, 'Cast', 'full-report.json', [{'kind': 'error'}])
        second = record_fault(self.root, 'Cast', 'full-report.json', [{'kind': 'error'}])
        self.assertNotEqual(first, second)
        self.assertTrue((self.root/first).is_file())
        self.assertTrue(first.startswith('modules/Cast/notes/'))
        with self.assertRaises(ValueError):
            record_fault(self.root, '../someone', 'full-report.json', [])

    def test_no_available_replacement_is_explicit_block(self):
        result = replacement(self.root, 'Cast', 'Gemini', ['start.json'])
        self.assertEqual(result['status'], 'BLOCKED_NO_CAPABLE_PAIR')
        self.assertIsNone(result['reviewer'])

    def test_legacy_without_start_never_certifies_complete_trace(self):
        self.pair.start = {'evidence': []}
        self.send()
        self.assertFalse(self.pair.audit()['trace_verified'])
