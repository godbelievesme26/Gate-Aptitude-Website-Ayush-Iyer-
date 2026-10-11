import sys
import re
import json
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2023.pdf')

full_text = ""
pages_text = []
for pno in range(len(doc)):
    txt = doc[pno].get_text('text')
    pages_text.append(txt)

# Split by Q.1, Q.2, ... Q.65
# Find page and position for each question
q_raw = {}

# Regex for question start
q_starts = []
for pno, ptxt in enumerate(pages_text):
    for m in re.finditer(r'(?:^|\n)Q\.(\d+)\b', ptxt):
        qnum = int(m.group(1))
        if 1 <= qnum <= 65:
            q_starts.append((qnum, pno + 1, m.start()))

# Sort by question number
q_starts.sort(key=lambda x: x[0])
print(f"Detected {len(q_starts)} questions in PDF text.")

# Extract blocks for each question
for idx, (qnum, page_num, pos) in enumerate(q_starts):
    # Find text between this Q.X and the next Q.Y (or end of question paper)
    p_text = pages_text[page_num - 1]
    
    # If next question is on same page:
    if idx + 1 < len(q_starts) and q_starts[idx + 1][1] == page_num:
        next_pos = q_starts[idx + 1][2]
        block = p_text[pos:next_pos]
    else:
        # Takes rest of page, and if next question is on subsequent page, check intermediate content
        block = p_text[pos:]
        # If question spans across pages
        next_page = q_starts[idx + 1][1] if idx + 1 < len(q_starts) else len(doc) + 1
        for extra_p in range(page_num, min(next_page, page_num + 2)):
            extra_text = pages_text[extra_p]
            if idx + 1 < len(q_starts) and extra_p + 1 == q_starts[idx + 1][1]:
                extra_block = extra_text[:q_starts[idx + 1][2]]
            else:
                extra_block = extra_text
            block += "\n" + extra_block
            
    q_raw[qnum] = block.strip()

print(f"Successfully extracted {len(q_raw)} question blocks.")

with open('scripts/ae2023_parsed_blocks.py', 'w', encoding='utf-8') as f:
    f.write("# Parsed raw blocks for AE2023\n")
    f.write("raw_blocks = " + repr(q_raw) + "\n")

print("Saved raw blocks to scripts/ae2023_parsed_blocks.py")
