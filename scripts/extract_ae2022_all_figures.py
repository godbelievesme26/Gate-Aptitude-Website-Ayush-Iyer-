import sys
import os
import fitz
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2022.pdf')
os.makedirs('figures', exist_ok=True)

def render_figure(page_num, rect, out_path, dpi=288):
    page = doc[page_num - 1]
    crop_rect = fitz.Rect(rect)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    im = Image.open(out_path)
    print(f"Rendered {out_path}: {im.size}, mode={im.mode}")

print("--- Extracting All AE2022 Figures ---")

# 1. GA Q.2 (Page 2) - Option figures
render_figure(2, (127, 220, 340, 280), 'figures/gate-2022-ae-ga-02-option-A.png')
render_figure(2, (127, 295, 340, 355), 'figures/gate-2022-ae-ga-02-option-B.png')
render_figure(2, (127, 370, 340, 430), 'figures/gate-2022-ae-ga-02-option-C.png')
render_figure(2, (127, 445, 340, 508), 'figures/gate-2022-ae-ga-02-option-D.png')

# 2. GA Q.5 (Page 5) - Question figure + Option figures
render_figure(5, (265, 75, 385, 175), 'figures/gate-2022-ae-ga-05-figure-1.png')
render_figure(5, (120, 252, 238, 365), 'figures/gate-2022-ae-ga-05-option-A.png')
render_figure(5, (120, 365, 238, 478), 'figures/gate-2022-ae-ga-05-option-B.png')
render_figure(5, (120, 478, 238, 590), 'figures/gate-2022-ae-ga-05-option-C.png')
render_figure(5, (120, 590, 238, 705), 'figures/gate-2022-ae-ga-05-option-D.png')

# 3. GA Q.9 (Page 9) - Four cities network graph
render_figure(9, (210, 310, 440, 520), 'figures/gate-2022-ae-ga-09-figure-1.png')

# 4. GA Q.10 (Page 10) - Case M and Case N square sheets
render_figure(10, (220, 250, 430, 345), 'figures/gate-2022-ae-ga-10-figure-1.png')

# 5. AE Q.16 (Page 14) - Control volume PQRS over flat plate
render_figure(14, (125, 215, 470, 340), 'figures/gate-2022-ae-ae-16-figure-1.png')

# 6. AE Q.17 (Page 15) - Velocity distribution u(y) and layers L1, L2
render_figure(15, (245, 145, 390, 300), 'figures/gate-2022-ae-ae-17-figure-1.png')

# 7. AE Q.20 (Page 17) - T-shaped cross-section beam
render_figure(17, (100, 138, 525, 230), 'figures/gate-2022-ae-ae-20-figure-1.png')

# 8. AE Q.21 (Page 18) - Three-member truss loaded at P
render_figure(18, (215, 138, 415, 305), 'figures/gate-2022-ae-ae-21-figure-1.png')

# 9. AE Q.22 (Page 19) - Thin-walled rectangular channel (i) and (ii)
render_figure(19, (120, 145, 505, 285), 'figures/gate-2022-ae-ae-22-figure-1.png')

# 10. AE Q.28 (Page 22) - Option figures (Mohr circles)
render_figure(22, (100, 165, 205, 260), 'figures/gate-2022-ae-ae-28-option-A.png')
render_figure(22, (100, 265, 220, 350), 'figures/gate-2022-ae-ae-28-option-B.png')
render_figure(22, (100, 355, 220, 438), 'figures/gate-2022-ae-ae-28-option-C.png')
render_figure(22, (100, 445, 245, 532), 'figures/gate-2022-ae-ae-28-option-D.png')

# 11. AE Q.33 (Page 24) - Plane-stress state element with 45 deg plane
render_figure(24, (260, 460, 380, 565), 'figures/gate-2022-ae-ae-33-figure-1.png')

# 12. AE Q.35 (Page 25) - Turbine blade velocity triangle / nozzle exit
render_figure(25, (155, 305, 480, 490), 'figures/gate-2022-ae-ae-35-figure-1.png')

# 13. AE Q.41 (Page 29) - Two-member truss with horizontal load F at R
render_figure(29, (215, 175, 420, 308), 'figures/gate-2022-ae-ae-41-figure-1.png')

# 14. AE Q.44 (Page 31) - Convergent nozzle discharging air
render_figure(31, (120, 215, 505, 390), 'figures/gate-2022-ae-ae-44-figure-1.png')

# 15. AE Q.52 (Page 35) - Solid cylinder housed inside another cylinder
render_figure(35, (265, 245, 388, 430), 'figures/gate-2022-ae-ae-52-figure-1.png')

# 16. AE Q.55 (Page 37) - Convergent-divergent nozzle expansion waves
render_figure(37, (118, 275, 515, 400), 'figures/gate-2022-ae-ae-55-figure-1.png')

# 17. AE Q.57 (Page 38) - Cantilever PQ Case I and Case II
render_figure(38, (115, 240, 520, 342), 'figures/gate-2022-ae-ae-57-figure-1.png')

# 18. AE Q.59 (Page 39) - Shaft with axial load and torque
render_figure(39, (145, 215, 495, 308), 'figures/gate-2022-ae-ae-59-figure-1.png')

# 19. AE Q.60 (Page 39) - Square rod with eccentric load and strain gages
render_figure(39, (135, 518, 505, 606), 'figures/gate-2022-ae-ae-60-figure-1.png')

# 20. AE Q.61 (Page 40) - Thin-walled I section dimensions
render_figure(40, (252, 178, 385, 272), 'figures/gate-2022-ae-ae-61-figure-1.png')

# 21. AE Q.62 (Page 40) - Damper spring mass system
render_figure(40, (250, 455, 388, 582), 'figures/gate-2022-ae-ae-62-figure-1.png')

# 22. AE Q.63 (Page 41) - Rigid prismatic bar suspended by two springs
render_figure(41, (210, 202, 428, 380), 'figures/gate-2022-ae-ae-63-figure-1.png')

print("All AE2022 figures rendered successfully!")
