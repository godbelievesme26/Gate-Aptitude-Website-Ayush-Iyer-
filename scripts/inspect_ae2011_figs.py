import fitz, os

doc = fitz.open('internal/ae/AE2011.pdf')

# Let's inspect vector drawings and text on each relevant page
pages_to_check = [3, 4, 6, 7, 8, 11]

for p in pages_to_check:
    page = doc[p-1]
    print(f"=== PAGE {p} DRAWINGS & TEXT RECTS ===")
    drawings = page.get_drawings()
    print(f"Total drawings: {len(drawings)}")
    for d in drawings:
        print(f"  Drawing rect: {d['rect']}")
