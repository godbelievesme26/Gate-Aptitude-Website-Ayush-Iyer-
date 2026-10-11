import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')

print("--- Inspecting Images per Page ---")
for pno in range(len(doc)):
    page = doc[pno]
    images = page.get_images(full=True)
    drawings = page.get_drawings()
    if len(images) > 0 or len(drawings) > 0:
        print(f"Page {pno+1}: {len(images)} raster images, {len(drawings)} vector drawings")
        for img_info in images:
            xref = img_info[0]
            base_img = doc.extract_image(xref)
            print(f"   XRef {xref}: ext={base_img['ext']}, size=({base_img['width']}x{base_img['height']}), bpc={base_img['bpc']}")
