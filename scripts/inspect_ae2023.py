import pymupdf
import json
import re

doc = pymupdf.open('internal/ae/AE2023.pdf')
print(f'Total pages: {len(doc)}')

questions_by_page = []
images_by_page = []

for page_idx, page in enumerate(doc):
    pno = page_idx + 1
    text = page.get_text('text')
    # Find question numbers
    q_matches = list(re.finditer(r'(?:^|\n)Q\.(\d+)\s+', text))
    q_nums = [int(m.group(1)) for m in q_matches]
    
    # Images on page
    imgs = [im for im in page.get_images() if im[2] not in [1252, 166]] # ignore common headers/logos if any
    
    print(f'Page {pno:02d}: Qs: {q_nums} | Images: {len(page.get_images())} (Candidate: {len(imgs)})')
    if imgs:
        for im in imgs:
            rects = page.get_image_rects(im[0])
            print(f'   -> Image xref {im[0]}: size {im[2]}x{im[3]}, rects: {rects}')

