import fitz, os

doc = fitz.open('internal/ae/AE2011.pdf')
os.makedirs('figures', exist_ok=True)
os.makedirs('tmp/fig_preview', exist_ok=True)

def crop_and_save(pno, rect, out_path, dpi=300):
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    pix.save(out_path)
    print(f"Saved {out_path} from page {pno}, rect {rect}")

# Let's define safe bounding boxes for each figure:
# Page 3: Q11 (two beams)
# Let's check text and drawings on Page 3 around Q11
crop_and_save(3, (100, 70, 480, 160), 'figures/gate-2011-ae-ae-11.png')

# Page 4: Q26 (cantilever beam with load P at L/2)
crop_and_save(4, (120, 660, 470, 755), 'figures/gate-2011-ae-ae-26.png')

# Page 6: Q37 (square plate with stresses)
crop_and_save(6, (140, 410, 450, 580), 'figures/gate-2011-ae-ae-37.png')

# Page 7: Q44 (expansion corner)
crop_and_save(7, (130, 425, 450, 560), 'figures/gate-2011-ae-ae-44.png')

# Page 7: Q45 (flat plate boundary layer)
crop_and_save(7, (130, 620, 460, 760), 'figures/gate-2011-ae-ae-45.png')

# Page 8: Q49 (cantilever beam)
crop_and_save(8, (120, 315, 460, 440), 'figures/gate-2011-ae-ae-49.png')

# Page 8: Q50/51 (compression corner)
crop_and_save(8, (130, 630, 460, 760), 'figures/gate-2011-ae-ae-50.png')

# Page 11: Q64 (target circles)
crop_and_save(11, (160, 175, 440, 415), 'figures/gate-2011-ae-ga-64.png')
