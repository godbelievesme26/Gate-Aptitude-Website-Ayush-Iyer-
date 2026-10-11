import pymupdf
import json

doc = pymupdf.open('internal/ae/AE2025.pdf')

for pno in [14, 15, 19, 20, 21, 29, 30, 31, 32, 33]: # 1-based page numbers
    page = doc[pno - 1]
    print(f"\n{'='*60}\nPage {pno} Image placements:")
    for img_info in page.get_images():
        xref = img_info[0]
        if img_info[2] != 1252 and img_info[2] != 166:
            rects = page.get_image_rects(xref)
            print(f"  xref {xref} ({img_info[2]}x{img_info[3]}): rects -> {rects}")
