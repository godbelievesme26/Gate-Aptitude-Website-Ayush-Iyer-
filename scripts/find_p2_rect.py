import fitz

doc = fitz.open("internal/ae/AE2016.pdf")
p2 = doc[1]
for img in p2.get_images():
    xref = img[0]
    for rect in p2.get_image_rects(xref):
        print("Image rect on page 2:", rect)

# Also check drawings on page 2
for d in p2.get_drawings():
    print("Drawing rect:", d["rect"])
