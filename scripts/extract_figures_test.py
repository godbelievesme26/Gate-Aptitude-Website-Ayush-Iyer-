import pymupdf
import os
from PIL import Image

doc = pymupdf.open('internal/ae/AE2025.pdf')
os.makedirs('tmp/ae2025_figures', exist_ok=True)

extracted = []
for pno in range(len(doc)):
    page = doc[pno]
    imgs = page.get_images()
    for img in imgs:
        xref = img[0]
        base_img = doc.extract_image(xref)
        if base_img['width'] != 1252 and base_img['width'] != 166:
            filename = f"tmp/ae2025_figures/p{pno+1:02d}_xref{xref}.{base_img['ext']}"
            with open(filename, 'wb') as f:
                f.write(base_img['image'])
            extracted.append({
                'page': pno + 1,
                'xref': xref,
                'file': filename,
                'width': base_img['width'],
                'height': base_img['height']
            })

print(f"Extracted {len(extracted)} images:")
for e in extracted:
    print(f"  Page {e['page']:02d}, xref {e['xref']}: {e['file']} ({e['width']}x{e['height']})")
