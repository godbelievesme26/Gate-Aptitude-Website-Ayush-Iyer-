import fitz

doc = fitz.open("internal/ae/AE2016.pdf")

def inspect_page_blocks(page_idx):
    p = doc[page_idx]
    blocks = p.get_text("blocks")
    print(f"=== PAGE {page_idx+1} BLOCKS ===")
    for b in blocks:
        print(f"({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}): {b[4][:40]!r}")

inspect_page_blocks(4) # Page 5 (AE Q13)
inspect_page_blocks(8) # Page 9 (AE Q38)
inspect_page_blocks(9) # Page 10 (AE Q40)
