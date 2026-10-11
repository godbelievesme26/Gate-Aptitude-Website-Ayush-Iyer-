import fitz

doc = fitz.open('internal/ae/AE2018.pdf')
for pno in range(12):
    page = doc[pno]
    imgs = page.get_images()
    drawings = page.get_drawings()
    print(f'Page {pno+1}: {len(imgs)} raster images, {len(drawings)} drawing paths')
    for img_info in imgs:
        xref = img_info[0]
        base_img = doc.extract_image(xref)
        w = base_img['width']
        h = base_img['height']
        ext = base_img['ext']
        print(f"   Image xref {xref}: size {w}x{h}, ext {ext}")
