#!/usr/bin/env python3
"""
Create .webp versions for post images in assets/images/posts.
Skips files that already have a .webp sibling.
Requires Pillow (PIL). If not installed or WEBP unsupported, exits gracefully.
"""

from pathlib import Path
import sys

try:
    from PIL import Image
except Exception:
    print("Pillow not available; skipping WebP conversion.")
    sys.exit(0)

root = Path('assets/images/posts')
created = 0
updated = 0
for p in root.rglob('*'):
    if not p.is_file():
        continue
    if p.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
        continue
    webp = p.with_suffix('.webp')
    src_mtime = p.stat().st_mtime
    dst_mtime = webp.stat().st_mtime if webp.exists() else 0
    # Regenerate if missing or source is newer than existing webp
    if (not webp.exists()) or (src_mtime > dst_mtime + 1):
        try:
            im = Image.open(p)
            im.save(webp, 'WEBP', quality=85, method=6)
            if dst_mtime == 0:
                print('Created', webp)
                created += 1
            else:
                print('Updated', webp)
                updated += 1
        except Exception as e:
            print('Failed', p, e)
print('Total webp created:', created, 'updated:', updated)
