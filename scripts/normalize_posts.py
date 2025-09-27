#!/usr/bin/env python3
"""
Normalize new/edited posts so manual posts follow generator rules:

- Ensure hyphenated primary category slugs; add redirect_from if it changes.
- Enforce AI-every-other-day for posts dated today (UTC):
  * if today is an AI day, primary becomes 'ai'
  * otherwise rotate through the NON_AI_CATEGORIES statefully
- Ensure canonical_url present and correct.
- If image is remote Unsplash, prefer credited backfill (delegated to existing script).
- If image is remote, cache locally and update front matter (delegated to cache script).

This script focuses on metadata normalization; image fetching/caching is handled
by the separate steps in the workflow.
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
STATE = ROOT / "assets" / "data" / "category_cycle.json"

CYCLE_CATEGORIES = [
    "research-strategy",
    "design",
    "ai",
    "data-analytics",
    "content",
    "career",
    "development",
    "news-culture",
]
NON_AI = [c for c in CYCLE_CATEGORIES if c != "ai"]


def slugify(text: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    text = (text or "").strip().lower()
    for ch in [" ", "_", "/", "\\", ":", ";", ",", ".", "|", "(", ")", "[", "]", "{" ,"}"]:
        text = text.replace(ch, "-")
    while "--" in text:
        text = text.replace("--", "-")
    return "".join(c for c in text if c in allowed).strip("-")


def parse_fm(text: str):
    if not text.startswith('---\n'):
        return None, text
    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        return None, text
    return parts[0][4:], parts[1]


def extract_list(fm: str, key: str):
    m = re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm, re.MULTILINE)
    if m:
        return [i.strip().strip('\"\'') for i in m.group(1).split(',') if i.strip()]
    return []


def replace_list(fm: str, key: str, items: list[str]):
    line = f'{key}: ["' + '", "'.join(items) + '"]\n'
    if re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm, re.MULTILINE):
        return re.sub(rf"^{key}:\s*\[(.*?)\]\s*$", line, fm, flags=re.MULTILINE)
    return line + fm

def replace_or_insert_after(fm: str, key: str, value: str, after_key: str):
    line = f"{key}: {value}\n"
    # replace existing
    import re
    if re.search(rf"^{key}:\s*.+$", fm, re.MULTILINE):
        return re.sub(rf"^{key}:\s*.+$", line, fm, flags=re.MULTILINE)
    # insert after anchor key if present
    m = re.search(rf"^{after_key}:.*$", fm, re.MULTILINE)
    if m:
        idx = m.end()
        return fm[:idx] + "\n" + line + fm[idx:]
    # otherwise prepend
    return line + fm


def extract_scalar(fm: str, key: str):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", fm, re.MULTILINE)
    return m.group(1).strip() if m else ''


def add_redirect_from(fm: str, path: str):
    if not path.startswith('/'):
        path = '/' + path
    block = re.search(r"^redirect_from:\s*\n((?:\s*-\s*.*\n)+)", fm, re.MULTILINE)
    if block:
        if path in block.group(1):
            return fm
        insert_pos = block.end()
        return fm[:insert_pos] + f"  - {path}\n" + fm[insert_pos:]
    if re.search(r"^redirect_from:\s*\[(.*?)\]\s*$", fm, re.MULTILINE):
        return re.sub(r"^redirect_from:\s*\[(.*?)\]\s*$", lambda m: f"redirect_from: [{m.group(1)}{', ' if m.group(1).strip() else ''}{path}]", fm, flags=re.MULTILINE)
    return fm + ("\n" if not fm.endswith("\n") else "") + f"redirect_from:\n  - {path}\n"


def compute_url(categories: list[str], date_str: str, filename: str, site_url: str):
    segs = [s for s in categories if s]
    try:
        dt = datetime.fromisoformat(date_str.split()[0])
    except Exception:
        y, m, d, *_ = filename.split('-', 3) + ['','','']
        dt = datetime(int(y), int(m), int(d))
    slug = filename.split('-', 3)[-1].rsplit('.', 1)[0]
    return f"{site_url}/{'/'.join(segs)}/{dt.strftime('%Y/%m/%d')}/{slug}/"


def today_ai(now: datetime):
    return (now.toordinal() % 2 == 0)


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {"index": -1, "last_date": "", "last_primary": ""}


def save_state(state: dict):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state))


def next_non_ai(now: datetime):
    st = load_state()
    today = now.strftime('%Y-%m-%d')
    if st.get('last_date') == today and st.get('last_primary') != 'ai':
        return st.get('last_primary')
    idx = (int(st.get('index', -1)) + 1) % len(NON_AI)
    cat = NON_AI[idx]
    st.update({'index': idx, 'last_date': today, 'last_primary': cat})
    save_state(st)
    return cat


def normalize():
    site_url = 'https://haiderali.co'
    now = datetime.now(timezone.utc)
    changed = 0
    for post in sorted(POSTS.glob('*.md')):
        text = post.read_text(encoding='utf-8')
        fm, body = parse_fm(text)
        if not fm:
            continue
        date = extract_scalar(fm, 'date')
        # Ensure last_modified_at exists (default to publish date)
        lastmod = extract_scalar(fm, 'last_modified_at')
        if date and not lastmod:
            fm = replace_or_insert_after(fm, 'last_modified_at', date, 'date')
        # Only enforce AI rule for today's posts
        enforce_ai = False
        try:
            if datetime.fromisoformat(date.split()[0]).date() == now.date():
                enforce_ai = True
        except Exception:
            pass
        cats = extract_list(fm, 'categories')
        if not cats:
            continue
        primary = slugify(cats[0])
        secondary = slugify(cats[1]) if len(cats) > 1 else None

        # Determine desired primary
        desired = primary
        if enforce_ai:
            desired = 'ai' if today_ai(now) else next_non_ai(now)

        # Slugify and ensure known categories
        if primary != desired:
            old_url = compute_url([primary, secondary] if secondary else [primary], date, post.name, site_url)
            cats_new = [desired] + ([secondary] if secondary else [])
            fm = replace_list(fm, 'categories', cats_new)
            fm = add_redirect_from(fm, old_url.replace(site_url, ''))
            changed += 1

        # Ensure canonical_url
        m = re.search(r"^canonical_url:\s*(.+)$", fm, re.MULTILINE)
        cats_final = extract_list(fm, 'categories') or cats
        canonical = compute_url(cats_final, date, post.name, site_url)
        if m:
            fm = re.sub(r"^canonical_url:\s*.+$", f"canonical_url: \"{canonical}\"", fm, flags=re.MULTILINE)
        else:
            fm = f"canonical_url: \"{canonical}\"\n" + fm

        # Write back if changed
        if fm != parse_fm(text)[0]:
            fm_block = fm.rstrip('\n') + "\n"
            new_text = f"---\n{fm_block}---\n{body}"
            post.write_text(new_text, encoding='utf-8')
    print(f"Normalized posts changed: {changed}")


if __name__ == '__main__':
    normalize()
