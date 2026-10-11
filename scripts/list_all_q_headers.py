import pymupdf
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    pno = p['page']
    text = p['text']
    imgs = p['images']
    print(f"\n{'='*70}\nPAGE {pno} (Images: {len(imgs)})")
    if imgs:
        for img in imgs:
            print(f"  IMAGE: xref {img['xref']}, {img['width']}x{img['height']}")
    for line in text.splitlines():
        if line.strip().startswith('Q.'):
            print(f"  QUESTION HEADER: {line.strip()}")
