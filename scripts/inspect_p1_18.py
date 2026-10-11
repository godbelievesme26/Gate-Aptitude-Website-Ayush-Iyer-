import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    if p['page'] <= 18:
        if p['images']:
            print(f"\n{'='*60}\nPage {p['page']}: {len(p['images'])} images")
            for img in p['images']:
                print(f"  xref {img['xref']}: {img['width']}x{img['height']} {img['ext']}")
            print("Text snippet:")
            print(p['text'].strip())
