import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

os.makedirs("figures", exist_ok=True)

# Helper to crop with dpi=300 for crisp figures
def crop_fig(page_idx, rect, out_path, dpi=300):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# 1. GA Q10: Monthly rainfall chart (Page 6, index 5)
# Image xref 41 is around Rect(138, 233, 490, 444)
crop_fig(5, fitz.Rect(130, 230, 500, 450), "figures/gate-2014-ae-ga-10-figure-1.png")

# 2. AE Q7 (Global Q17): Diamond airfoil (Page 7, index 6)
# Image xref 47 is around Rect(158, 639, 468, 709)
crop_fig(6, fitz.Rect(150, 635, 475, 715), "figures/gate-2014-ae-ae-17-figure-1.png")

# 3. AE Q8 (Global Q18): Oblique shock (Page 8, index 7)
# Image xref 54 is around Rect(243, 118, 386, 178)
crop_fig(7, fitz.Rect(235, 115, 395, 185), "figures/gate-2014-ae-ae-18-figure-1.png")

# 4. AE Q9 (Global Q19): Streamlines vortex (Page 8, index 7)
# Image xref 56 is around Rect(253, 311, 376, 436)
crop_fig(7, fitz.Rect(245, 305, 385, 442), "figures/gate-2014-ae-ae-19-figure-1.png")

# 5. AE Q10 (Global Q20): Diverging channel (Page 8, index 7)
# Image xref 58 is around Rect(217, 520, 412, 608)
crop_fig(7, fitz.Rect(210, 515, 420, 615), "figures/gate-2014-ae-ae-20-figure-1.png")

# 6. AE Q13 (Global Q23): 4 Option figures (Page 9, index 8)
# A: Rect(110, 185, 232, 275)
# B: Rect(322, 185, 434, 276)
# C: Rect(109, 278, 231, 369)
# D: Rect(323, 278, 442, 369)
crop_fig(8, fitz.Rect(100, 180, 240, 278), "figures/gate-2014-ae-ae-23-option-A.png")
crop_fig(8, fitz.Rect(315, 180, 445, 278), "figures/gate-2014-ae-ae-23-option-B.png")
crop_fig(8, fitz.Rect(100, 275, 240, 372), "figures/gate-2014-ae-ae-23-option-C.png")
crop_fig(8, fitz.Rect(315, 275, 450, 372), "figures/gate-2014-ae-ae-23-option-D.png")

# 7. AE Q32 (Global Q42): Four objects (Page 12, index 11)
# Rect(95, 129, 537, 216)
crop_fig(11, fitz.Rect(90, 125, 545, 222), "figures/gate-2014-ae-ae-42-figure-1.png")

# 8. AE Q33 (Global Q43): Stationary normal shock (Page 12, index 11)
# Rect(240, 397, 387, 450)
crop_fig(11, fitz.Rect(235, 392, 395, 455), "figures/gate-2014-ae-ae-43-figure-1.png")

# 9. AE Q34 (Global Q44): Subsonic body (Page 12, index 11)
# Rect(184, 549, 442, 603)
crop_fig(11, fitz.Rect(180, 545, 450, 610), "figures/gate-2014-ae-ae-44-figure-1.png")

# 10. AE Q37 (Global Q47): Pipe flow tank (Page 13, index 12)
# Rect(182, 667, 446, 774)
crop_fig(12, fitz.Rect(175, 660, 455, 780), "figures/gate-2014-ae-ae-47-figure-1.png")

# 11. AE Q38 (Global Q48): Steel beam overhangs (Page 14, index 13)
# Rect(93, 142, 523, 225)
crop_fig(13, fitz.Rect(88, 138, 530, 230), "figures/gate-2014-ae-ae-48-figure-1.png")

# 12. AE Q39 (Global Q49): Shaft Design I & II (Page 14, index 13)
# Rect(203, 333, 425, 471)
crop_fig(13, fitz.Rect(195, 328, 435, 478), "figures/gate-2014-ae-ae-49-figure-1.png")

# 13. AE Q40 (Global Q50): Column buckling (Page 14, index 13)
# Rect(168, 593, 460, 657)
crop_fig(13, fitz.Rect(160, 588, 470, 662), "figures/gate-2014-ae-ae-50-figure-1.png")

# 14. AE Q43 (Global Q53): Spring mass on beam (Page 15, index 14)
# Rect(191, 286, 437, 369)
crop_fig(14, fitz.Rect(185, 280, 445, 375), "figures/gate-2014-ae-ae-53-figure-1.png")

print("All AE2014 figures extracted.")
