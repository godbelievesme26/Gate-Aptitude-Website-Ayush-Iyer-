import pymupdf
from PIL import Image, ImageChops

doc = pymupdf.open('internal/ae/AE2023.pdf')

# Q3
page2 = doc[1]
rect2 = pymupdf.Rect(170, 126, 400, 232)
pix2 = page2.get_pixmap(clip=rect2, dpi=300)
im2 = Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples)
bbox2 = ImageChops.difference(im2, Image.new('RGB', im2.size, 'white')).getbbox()
if bbox2:
    # pad slightly
    bbox2 = (max(0, bbox2[0]-4), max(0, bbox2[1]-4), min(im2.width, bbox2[2]+4), min(im2.height, bbox2[3]+4))
    im2 = im2.crop(bbox2)
im2.save('scratch/q03_clean.png')

# Q5
page4 = doc[3]
rect4 = pymupdf.Rect(172, 192, 395, 410)
pix4 = page4.get_pixmap(clip=rect4, dpi=300)
im4 = Image.frombytes("RGB", [pix4.width, pix4.height], pix4.samples)
bbox4 = ImageChops.difference(im4, Image.new('RGB', im4.size, 'white')).getbbox()
if bbox4:
    bbox4 = (max(0, bbox4[0]-4), max(0, bbox4[1]-4), min(im4.width, bbox4[2]+4), min(im4.height, bbox4[3]+4))
    im4 = im4.crop(bbox4)
im4.save('scratch/q05_clean.png')

print("Saved clean Q3 and Q5 images.")
