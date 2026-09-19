"""Presentation rules for one WeChat reply, without changing quoted code."""
import re

def normalize_reply(text):
    if not text:
        return text
    match = re.match(r'^\s*(「[^」\n]{1,40}[:：]」)', text)
    if not match:
        return text
    prefix = match.group(1)
    result, seen, fence = [], False, None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)[0]
            if fence is None: fence = token
            elif fence == token: fence = None
        if fence is None and line.lstrip().startswith(prefix):
            if seen:
                line = re.sub(r'^\s*' + re.escape(prefix) + r'[ \t]*', '', line, count=1)
            seen = True
        result.append(line)
    return ''.join(result)
