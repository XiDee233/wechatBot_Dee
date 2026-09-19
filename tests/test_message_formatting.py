"""Regression tests without connecting to WeChat or an LLM API."""
import ast
import logging
from pathlib import Path
import random
import re
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'send_reply', 'split_message_with_context', 'contains_code_block',
         'remove_timestamps', 'remove_parentheses_and_content'}

class MessageFormattingTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((ROOT / 'bot.py').read_text(encoding='utf-8-sig'))
        subset = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                                  and n.name in NAMES], type_ignores=[])
        self.enabled = False
        self.wx = SimpleNamespace(SendMsg=Mock(return_value=True))
        self.ns = dict(re=re, random=random, logger=logging.getLogger('format-test'),
                       time=SimpleNamespace(time=lambda: 0, sleep=lambda _: None),
                       is_sending_message=False, ENABLE_EMOJI_SENDING=False,
                       ENABLE_MEMORY=False, REMOVE_PARENTHESES=True, wx=self.wx,
                       get_dynamic_config=lambda key, default: self.enabled)
        exec(compile(subset, 'bot.py', 'exec'), self.ns)

    def test_whole_reply_preserves_separators(self):
        text = '第一段\n\n    第二段\nprice=$10, path=C:\\new\\test'
        self.assertEqual(self.ns['split_message_with_context'](text), [text])

    def test_shader_is_sent_once_unchanged(self):
        text = '说明\n```hlsl\nShader "Custom/SimpleColor"\n{\n    float4 frag() : SV_Target\n    {\n        return float4(1, 1, 1, 1);\n    }\n}\n```\n结束'
        for enabled in (False, True):
            self.enabled = enabled
            self.wx.SendMsg.reset_mock()
            self.ns['send_reply']('test-group', 'test', 'test', '', text)
            self.wx.SendMsg.assert_called_once_with(msg=text, who='test-group')

    def test_code_literals_and_unclosed_fences_are_preserved(self):
        self.enabled = True
        for text in ('```python\nprint("$10\\n[tickle]")', '~~~python\n    value = "$10"\n~~~'):
            self.assertEqual(self.ns['split_message_with_context'](text), [text])

    def test_optional_legacy_prose_split(self):
        self.enabled = True
        self.assertEqual(self.ns['split_message_with_context']('第一行\n第二行'), ['第一行', '第二行'])

    def test_empty_and_indentation(self):
        self.assertEqual(self.ns['split_message_with_context'](' \n'), [])
        self.assertEqual(self.ns['remove_timestamps']('正文\n    保留缩进'), '正文\n    保留缩进')

if __name__ == '__main__':
    unittest.main()
