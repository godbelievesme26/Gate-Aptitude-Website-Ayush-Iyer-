import pymupdf
from PIL import Image

doc = pymupdf.open('internal/ae/AE2023.pdf')

for pno in [2, 3, 4, 5]:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=150)
    pix.save(f'scratch/page_{pno:02d}.png')
    print(f"Page {pno} text:\n{page.get_text('text')}\n---")
