import fitz
import os

doc = fitz.open('internal/ae/AE2023.pdf')
os.makedirs('scratch/ae2023_pages', exist_ok=True)

# Render thumbnail of each page so we can inspect where diagrams exist
for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
    pix.save(f'scratch/ae2023_pages/page_{pno+1:02d}.png')

print("Rendered 35 page thumbnails in scratch/ae2023_pages/")
