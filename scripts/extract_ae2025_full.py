import pymupdf
import json
import re
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

doc = pymupdf.open('internal/ae/AE2025.pdf')
key_doc = pymupdf.open('internal/ae/AE2025-key.pdf')

# 1. Parse official key
keys = {}
for page in key_doc:
    lines = page.get_text().splitlines()
    for line in lines:
        # e.g., "1 5 MCQ GA A 1" or "34 5 NAT AE 0.16 to 0.17 1"
        m = re.match(r'^\s*(\d+)\s+(\d+)\s+(MCQ|MSQ|NAT)\s+(GA|AE)\s+(.+?)\s+([12])\s*$', line)
        if m:
            qnum, session, qtype, section, raw_key, marks = m.groups()
            keys[int(qnum)] = {
                'number': int(qnum),
                'session': int(session),
                'type': qtype,
                'section': section,
                'rawKey': raw_key,
                'marks': int(marks)
            }

print(f"Parsed {len(keys)} keys from official key PDF.")

# 2. Extract full text from AE2025.pdf
pages_text = []
for pno, page in enumerate(doc, 1):
    text = page.get_text("text")
    pages_text.append((pno, text, page))

# Let's extract question boundaries across pages
# In GATE papers, questions start with "Q.<number>"
full_text = ""
page_boundaries = []
current_pos = 0
for pno, text, page in pages_text:
    # remove headers/footers if needed
    cleaned_page = text
    # record page index for character positions
    page_boundaries.append((current_pos, current_pos + len(cleaned_page), pno, page))
    full_text += cleaned_page + "\n---PAGE---\n"
    current_pos = len(full_text)

# Search for Q.1 to Q.65
raw_questions = {}
for qnum in range(1, 66):
    pattern = rf'(?:^|\n)Q\.{qnum}\s+(.*?)(?=\nQ\.\d+|\nGATE 2025|\Z)'
    # Find matching block
    matches = list(re.finditer(rf'(?:^|\n)Q\.{qnum}\s+(.*?)(?=(?:\nQ\.(?:[1-9]|[1-5][0-9]|6[0-5])\s+)|\Z)', full_text, re.DOTALL))
    if matches:
        # Take the best match (avoiding sub-references like "Q.1 – Q.5 Carry")
        for m in matches:
            body = m.group(1).strip()
            # If body starts with "– Q.5 Carry", skip
            if re.match(r'^[–−-]\s*Q\.\d+', body):
                continue
            raw_questions[qnum] = body
            break

print(f"Found raw text for {len(raw_questions)} of 65 questions.")
for qnum in range(1, 66):
    if qnum not in raw_questions:
        print(f"MISSING: Q.{qnum}")

# Save extracted raw questions and keys to inspect
with open('internal/ae/AE2025-raw-extracted.json', 'w', encoding='utf-8') as f:
    json.dump({
        'keys': keys,
        'questions': raw_questions
    }, f, ensure_ascii=False, indent=2)

print("Saved internal/ae/AE2025-raw-extracted.json")
