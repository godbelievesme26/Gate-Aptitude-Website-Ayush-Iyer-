import sys
import os
import fitz
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')
os.makedirs('figures', exist_ok=True)

def save_crop(page_num, rect, out_path, margin=8, dpi=288):
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
    # Check image validity
    im = Image.open(out_path)
    print(f"Saved {out_path}: {im.size}, mode={im.mode}, extrema={im.getextrema()}")

print("--- Rendering All AE2024 Figures from PDF Pages ---")

# 1. GA Q8: Pie chart (Page 6)
save_crop(6, (180, 125, 435, 380), 'figures/gate-2024-ae-ga-08-figure-1.png', margin=12)

# 2. GA Q10: 3x3 square grid (Page 7)
save_crop(7, (200, 415, 435, 492), 'figures/gate-2024-ae-ga-10-figure-1.png', margin=10)

# 3. AE Q14: Vibration responses P, Q, R, S (Page 11)
save_crop(11, (200, 215, 438, 395), 'figures/gate-2024-ae-ae-14-figure-1.png', margin=10)

# 4. AE Q18: Thermodynamics p-v processes (Page 14)
save_crop(14, (240, 132, 398, 278), 'figures/gate-2024-ae-ae-18-figure-1.png', margin=10)

# 5. AE Q20: Option figures (Page 16)
save_crop(16, (115, 170, 280, 282), 'figures/gate-2024-ae-ae-20-option-A.png', margin=6)
save_crop(16, (115, 298, 280, 408), 'figures/gate-2024-ae-ae-20-option-B.png', margin=6)
save_crop(16, (115, 425, 280, 535), 'figures/gate-2024-ae-ae-20-option-C.png', margin=6)
save_crop(16, (115, 552, 280, 662), 'figures/gate-2024-ae-ae-20-option-D.png', margin=6)

# 6. AE Q23: Supersonic flow (Page 18)
save_crop(18, (210, 148, 428, 256), 'figures/gate-2024-ae-ae-23-figure-1.png', margin=10)

# 7. AE Q24: Two airfoils (Page 19)
save_crop(19, (115, 164, 515, 236), 'figures/gate-2024-ae-ae-24-figure-1.png', margin=10)

# 8. AE Q25: Stress-strain diagrams (Page 20)
save_crop(20, (398, 158, 492, 250), 'figures/gate-2024-ae-ae-25-figure-1.png', margin=8)
save_crop(20, (394, 344, 486, 438), 'figures/gate-2024-ae-ae-25-figure-2.png', margin=8)

# 9. AE Q28: Stability curves (Page 22)
save_crop(22, (190, 120, 448, 284), 'figures/gate-2024-ae-ae-28-figure-1.png', margin=10)

# 10. AE Q37: Solid of revolution (Page 25)
save_crop(25, (244, 134, 394, 294), 'figures/gate-2024-ae-ae-37-figure-1.png', margin=10)

# 11. AE Q43: Shock structures (Page 29)
save_crop(29, (118, 160, 510, 298), 'figures/gate-2024-ae-ae-43-figure-1.png', margin=10)

# 12. AE Q44: Expansion fan (Page 30)
save_crop(30, (212, 198, 426, 346), 'figures/gate-2024-ae-ae-44-figure-1.png', margin=10)

# 13. AE Q46: Yield loci (Page 32)
save_crop(32, (195, 148, 442, 334), 'figures/gate-2024-ae-ae-46-figure-1.png', margin=10)

# 14. AE Q48: Yawing moment curve (Page 34)
save_crop(34, (400, 210, 506, 310), 'figures/gate-2024-ae-ae-48-figure-1.png', margin=8)

# 15. AE Q52: State of stress (Page 36)
save_crop(36, (150, 188, 488, 346), 'figures/gate-2024-ae-ae-52-figure-1.png', margin=10)

# 16. AE Q53: Truss structure (Page 36)
save_crop(36, (262, 442, 376, 608), 'figures/gate-2024-ae-ae-53-figure-1.png', margin=10)

# 17. AE Q54: Beam cross section (Page 37)
save_crop(37, (244, 160, 394, 302), 'figures/gate-2024-ae-ae-54-figure-1.png', margin=10)

# 18. AE Q63: Control volume (Page 39)
save_crop(39, (118, 350, 520, 522), 'figures/gate-2024-ae-ae-63-figure-1.png', margin=10)

print("All 22 figures re-extracted with clean page rendering!")
