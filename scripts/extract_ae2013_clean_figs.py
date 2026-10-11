import fitz
import json
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "internal/ae/AE2013.pdf"
key_pdf_path = "internal/ae/AE2013-key.pdf"

with open(pdf_path, "rb") as f:
    pdf_sha = hashlib.sha256(f.read()).hexdigest()

with open(key_pdf_path, "rb") as f:
    key_sha = hashlib.sha256(f.read()).hexdigest()

doc = fitz.open(pdf_path)

# Extract and crop all accurate figures
os.makedirs("figures", exist_ok=True)

def crop_fig(page_idx, rect, out_path, dpi=300):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# Q16 figure: page 7 (index 6), Rect(180, 110, 420, 240)
crop_fig(6, fitz.Rect(180, 110, 420, 240), "figures/gate-2013-ae-ae-16-figure-1.png")

# Q17 figure: page 7 (index 6), Rect(200, 395, 480, 595)
crop_fig(6, fitz.Rect(200, 395, 480, 595), "figures/gate-2013-ae-ae-17-figure-1.png")

# Q18 figure: page 8 (index 7), Rect(200, 110, 430, 240)
crop_fig(7, fitz.Rect(200, 110, 430, 240), "figures/gate-2013-ae-ae-18-figure-1.png")

# Q36 figure: page 12 (index 11), Rect(170, 110, 440, 250)
crop_fig(11, fitz.Rect(170, 110, 440, 250), "figures/gate-2013-ae-ae-36-figure-1.png")

# Q37 figure: page 12 (index 11), Rect(180, 420, 440, 560)
crop_fig(11, fitz.Rect(180, 420, 440, 560), "figures/gate-2013-ae-ae-37-figure-1.png")

# Q38 figure: page 13 (index 12), Rect(180, 100, 440, 240)
crop_fig(12, fitz.Rect(180, 100, 440, 240), "figures/gate-2013-ae-ae-38-figure-1.png")

# Q41 figure: page 14 (index 13), Rect(170, 90, 450, 240)
crop_fig(13, fitz.Rect(170, 90, 450, 240), "figures/gate-2013-ae-ae-41-figure-1.png")

# Q44 figure: page 15 (index 14), Rect(150, 90, 470, 200)
crop_fig(14, fitz.Rect(150, 90, 470, 200), "figures/gate-2013-ae-ae-44-figure-1.png")

# Q54-55 linked figure: page 17 (index 16) - wait, is there a figure on page 17? Let's check page 17!
# Page 17 text has no figure.

print("Figures extracted.")
