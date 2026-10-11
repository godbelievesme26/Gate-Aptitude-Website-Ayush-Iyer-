import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2013.pdf")

os.makedirs("tmp/ae2013_clean_crops", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# Helper to crop with dpi=200 for clean questions
def crop_q(page_idx, rect, out_path, dpi=200):
    page = doc[page_idx]
    pix = page.get_pixmap(clip=rect, dpi=dpi)
    pix.save(out_path)
    print(f"Saved {out_path} ({pix.width}x{pix.height})")

# Let's write question bounds for each question
# Page 4 (index 3)
crop_q(3, fitz.Rect(50, 70, 550, 200), "tmp/ae2013_clean_crops/q01_ae_01.png")
crop_q(3, fitz.Rect(50, 200, 550, 310), "tmp/ae2013_clean_crops/q02_ae_02.png")
crop_q(3, fitz.Rect(50, 310, 550, 420), "tmp/ae2013_clean_crops/q03_ae_03.png")
crop_q(3, fitz.Rect(50, 420, 550, 530), "tmp/ae2013_clean_crops/q04_ae_04.png")
crop_q(3, fitz.Rect(50, 530, 550, 700), "tmp/ae2013_clean_crops/q05_ae_05.png")

# Page 5 (index 4)
crop_q(4, fitz.Rect(50, 45, 550, 160), "tmp/ae2013_clean_crops/q06_ae_06.png")
crop_q(4, fitz.Rect(50, 160, 550, 260), "tmp/ae2013_clean_crops/q07_ae_07.png")
crop_q(4, fitz.Rect(50, 260, 550, 370), "tmp/ae2013_clean_crops/q08_ae_08.png")
crop_q(4, fitz.Rect(50, 370, 550, 510), "tmp/ae2013_clean_crops/q09_ae_09.png")
crop_q(4, fitz.Rect(50, 510, 550, 710), "tmp/ae2013_clean_crops/q10_ae_10.png")

# Page 6 (index 5)
crop_q(5, fitz.Rect(50, 45, 550, 190), "tmp/ae2013_clean_crops/q11_ae_11.png")
crop_q(5, fitz.Rect(50, 190, 550, 310), "tmp/ae2013_clean_crops/q12_ae_12.png")
crop_q(5, fitz.Rect(50, 310, 550, 450), "tmp/ae2013_clean_crops/q13_ae_13.png")
crop_q(5, fitz.Rect(50, 450, 550, 580), "tmp/ae2013_clean_crops/q14_ae_14.png")
crop_q(5, fitz.Rect(50, 580, 550, 710), "tmp/ae2013_clean_crops/q15_ae_15.png")

# Page 7 (index 6)
crop_q(6, fitz.Rect(50, 45, 550, 380), "tmp/ae2013_clean_crops/q16_ae_16.png")
crop_q(6, fitz.Rect(50, 380, 550, 680), "tmp/ae2013_clean_crops/q17_ae_17.png")

# Page 8 (index 7)
crop_q(7, fitz.Rect(50, 45, 550, 340), "tmp/ae2013_clean_crops/q18_ae_18.png")
crop_q(7, fitz.Rect(50, 340, 550, 450), "tmp/ae2013_clean_crops/q19_ae_19.png")
crop_q(7, fitz.Rect(50, 450, 550, 580), "tmp/ae2013_clean_crops/q20_ae_20.png")
crop_q(7, fitz.Rect(50, 580, 550, 710), "tmp/ae2013_clean_crops/q21_ae_21.png")

# Page 9 (index 8)
crop_q(8, fitz.Rect(50, 45, 550, 190), "tmp/ae2013_clean_crops/q22_ae_22.png")
crop_q(8, fitz.Rect(50, 190, 550, 360), "tmp/ae2013_clean_crops/q23_ae_23.png")
crop_q(8, fitz.Rect(50, 360, 550, 530), "tmp/ae2013_clean_crops/q24_ae_24.png")
crop_q(8, fitz.Rect(50, 530, 550, 710), "tmp/ae2013_clean_crops/q25_ae_25.png")

# Page 10 (index 9)
crop_q(9, fitz.Rect(50, 70, 550, 200), "tmp/ae2013_clean_crops/q26_ae_26.png")
crop_q(9, fitz.Rect(50, 200, 550, 340), "tmp/ae2013_clean_crops/q27_ae_27.png")
crop_q(9, fitz.Rect(50, 340, 550, 530), "tmp/ae2013_clean_crops/q28_ae_28.png")
crop_q(9, fitz.Rect(50, 530, 550, 710), "tmp/ae2013_clean_crops/q29_ae_29.png")

# Page 11 (index 10)
crop_q(10, fitz.Rect(50, 45, 550, 170), "tmp/ae2013_clean_crops/q30_ae_30.png")
crop_q(10, fitz.Rect(50, 170, 550, 300), "tmp/ae2013_clean_crops/q31_ae_31.png")
crop_q(10, fitz.Rect(50, 300, 550, 410), "tmp/ae2013_clean_crops/q32_ae_32.png")
crop_q(10, fitz.Rect(50, 410, 550, 510), "tmp/ae2013_clean_crops/q33_ae_33.png")
crop_q(10, fitz.Rect(50, 510, 550, 610), "tmp/ae2013_clean_crops/q34_ae_34.png")
crop_q(10, fitz.Rect(50, 610, 550, 720), "tmp/ae2013_clean_crops/q35_ae_35.png")

# Page 12 (index 11)
crop_q(11, fitz.Rect(50, 45, 550, 360), "tmp/ae2013_clean_crops/q36_ae_36.png")
crop_q(11, fitz.Rect(50, 360, 550, 680), "tmp/ae2013_clean_crops/q37_ae_37.png")

# Page 13 (index 12)
crop_q(12, fitz.Rect(50, 45, 550, 360), "tmp/ae2013_clean_crops/q38_ae_38.png")
crop_q(12, fitz.Rect(50, 360, 550, 540), "tmp/ae2013_clean_crops/q39_ae_39.png")
crop_q(12, fitz.Rect(50, 540, 550, 720), "tmp/ae2013_clean_crops/q40_ae_40.png")

# Page 14 (index 13)
crop_q(13, fitz.Rect(50, 45, 550, 340), "tmp/ae2013_clean_crops/q41_ae_41.png")
crop_q(13, fitz.Rect(50, 340, 550, 500), "tmp/ae2013_clean_crops/q42_ae_42.png")
crop_q(13, fitz.Rect(50, 500, 550, 720), "tmp/ae2013_clean_crops/q43_ae_43.png")

# Page 15 (index 14)
crop_q(14, fitz.Rect(50, 45, 550, 300), "tmp/ae2013_clean_crops/q44_ae_44.png")
crop_q(14, fitz.Rect(50, 300, 550, 430), "tmp/ae2013_clean_crops/q45_ae_45.png")
crop_q(14, fitz.Rect(50, 430, 550, 560), "tmp/ae2013_clean_crops/q46_ae_46.png")
crop_q(14, fitz.Rect(50, 560, 550, 720), "tmp/ae2013_clean_crops/q47_ae_47.png")

# Page 16 (index 15)
crop_q(15, fitz.Rect(50, 45, 550, 280), "tmp/ae2013_clean_crops/q48_49_common_ae.png")
crop_q(15, fitz.Rect(50, 280, 550, 500), "tmp/ae2013_clean_crops/q50_51_common_ae.png")
crop_q(15, fitz.Rect(50, 500, 550, 720), "tmp/ae2013_clean_crops/q52_53_common_ae.png")

# Page 17 (index 16)
crop_q(16, fitz.Rect(50, 45, 550, 450), "tmp/ae2013_clean_crops/q54_55_linked_ae.png")

# Page 18 (index 17) - GA Q56 to Q63
crop_q(17, fitz.Rect(50, 60, 550, 160), "tmp/ae2013_clean_crops/q56_ga_01.png")
crop_q(17, fitz.Rect(50, 160, 550, 260), "tmp/ae2013_clean_crops/q57_ga_02.png")
crop_q(17, fitz.Rect(50, 260, 550, 360), "tmp/ae2013_clean_crops/q58_ga_03.png")
crop_q(17, fitz.Rect(50, 360, 550, 460), "tmp/ae2013_clean_crops/q59_ga_04.png")
crop_q(17, fitz.Rect(50, 460, 550, 560), "tmp/ae2013_clean_crops/q60_ga_05.png")
crop_q(17, fitz.Rect(50, 560, 550, 640), "tmp/ae2013_clean_crops/q61_ga_06.png")
crop_q(17, fitz.Rect(50, 640, 550, 720), "tmp/ae2013_clean_crops/q62_ga_07.png")

# Page 19 (index 18) - GA Q63, Q64, Q65
crop_q(18, fitz.Rect(50, 45, 550, 150), "tmp/ae2013_clean_crops/q63_ga_08.png")
crop_q(18, fitz.Rect(50, 150, 550, 250), "tmp/ae2013_clean_crops/q64_ga_09.png")
crop_q(18, fitz.Rect(50, 250, 550, 370), "tmp/ae2013_clean_crops/q65_ga_10.png")

print("All crops saved.")
