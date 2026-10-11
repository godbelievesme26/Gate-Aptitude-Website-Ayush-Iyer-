import sys
import json
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('AE PYQ Papers/AE2024.pdf')

full_text = ""
for pno in range(len(doc)):
    page_text = doc[pno].get_text('text')
    full_text += f"\n\n=== [PAGE {pno+1}] ===\n" + page_text

with open('scripts/ae2024_full_dump.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Saved scripts/ae2024_full_dump.txt (Length:", len(full_text), "chars)")
