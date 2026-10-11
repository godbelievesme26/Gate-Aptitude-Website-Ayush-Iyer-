import pymupdf
import json
import re

doc = pymupdf.open('internal/ae/AE2025.pdf')
print(f"Total pages: {len(doc)}")

questions_found = []
images_found = []

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    # Check images on page
    imgs = page.get_images()
    for img in imgs:
        xref = img[0]
        base_image = doc.extract_image(xref)
        images_found.append({
            'page': page_num + 1,
            'xref': xref,
            'width': base_image['width'],
            'height': base_image['height'],
            'ext': base_image['ext']
        })
        
    # Search for question patterns: Q.1 to Q.65
    for match in re.finditer(r'Q\.(\d+)\s+', text):
        qnum = int(match.group(1))
        questions_found.append({
            'qnum': qnum,
            'page': page_num + 1,
            'start': match.start()
        })

print(f"Total question occurrences: {len(questions_found)}")
print("Questions by number:", sorted(set(q['qnum'] for q in questions_found)))
print(f"Total images found: {len(images_found)}")
for img in images_found:
    print(f"  Page {img['page']}: xref {img['xref']}, {img['width']}x{img['height']}, {img['ext']}")
