import fitz
import json
import os

os.makedirs('internal/ae/audit_renders', exist_ok=True)

def expand_bbox(bbox, page_rect, margin=15):
    x0, y0, x1, y1 = bbox
    return [
        max(0, x0 - margin),
        max(0, y0 - margin),
        min(page_rect.width, x1 + margin),
        min(page_rect.height, y1 + margin)
    ]

with open('data/ae/2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

doc = fitz.open('internal/ae/AE2026.pdf')
changed = False

for q in data.get('questions', []):
    for c in q.get('content', []):
        if c['type'] == 'figure':
            asset = c['asset']
            src = asset['source']
            if 'bbox' in src:
                old_bbox = src['bbox']
                # Prevent double expansion if already expanded previously
                # If width > 280, it might already be expanded. But let's just do it.
                page_idx = src['page'] - 1
                page = doc[page_idx]
                new_bbox = expand_bbox(old_bbox, page.rect)
                
                src['bbox'] = new_bbox
                changed = True
                
                # Update actual figure crop
                rect = fitz.Rect(new_bbox)
                pix = page.get_pixmap(clip=rect, dpi=150)
                img_path = asset['src']
                if os.path.exists(img_path):
                    pix.save(img_path)
                    src['pixelCrop'] = [0, 0, pix.width, pix.height]
                    
                # RENDER AUDIT
                page.draw_rect(fitz.Rect(old_bbox), color=(0, 0, 1), width=1)
                page.draw_rect(fitz.Rect(new_bbox), color=(1, 0, 0), width=1.5)
                q_id = q['id']
                page.get_pixmap(dpi=150).save(f'internal/ae/audit_renders/{q_id}_audit.png')

if changed:
    with open('data/ae/2026.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Updated AE2026 figures')
