import fitz
import os
import re
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open("internal/ae/AE2014.pdf")
os.makedirs("tmp/ae2014_clean_crops", exist_ok=True)

# Let's extract text blocks with bboxes for pages 5 to 17
pages_blocks = []
for pno in range(4, 17):
    page = doc[pno]
    blocks = page.get_text("blocks")
    pages_blocks.append((pno + 1, page, blocks))

print(f"Loaded {len(pages_blocks)} pages.")

# Let's scan for question headers: Q.1, Q.2 ...
# On GA pages (5-6): Q.1 to Q.10
# On AE pages (7-17): Q.1 to Q.55

# Let's inspect where questions start on each page
for pno, page, blocks in pages_blocks:
    print(f"\n--- Page {pno} ---")
    for b in blocks:
        text = b[4].strip()
        lines = text.split('\n')
        first_line = lines[0].strip() if lines else ""
        if re.match(r'^Q\.\s*\d+', first_line):
            print(f"  [{b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}] {first_line[:60]}")
