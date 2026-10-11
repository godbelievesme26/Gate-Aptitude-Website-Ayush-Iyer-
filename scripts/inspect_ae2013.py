import fitz # PyMuPDF
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "internal/ae/AE2013.pdf"
key_path = "internal/ae/AE2013-key.pdf"

doc = fitz.open(pdf_path)
print(f"AE2013.pdf pages: {len(doc)}")

os.makedirs("tmp/ae2013_pages", exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(f"tmp/ae2013_pages/page_{i+1:02d}.png")
    text = page.get_text()
    print(f"--- PAGE {i+1} --- ({len(text)} chars)")
    print(text[:300].replace('\n', ' '))

print("\n--- KEY PDF ---")
key_doc = fitz.open(key_path)
print(f"AE2013-key.pdf pages: {len(key_doc)}")
for i, page in enumerate(key_doc):
    text = page.get_text()
    print(f"--- KEY PAGE {i+1} ---")
    print(text)
