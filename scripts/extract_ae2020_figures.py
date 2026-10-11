import fitz
import os
from PIL import Image

doc = fitz.open("internal/ae/AE2020.pdf")
os.makedirs("figures", exist_ok=True)

def render_crop(page_num, rect, out_path, dpi=288):
    page = doc[page_num - 1]
    crop_rect = fitz.Rect(rect)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    im = Image.open(out_path)
    print(f"Rendered {out_path}: {im.size}, mode={im.mode}")

print("--- Rendering Perfect AE2020 Figure Crops ---")

# 1. GA Q.8 (Page 2) - Circle with inscribed rectangle PQRS
render_crop(2, (180, 380, 440, 532), "figures/gate-2020-ae-ga-08-figure-1.png")

# 2. GA Q.10 (Page 3) - Bar chart of School P and Q enrollment
render_crop(3, (145, 75, 455, 245), "figures/gate-2020-ae-ga-10-figure-1.png")

# 3. AE Q.6 (Page 4) - Two counter-rotating line vortices
render_crop(4, (180, 275, 440, 360), "figures/gate-2020-ae-ae-06-figure-1.png")

# 4. AE Q.7 (Page 4) - Streamlines through channel
render_crop(4, (80, 580, 425, 755), "figures/gate-2020-ae-ae-07-figure-1.png")

# 5. AE Q.17 (Page 6) - Airfoil section with regions I, II, III, IV
render_crop(6, (125, 520, 485, 605), "figures/gate-2020-ae-ae-17-figure-1.png")

# 6. AE Q.24 (Page 7) - Thin walled beam
render_crop(7, (140, 500, 470, 572), "figures/gate-2020-ae-ae-24-figure-1.png")

# 7. AE Q.25 (Page 7) - Airplane at bottom of vertical circle
render_crop(7, (130, 678, 490, 725), "figures/gate-2020-ae-ae-25-figure-1.png")

# 8. AE Q.27 (Page 8) - Wedge shaped airfoil
render_crop(8, (85, 120, 445, 205), "figures/gate-2020-ae-ae-27-figure-1.png")
# Options A, B, C, D (xref 147, 148, 149, 150)
render_crop(8, (90, 245, 290, 318), "figures/gate-2020-ae-ae-27-option-A.png")
render_crop(8, (90, 321, 290, 395), "figures/gate-2020-ae-ae-27-option-B.png")
render_crop(8, (90, 398, 290, 472), "figures/gate-2020-ae-ae-27-option-C.png")
render_crop(8, (90, 475, 290, 549), "figures/gate-2020-ae-ae-27-option-D.png")

# 9. AE Q.29 (Page 9) - Stepped cantilever beam
render_crop(9, (160, 122, 470, 200), "figures/gate-2020-ae-ae-29-figure-1.png")

# 10. AE Q.34 (Page 10) - State of stress
render_crop(10, (200, 650, 420, 765), "figures/gate-2020-ae-ae-34-figure-1.png")
# Options A, B, C, D on Page 11 (xref 186, 187, 188, 189)
render_crop(11, (90, 28, 220, 128), "figures/gate-2020-ae-ae-34-option-A.png")
render_crop(11, (90, 132, 220, 235), "figures/gate-2020-ae-ae-34-option-B.png")
render_crop(11, (90, 238, 225, 348), "figures/gate-2020-ae-ae-34-option-C.png")
render_crop(11, (90, 352, 222, 458), "figures/gate-2020-ae-ae-34-option-D.png")

# 11. AE Q.38 (Page 12) - Airfoil wake velocity profile
render_crop(12, (130, 295, 450, 420), "figures/gate-2020-ae-ae-38-figure-1.png")

# 12. AE Q.49 (Page 14) - T-S diagram
render_crop(14, (185, 60, 420, 190), "figures/gate-2020-ae-ae-49-figure-1.png")

# 13. AE Q.52 (Page 14) - 2-DOF spring mass system
render_crop(14, (130, 545, 490, 652), "figures/gate-2020-ae-ae-52-figure-1.png")

# 14. AE Q.53 (Page 14) - Propped cantilever beam
render_crop(14, (130, 742, 480, 810), "figures/gate-2020-ae-ae-53-figure-1.png")

print("All AE2020 figures updated successfully.")
