import sys
import os
import fitz
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')
os.makedirs('figures', exist_ok=True)

# Let's inspect pages and image rects
extracted_figures = []

for pno in range(len(doc)):
    page = doc[pno]
    images = page.get_images(full=True)
    for img_idx, img_info in enumerate(images):
        xref = img_info[0]
        base_img = doc.extract_image(xref)
        # Skip IISc header logo (235x166 or similar on every page)
        if base_img['width'] == 235 and base_img['height'] == 166:
            continue
        
        # Get image rect on page
        rects = page.get_image_rects(xref)
        print(f"Page {pno+1}: XRef {xref}, Ext {base_img['ext']}, Size ({base_img['width']}x{base_img['height']}), Rects: {rects}")
