import fitz
import json
import os

os.makedirs('internal/ae/audit_renders', exist_ok=True)

with open('internal/ae/forensic_audit_granular.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)
    
def expand_bbox_safely(bbox, page, margin=20):
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

repaired_count = 0
unverifiable_figures = []

years_to_process = set([q['year'] for q in audit_data['questions'] if q['components']['figure'] == 'FAIL'])

for y in years_to_process:
    json_path = f'data/ae/{y}.json'
    if not os.path.exists(json_path):
        continue
        
    doc = fitz.open(f'internal/ae/AE{y}.pdf')
    with open(json_path, 'r', encoding='utf-8') as f:
        year_data = json.load(f)
        
    changed = False
    for q in year_data.get('questions', []):
        audit_record = next((aq for aq in audit_data['questions'] if aq['id'] == q['id']), None)
        if not audit_record or audit_record['components']['figure'] != 'FAIL':
            continue
            
        for c in q.get('content', []) + q.get('figures', []):
            if c.get('type') == 'figure' or 'src' in c:
                asset = c.get('asset', c)
                src = asset.get('source', {})
                if 'bbox' in src:
                    old_bbox = src['bbox']
                    page_idx = src['page'] - 1
                    page = doc[page_idx]
                    
                    new_bbox = expand_bbox_safely(old_bbox, page, margin=20)
                    src['bbox'] = new_bbox
                    
                    rect = fitz.Rect(new_bbox)
                    pix = page.get_pixmap(clip=rect, dpi=150)
                    img_path = asset.get('src')
                    if img_path and os.path.exists(img_path):
                        pix.save(img_path)
                        src['pixelCrop'] = [0, 0, pix.width, pix.height]
                        
                    page.draw_rect(fitz.Rect(old_bbox), color=(0, 0, 1), width=1)
                    page.draw_rect(fitz.Rect(new_bbox), color=(1, 0, 0), width=1.5)
                    q_id = q['id']
                    page.get_pixmap(dpi=150).save(f'internal/ae/audit_renders/{q_id}_audit_safe.png')
                    changed = True
                    repaired_count += 1
                else:
                    unverifiable_figures.append(q['id'])
                    
    if changed:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(year_data, f, indent=2, ensure_ascii=False)

print('Repaired figure count:', repaired_count)
print('Unverifiable figure count:', len(unverifiable_figures))
with open('internal/ae/missing_bboxes.json', 'w', encoding='utf-8') as f:
    json.dump(unverifiable_figures, f, indent=2)
