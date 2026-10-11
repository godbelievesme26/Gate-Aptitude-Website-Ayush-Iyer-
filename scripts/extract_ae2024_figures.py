import sys
import os
import fitz
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')
os.makedirs('figures', exist_ok=True)

# Function to save high-res render from page rect with safe margin
def save_page_rect_crop(doc, page_num, rect, out_path, margin=15, dpi=216):
    page = doc[page_num - 1]
    # Expand rect by margin
    crop_rect = fitz.Rect(
        max(0, rect.x0 - margin),
        max(0, rect.y0 - margin),
        min(page.rect.width, rect.x1 + margin),
        min(page.rect.height, rect.y1 + margin)
    )
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    pix.save(out_path)
    print(f"Saved: {out_path} ({pix.width}x{pix.height}) from Page {page_num}, Rect: {crop_rect}")

# Function to extract raw image XRef or save it
def save_raw_image(doc, xref, out_path):
    base_img = doc.extract_image(xref)
    image_bytes = base_img["image"]
    image_ext = base_img["ext"]
    img = Image.open(io.BytesIO(image_bytes))
    img.save(out_path, format="PNG")
    print(f"Saved raw XRef {xref} -> {out_path} ({img.width}x{img.height})")

print("--- Extracting AE2024 Figures ---")

# Q8: Pie chart on Page 6 (Rect: roughly around the pie chart at bottom/right of page 6)
# Let's inspect page 6 drawings/text rect
p6 = doc[5]
# Let's crop the pie chart area on page 6: rect roughly (150, 100, 480, 420)
save_page_rect_crop(doc, 6, fitz.Rect(180, 115, 450, 400), 'figures/gate-2024-ae-ga-08-figure-1.png', margin=10)

# Q9: Folded paper on Page 7 (XRef 57)
save_raw_image(doc, 57, 'figures/gate-2024-ae-ga-09-figure-1.png')

# Q10: 3x3 square grid on Page 7
# Let's crop Q10 grid on page 7
save_page_rect_crop(doc, 7, fitz.Rect(180, 520, 360, 680), 'figures/gate-2024-ae-ga-10-figure-1.png', margin=10)

# Q14: P, Q, R, S free vibration on Page 11 (XRef 68)
save_raw_image(doc, 68, 'figures/gate-2024-ae-ae-14-figure-1.png')

# Q18: Thermodynamics p-v diagram on Page 14 (XRef 85)
save_raw_image(doc, 85, 'figures/gate-2024-ae-ae-18-figure-1.png')

# Q20: Option figures on Page 16 (XRefs 91, 93, 95, 97)
save_raw_image(doc, 91, 'figures/gate-2024-ae-ae-20-option-A.png')
save_raw_image(doc, 93, 'figures/gate-2024-ae-ae-20-option-B.png')
save_raw_image(doc, 95, 'figures/gate-2024-ae-ae-20-option-C.png')
save_raw_image(doc, 97, 'figures/gate-2024-ae-ae-20-option-D.png')

# Q23: Supersonic flow on Page 18 (XRef 108)
save_raw_image(doc, 108, 'figures/gate-2024-ae-ae-23-figure-1.png')

# Q24: Two airfoils on Page 19 (XRef 111)
save_raw_image(doc, 111, 'figures/gate-2024-ae-ae-24-figure-1.png')

# Q25: Airfoil / control surface diagrams on Page 20 (XRefs 114, 116)
save_raw_image(doc, 114, 'figures/gate-2024-ae-ae-25-figure-1.png')
save_raw_image(doc, 116, 'figures/gate-2024-ae-ae-25-figure-2.png')

# Q28: Longitudinal stability curves on Page 22 (XRef 124)
save_raw_image(doc, 124, 'figures/gate-2024-ae-ae-28-figure-1.png')

# Q37: Solid of revolution on Page 25 (XRef 132)
save_raw_image(doc, 132, 'figures/gate-2024-ae-ae-37-figure-1.png')

# Q43: Shock structures on Page 29 (XRef 147)
save_raw_image(doc, 147, 'figures/gate-2024-ae-ae-43-figure-1.png')

# Q44: Expansion fan on Page 30 (XRef 150)
save_raw_image(doc, 150, 'figures/gate-2024-ae-ae-44-figure-1.png')

# Q46: Yield loci on Page 32 (XRef 155)
save_raw_image(doc, 155, 'figures/gate-2024-ae-ae-46-figure-1.png')

# Q49: Axial turbine diagram on Page 34 (XRef 161)
save_raw_image(doc, 161, 'figures/gate-2024-ae-ae-49-figure-1.png')

# Q52: Mohr circle / state of stress on Page 36 (XRef 167)
save_raw_image(doc, 167, 'figures/gate-2024-ae-ae-52-figure-1.png')

# Q53: Truss structure on Page 36 (XRef 169)
save_raw_image(doc, 169, 'figures/gate-2024-ae-ae-53-figure-1.png')

# Q54: Thin-walled beam cross section on Page 37 (XRef 173)
save_raw_image(doc, 173, 'figures/gate-2024-ae-ae-54-figure-1.png')

# Q63: Control volume on Page 39 (XRef 180)
save_raw_image(doc, 180, 'figures/gate-2024-ae-ae-63-figure-1.png')

print("All AE2024 figures extracted successfully.")
