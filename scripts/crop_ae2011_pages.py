import fitz, os

doc = fitz.open('internal/ae/AE2011.pdf')
os.makedirs('tmp/ae2011_crops', exist_ok=True)
os.makedirs('figures', exist_ok=True)

# Let's inspect each page's blocks and draw bounding boxes / extract crops
for pno, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    pix.save(f'tmp/ae2011_crops/page_{pno+1:02d}.png')

print("Saved all pages as PNG.")
