import json

with open('internal/ae/AE2023-pages.json', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    if p['images']:
        print(f"Page {p['page']:02d}: {len(p['images'])} images")
        for im in p['images']:
            print(f"   xref: {im['xref']}, size: {im['width']}x{im['height']}, rects: {im['rects']}")
