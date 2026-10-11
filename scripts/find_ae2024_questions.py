import sys
import json
import fitz
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'AE PYQ Papers/AE2024.pdf'
doc = fitz.open(pdf_path)

# Let's inspect where Q.1 to Q.65 appear across the pages
q_pattern = re.compile(r'Q\.(\d+)\b')

question_locations = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text('text')
    matches = list(q_pattern.finditer(text))
    # Filter out header matches like "Q.1 – Q.5 Carry ONE mark"
    valid_qs = []
    for m in matches:
        qnum = int(m.group(1))
        # check surrounding text
        start = max(0, m.start() - 10)
        end = min(len(text), m.end() + 20)
        snippet = text[start:end].replace('\n', ' ')
        if '–' not in snippet and '-' not in snippet and 'Carry' not in snippet:
            valid_qs.append((qnum, m.start(), pno + 1))
    
    # print summary
    if valid_qs:
        print(f"Page {pno+1}: Questions found -> {[q[0] for q in valid_qs]}")
