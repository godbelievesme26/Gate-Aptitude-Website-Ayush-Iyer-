import sys
import re
import fitz

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('internal/ae/AE2023.pdf')

full_doc_lines = []
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text('text')
    for line in txt.split('\n'):
        # Strip header/footer artifacts
        l = line.strip()
        if 'Aerospace Engineering (AE)' in l or 'Organizing Institute: IIT Kanpur' in l or re.match(r'^Page \d+ of \d+', l):
            continue
        full_doc_lines.append(l)

# Now iterate through lines and gather questions
questions_text = {}
current_q = None
current_lines = []

for line in full_doc_lines:
    # Check if this line is a section header like "Q.1 – Q.5 Carry ONE mark Each"
    if re.match(r'^Q\.\s*\d+\s*[-–—]\s*Q\.\s*\d+', line):
        continue
    
    # Check for question start: Q.X or Q. X
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

print(f"Parsed {len(questions_text)} questions (Q1 to Q{max(questions_text.keys())})")

with open('scripts/parse_ae2023_blocks.py', 'w', encoding='utf-8') as f:
    f.write("# Parsed blocks for AE2023\n")
    f.write("q_blocks = " + repr(questions_text) + "\n")

print("Saved scripts/parse_ae2023_blocks.py")
