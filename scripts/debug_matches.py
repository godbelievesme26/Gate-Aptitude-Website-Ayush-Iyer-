import pymupdf
import re

doc = pymupdf.open('internal/ae/AE2025.pdf')
found = []
for page_idx in range(len(doc)):
    text = doc[page_idx].get_text('text')
    starts = list(re.finditer(r'(?:^|\n)Q\.(\d+)\s+(?![–−-])', text))
    for m in starts:
        n = int(m.group(1))
        found.append((n, page_idx + 1))

print(f"Total entries: {len(found)}")
by_num = {}
for n, p in found:
    by_num.setdefault(n, []).append(p)

print(f"Unique numbers: {len(by_num)}")
for n in range(1, 66):
    if n not in by_num:
        print(f"Missing Q.{n}")
    elif len(by_num[n]) > 1:
        print(f"Duplicate Q.{n}: {by_num[n]}")
