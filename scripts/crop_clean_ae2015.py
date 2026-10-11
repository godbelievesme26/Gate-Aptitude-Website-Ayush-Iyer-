import fitz
import os
from PIL import Image

os.makedirs('tmp/ae2015_clean_crops', exist_ok=True)
doc = fitz.open('internal/ae/AE2015.pdf')

# Collect question headers
q_headers = []
for pno in range(len(doc)):
    page = doc[pno]
    blocks = page.get_text('blocks')
    for b in blocks:
        text = b[4].strip()
        if text.startswith('Question Number :'):
            parts = text.split('Question Type :')
            q_num = int(parts[0].replace('Question Number :', '').strip())
            q_type = parts[1].strip() if len(parts) > 1 else 'MCQ'
            q_headers.append({
                'num': q_num,
                'type': q_type,
                'pno': pno,
                'y0': b[1]
            })

q_headers.sort(key=lambda x: x['num'])

for idx in range(len(q_headers)):
    q = q_headers[idx]
    q_num = q['num']
    pno = q['pno']
    y0 = q['y0']
    
    next_q = q_headers[idx + 1] if idx + 1 < len(q_headers) else None
    
    # Collect pixmaps for the slices of this question
    slices = []
    if next_q is None or next_q['pno'] == pno:
        end_y = next_q['y0'] if next_q else doc[pno].rect.height
        page = doc[pno]
        rect = fitz.Rect(0, max(0, y0 - 4), page.rect.width, min(page.rect.height, end_y))
        pix = page.get_pixmap(dpi=200, clip=rect)
        slices.append(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
    else:
        # Page pno from y0 to bottom
        p1 = doc[pno]
        r1 = fitz.Rect(0, max(0, y0 - 4), p1.rect.width, p1.rect.height)
        pix1 = p1.get_pixmap(dpi=200, clip=r1)
        slices.append(Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples))
        
        # Next page up to next_q['y0']
        p2 = doc[next_q['pno']]
        r2 = fitz.Rect(0, 0, p2.rect.width, next_q['y0'])
        pix2 = p2.get_pixmap(dpi=200, clip=r2)
        slices.append(Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples))
    
    # Stitch slices vertically
    total_h = sum(im.height for im in slices)
    max_w = max(im.width for im in slices)
    stitched = Image.new("RGB", (max_w, total_h), (255, 255, 255))
    curr_y = 0
    for im in slices:
        stitched.paste(im, (0, curr_y))
        curr_y += im.height
    
    stitched.save(f'tmp/ae2015_clean_crops/q{q_num:02d}.png')

print("All 65 clean question images saved to tmp/ae2015_clean_crops/")
