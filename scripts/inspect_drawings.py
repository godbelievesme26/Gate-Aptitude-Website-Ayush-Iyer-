import pymupdf

doc = pymupdf.open('internal/ae/AE2023.pdf')

for pno in [2, 4]:
    page = doc[pno - 1]
    print(f"=== PAGE {pno} DRAWINGS & BLOCKS ===")
    drawings = page.get_drawings()
    print(f"Total drawings: {len(drawings)}")
    for d in drawings[:10]:
        print(d.get('rect'))
    
    # Text blocks
    blocks = page.get_text('blocks')
    for b in blocks:
        print(f"Block: bbox={b[:4]}, text={repr(b[4][:30])}")
