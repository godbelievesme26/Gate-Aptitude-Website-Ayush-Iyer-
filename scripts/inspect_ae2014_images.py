import fitz # PyMuPDF
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("internal/ae/AE2014.pdf")

print("Inspecting images and drawings across pages 5 to 17...")

for page_idx in range(4, 17): # 0-indexed: pages 5 to 17
    page = doc[page_idx]
    image_list = page.get_images(full=True)
    drawings = page.get_drawings()
    print(f"\nPage {page_idx+1}: {len(image_list)} raster images, {len(drawings)} drawing paths")
    for img in image_list:
        xref = img[0]
        base_image = doc.extract_image(xref)
        print(f"  Raster image xref {xref}: {base_image['width']}x{base_image['height']}, ext: {base_image['ext']}")

