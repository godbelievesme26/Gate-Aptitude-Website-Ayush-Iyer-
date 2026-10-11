import fitz
import json
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

pdf_path = "internal/ae/AE2014.pdf"
key_pdf_path = "internal/ae/AE2014-key.pdf"

with open(pdf_path, "rb") as f:
    pdf_sha = hashlib.sha256(f.read()).hexdigest()

with open(key_pdf_path, "rb") as f:
    key_sha = hashlib.sha256(f.read()).hexdigest()

os.makedirs("figures", exist_ok=True)

def crop_fig(page_idx, rect, out_path, dpi=300):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# Clean crops
crop_fig(5, fitz.Rect(135, 230, 495, 445), "figures/gate-2014-ae-ga-10-figure-1.png")
crop_fig(6, fitz.Rect(155, 638, 470, 710), "figures/gate-2014-ae-ae-17-figure-1.png")
crop_fig(7, fitz.Rect(240, 118, 390, 180), "figures/gate-2014-ae-ae-18-figure-1.png")
crop_fig(7, fitz.Rect(250, 310, 380, 438), "figures/gate-2014-ae-ae-19-figure-1.png")
crop_fig(7, fitz.Rect(215, 520, 415, 610), "figures/gate-2014-ae-ae-20-figure-1.png")
crop_fig(8, fitz.Rect(108, 184, 235, 276), "figures/gate-2014-ae-ae-23-option-A.png")
crop_fig(8, fitz.Rect(320, 184, 436, 276), "figures/gate-2014-ae-ae-23-option-B.png")
crop_fig(8, fitz.Rect(108, 278, 235, 370), "figures/gate-2014-ae-ae-23-option-C.png")
crop_fig(8, fitz.Rect(320, 278, 444, 370), "figures/gate-2014-ae-ae-23-option-D.png")
crop_fig(11, fitz.Rect(93, 128, 540, 218), "figures/gate-2014-ae-ae-42-figure-1.png")
crop_fig(11, fitz.Rect(238, 396, 390, 452), "figures/gate-2014-ae-ae-43-figure-1.png")
crop_fig(11, fitz.Rect(182, 548, 445, 605), "figures/gate-2014-ae-ae-44-figure-1.png")
crop_fig(12, fitz.Rect(180, 666, 450, 776), "figures/gate-2014-ae-ae-47-figure-1.png")
crop_fig(13, fitz.Rect(92, 140, 525, 226), "figures/gate-2014-ae-ae-48-figure-1.png")
crop_fig(13, fitz.Rect(200, 332, 428, 472), "figures/gate-2014-ae-ae-49-figure-1.png")
crop_fig(13, fitz.Rect(165, 592, 462, 658), "figures/gate-2014-ae-ae-50-figure-1.png")
crop_fig(14, fitz.Rect(188, 285, 440, 370), "figures/gate-2014-ae-ae-53-figure-1.png")

print("All figures re-extracted.")
