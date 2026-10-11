import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'AE PYQ Papers/AE2024.pdf'
doc = fitz.open(pdf_path)
print(f"AE2024 Page Count: {len(doc)}")

for page_num in range(len(doc)):
    text = doc[page_num].get_text('text')
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    header = lines[:3] if lines else []
    print(f"Page {page_num + 1}: {header}")
