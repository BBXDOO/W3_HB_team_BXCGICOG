import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from core.runtime.agents.cast import CastAgent
from core.runtime.engine_v2 import run


class CastStructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, body in {
            'modules/Cast/module.json': json.dumps({'file_access': {'read': ['core/', 'modules/Cast/']}}),
            'core/identity/profiles/Cast.idp.json': json.dumps({'module': 'Cast', 'version': '2.0'}),
            'core/example.py': 'import json\ndef inspect(value):\n    return json.dumps(value)\n',
            'Cast/context/session_summary.md': '# Prior context\nHistorical, not current evidence.\n',
        }.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)

    def call(self, task='structural_inspect', paths=None, **extra):
        context = {'authority_context': {'repo_root': str(self.root)},
                   'payload': {'source_paths': paths if paths is not None else ['core/example.py']},
                   'request': {'source_id': 'RQ-CAST-TEST'}, **extra}
        return CastAgent().execute(task, {'kind': task}, context)

    def test_registry_tasks_create_verifiable_separate_artifacts(self):
        original = (self.root/'core/example.py').read_bytes()
        for task in ('structural_inspect', 'structural_adapt', 'capability_learn'):
            result = self.call(task)
            self.assertEqual(result['status'], 'COMPLETED')
            self.assertTrue(result['review'])
            self.assertFalse(result['authority']['decision_allowed'])
            self.assertEqual(len(result['artifacts']), 2)
            for artifact in result['artifacts']:
                data = (self.root/artifact['path']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), artifact['sha256'])
            report = result['details']
            self.assertEqual(report['facts'][0]['symbols'][0]['name'], 'inspect')
            self.assertEqual(report['request_id'], 'RQ-CAST-TEST')
            self.assertFalse(report['closed'])
            self.assertIn('historical', report['continuity']['usage'])
        self.assertEqual(original, (self.root/'core/example.py').read_bytes())

    def test_engine_routes_registered_capability_without_host_import_strings(self):
        with patch('core.runtime.engine_v2.add_memory'), patch('core.runtime.engine_v2.search_memory', return_value=[]):
            result = run('structural_inspect', {'payload': {'source_paths': ['core/example.py']}},
                         authority_context={'repo_root': str(self.root)})
        self.assertEqual(result['module'], 'Cast')
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertEqual(result['result_validation']['status'], 'valid')

    def test_request_cannot_choose_repository(self):
        result = self.call(payload={'repo_root': '/', 'source_paths': ['etc/passwd']})
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')
        self.assertFalse(result['mutated'])

    def test_missing_scope_escape_and_invalid_inputs_fail_before_write(self):
        for paths in ([], ['core/missing.py'], ['../outside'], ['/etc/passwd'], ['requests/secret.md'], [{}]):
            self.assertEqual(self.call(paths=paths)['status'], 'REVIEW_REQUIRED')
        self.assertFalse((self.root/'modules/Cast/reports').exists())

    def test_symlink_source_cannot_escape_repository(self):
        (self.root/'core/link').symlink_to('/etc/passwd')
        self.assertEqual(self.call(paths=['core/link'])['status'], 'REVIEW_REQUIRED')

    def test_symlink_output_cannot_escape_workspace(self):
        outside = self.root/'outside'
        outside.mkdir()
        (self.root/'modules/Cast/reports').symlink_to(outside)
        self.assertEqual(self.call()['status'], 'REVIEW_REQUIRED')
        self.assertEqual(list(outside.iterdir()), [])

    def test_syntax_error_has_explicit_review_and_no_artifact(self):
        (self.root/'core/example.py').write_text('def broken(')
        self.assertEqual(self.call()['status'], 'REVIEW_REQUIRED')
        self.assertFalse((self.root/'modules/Cast/reports').exists())

    def test_unrelated_old_memory_does_not_complete_current_reasoning(self):
        result = CastAgent().execute('reason', {'kind': 'reasoning'},
                                     {'records': [{'source': 'Cast', 'topic': 'another task'}]})
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')

    def test_critical_reasoning_registry_alias_structures_explicit_observations(self):
        result = CastAgent().execute('critical_reasoning', {},
                                     {'payload': {'observations': ['Observed gateway review gate']}})
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertEqual(result['action'], 'structure_context')
        self.assertFalse(result['authority']['decision_allowed'])

    def test_malformed_report_value_returns_review_instead_of_crashing(self):
        result = CastAgent().execute('report', {'kind': 'subsystem_report',
                                               'subsystem': 'MPCP', 'reported': {}}, {})
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')

    def test_interrupted_second_write_retains_first_artifact(self):
        original = Path.open
        def interrupted(path, *args, **kwargs):
            if '/artifacts/private/' in str(path) and args and args[0] == 'xb':
                raise OSError('simulated storage interruption')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', interrupted):
            result = self.call()
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')
        self.assertTrue(result['mutated'])
        self.assertEqual(len(result['artifacts']), 1)
        self.assertTrue((self.root/result['artifacts'][0]['path']).is_file())


if __name__ == '__main__':
    unittest.main()
