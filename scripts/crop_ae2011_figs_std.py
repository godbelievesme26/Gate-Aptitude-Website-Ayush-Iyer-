import fitz, os

doc = fitz.open('internal/ae/AE2011.pdf')
os.makedirs('figures', exist_ok=True)

def crop_and_save(pno, rect, out_path, dpi=300):
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    pix.save(out_path)
    print(f"Saved {out_path} from page {pno}, rect {rect}")

# Clean and precise figure crops:
# Q11 (Page 3): Two beams
crop_and_save(3, (75, 180, 280, 280), 'figures/gate-2011-ae-ae-11-figure-1.png')

# Q26 (Page 4): Cantilever beam with point load P at L/2 and dimension L
crop_and_save(4, (110, 688, 460, 765), 'figures/gate-2011-ae-ae-26-figure-1.png')

# Q37 (Page 6): Rectangular plate with stresses and x,y coordinate axes
crop_and_save(6, (140, 415, 450, 515), 'figures/gate-2011-ae-ae-37-figure-1.png')

# Q44 (Page 7): Expansion corner with flow properties M1, p1, T1, theta, M2
crop_and_save(7, (165, 495, 450, 560), 'figures/gate-2011-ae-ae-44-figure-1.png')

# Q45 (Page 7): Boundary layer over flat plate
crop_and_save(7, (130, 640, 440, 715), 'figures/gate-2011-ae-ae-45-figure-1.png')

# Q49 (Page 8): Cantilever beam with x=0 to x=L
crop_and_save(8, (90, 360, 360, 445), 'figures/gate-2011-ae-ae-49-figure-1.png')

# Q50 (Page 8): Compression corner with shock wave beta, angle theta, point P
crop_and_save(8, (80, 625, 330, 700), 'figures/gate-2011-ae-ae-50-figure-1.png')

# Q64 (Page 11): Concentric target circles with points
crop_and_save(11, (160, 175, 440, 415), 'figures/gate-2011-ae-ga-64-figure-1.png')

print("All figure crops updated successfully.")
