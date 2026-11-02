import unittest

from tools.origin_cycle import intake_github


class OriginStatusIntakeTests(unittest.TestCase):
    def event(self, body, *, state='open', action='edited'):
        return {'sender': {'login': 'BBXDOO'}, 'action': action,
                'issue': {'number': 309, 'id': 1, 'state': state,
                          'title': 'ChatGPT prior task status', 'body': body}}

    def test_status_marker_does_not_replay_quoted_operations_or_create_text_followup(self):
        body = '<!-- w3-status-update -->\n@ChatGPT historical receipt\n```w3-origin\n{"operations":[{"action":"read","path":"protocol/mpcp/runtime/README.md"}]}\n```'
        self.assertEqual(intake_github(self.event(body), 'issues'), [])

    def test_edit_closed_issue_is_not_new_work(self):
        self.assertEqual(intake_github(self.event('@ChatGPT status changed', state='closed'), 'issues'), [])

    def test_reopened_explicit_request_still_dispatches(self):
        event = self.event('@ChatGPT read current context', action='reopened')
        self.assertEqual(intake_github(event, 'issues')[0]['target'], 'ChatGPT')

    def test_comment_status_marker_is_respected(self):
        event = self.event('historical')
        event['comment'] = {'id': 2, 'body': '<!-- w3-status-update -->\nChatGPT report only'}
        self.assertEqual(intake_github(event, 'issue_comment'), [])

    def test_non_owner_still_cannot_dispatch(self):
        event = self.event('@ChatGPT read')
        event['sender']['login'] = 'someone-else'
        self.assertEqual(intake_github(event, 'issues'), [])


if __name__ == '__main__':
    unittest.main()
