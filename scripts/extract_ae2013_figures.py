import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2013.pdf")

os.makedirs("figures", exist_ok=True)

def crop_fig(page_idx, rect, out_path, dpi=300):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# 1. Q16: Thin-walled member cross section (Page 7, index 6)
crop_fig(6, fitz.Rect(180, 110, 420, 270), "figures/gate-2013-ae-ae-16-figure-1.png")

# 2. Q17: Cantilever beam (Page 7, index 6)
crop_fig(6, fitz.Rect(180, 430, 440, 560), "figures/gate-2013-ae-ae-17-figure-1.png")

# 3. Q18: Stiffened 4-boom cross section (Page 8, index 7)
crop_fig(7, fitz.Rect(200, 110, 430, 240), "figures/gate-2013-ae-ae-18-figure-1.png")

# 4. Q36: Flow past cylinder streamlines (Page 12, index 11)
crop_fig(11, fitz.Rect(170, 110, 440, 250), "figures/gate-2013-ae-ae-36-figure-1.png")

# 5. Q37: Wing with vortex / wake (Page 12, index 11)
crop_fig(11, fitz.Rect(180, 420, 440, 560), "figures/gate-2013-ae-ae-37-figure-1.png")

# 6. Q38: 4 identical booms cross section (Page 13, index 12)
crop_fig(12, fitz.Rect(180, 100, 440, 240), "figures/gate-2013-ae-ae-38-figure-1.png")

# 7. Q41: Steel structure truss (Page 14, index 13)
crop_fig(13, fitz.Rect(170, 90, 450, 240), "figures/gate-2013-ae-ae-41-figure-1.png")

# 8. Q44: Simply supported beam with overhang (Page 15, index 14)
crop_fig(14, fitz.Rect(150, 90, 470, 200), "figures/gate-2013-ae-ae-44-figure-1.png")

# 9. Q54-55 (Linked questions): Wing-body airplane (Page 17, index 16)
crop_fig(16, fitz.Rect(170, 100, 440, 270), "figures/gate-2013-ae-ae-54-figure-1.png")

print("All AE2013 figures extracted.")
