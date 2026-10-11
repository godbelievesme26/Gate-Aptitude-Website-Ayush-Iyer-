import os
import fitz
import json

doc = fitz.open("internal/ae/AE2020.pdf")
print(f"AE2020.pdf has {len(doc)} pages.")

os.makedirs("tmp/ae2020_pages", exist_ok=True)

pages_data = []
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text")
    pages_data.append({
        "page": page_num + 1,
        "text": text
    })
    
    pix = page.get_pixmap(dpi=200)
    pix.save(f"tmp/ae2020_pages/page_{page_num+1:02d}.png")

with open("tmp/ae2020_text.json", "w", encoding="utf-8") as f:
    json.dump(pages_data, f, indent=2, ensure_ascii=False)

print("Saved page images and text dump to tmp/.")
