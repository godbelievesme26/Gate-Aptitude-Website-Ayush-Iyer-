import fitz
import os
from PIL import Image
import io

os.makedirs('tmp/ae2015_extracted_imgs', exist_ok=True)
doc = fitz.open('internal/ae/AE2015.pdf')

seen_xrefs = set()
for pno in range(len(doc)):
    page = doc[pno]
    for img_info in page.get_images():
        xref = img_info[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        base = doc.extract_image(xref)
        w, h, ext = base['width'], base['height'], base['ext']
        if h > 40: # skip small radio icons
            im = Image.open(io.BytesIO(base['image']))
            im.save(f'tmp/ae2015_extracted_imgs/xref_{xref}_p{pno+1}_{w}x{h}.png')
            print(f"Page {pno+1:02d}: xref={xref:3d} | size=({w}x{h}) -> tmp/ae2015_extracted_imgs/xref_{xref}_p{pno+1}_{w}x{h}.png")
