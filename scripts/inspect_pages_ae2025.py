import pymupdf
import json
import re
import hashlib
from PIL import Image, ImageChops
from pathlib import Path

doc = pymupdf.open('internal/ae/AE2025.pdf')
key_doc = pymupdf.open('internal/ae/AE2025-key.pdf')

# 1. Parse Key
lines = [l.strip() for p in key_doc for l in p.get_text().splitlines() if l.strip()]
keys = {}
i = 0
while i < len(lines):
    if lines[i] in ['Answer Key for Aerospace Engineering (AE)', 'Q. No.', 'Session', 'Q. Type', 'Section', 'Key/Range', 'Marks', 'Page 1 of 2', 'Page 2 of 2']:
        i += 1
        continue
    if lines[i].isdigit() and i + 5 < len(lines) and lines[i+2] in ['MCQ', 'MSQ', 'NAT']:
        num = int(lines[i])
        keys[num] = {
            'number': num,
            'session': int(lines[i+1]),
            'type': lines[i+2],
            'section': lines[i+3],
            'rawKey': lines[i+4],
            'marks': int(lines[i+5])
        }
        i += 6
    else:
        i += 1

print(f"Parsed {len(keys)} official keys.")
assert len(keys) == 65
assert sorted(keys.keys()) == list(range(1, 66))

# Write AE2025-key.json
key_hash = hashlib.sha256(Path('internal/ae/AE2025-key.pdf').read_bytes()).hexdigest()
with open('internal/ae/AE2025-key.json', 'w', encoding='utf-8') as f:
    json.dump({
        'source': 'internal/ae/AE2025-key.pdf',
        'sha256': key_hash,
        'url': 'https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf',
        'rows': list(keys.values())
    }, f, ensure_ascii=False, indent=2)

# 2. Inspect Question Text and Images by Page
page_info = []
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text()
    imgs = page.get_images()
    page_info.append({
        'page': pno + 1,
        'text': text,
        'image_count': len(imgs),
        'images': imgs
    })

# Let's inspect where questions are located across the 34 pages
q_map = {}
for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text()
    # Find occurrences of Q.<number>
    matches = list(re.finditer(r'(?:^|\n)Q\.(\d+)\s+', text))
    for m in matches:
        qnum = int(m.group(1))
        # Skip section range notes like Q.1 - Q.5 Carry ONE mark
        start_idx = m.end()
        following = text[start_idx:start_idx+30]
        if re.match(r'^[–−-]\s*Q\.\d+', following):
            continue
        if qnum not in q_map:
            q_map[qnum] = []
        q_map[qnum].append(pno + 1)

print(f"Mapped {len(q_map)} questions to pages.")
for qnum in range(1, 66):
    pages = q_map.get(qnum, [])
    print(f"Q.{qnum:02d} -> Page(s): {pages}, Type: {keys[qnum]['type']}, Marks: {keys[qnum]['marks']}, Key: {keys[qnum]['rawKey']}")
