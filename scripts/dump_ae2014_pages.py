import fitz
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open("internal/ae/AE2014.pdf")

for pno in range(4, 17): # 0-indexed: 4 is Page 5, 16 is Page 17
    page = doc[pno]
    print(f"\n======================================")
    print(f"PAGE {pno+1}")
    print(f"======================================")
    text = page.get_text()
    print(text)
