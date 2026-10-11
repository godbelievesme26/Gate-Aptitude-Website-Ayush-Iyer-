import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('internal/ae/AE2022.pdf')

print("Total pages in AE2022.pdf:", len(doc))

for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    qlines = [l.strip() for l in txt.split('\n') if l.strip().startswith('Q.')]
    imgs = page.get_images()
    # Filter header image
    content_imgs = [img for img in imgs if img[0] not in (14, 2909, 1)]
    drawings = [d for d in page.get_drawings() if d['rect'].y0 > 70 and d['rect'].y1 < 750 and (d['rect'].width > 15 or d['rect'].height > 15)]
    
    if content_imgs or drawings or any(k in txt.lower() for k in ['figure', 'shown', 'schematic']):
        print(f"=== Page {pno+1} === (Qs: {qlines})")
        print(f"  Content Imgs: {len(content_imgs)}, Drawings: {len(drawings)}")
        for img in content_imgs:
            xref = img[0]
            print(f"    Img XRef {xref}: {page.get_image_rects(xref)}")
        blocks = page.get_text('blocks')
        for b in blocks:
            t = b[4].strip().replace('\n', ' ')
            if len(t) > 60: t = t[:60] + '...'
            print(f"    Text ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}) -> {t}")
