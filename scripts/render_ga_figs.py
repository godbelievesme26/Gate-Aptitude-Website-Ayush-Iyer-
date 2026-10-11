import pymupdf
from PIL import Image

doc = pymupdf.open('internal/ae/AE2023.pdf')

# Page 2 (Q3)
page2 = doc[1] # 0-indexed page 2
# Let's render page 2 at 300 DPI
pix2 = page2.get_pixmap(dpi=300)
pix2.save('scratch/page_02_300dpi.png')

# Page 4 (Q5)
page4 = doc[3] # 0-indexed page 4
pix4 = page4.get_pixmap(dpi=300)
pix4.save('scratch/page_04_300dpi.png')

print("Page 2 and 4 rendered at 300 DPI.")
