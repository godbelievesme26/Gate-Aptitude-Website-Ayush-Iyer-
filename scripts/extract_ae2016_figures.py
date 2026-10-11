import fitz

doc = fitz.open("internal/ae/AE2016.pdf")

# 1. GA Q6: Page 2 (idx 1)
p2 = doc[1]
rect_ga6 = fitz.Rect(92, 167, 558, 463)
pix = p2.get_pixmap(dpi=300, clip=rect_ga6)
pix.save("figures/gate-2016-ae-ga-06-figure-1.png")

# 2. AE Q13: Page 5 (idx 4)
p5 = doc[4]
rect_ae13 = fitz.Rect(105, 438, 520, 556)
pix = p5.get_pixmap(dpi=300, clip=rect_ae13)
pix.save("figures/gate-2016-ae-ae-23-figure-1.png")

# 3. AE Q14: Page 6 (idx 5)
p6 = doc[5]
rect_ae14 = fitz.Rect(230, 70, 430, 220)
pix = p6.get_pixmap(dpi=300, clip=rect_ae14)
pix.save("figures/gate-2016-ae-ae-24-figure-1.png")

# 4. AE Q30: Page 8 (idx 7)
p8 = doc[7]
rect_ae30 = fitz.Rect(235, 110, 425, 245)
pix = p8.get_pixmap(dpi=300, clip=rect_ae30)
pix.save("figures/gate-2016-ae-ae-40-figure-1.png")

# 5. AE Q38: Page 9 (idx 8)
p9 = doc[8]
rect_ae38 = fitz.Rect(180, 282, 440, 442)
pix = p9.get_pixmap(dpi=300, clip=rect_ae38)
pix.save("figures/gate-2016-ae-ae-48-figure-1.png")

# 6. AE Q40: Page 10 (idx 9)
p10 = doc[9]
rect_ae40 = fitz.Rect(230, 88, 425, 228)
pix = p10.get_pixmap(dpi=300, clip=rect_ae40)
pix.save("figures/gate-2016-ae-ae-50-figure-1.png")

print("Re-extracted all 6 figures with exact bounding boxes.")
