import pymupdf
import json
import re

doc = pymupdf.open('internal/ae/AE2025.pdf')

for pno in range(9, len(doc)): # Page 10 to 34 (0-indexed 9 to 33)
    page = doc[pno]
    text = page.get_text()
    imgs = page.get_images()
    print(f"\n{'='*50}\n--- PAGE {pno+1} --- (Images: {len(imgs)})")
    for img in imgs:
        xref = img[0]
        base_img = doc.extract_image(xref)
        if base_img['width'] > 200 and base_img['width'] != 1252:
            print(f"  [Embedded Image] xref: {xref}, size: {base_img['width']}x{base_img['height']}")
    print(text.strip())
