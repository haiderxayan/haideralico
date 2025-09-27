#!/usr/bin/env python3
"""
Migrate Jekyll posts to SEO-friendly category slugs and add redirects.

What it does (by default):
- Normalizes categories to hyphenated, lowercase slugs (e.g., "UX Design" -> "ux-design").
- Computes the previous URL and adds a `redirect_from` entry so old links 301 to the new path.

Optional (not enabled unless arguments are passed):
- Spread post dates across a window to avoid bunching (adds redirects for old dates as well).

Usage:
  python scripts/migrate_posts.py --dry-run
  python scripts/migrate_posts.py --apply

Optional flags:
  --spread-dates --months 12 --start "2024-01-01" --end "2024-12-31"

Notes:
- Requires no external dependencies; parses simple YAML front matter heuristically.
- Only updates posts with a detected change.
"""

from __future__ import annotations

import re
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"


def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    for ch in [" ", "_", "/", "\\", ":", ";", ",", ".", "|", "(", ")", "[", "]", "{" ,"}"]:
        text = text.replace(ch, "-")
    while "--" in text:
        text = text.replace("--", "-")
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    return "".join(c for c in text if c in allowed).strip("-")


def parse_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, text
    fm_text = parts[0][4:]
    body = parts[1]
    return fm_text, body


def extract_key_list(fm_text: str, key: str):
    # Supports one-line array: key: [a, b] or key: ["A", "B"]
    m = re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm_text, re.MULTILINE)
    if m:
        items = [i.strip().strip('"\'') for i in m.group(1).split(',') if i.strip()]
        return items
    # Supports multi-line simple list:
    block = re.search(rf"^{key}:\s*\n((?:\s*-\s*.*\n)+)", fm_text, re.MULTILINE)
    if block:
        lines = block.group(1).splitlines()
        items = []
        for ln in lines:
            m2 = re.match(r"\s*-\s*(.*?)\s*$", ln)
            if m2:
                items.append(m2.group(1).strip().strip('"\''))
        return items
    return None


def replace_key_list(fm_text: str, key: str, items: list[str]):
    new_line = f'{key}: ["' + '", "'.join(items) + '"]\n'
    if re.search(rf"^{key}:\s*\[(.*?)\]\s*$", fm_text, re.MULTILINE):
        return re.sub(rf"^{key}:\s*\[(.*?)\]\s*$", new_line, fm_text, flags=re.MULTILINE)
    elif re.search(rf"^{key}:\s*\n((?:\s*-\s*.*\n)+)", fm_text, re.MULTILINE):
        # Replace whole block
        return re.sub(rf"^{key}:\s*\n((?:\s*-\s*.*\n)+)", new_line, fm_text, flags=re.MULTILINE)
    else:
        # Insert after title/date if possible, else at top
        anchor = re.search(r"^(title:.*\n)", fm_text, re.MULTILINE)
        if not anchor:
            anchor = re.search(r"^(date:.*\n)", fm_text, re.MULTILINE)
        if anchor:
            idx = anchor.end()
            return fm_text[:idx] + new_line + fm_text[idx:]
        return new_line + fm_text


def extract_scalar(fm_text: str, key: str):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", fm_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def add_redirect_from(fm_text: str, path: str):
    # Ensure path starts with '/'
    if not path.startswith('/'):
        path = '/' + path
    # If redirect_from already exists, append if missing
    block = re.search(r"^redirect_from:\s*\n((?:\s*-\s*.*\n)+)", fm_text, re.MULTILINE)
    if block:
        lines = block.group(1).splitlines()
        existing = set()
        for ln in lines:
            m2 = re.match(r"\s*-\s*(.*?)\s*$", ln)
            if m2:
                existing.add(m2.group(1).strip())
        if path in existing:
            return fm_text
        # Append new line at end of block
        insert_pos = block.end()
        return fm_text[:insert_pos] + f"  - {path}\n" + fm_text[insert_pos:]
    # Or one-line array form
    m = re.search(r"^redirect_from:\s*\[(.*?)\]\s*$", fm_text, re.MULTILINE)
    if m:
        items = [i.strip() for i in m.group(1).split(',') if i.strip()]
        if path in items:
            return fm_text
        inner = m.group(1) + (", " if m.group(1).strip() else "") + path
        return re.sub(r"^redirect_from:\s*\[(.*?)\]\s*$", f"redirect_from: [{inner}]", fm_text, flags=re.MULTILINE)
    # Else create new block after categories if possible
    anchor = re.search(r"^(categories:.*\n)", fm_text, re.MULTILINE)
    new_block = f"redirect_from:\n  - {path}\n"
    if anchor:
        idx = anchor.end()
        return fm_text[:idx] + new_block + fm_text[idx:]
    # Else append at end of front matter
    return fm_text + ("\n" if not fm_text.endswith("\n") else "") + new_block


