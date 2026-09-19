import unittest
from unittest.mock import Mock
from reply_format import extract_manual_mention, normalize_reply
from history_tools import query_notice

class ReplyPresentationTests(unittest.TestCase):
    def test_signature_once(self):
        text = '「AI彬哥:」第一段\n\n「AI彬哥:」第二段'
        self.assertEqual(normalize_reply(text), '「AI彬哥:」第一段\n\n第二段')
    def test_code_not_rewritten(self):
        text = '「AI彬哥:」例子\n```text\n「AI彬哥:」原样保留\n```\n「AI彬哥:」说明'
        self.assertEqual(normalize_reply(text), '「AI彬哥:」例子\n```text\n「AI彬哥:」原样保留\n```\n说明')
    def test_normal_reply_unchanged(self):
        text = '第一段\n\n第二段'
        self.assertEqual(normalize_reply(text), text)
    def test_explicit_failure_not_no_records(self):
        reply = query_notice({'status': 'unavailable', 'error_type': 'PermissionError'}, {})
        self.assertIn('PermissionError', reply)
        self.assertNotIn('没有找到', reply)
        self.assertNotIn('重新登录', reply)
        self.assertNotIn('稍后', reply)

    def test_leading_plain_at_is_promoted_to_action(self):
        self.assertEqual(
            extract_manual_mention('「AI彬哥:」@吴开森 行，按你给的名字来。'),
            '吴开森',
        )
        self.assertIsNone(extract_manual_mention('我只是讨论一下@吴开森'))

if __name__ == '__main__': unittest.main()
