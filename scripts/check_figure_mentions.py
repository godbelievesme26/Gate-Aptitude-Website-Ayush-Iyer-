import pymupdf
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Combine all AE pages text (page 10 to 34)
ae_text = "\n".join(p['text'] for p in pages if p['page'] >= 10)

# Find all questions mentioning 'figure' or 'shown' or 'table'
for m in re.finditer(r'(Q\.\d+)\s+(.*?)(?=\nQ\.\d+|\Z)', ae_text, re.DOTALL):
    qhead = m.group(1)
    body = m.group(2)
    qnum = int(qhead[2:])
    if '–' in qhead or 'Carry' in body[:30]:
        continue
    has_fig_word = bool(re.search(r'\b(figure|fig\.|shown in the figure|diagram|table)\b', body, re.I))
    print(f"Q.{qnum:02d}: mentions fig/table -> {has_fig_word}")
    if has_fig_word:
        snippet = re.sub(r'\s+', ' ', body[:140])
        print(f"   Snippet: {snippet}")
