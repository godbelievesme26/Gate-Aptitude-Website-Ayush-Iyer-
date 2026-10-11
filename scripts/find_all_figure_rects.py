import fitz

doc = fitz.open("internal/ae/AE2016.pdf")

print("--- PAGE 5 (AE Q13) ---")
p5 = doc[4]
for d in p5.get_drawings():
    if d["rect"].y0 > 50 and d["rect"].y1 < 790:
        print("p5 drawing:", d["rect"])

print("--- PAGE 6 (AE Q14) ---")
p6 = doc[5]
for d in p6.get_drawings():
    if d["rect"].y0 > 50 and d["rect"].y1 < 790:
        print("p6 drawing:", d["rect"])

print("--- PAGE 8 (AE Q30) ---")
p8 = doc[7]
for d in p8.get_drawings():
    if d["rect"].y0 > 50 and d["rect"].y1 < 790:
        print("p8 drawing:", d["rect"])

print("--- PAGE 9 (AE Q38) ---")
p9 = doc[8]
for d in p9.get_drawings():
    if d["rect"].y0 > 50 and d["rect"].y1 < 790:
        print("p9 drawing:", d["rect"])

print("--- PAGE 10 (AE Q40) ---")
p10 = doc[9]
for d in p10.get_drawings():
    if d["rect"].y0 > 50 and d["rect"].y1 < 790:
        print("p10 drawing:", d["rect"])
