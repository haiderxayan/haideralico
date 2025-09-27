#!/usr/bin/env python3
"""
Repair front matter delimiter placement in posts where the closing '---' was
accidentally appended to the last key line (e.g., `image_alt: ...---`).

This script ensures the closing '---' is on its own line.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"


def repair(text: str) -> str:
    if not text.startswith('---\n'):
        return text
    # Split once after the opening delimiter
    rest = text[4:]
    # Look for the first occurrence of a line that ends with --- (possibly joined)
    # If we find lines like '...---\n', break them into '...\n---\n'
    def fix_block(block: str) -> str:
        lines = block.splitlines(keepends=True)
        out = []
        fixed = False
        for i, ln in enumerate(lines):
            if i == 0 and ln.strip() == '':
                out.append(ln)
                continue
            if ln.rstrip('\n').endswith('---') and not ln.lstrip().startswith('---'):
                # Split before the trailing delimiter
                prefix = ln.rstrip('\n')[:-3].rstrip()
                out.append(prefix + '\n')
                out.append('---\n')
                # Append the remainder (if any lines left) and stop processing the rest as front matter
                out.extend(lines[i+1:])
                fixed = True
                break
            out.append(ln)
        return ''.join(out), fixed

    fixed_block, fixed = fix_block(rest)
    if fixed:
        return '---\n' + fixed_block
    return text


def main():
    changed = 0
    for post in POSTS.glob('*.md'):
        t = post.read_text(encoding='utf-8')
        nt = repair(t)
        if nt != t:
            post.write_text(nt, encoding='utf-8')
            print(f"Repaired: {post}")
            changed += 1
    print(f"Total repaired: {changed}")


if __name__ == '__main__':
    main()

