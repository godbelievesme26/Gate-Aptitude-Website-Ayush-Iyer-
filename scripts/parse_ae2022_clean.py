import sys
import re
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2022.pdf')

full_doc_lines = []
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    for line in txt.split('\n'):
        l = line.strip()
        if 'GATE 2022 Aerospace Engineering (AE)' in l or re.match(r'^Page \d+ of \d+', l):
            continue
        full_doc_lines.append(l)

questions_text = {}
current_q = None
current_lines = []

for line in full_doc_lines:
    if re.match(r'^Q\.\s*\d+\s*[-–—]\s*Q\.\s*\d+', line):
        continue
    
    m = re.match(r'^Q\.?\s*(\d+)\b', line)
    if m:
        qnum = int(m.group(1))
        if 1 <= qnum <= 65:
            if current_q is not None:
                questions_text[current_q] = "\n".join(current_lines).strip()
            current_q = qnum
            current_lines = [line]
            continue
            
    if current_q is not None:
        current_lines.append(line)

if current_q is not None:
    questions_text[current_q] = "\n".join(current_lines).strip()

print(f"Parsed {len(questions_text)} questions for AE2022 (Q1 to Q{max(questions_text.keys())})")

with open('scripts/parse_ae2022_blocks.py', 'w', encoding='utf-8') as f:
    f.write("# Parsed blocks for AE2022\n")
    f.write("q_blocks = " + repr(questions_text) + "\n")

print("Saved scripts/parse_ae2022_blocks.py")
