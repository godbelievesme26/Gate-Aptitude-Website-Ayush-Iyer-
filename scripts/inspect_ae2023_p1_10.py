import sys
import fitz
import json

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2023.pdf')

def get_page_text(p):
    return doc[p - 1].get_text('text')

# Let's inspect pages 1 to 10 for Q1-Q17
for p in range(1, 11):
    print(f"=== PAGE {p} ===")
    print(get_page_text(p))
