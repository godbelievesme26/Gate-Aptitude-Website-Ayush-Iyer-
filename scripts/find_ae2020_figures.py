import fitz

doc = fitz.open("internal/ae/AE2020.pdf")

print("--- Inspecting large images / diagrams across all pages ---")
for page_idx in range(15):
    page = doc[page_idx]
    for img_info in page.get_image_info(xrefs=True):
        w, h = img_info['width'], img_info['height']
        bbox = img_info['bbox']
        # If image is larger than single-line text or formulas
        if h > 30 or w > 200:
            print(f"Page {page_idx+1}: xref={img_info['xref']}, size=({w}x{h}), bbox=({bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f})")
