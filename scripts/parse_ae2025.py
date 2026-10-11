import pymupdf
import json
import re

doc = pymupdf.open('internal/ae/AE2025.pdf')

questions = {}

for page_idx in range(len(doc)):
    page = doc[page_idx]
    text = page.get_text()
    
    # Split text by Q.X
    blocks = re.split(r'\n(?=Q\.(\d+)\s+)', text)
    # The first block might be header or continuation of previous question
    for b in page.get_text("blocks"):
        pass

# Let's write a structured extractor
lines_by_page = []
for pno, page in enumerate(doc, 1):
    text = page.get_text("text")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines_by_page.append((pno, text, lines))

# Let's find question headers
q_positions = []
for pno, text, lines in lines_by_page:
    for m in re.finditer(r'(?:^|\n)Q\.(\d+)\s+(.*?)(?=\nQ\.\d+|\Z)', text, re.DOTALL):
        qnum = int(m.group(1))
        content = m.group(2).strip()
        q_positions.append((qnum, pno, content))

print(f"Extracted {len(q_positions)} question blocks.")
for qnum, pno, content in sorted(q_positions, key=lambda x: x[0]):
    first_line = content.split('\n')[0][:80]
    print(f"Q.{qnum:02d} (Page {pno:02d}): {first_line}")
