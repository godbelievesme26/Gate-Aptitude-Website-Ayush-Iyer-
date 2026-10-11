import sys
import json
import hashlib
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'AE PYQ Papers/AE2024.pdf'
doc = fitz.open(pdf_path)

with open(pdf_path, 'rb') as f:
    pdf_sha256 = hashlib.sha256(f.read()).hexdigest()

print(f"AE2024 SHA256: {pdf_sha256}")
print(f"Total Pages: {len(doc)}")

# Extract text per page
pages_data = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text('text')
    images = page.get_images(full=True)
    pages_data.append({
        'page': pno + 1,
        'text': text,
        'images_count': len(images)
    })

print(f"Pages extracted: {len(pages_data)}")
for p in pages_data[:5]:
    print(f"\n--- PAGE {p['page']} (images: {p['images_count']}) ---")
    print(p['text'][:300])

with open('scripts/ae2024_raw_pages.json', 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, indent=2, ensure_ascii=False)
print("\nSaved scripts/ae2024_raw_pages.json")
