import fitz

doc = fitz.open("internal/ae/AE2020.pdf")

for page_idx in range(min(5, len(doc))):
    page = doc[page_idx]
    print(f"=== Page {page_idx+1} ===")
    img_list = page.get_images()
    print(f"Total images: {len(img_list)}")
    for img_info in page.get_image_info(xrefs=True):
        print(f"  bbox: ({img_info['bbox'][0]:.1f}, {img_info['bbox'][1]:.1f}, {img_info['bbox'][2]:.1f}, {img_info['bbox'][3]:.1f}), xref={img_info['xref']}, width={img_info['width']}, height={img_info['height']}")
