import fitz
import json

doc = fitz.open("internal/ae/AE2020.pdf")

with open("tmp/ae2020_detail.txt", "w", encoding="utf-8") as out:
    for page_idx in range(15):
        page = doc[page_idx]
        out.write(f"============================== PAGE {page_idx+1} ==============================\n")
        
        # Check images on page
        images = page.get_images()
        out.write(f"Images on page: {len(images)}\n")
        for img_idx, img in enumerate(images):
            xref = img[0]
            base_img = doc.extract_image(xref)
            out.write(f"  Img {img_idx}: xref={xref}, ext={base_img['ext']}, w={base_img['width']}, h={base_img['height']}\n")
        
        # Check drawings / vector graphics
        drawings = page.get_drawings()
        out.write(f"Drawings on page: {len(drawings)}\n")
        
        # Print text blocks with bounding boxes
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if text:
                out.write(f"  Block ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}):\n")
                for line in text.split('\n'):
                    out.write(f"    {line}\n")

print("Wrote tmp/ae2020_detail.txt successfully.")
