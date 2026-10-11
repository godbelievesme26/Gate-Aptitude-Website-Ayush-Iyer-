import fitz
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2013.pdf")

for pno in range(3, len(doc)): # pages 4 to 19 (0-indexed 3 to 18)
    page = doc[pno]
    print(f"\n======================================")
    print(f"PAGE {pno+1}")
    print(f"======================================")
    images = page.get_images(full=True)
    drawings = page.get_drawings()
    print(f"[{len(images)} images, {len(drawings)} drawings]")
    for img in images:
        xref = img[0]
        rects = page.get_image_rects(xref)
        print(f"  Image xref {xref}: rects={rects}")
    print("--- TEXT ---")
    print(page.get_text())
