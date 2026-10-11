import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('internal/ae/AE2021.pdf')

print("Total pages:", len(doc))

full_text = []
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    full_text.append(f"=== Page {pno+1} ===\n{txt}")
    
with open('scripts/ae2021_full_dump.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(full_text))

print("Dumped all pages to scripts/ae2021_full_dump.txt")

# Inspect figures / drawings
print("\n--- Inspecting Figures & Drawings per Page ---")
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    qlines = [l.strip() for l in txt.split('\n') if l.strip().startswith('Q.')]
    imgs = [img for img in page.get_images() if img[0] not in (14, 2909, 1, 368)]
    drawings = [d for d in page.get_drawings() if d['rect'].y0 > 70 and d['rect'].y1 < 750 and d['rect'].width > 10 and d['rect'].height > 10]
    content_drawings = [d for d in drawings if not (d['rect'].width > 400 and d['rect'].height < 5) and not (d['rect'].height > 300 and d['rect'].width < 5)]
    has_fig_word = any(w in txt.lower() for w in ['figure', 'shown', 'schematic', 'below', 'diagram'])
    if imgs or content_drawings or has_fig_word:
        print(f"Page {pno+1}: Qs={qlines}, Imgs={len(imgs)}, ContentDrawings={len(content_drawings)}, HasFigWord={has_fig_word}")
