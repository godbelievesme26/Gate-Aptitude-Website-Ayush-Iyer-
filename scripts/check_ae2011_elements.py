import fitz, sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('internal/ae/AE2011.pdf')

def inspect_page_elements(pno, y_min, y_max):
    page = doc[pno - 1]
    print(f"\n--- Elements on Page {pno} between y={y_min} and y={y_max} ---")
    blocks = page.get_text('blocks')
    for b in blocks:
        if not (b[3] < y_min or b[1] > y_max):
            print(f"  TEXT [y={b[1]:.1f}-{b[3]:.1f}, x={b[0]:.1f}-{b[2]:.1f}]: {repr(b[4].strip())}")
    drawings = page.get_drawings()
    for d in drawings:
        r = d['rect']
        if not (r.y1 < y_min or r.y0 > y_max):
            print(f"  DRAWING: {r}")

inspect_page_elements(3, 50, 180)   # Q11
inspect_page_elements(4, 630, 770)  # Q26
inspect_page_elements(6, 380, 610)  # Q37
inspect_page_elements(7, 400, 580)  # Q44
inspect_page_elements(7, 580, 770)  # Q45
inspect_page_elements(8, 300, 470)  # Q49
inspect_page_elements(8, 550, 780)  # Q50/51
inspect_page_elements(11, 130, 440) # Q64
