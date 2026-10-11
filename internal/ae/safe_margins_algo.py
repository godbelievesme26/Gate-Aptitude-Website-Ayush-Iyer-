import fitz
import json
import os

os.makedirs('internal/ae/audit_renders', exist_ok=True)

def expand_bbox_safely(bbox, page, margin=15):
    text_blocks = page.get_text('blocks')
    x0, y0, x1, y1 = bbox
    
    new_x0 = max(0, x0 - margin)
    new_y0 = max(0, y0 - margin)
    new_x1 = min(page.rect.width, x1 + margin)
    new_y1 = min(page.rect.height, y1 + margin)
    
    for b in text_blocks:
        bx0, by0, bx1, by1 = b[:4]
        text = b[4].strip()
        if not text:
            continue
            
        if by1 <= y0 + 1:
            if by1 > new_y0 and bx1 > new_x0 and bx0 < new_x1:
                new_y0 = by1 + 1
        if by0 >= y1 - 1:
            if by0 < new_y1 and bx1 > new_x0 and bx0 < new_x1:
                new_y1 = by0 - 1
        if bx1 <= x0 + 1:
            if bx1 > new_x0 and by1 > new_y0 and by0 < new_y1:
                new_x0 = bx1 + 1
        if bx0 >= x1 - 1:
            if bx0 < new_x1 and by1 > new_y0 and by0 < new_y1:
                new_x1 = bx0 - 1

    return [new_x0, new_y0, new_x1, new_y1]

with open('data/ae/2026.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

doc = fitz.open('internal/ae/AE2026.pdf')

for q in data.get('questions', []):
    if q['id'] == 'gate-2026-ae-ae-11':
        for c in q.get('content', []):
            if c['type'] == 'figure':
                asset = c['asset']
                src = asset['source']
                if 'bbox' in src:
                    old_bbox = src['bbox']
                    page_idx = src['page'] - 1
                    page = doc[page_idx]
                    
                    new_bbox = expand_bbox_safely(old_bbox, page, margin=20)
                    src['bbox'] = new_bbox
                    
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
                    page.get_pixmap(dpi=150).save(f'internal/ae/audit_renders/{q_id}_audit_safe.png')

with open('data/ae/2026.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Applied safe margin to Q11')
