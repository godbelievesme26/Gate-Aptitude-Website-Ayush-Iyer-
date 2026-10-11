import fitz
import json
import os
import glob

for json_file in glob.glob('data/ae/20*.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'year' not in data:
        data['year'] = int(os.path.basename(json_file)[:4])
    year = data['year']
    pdf_path = f'internal/ae/AE{year}.pdf'
    if not os.path.exists(pdf_path):
        continue
    
    doc = fitz.open(pdf_path)
    changed = False
    
    for q in data.get('questions', []):
        for c in q.get('content', []):
            if c['type'] == 'figure':
                asset = c['asset']
                src = asset['source']
                if 'bbox' in src:
                    bbox = src['bbox']
                    page_idx = src['page'] - 1
                    try:
                        page = doc[page_idx]
                        page_rect = page.rect
                        new_bbox = [
                            max(0, bbox[0] - 12),
                            max(0, bbox[1] - 12),
                            min(page_rect.width, bbox[2] + 12),
                            min(page_rect.height, bbox[3] + 12)
                        ]
                        if abs(new_bbox[0] - bbox[0]) > 1:
                            src['bbox'] = new_bbox
                            changed = True
                            rect = fitz.Rect(new_bbox)
                            pix = page.get_pixmap(clip=rect, dpi=150)
                            img_path = asset['src']
                            if os.path.exists(img_path):
                                pix.save(img_path)
                                src['pixelCrop'] = [0, 0, pix.width, pix.height]
                    except Exception as e:
                        pass
                        
        if 'figures' in q:
            for fig in q['figures']:
                src = fig['source']
                if 'bbox' in src:
                    bbox = src['bbox']
                    page_idx = src['page'] - 1
                    try:
                        page = doc[page_idx]
                        page_rect = page.rect
                        new_bbox = [
                            max(0, bbox[0] - 12),
                            max(0, bbox[1] - 12),
                            min(page_rect.width, bbox[2] + 12),
                            min(page_rect.height, bbox[3] + 12)
                        ]
                        if abs(new_bbox[0] - bbox[0]) > 1:
                            src['bbox'] = new_bbox
                            changed = True
                            rect = fitz.Rect(new_bbox)
                            pix = page.get_pixmap(clip=rect, dpi=150)
                            img_path = fig['src']
                            if os.path.exists(img_path):
                                pix.save(img_path)
                                src['pixelCrop'] = [0, 0, pix.width, pix.height]
                    except Exception as e:
                        pass

    if changed:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'Updated {json_file}')