def compute_url(categories: list[str], date_str: str, filename: str):
    # categories segments
    segs = [s for s in categories if s]
    # Attempt to parse date
    y = m = d = None
    try:
        dt = datetime.fromisoformat(date_str.split('#')[0].strip().split()[0])
        y = dt.strftime('%Y')
        m = dt.strftime('%m')
        d = dt.strftime('%d')
    except Exception:
        # fallback: take from filename prefix
        parts = filename.split('-', 3)
        if len(parts) >= 3:
            y, m, d = parts[0], parts[1], parts[2]
    slug = filename.split('-', 3)[-1].rsplit('.', 1)[0]
    cat_path = '/'.join(segs)
    return f"/{cat_path}/{y}/{m}/{d}/{slug}/"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='Do not write changes')
    ap.add_argument('--apply', action='store_true', help='Write changes')
    ap.add_argument('--spread-dates', action='store_true', help='Evenly spread dates across a range for a given year')
    ap.add_argument('--year', type=int, default=2024, help='Year to redistribute (default: 2024)')
    ap.add_argument('--start', type=str, default=None, help='Start date YYYY-MM-DD (defaults to Jan 1 of year)')
    ap.add_argument('--end', type=str, default=None, help='End date YYYY-MM-DD (defaults to Dec 31 of year)')
    args = ap.parse_args()

    if not args.apply and not args.dry_run:
        args.dry_run = True

    changed = 0
    # First pass: category normalization and redirect_from for category path
    posts = sorted(POSTS.glob('*.md'))
    for post in posts:
        text = post.read_text(encoding='utf-8')
        fm_text, body = parse_front_matter(text)
        if fm_text is None:
            continue

        orig_fm = fm_text
        title = extract_scalar(fm_text, 'title') or ''
        date = extract_scalar(fm_text, 'date') or ''
        categories = extract_key_list(fm_text, 'categories') or []

        # Compute old URL based on current categories (lowercase, not slugified to mimic existing output)
        old_cats_for_url = [('/'.join(c.split('/'))).lower() for c in categories]
        old_url = compute_url(old_cats_for_url, date, post.name)
        # Encode spaces for redirect path
        old_url_encoded = '/'.join(quote(seg, safe='') for seg in old_url.split('/'))

        # Normalize categories to SEO slugs
        new_categories = [slugify(c) for c in categories]

        if new_categories != categories:
            fm_text = replace_key_list(fm_text, 'categories', new_categories)
            # Build new URL
            new_url = compute_url(new_categories, date, post.name)
            if old_url != new_url:
                fm_text = add_redirect_from(fm_text, old_url_encoded)

        # Optional: date spreading (disabled by default)
        # Left as a future extension; we only handle categories now.

        if fm_text != orig_fm:
            changed += 1
            # Ensure a newline before closing front matter marker
            fm_block = fm_text.rstrip('\n') + "\n"
            new_text = f"---\n{fm_block}---\n{body}"
            if args.apply:
                post.write_text(new_text, encoding='utf-8')
                print(f"UPDATED: {post}")
            else:
                print(f"WOULD UPDATE: {post}")

    # Optional: spread dates across a range for a given year
    if args.spread_dates:
        # Collect posts in target year (based on current front matter date or filename)
        targets = []
        for post in posts:
            text = post.read_text(encoding='utf-8')
            fm_text, body = parse_front_matter(text)
            if fm_text is None:
                continue
            date = extract_scalar(fm_text, 'date')
            dt = None
            if date:
                try:
                    dt = datetime.fromisoformat(date.split('#')[0].strip())
                except Exception:
                    dt = None
            if dt is None:
                # fallback from filename
                parts = post.name.split('-', 3)
                if len(parts) >= 3:
                    try:
                        dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                    except Exception:
                        pass
            if dt and dt.year == args.year:
                targets.append((post, fm_text, body, dt))

        if targets:
            targets.sort(key=lambda x: (x[3], x[0].name))
            # Date window
            if args.start:
                start_dt = datetime.fromisoformat(args.start)
            else:
                start_dt = datetime(args.year, 1, 1)
            if args.end:
                end_dt = datetime.fromisoformat(args.end)
            else:
                end_dt = datetime(args.year, 12, 31)
            if end_dt <= start_dt:
                end_dt = datetime(args.year, 12, 31)
            span_days = (end_dt - start_dt).days
            n = len(targets)
            # Avoid division by zero
            step = span_days // max(1, n)
            # Use mid-day UTC for consistency
            base_time = "12:00:00 +0000"

            for i, (post, fm_text, body, old_dt) in enumerate(targets):
                # Compute new date
                new_dt = start_dt + timedelta(days=min(span_days, i * step))
                new_date_str = new_dt.strftime(f"%Y-%m-%d {base_time}")

                # Compute URL before change (using normalized categories after previous pass)
                categories = extract_key_list(fm_text, 'categories') or []
                old_url = compute_url(categories, extract_scalar(fm_text, 'date') or old_dt.isoformat(), post.name)
                old_url_encoded = '/'.join(quote(seg, safe='') for seg in old_url.split('/'))

                # Replace date in front matter
                if re.search(r"^date:\s*.+$", fm_text, flags=re.MULTILINE):
                    fm_text2 = re.sub(r"^date:\s*.+$", f"date: {new_date_str}", fm_text, flags=re.MULTILINE)
                else:
                    fm_text2 = f"date: {new_date_str}\n" + fm_text

                # Compute new URL path
                new_url = compute_url(categories, new_date_str, post.name)
                if new_url != old_url:
                    fm_text2 = add_redirect_from(fm_text2, old_url_encoded)

                if fm_text2 != fm_text:
                    changed += 1
                    fm_block = fm_text2.rstrip('\n') + "\n"
                    new_text = f"---\n{fm_block}---\n{body}"
                    if args.apply:
                        post.write_text(new_text, encoding='utf-8')
                        print(f"UPDATED DATE: {post} -> {new_date_str}")
                    else:
                        print(f"WOULD UPDATE DATE: {post} -> {new_date_str}")

    print(f"\nPosts changed: {changed}")


if __name__ == '__main__':
    main()
