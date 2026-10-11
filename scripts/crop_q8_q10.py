import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')
p7 = doc[6]

# Let's render page 7 around Q10
pix = p7.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(150, 400, 450, 520))
pix.save('figures/gate-2024-ae-ga-10-figure-1.png')
print("Saved Q10 figure: figures/gate-2024-ae-ga-10-figure-1.png", pix.width, "x", pix.height)

# Also let's re-render Q8 pie chart
p6 = doc[5]
pix8 = p6.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(180, 120, 450, 360))
pix8.save('figures/gate-2024-ae-ga-08-figure-1.png')
print("Saved Q8 figure: figures/gate-2024-ae-ga-08-figure-1.png", pix8.width, "x", pix8.height)
