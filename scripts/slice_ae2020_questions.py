import fitz
import os

doc = fitz.open("internal/ae/AE2020.pdf")
os.makedirs("tmp/ae2020_questions", exist_ok=True)

# Find all Q.No. markers
q_markers = []
for page_idx in range(15):
    page = doc[page_idx]
    blocks = page.get_text("blocks")
    for b in blocks:
        text = b[4].strip()
        if text.startswith("Q.No."):
            q_markers.append({
                "page": page_idx + 1,
                "text": text,
                "bbox": b[:4]
            })

print(f"Found {len(q_markers)} question markers:")
for m in q_markers:
    print(f"  Page {m['page']}: {m['text']} at y={m['bbox'][1]:.1f}")
