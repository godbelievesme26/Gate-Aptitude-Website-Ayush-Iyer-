import sys
import os
import fitz
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2021.pdf')
os.makedirs('figures', exist_ok=True)

def render_figure(page_num, rect, out_path, dpi=288):
    page = doc[page_num - 1]
    crop_rect = fitz.Rect(rect)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    im = Image.open(out_path)
    print(f"Rendered {out_path}: {im.size}, mode={im.mode}")

print("--- Extracting All AE2021 Figures ---")

# 1. GA Q.2 (Page 2) - Main + Option figures
render_figure(2, (146, 103, 398, 285), 'figures/gate-2021-ae-ga-02-figure-1.png')
render_figure(2, (146, 312, 368, 353), 'figures/gate-2021-ae-ga-02-option-A.png')
render_figure(2, (146, 360, 368, 400), 'figures/gate-2021-ae-ga-02-option-B.png')
render_figure(2, (146, 407, 368, 448), 'figures/gate-2021-ae-ga-02-option-C.png')
render_figure(2, (146, 455, 368, 495), 'figures/gate-2021-ae-ga-02-option-D.png')

# 2. GA Q.9 (Page 5) - Square PQRS with sectors
render_figure(5, (214, 324, 429, 488), 'figures/gate-2021-ae-ga-09-figure-1.png')

# 3. AE Q.4 (Q14) (Page 8) - Nozzles A and B wave patterns
render_figure(8, (171, 142, 490, 369), 'figures/gate-2021-ae-ae-14-figure-1.png')

# 4. AE Q.10 (Q20) (Page 10) - Uniaxial tension test
render_figure(10, (183, 332, 478, 480), 'figures/gate-2021-ae-ae-20-figure-1.png')

# 5. AE Q.11 (Q21) (Page 11) - State of stress 2D element
render_figure(11, (195, 138, 441, 313), 'figures/gate-2021-ae-ae-21-figure-1.png')

# 6. AE Q.13 (Q23) (Page 12) - Cm vs alpha curve
render_figure(12, (214, 134, 441, 305), 'figures/gate-2021-ae-ae-23-figure-1.png')

# 7. AE Q.14 (Q24) (Page 13) - Oblique shock on wedge
render_figure(13, (201, 213, 466, 440), 'figures/gate-2021-ae-ae-24-figure-1.png')

# 8. AE Q.21 (Q31) (Page 16) - Free vortex filament and loop ABCDEFA
render_figure(16, (171, 142, 490, 337), 'figures/gate-2021-ae-ae-31-figure-1.png')

# 9. AE Q.26 (Q36) (Page 18) - Spring-mass system with rigid rod
render_figure(18, (232, 221, 441, 381), 'figures/gate-2021-ae-ae-36-figure-1.png')

# 10. AE Q.27 (Q37) (Page 19) - Three glasses P, Q, R with ice cubes
render_figure(19, (189, 174, 478, 325), 'figures/gate-2021-ae-ae-37-figure-1.png')

# 11. AE Q.29 (Q39) (Page 20) - Optical visualization setup
render_figure(20, (171, 158, 490, 341), 'figures/gate-2021-ae-ae-39-figure-1.png')

# 12. AE Q.33 (Q43) (Page 22) - Moving vs stationary normal shock
render_figure(22, (159, 198, 502, 353), 'figures/gate-2021-ae-ae-43-figure-1.png')

# 13. AE Q.40 (Q50) (Page 25) - Water tank on cart with vane
render_figure(25, (171, 237, 490, 377), 'figures/gate-2021-ae-ae-50-figure-1.png')

# 14. AE Q.46 (Q56) (Page 27) - Velocity triangle
render_figure(27, (232, 447, 429, 598), 'figures/gate-2021-ae-ae-56-figure-1.png')

# 15. AE Q.49 (Q59) (Page 29) - Rigid horizontal bar ABC with columns
render_figure(29, (171, 249, 484, 499), 'figures/gate-2021-ae-ae-59-figure-1.png')

# 16. AE Q.50 (Q60) (Page 30) - Two-cell wing box
render_figure(30, (177, 158, 478, 385), 'figures/gate-2021-ae-ae-60-figure-1.png')

# 17. AE Q.51 (Q61) (Page 30) - Two cantilever beams in contact
render_figure(30, (177, 498, 472, 602), 'figures/gate-2021-ae-ae-61-figure-1.png')

# 18. AE Q.52 (Q62) (Page 31) - Signboard supported by hollow pole
render_figure(31, (171, 201, 484, 428), 'figures/gate-2021-ae-ae-62-figure-1.png')

# 19. AE Q.53 (Q63) (Page 31) - Airplane steady pull-up maneuver CG, CP, T
render_figure(31, (195, 586, 478, 697), 'figures/gate-2021-ae-ae-63-figure-1.png')

print("All AE2021 figures extracted successfully.")
