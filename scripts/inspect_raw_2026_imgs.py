import pypdf
from PIL import Image

reader = pypdf.PdfReader('internal/ae/AE2026.pdf')

pages_to_check = [10, 11, 15, 17, 19, 21, 22, 26, 28, 30, 33, 34, 37, 38, 39]

for pno in pages_to_check:
    page = reader.pages[pno - 1]
    for im in page.images:
        if im.name.startswith('Im1.'):
            raw_im = im.image
            print(f"Page {pno}: raw embedded size {raw_im.size}, mode {raw_im.mode}")
