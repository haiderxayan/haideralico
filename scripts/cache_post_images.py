#!/usr/bin/env python3
"""
Download and cache remote post images locally under assets/images/posts/YYYY/MM/slug.ext,
then rewrite the post front matter `image:` to the local path. Preserves credit fields.

Only processes posts whose `image:` is an HTTP(S) URL.
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"


def _ext_from_content_type(ct: str) -> str:
    ct = (ct or '').lower()
    if 'image/webp' in ct:
        return 'webp'
    if 'image/png' in ct:
        return 'png'
    if 'image/jpeg' in ct or 'image/jpg' in ct:
        return 'jpg'
    if 'image/svg' in ct:
        return 'svg'
    return 'jpg'


def parse_front_matter(text: str):
    if not text.startswith('---\n'):
        return None, text
    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        return None, text
    return parts[0][4:], parts[1]


def replace_or_insert(fm: str, key: str, value: str):
    line = f"{key}: \"{value}\"\n"
    pattern = re.compile(rf"^{key}:\s*.*$", re.MULTILINE)
    if pattern.search(fm):
        return pattern.sub(line, fm)
    after = re.search(r"^(title:.*\n)", fm, re.MULTILINE)
    if not after:
        after = re.search(r"^(date:.*\n)", fm, re.MULTILINE)
    if after:
        idx = after.end()
        return fm[:idx] + line + fm[idx:]
    return line + fm


def cache_image(image_url: str, date_str: str, filename: str) -> Optional[str]:
    try:
        # Determine date for path
        try:
            dt = datetime.fromisoformat(date_str.split()[0])
        except Exception:
            parts = filename.split('-', 3)
            dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        y = dt.strftime('%Y')
        m = dt.strftime('%m')
        slug = filename.replace('.md', '').split('-', 3)[-1]
        out_dir = ROOT / 'assets' / 'images' / 'posts' / y / m
        out_dir.mkdir(parents=True, exist_ok=True)

        # Fetch image
        headers = {"User-Agent": "CachePostImages/1.0"}
        resp = requests.get(image_url, headers=headers, timeout=25, stream=True)
        if resp.status_code != 200:
            return None
        ext = _ext_from_content_type(resp.headers.get('Content-Type', ''))
        out_path = out_dir / f"{slug}.{ext}"
        if not out_path.exists():
            with open(out_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
        rel = out_path.relative_to(ROOT)
        return f"/{rel.as_posix()}"
    except Exception:
        return None


def main():
    changed = 0
    for post in sorted(POSTS.glob('*.md')):
        text = post.read_text(encoding='utf-8')
        fm, body = parse_front_matter(text)
        if not fm:
            continue
        # Extract image
        m = re.search(r"^image:\s*\"(.+?)\"\s*$", fm, re.MULTILINE)
        if not m:
            continue
        image_url = m.group(1).strip()
        if not image_url.startswith('http://') and not image_url.startswith('https://'):
            continue
        # Extract date
        dm = re.search(r"^date:\s*(.+)$", fm, re.MULTILINE)
        date_str = (dm.group(1).strip() if dm else '')
        new_path = cache_image(image_url, date_str, post.name)
        if not new_path:
            continue
        fm2 = replace_or_insert(fm, 'image', new_path)
        if fm2 != fm:
            fm_block = fm2.rstrip('\n') + "\n"
            new_text = f"---\n{fm_block}---\n{body}"
            post.write_text(new_text, encoding='utf-8')
            changed += 1
            print('Cached:', post.name, '->', new_path)

    print('Total cached:', changed)


if __name__ == '__main__':
    main()
