#!/usr/bin/env python3
"""Backfill locally cached Unsplash images for posts using source.unsplash.com fallbacks."""

import os
from datetime import datetime
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"

import sys
sys.path.append(str(ROOT / 'scripts'))
import daily_article_generator as dag


def load_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            continue
        parts = text.split('\n---\n', 1)
        if len(parts) != 2:
            continue
        fm = parts[0][4:]
        body = parts[1]
        data = yaml.safe_load(fm) or {}
        data['__path'] = path
        data['__body'] = body
        posts.append(data)
    return posts


def format_front_matter(data: dict) -> str:
    clean = {k: v for k, v in data.items() if not k.startswith('__')}
    return yaml.safe_dump(clean, sort_keys=False).strip() + '\n'


def backfill():
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key:
        print('UNSPLASH_ACCESS_KEY missing. Aborting.')
        return
    updated = 0
    skipped = 0
    for meta in load_posts():
        img = meta.get('image')
        if not img or 'source.unsplash.com' not in img:
            continue
        title = meta.get('title') or ''
        categories = meta.get('categories') or []
        topic = ''
        if categories:
            topic = categories[-1].replace('-', ' ')
        if not topic:
            topic = title
        topic = topic or 'ux design'
        try:
            image_url, alt, credit_text, credit_url = dag.fetch_unsplash_image(topic)
        except Exception as exc:
            skipped += 1
            print(f"Failed to fetch for {meta['__path'].name}: {exc}")
            continue
        if not image_url:
            skipped += 1
            print(f"No image for {meta['__path'].name}")
            continue
        # Determine post date for caching path
        date_str = meta.get('date')
        slug = meta['__path'].name.replace('.md', '').split('-', 3)[-1]
        try:
            if date_str:
                dt = datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d')
            else:
                raise ValueError
        except Exception:
            dt = datetime.today()
        # Use the generator helper to cache locally
        now = datetime(dt.year, dt.month, dt.day)
        local_path = dag.cache_image_locally(image_url, now, slug)
        meta['image'] = local_path or image_url
        meta['image_alt'] = alt
        meta['image_credit_text'] = credit_text
        meta['image_credit_url'] = credit_url
        fm_text = format_front_matter(meta)
        new_content = f"---\n{fm_text}---\n{meta['__body']}"
        meta['__path'].write_text(new_content, encoding='utf-8')
        updated += 1
        print(f"Updated {meta['__path'].name} -> {meta['image']}")
    print(f"Updated posts: {updated}; skipped: {skipped}")


if __name__ == '__main__':
    backfill()
