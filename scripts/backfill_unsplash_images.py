#!/usr/bin/env python3
"""
Backfill Unsplash images with author credit for existing posts.

Strategy:
- For each post, if image credit is missing or generic, search Unsplash by title/topic and set a credited image.
- Avoid reuse: track used photo IDs in assets/data/used_unsplash.json

Requires env UNSPLASH_ACCESS_KEY.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
USED_STORE = ROOT / "assets" / "data" / "used_unsplash.json"
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


def request_json(url: str):
    req = Request(url, headers={
        'Authorization': f'Client-ID {ACCESS_KEY}',
        'Accept-Version': 'v1',
        'User-Agent': 'BackfillUnsplash/1.0'
    })
    with urlopen(req, timeout=12) as resp:
        return json.load(resp)


def search_photo(query: str, used_ids: set):
    url = 'https://api.unsplash.com/search/photos?' + urlencode({
        'query': query,
        'orientation': 'landscape',
        'per_page': 10,
        'order_by': 'relevant',
        'content_filter': 'high',
    })
    data = request_json(url)
    results = data.get('results') or []
    for r in results:
        pid = r.get('id')
        if pid and pid not in used_ids:
            base = r['urls'].get('raw') or r['urls'].get('regular')
            if base:
                sep = '&' if '?' in base else '?'
                img_url = f"{base}{sep}w=1200&h=630&fit=crop&auto=format"
            else:
                img_url = r['urls'].get('regular')
            alt = r.get('alt_description') or query
            user = r.get('user', {})
            author = user.get('name') or user.get('username') or 'Unsplash contributor'
            author_url = user.get('links', {}).get('html') or 'https://unsplash.com/'
            return {
                'id': pid,
                'image': img_url,
                'alt': alt,
                'credit_text': f"Photo by {author} on Unsplash",
                'credit_url': author_url,
            }
    return None


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
    # insert after title/date if present
    after = re.search(r"^(title:.*\n)", fm, re.MULTILINE)
    if not after:
        after = re.search(r"^(date:.*\n)", fm, re.MULTILINE)
    if after:
        idx = after.end()
        return fm[:idx] + line + fm[idx:]
    return line + fm


def main():
    if not ACCESS_KEY:
        print("Set UNSPLASH_ACCESS_KEY in environment.")
        return
    used_ids = set()
    if USED_STORE.exists():
        try:
            used_ids = set(json.loads(USED_STORE.read_text(encoding='utf-8')))
        except Exception:
            pass

    changed = 0
    for post in sorted(POSTS.glob('*.md')):
        text = post.read_text(encoding='utf-8')
        fm, body = parse_front_matter(text)
        if not fm:
            continue
        # Skip if has proper credit
        has_credit = re.search(r"^image_credit_text:\s*\"Photo by .* on Unsplash\"$", fm, re.MULTILINE)
        if has_credit:
            continue
        # Use title and categories for query
        title_m = re.search(r"^title:\s*\"(.+?)\"$", fm, re.MULTILINE)
        title = title_m.group(1) if title_m else ''
        cats_m = re.search(r"^categories:\s*\[(.*?)\]$", fm, re.MULTILINE)
        cat = ''
        if cats_m:
            parts = [p.strip().strip('"\'') for p in cats_m.group(1).split(',') if p.strip()]
            if parts:
                cat = parts[-1]
        queries = []
        if 'book' in title.lower():
            queries.append(title)
            queries.append(f"{title.split(':')[0]} book")
        queries.append(cat.replace('-', ' '))
        queries.append(title)
        queries.append('ux design')
        # Try queries
        photo = None
        for q in queries:
            q = q.strip()
            if not q:
                continue
            try:
                photo = search_photo(q, used_ids)
            except Exception:
                photo = None
            if photo:
                break
        if not photo:
            continue
        used_ids.add(photo['id'])
        # Update front matter
        fm2 = fm
        fm2 = replace_or_insert(fm2, 'image', photo['image'])
        fm2 = replace_or_insert(fm2, 'image_alt', photo['alt'])
        fm2 = replace_or_insert(fm2, 'image_credit_text', photo['credit_text'])
        fm2 = replace_or_insert(fm2, 'image_credit_url', photo['credit_url'])
        if fm2 != fm:
            fm_block = fm2.rstrip('\n') + "\n"
            new_text = f"---\n{fm_block}---\n{body}"
            post.write_text(new_text, encoding='utf-8')
            changed += 1
            print('Updated image for:', post.name, '->', photo['credit_text'])

    USED_STORE.parent.mkdir(parents=True, exist_ok=True)
    USED_STORE.write_text(json.dumps(sorted(list(used_ids))), encoding='utf-8')
    print('Total updated:', changed)


if __name__ == '__main__':
    main()
