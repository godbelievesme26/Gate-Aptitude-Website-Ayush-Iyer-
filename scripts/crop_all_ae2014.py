import fitz
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("internal/ae/AE2014.pdf")
os.makedirs("tmp/ae2014_clean_crops", exist_ok=True)

# Define questions per page:
# For each page from 5 to 17 (0-indexed: 4 to 16)
# Find all question headers: Q.1, Q.2, ...
# Crop from the start of Q_i to the start of Q_{i+1} (or bottom of page)

q_crops = [] # (q_num, page_num, rect)

page_defs = [
    (4, 'GA', [(1, 80), (2, 165), (3, 248), (4, 330), (5, 430), (6, 530), (7, 580)], 720),
    (5, 'GA', [(8, 45), (9, 120), (10, 190)], 470),
    (6, 'AE', [(1, 80), (2, 165), (3, 235), (4, 320), (5, 455), (6, 510), (7, 595)], 735),
    (7, 'AE', [(8, 55), (9, 245), (10, 465), (11, 650)], 730),
    (8, 'AE', [(12, 55), (13, 125), (14, 355), (15, 450), (16, 520), (17, 660)], 720),
    (9, 'AE', [(18, 50), (19, 160), (20, 230), (21, 310), (22, 360), (23, 415), (24, 475), (25, 535), (26, 615)], 730),
    (10, 'AE', [(27, 50), (28, 165), (29, 245), (30, 380), (31, 480)], 720),
    (11, 'AE', [(32, 50), (33, 330), (34, 470)], 720),
    (12, 'AE', [(35, 50), (36, 180), (37, 515)], 775),
    (13, 'AE', [(38, 55), (39, 240), (40, 500), (41, 680)], 770),
    (14, 'AE', [(42, 45), (43, 220), (44, 400), (45, 470), (46, 540)], 720),
    (15, 'AE', [(47, 50), (48, 140), (49, 220), (50, 315), (51, 375), (52, 470), (53, 515)], 720),
    (16, 'AE', [(54, 50), (55, 210)], 350),
]

q_idx = 1
for pno, sec, qlist, pbottom in page_defs:
    page = doc[pno]
    for i, (local_qno, y_top) in enumerate(qlist):
        y_bottom = qlist[i+1][1] if i+1 < len(qlist) else pbottom
        rect = fitz.Rect(50, y_top - 5, 550, y_bottom + 5)
        pix = page.get_pixmap(clip=rect, dpi=200)
        fname = f"tmp/ae2014_clean_crops/q{q_idx:02d}_{sec.lower()}_{local_qno:02d}.png"
        pix.save(fname)
        print(f"Saved Q{q_idx:02d} ({sec} Q{local_qno}) -> {fname}")
        q_idx += 1

print(f"Total questions cropped: {q_idx - 1}")
