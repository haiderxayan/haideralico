#!/usr/bin/env python3
"""
Fix bracketed numeric citations in a post by:
- Removing inline [n] markers that are not links
- Converting trailing [n](url) lines into a simple References bullet list
"""

import re
from pathlib import Path

POST = Path('_posts/2025-09-27-why-i-embraced-ethical-pessimism-after-reading-roy-scrantons-climate-philosophy.md')

def main():
    text = POST.read_text(encoding='utf-8')
    # Split to front matter and body
    if not text.startswith('---\n'):
        return
    fm, body = text.split('\n---\n', 1)

    # Remove inline citation markers [n] in the body that are not part of a link '](...)'
    # Safe heuristic: replace standalone [number] not immediately followed by '(' (link)
    body = re.sub(r"\[(\d{1,2})\](?!\()", "", body)

    # Convert trailing numeric links [n](url) into References list
    lines = body.splitlines()
    new_lines = []
    refs = []
    for ln in lines:
        m = re.match(r"^\[(\d{1,2})\]\((.*)\)\s*$", ln.strip())
        if m:
            refs.append(m.group(2))
        else:
            new_lines.append(ln)
    if refs:
        # Remove trailing blank lines
        while new_lines and new_lines[-1].strip() == '':
            new_lines.pop()
        new_lines.append('\n## References')
        for url in refs:
            new_lines.append(f"- {url}")
        new_lines.append('')
    body2 = "\n".join(new_lines)
    POST.write_text(fm + '\n---\n' + body2, encoding='utf-8')

if __name__ == '__main__':
    main()
