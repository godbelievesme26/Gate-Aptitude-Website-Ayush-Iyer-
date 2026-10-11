import fitz

doc = fitz.open('internal/ae/AE2017.pdf')
print(f"AE2017.pdf page count: {len(doc)}")

for pno in range(len(doc)):
    page = doc[pno]
    imgs = page.get_images()
    drawings = page.get_drawings()
    if len(imgs) > 0 or len(drawings) > 0:
        print(f"Page {pno+1:02d}: {len(imgs)} raster images, {len(drawings)} drawing paths")
        for img_info in imgs:
            xref = img_info[0]
            base_img = doc.extract_image(xref)
            w = base_img['width']
            h = base_img['height']
            ext = base_img['ext']
            print(f"   Image xref {xref}: size {w}x{h}, ext {ext}")
