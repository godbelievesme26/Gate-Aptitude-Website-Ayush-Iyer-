import fitz
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

# Extract exact text from each question's bounding box in the PDF
# Let's read the exact text blocks from pages 5 to 17
for pno in range(4, 17):
    page = doc[pno]
    blocks = page.get_text("blocks")
    print(f"\n================ PAGE {pno+1} BLOCKS ================")
    for b in blocks:
        if b[4].strip():
            print(f"--- Block at y=[{b[1]:.1f}, {b[3]:.1f}] ---")
            print(b[4].strip())
