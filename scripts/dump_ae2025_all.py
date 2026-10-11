import pymupdf
import json

doc = pymupdf.open('internal/ae/AE2025.pdf')

pages_data = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text("text")
    blocks = page.get_text("blocks")
    imgs = page.get_images()
    
    extracted_imgs = []
    for img in imgs:
        xref = img[0]
        base_img = doc.extract_image(xref)
        if base_img['width'] != 1252 and base_img['width'] != 166:
            extracted_imgs.append({
                'xref': xref,
                'width': base_img['width'],
                'height': base_img['height'],
                'ext': base_img['ext']
            })
            
    pages_data.append({
        'page': pno + 1,
        'text': text,
        'blocks': blocks,
        'images': extracted_imgs
    })

with open('internal/ae/AE2025-pages.json', 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print("Saved internal/ae/AE2025-pages.json successfully.")
