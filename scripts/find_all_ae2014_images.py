import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

for pno in range(4, 17):
    page = doc[pno]
    images = page.get_images(full=True)
    if images:
        print(f"\n--- Page {pno+1} ---")
        for img in images:
            xref = img[0]
            # find bbox of image on page
            rects = page.get_image_rects(xref)
            print(f"Image xref {xref}: rects={rects}")
            # print surrounding text near rect
            for r in rects:
                # get text above and below rect
                area = fitz.Rect(50, max(0, r.y0 - 50), 550, min(page.rect.height, r.y1 + 50))
                print(f"  Surrounding text: {page.get_text('text', clip=area)[:150].replace('\n', ' ')}")
