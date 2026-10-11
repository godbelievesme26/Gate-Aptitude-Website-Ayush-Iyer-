import fitz
from PIL import Image
import os

doc = fitz.open('AE PYQ Papers/AE2024.pdf')

def save_crop(page_num, rect, out_path, margin=10, dpi=288):
    page = doc[page_num - 1]
    crop_rect = fitz.Rect(
        max(0, rect[0] - margin),
        max(0, rect[1] - margin),
        min(page.rect.width, rect[2] + margin),
        min(page.rect.height, rect[3] + margin)
    )
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    print(f"Rendered: {out_path} ({pix.width}x{pix.height}) from page {page_num}")

# Let's find exact coordinates on each page:
# Q8: Pie chart (Page 6)
save_crop(6, (180, 115, 450, 400), 'figures/gate-2024-ae-ga-08-figure-1.png', margin=12)

# Q9: Folded paper (Page 7, top half)
# Let's inspect page 7 text to find exact y bounds
# Q10: 3x3 square grid (Page 7, bottom half)
# Let's render page 7 figures
# Let's find rects on page 7:
save_crop(7, (70, 180, 500, 310), 'figures/gate-2024-ae-ga-09-figure-1.png', margin=10)
save_crop(7, (180, 520, 360, 680), 'figures/gate-2024-ae-ga-10-figure-1.png', margin=12)

# Q14: Vibration responses P, Q, R, S (Page 11)
save_crop(11, (180, 180, 420, 410), 'figures/gate-2024-ae-ae-14-figure-1.png', margin=12)

# Q18: Thermodynamics p-v processes (Page 14)
save_crop(14, (180, 150, 420, 400), 'figures/gate-2024-ae-ae-18-figure-1.png', margin=12)

# Q20: Drag polar options (A), (B), (C), (D) (Page 16)
# On Page 16, let's find the 4 option boxes:
# Option A is top-left, B top-right, C bottom-left, D bottom-right or stacked
# Let's check coordinates on page 16:
# Let's inspect page 16 drawings
