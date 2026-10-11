import fitz
import json
import os

with open('internal/ae/missing_bboxes.json', 'r', encoding='utf-8') as f:
    missing = json.load(f)

# Group by year
years = {}
for q_id in missing:
    y = int(q_id.split('-')[1])
    if y not in years:
        years[y] = []
    years[y].append(q_id)

repaired_count = 0

for y in years:
    json_path = f'data/ae/{y}.json'
    doc = fitz.open(f'internal/ae/AE{y}.pdf')
    with open(json_path, 'r', encoding='utf-8') as f:
        year_data = json.load(f)
        
    changed = False
    for q in year_data.get('questions', []):
        if q['id'] not in years[y]:
            continue
            
        for c in q.get('content', []) + q.get('figures', []):
            if c.get('type') == 'figure' or 'src' in c:
                asset = c.get('asset', c)
                src = asset.get('source', {})
                if 'page' not in src:
                    continue
                page_idx = src['page'] - 1
                page = doc[page_idx]
                
                # Attempt independent localization
                images = page.get_images()
                if len(images) == 1:
                    # Exactly one raster image
                    img = images[0]
                    rects = page.get_image_rects(img[0])
                    if len(rects) == 1:
                        src['bbox'] = [rects[0].x0, rects[0].y0, rects[0].x1, rects[0].y1]
                        changed = True
                        repaired_count += 1
                        print(f"Localized {q['id']}")

    if changed:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(year_data, f, indent=2, ensure_ascii=False)

print('Localized count:', repaired_count)
