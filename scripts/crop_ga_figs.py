import pymupdf
from PIL import Image, ImageChops

doc = pymupdf.open('internal/ae/AE2023.pdf')

# Page 2 (Q3) - crop rect: [160, 115, 410, 245]
page2 = doc[1]
rect2 = pymupdf.Rect(160, 115, 410, 245)
pix2 = page2.get_pixmap(clip=rect2, dpi=300)
pix2.save('scratch/q03_fig.png')

# Page 4 (Q5) - crop rect: [170, 185, 400, 415]
page4 = doc[3]
rect4 = pymupdf.Rect(170, 185, 400, 415)
pix4 = page4.get_pixmap(clip=rect4, dpi=300)
pix4.save('scratch/q05_fig.png')

print("Cropped Q3 and Q5 figures to scratch/.")
