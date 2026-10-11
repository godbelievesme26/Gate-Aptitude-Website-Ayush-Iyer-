import fitz

doc = fitz.open("internal/ae/AE2020.pdf")

pages_to_check = [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14]

for p in pages_to_check:
    page = doc[p - 1]
    print(f"=== Page {p} Images ===")
    for img in page.get_image_info(xrefs=True):
        bbox = img['bbox']
        print(f"  xref={img['xref']}, size=({img['width']}x{img['height']}), bbox=({bbox[0]:.2f}, {bbox[1]:.2f}, {bbox[2]:.2f}, {bbox[3]:.2f})")
