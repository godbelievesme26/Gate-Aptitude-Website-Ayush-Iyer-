import pymupdf
import json
import re

doc = pymupdf.open('internal/ae/AE2023.pdf')
print(f"Total pages: {len(doc)}")

pages_data = []

for page_idx, page in enumerate(doc):
    pno = page_idx + 1
    text = page.get_text('text')
    
    # Candidate images (excluding header logo xref 2909 and tiny 2x2 placeholder images)
    raw_imgs = page.get_images()
    valid_imgs = []
    for im in raw_imgs:
        xref = im[0]
        w, h = im[2], im[3]
        if w > 10 and h > 10 and (w != 274 and h != 97): # skip logo
            rects = page.get_image_rects(xref)
            valid_imgs.append({
                'xref': xref,
                'width': w,
                'height': h,
                'rects': [[round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2)] for r in rects]
            })
            
    pages_data.append({
        'page': pno,
        'text': text,
        'images': valid_imgs
    })

with open('internal/ae/AE2023-pages.json', 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print("Saved internal/ae/AE2023-pages.json")
