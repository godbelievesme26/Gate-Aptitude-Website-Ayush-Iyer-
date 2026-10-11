import sys
import os
import fitz
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2023.pdf')
os.makedirs('figures', exist_ok=True)

def render_figure(page_num, rect, out_path, dpi=288):
    page = doc[page_num - 1]
    crop_rect = fitz.Rect(rect)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    im = Image.open(out_path)
    print(f"Rendered {out_path}: {im.size}, mode={im.mode}, extrema={im.getextrema()}")

# 1. GA Q.3: Parallelogram (Page 2)
render_figure(2, (180, 125, 400, 240), 'figures/gate-2023-ae-ga-03-figure-1.png')

# 2. GA Q.5: 16-square grid (Page 4)
render_figure(4, (175, 190, 390, 410), 'figures/gate-2023-ae-ga-05-figure-1.png')

# 3. AE Q.14: Wing cross section (Page 9)
render_figure(9, (185, 510, 455, 600), 'figures/gate-2023-ae-ae-14-figure-1.png')

# 4. AE Q.18: Option airfoil figures (Page 12)
# Let's check coordinates of options on Page 12
render_figure(12, (115, 185, 355, 238), 'figures/gate-2023-ae-ae-18-option-A.png')
render_figure(12, (115, 255, 355, 308), 'figures/gate-2023-ae-ae-18-option-B.png')
render_figure(12, (115, 325, 355, 378), 'figures/gate-2023-ae-ae-18-option-C.png')
render_figure(12, (115, 395, 355, 448), 'figures/gate-2023-ae-ae-18-option-D.png')

# 5. AE Q.19: Option figures (Page 13)
render_figure(13, (115, 210, 268, 335), 'figures/gate-2023-ae-ae-19-option-A.png')
render_figure(13, (115, 350, 268, 470), 'figures/gate-2023-ae-ae-19-option-B.png')
render_figure(13, (115, 485, 268, 602), 'figures/gate-2023-ae-ae-19-option-C.png')
render_figure(13, (115, 618, 268, 735), 'figures/gate-2023-ae-ae-19-option-D.png')

# 6. AE Q.23: Diagram (Page 15)
render_figure(15, (180, 498, 458, 590), 'figures/gate-2023-ae-ae-23-figure-1.png')

# 7. AE Q.24: Option figures (Page 16)
render_figure(16, (115, 208, 260, 332), 'figures/gate-2023-ae-ae-24-option-A.png')
render_figure(16, (115, 350, 265, 452), 'figures/gate-2023-ae-ae-24-option-B.png')
render_figure(16, (115, 470, 262, 570), 'figures/gate-2023-ae-ae-24-option-C.png')
render_figure(16, (115, 588, 278, 736), 'figures/gate-2023-ae-ae-24-option-D.png')

# 8. AE Q.30: Wing vibration (Page 19)
render_figure(19, (250, 575, 388, 702), 'figures/gate-2023-ae-ae-30-figure-1.png')

# 9. AE Q.32: Landing aircraft (Page 20)
render_figure(20, (125, 340, 512, 425), 'figures/gate-2023-ae-ae-32-figure-1.png')

# 10. AE Q.37: Supersonic intake (Page 23)
render_figure(23, (115, 160, 505, 275), 'figures/gate-2023-ae-ae-37-figure-1.png')

# 11. AE Q.41: Scramjet engine (Page 26)
render_figure(26, (115, 175, 500, 258), 'figures/gate-2023-ae-ae-41-figure-1.png')

# 12. AE Q.44: Supersonic duct (Page 28)
render_figure(28, (115, 132, 512, 230), 'figures/gate-2023-ae-ae-44-figure-1.png')

# 13. AE Q.49: Rigid bar (Page 31)
render_figure(31, (218, 160, 418, 280), 'figures/gate-2023-ae-ae-49-figure-1.png')

# 14. AE Q.50: Cantilever beam (Page 31)
render_figure(31, (210, 415, 426, 492), 'figures/gate-2023-ae-ae-50-figure-1.png')

# 15. AE Q.52: Shear flow (Page 32)
render_figure(32, (174, 195, 462, 335), 'figures/gate-2023-ae-ae-52-figure-1.png')

print("All AE2023 figure renders generated!")
