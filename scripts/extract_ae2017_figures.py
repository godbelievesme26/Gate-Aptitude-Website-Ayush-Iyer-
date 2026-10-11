import os
from PIL import Image
import numpy as np

os.makedirs('figures', exist_ok=True)

def crop_figure(src_path, crop_box, out_path, pad=12):
    im = Image.open(src_path)
    cropped = im.crop(crop_box)
    
    # Auto-trim white borders around the crop with safe margin
    gray = cropped.convert('L')
    arr = np.array(gray)
    mask = arr < 250
    if np.any(mask):
        ymin, xmin = np.min(np.where(mask), axis=1)
        ymax, xmax = np.max(np.where(mask), axis=1)
        w, h = cropped.size
        xmin = max(0, xmin - pad)
        ymin = max(0, ymin - pad)
        xmax = min(w, xmax + pad + 1)
        ymax = min(h, ymax + pad + 1)
        cropped = cropped.crop((xmin, ymin, xmax, ymax))
    
    cropped.save(out_path)
    print(f"Saved {out_path} ({cropped.size})")

crops = [
    # Block 09 (AE 09 / Paper Q19): T-s diagram
    ('tmp/ae2017_q_imgs/q_block_09_p04_xref36.png', (0, 115, 851, 365), 'figures/gate-2017-ae-ae-19-figure-1.png', 12),
    # Block 21 (AE 21 / Paper Q31): Airfoil cross-section with spar caps
    ('tmp/ae2017_q_imgs/q_block_21_p07_xref72.png', (0, 60, 860, 190), 'figures/gate-2017-ae-ae-31-figure-1.png', 12),
    # Block 34 (AE 34 / Paper Q44): Expansion fan geometry
    ('tmp/ae2017_q_imgs/q_block_34_p11_xref114.png', (180, 220, 859, 476), 'figures/gate-2017-ae-ae-44-figure-1.png', 12),
    # Block 35 (AE 35 / Paper Q45): Shock wave in straight duct
    ('tmp/ae2017_q_imgs/q_block_35_p11_xref116.png', (200, 172, 750, 289), 'figures/gate-2017-ae-ae-45-figure-1.png', 12),
    # Block 36 (AE 36 / Paper Q46): Pipe nozzle flange
    ('tmp/ae2017_q_imgs/q_block_36_p12_xref122.png', (150, 110, 832, 297), 'figures/gate-2017-ae-ae-46-figure-1.png', 12),
    # Block 38 (AE 38 / Paper Q48): Pitching moment Cm vs alpha graph
    ('tmp/ae2017_q_imgs/q_block_38_p12_xref126.png', (50, 90, 520, 285), 'figures/gate-2017-ae-ae-48-figure-1.png', 12),
    # Block 46 (AE 46 / Paper Q56): Axial compressor velocity triangles
    ('tmp/ae2017_q_imgs/q_block_46_p15_xref154.png', (250, 10, 800, 340), 'figures/gate-2017-ae-ae-56-figure-1.png', 12),
    # Block 51 (AE 51 / Paper Q61): Cantilever beam with distributed load and tip mass
    ('tmp/ae2017_q_imgs/q_block_51_p16_xref167.png', (0, 80, 851, 235), 'figures/gate-2017-ae-ae-61-figure-1.png', 12),
    # Block 52 (AE 52 / Paper Q62): State of plane stress element
    ('tmp/ae2017_q_imgs/q_block_52_p17_xref171.png', (200, 70, 650, 284), 'figures/gate-2017-ae-ae-62-figure-1.png', 12),
    # Block 53 (AE 53 / Paper Q63): Thin-walled square tube under moment
    ('tmp/ae2017_q_imgs/q_block_53_p17_xref173.png', (200, 90, 750, 357), 'figures/gate-2017-ae-ae-63-figure-1.png', 12),
    # Block 54 (AE 54 / Paper Q64): 2-cell wing box shear flow
    ('tmp/ae2017_q_imgs/q_block_54_p18_xref177.png', (0, 125, 849, 401), 'figures/gate-2017-ae-ae-64-figure-1.png', 12),
    # Block 55 (AE 55 / Paper Q65): Mass on two 45 degree springs
    ('tmp/ae2017_q_imgs/q_block_55_p18_xref179.png', (150, 130, 650, 359), 'figures/gate-2017-ae-ae-65-figure-1.png', 12),
    # Block 65 (GA 10 / Paper Q10): Geographical contour map
    ('tmp/ae2017_q_imgs/q_block_65_p21_xref212.png', (180, 65, 780, 345), 'figures/gate-2017-ae-ga-10-figure-1.png', 12),
]

for src, box, dst, pad in crops:
    crop_figure(src, box, dst, pad)

print("All 13 figures re-extracted with clean margins.")
