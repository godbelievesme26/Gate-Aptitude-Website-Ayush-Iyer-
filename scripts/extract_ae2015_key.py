import fitz
import json
import re

doc = fitz.open('internal/ae/AE2015.pdf')
green_xrefs = {227, 228, 173, 179, 250}

# Collect all question definitions
# Each question has a header 'Question Number : X  Question Type : Y'
# and either 'Options :' with 4 option icons (for MCQ) or 'Correct Answer :' (for NAT)

questions_key = {}

# Let's map questions across pages
q_headers = []
for pno, page in enumerate(doc):
    blocks = page.get_text('blocks')
    for b in blocks:
        text = b[4].strip()
        if text.startswith('Question Number :'):
            parts = text.split('Question Type :')
            q_num = int(parts[0].replace('Question Number :', '').strip())
            q_type = parts[1].strip() if len(parts) > 1 else 'MCQ'
            q_headers.append({
                'num': q_num,
                'type': q_type,
                'pno': pno,
                'rect': fitz.Rect(b[:4])
            })

q_headers.sort(key=lambda x: x['num'])

for idx, q in enumerate(q_headers):
    q_num = q['num']
    q_type = q['type']
    pno = q['pno']
    page = doc[pno]
    
    # Range of this question
    # Starts at q['rect'].y0
    # Ends at next question on this page, or if none, check next page before first question
    next_q = q_headers[idx + 1] if idx + 1 < len(q_headers) else None
    
    if q_type == 'NAT':
        # Search for 'Correct Answer :' in text on this page or next page
        # Collect text blocks from this question onwards
        found_ans = None
        # check this page
        for b in page.get_text('blocks'):
            if b[1] >= q['rect'].y0:
                if 'Correct Answer' in b[4]:
                    lines = [l.strip() for l in b[4].split('\n') if l.strip()]
                    for l_idx, l in enumerate(lines):
                        if 'Correct Answer' in l and l_idx + 1 < len(lines):
                            found_ans = lines[l_idx + 1]
                        elif 'Correct Answer:' in l:
                            found_ans = l.replace('Correct Answer:', '').strip()
        # if not found, check top of next page
        if not found_ans and pno + 1 < len(doc):
            next_page = doc[pno + 1]
            for b in next_page.get_text('blocks'):
                if next_q and b[1] >= next_q['rect'].y0 and next_q['pno'] == pno + 1:
                    break
                if 'Correct Answer' in b[4]:
                    lines = [l.strip() for l in b[4].split('\n') if l.strip()]
                    for l_idx, l in enumerate(lines):
                        if 'Correct Answer' in l and l_idx + 1 < len(lines):
                            found_ans = lines[l_idx + 1]
                        elif 'Correct Answer:' in l:
                            found_ans = l.replace('Correct Answer:', '').strip()
        
        # parse range or single value
        # e.g. "24.99 to 25.01" or "280"
        questions_key[f"AE2015-Q{q_num:02d}"] = {
            "questionNumber": q_num,
            "type": "NAT",
            "rawKey": found_ans
        }
    else: # MCQ
        # Find the 4 option icons between q['rect'].y0 and next question
        # Option icons on this page after q['rect'].y0
        option_icons = []
        for img in page.get_images():
            xref = img[0]
            rects = page.get_image_rects(xref)
            for r in rects:
                if r.height < 30 and r.y0 >= q['rect'].y0:
                    if next_q and next_q['pno'] == pno and r.y0 >= next_q['rect'].y0:
                        continue
                    option_icons.append({'xref': xref, 'y0': r.y0, 'is_green': xref in green_xrefs})
        
        # If fewer than 4 icons and next page exists before next question
        if len(option_icons) < 4 and pno + 1 < len(doc):
            next_page = doc[pno + 1]
            for img in next_page.get_images():
                xref = img[0]
                rects = next_page.get_image_rects(xref)
                for r in rects:
                    if r.height < 30:
                        if next_q and next_q['pno'] == pno + 1 and r.y0 >= next_q['rect'].y0:
                            continue
                        option_icons.append({'xref': xref, 'y0': r.y0, 'is_green': xref in green_xrefs})
        
        option_icons.sort(key=lambda x: x['y0'])
        
        correct_letter = None
        for opt_idx, opt in enumerate(option_icons):
            if opt['is_green']:
                correct_letter = chr(ord('A') + opt_idx)
                break
        
        questions_key[f"AE2015-Q{q_num:02d}"] = {
            "questionNumber": q_num,
            "type": "MCQ",
            "numOptionIcons": len(option_icons),
            "correctOption": correct_letter
        }

print("Extracted key for all 65 questions:")
for qid in sorted(questions_key.keys()):
    print(f"{qid}: {questions_key[qid]}")

with open('internal/ae/AE2015-key.json', 'w', encoding='utf-8') as f:
    json.dump(questions_key, f, indent=2)
print("Saved internal/ae/AE2015-key.json")
