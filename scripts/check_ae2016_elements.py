import fitz

doc = fitz.open("internal/ae/AE2016.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    drawings = page.get_drawings()
    images = page.get_images()
    print(f"Page {page_num+1}: {len(drawings)} vector drawings, {len(images)} raster images")
