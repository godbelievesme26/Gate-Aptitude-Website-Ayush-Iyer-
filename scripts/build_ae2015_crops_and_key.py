import fitz
import json
import os
import re

doc = fitz.open('internal/ae/AE2015.pdf')
green_xrefs = {227, 228, 173, 179, 250}

# Step 1: Collect all question headers with page and y0
q_list = []
for pno in range(len(doc)):
    page = doc[pno]
    blocks = page.get_text('blocks')
    for b in blocks:
        text = b[4].strip()
        if text.startswith('Question Number :'):
            parts = text.split('Question Type :')
            q_num = int(parts[0].replace('Question Number :', '').strip())
            q_type = parts[1].strip() if len(parts) > 1 else 'MCQ'
            q_list.append({
                'num': q_num,
                'type': q_type,
                'pno': pno,
                'y0': b[1],
                'y1': b[3]
            })

q_list.sort(key=lambda x: x['num'])

# Step 2: Determine exact start and end for each question
# A question starts at (pno, y0)
# And ends at the start of the next question, or page bottom if it continues
processed_keys = {}

for idx in range(len(q_list)):
    q = q_list[idx]
    q_num = q['num']
    q_type = q['type']
    pno = q['pno']
    y0 = q['y0']
    
    next_q = q_list[idx + 1] if idx + 1 < len(q_list) else None
    
    # Collect all image icons and text blocks belonging strictly to this question
    # On page pno (from y0 down to next_q.y0 if on same page, else down to page bottom)
    # On page pno + 1 (from top down to next_q.y0 if next_q is on pno + 1, else all)
    
    q_pages = []
    if next_q is None or next_q['pno'] == pno:
        end_y = next_q['y0'] if next_q else doc[pno].rect.height
        q_pages.append((pno, y0, end_y))
    else:
        # Question spans from pno (y0 to bottom) to next_q['pno'] (top to next_q['y0'])
        q_pages.append((pno, y0, doc[pno].rect.height))
        for mid_pno in range(pno + 1, next_q['pno']):
            q_pages.append((mid_pno, 0, doc[mid_pno].rect.height))
        q_pages.append((next_q['pno'], 0, next_q['y0']))
    
    # Extract data within these bounds
    all_text = []
    option_icons = []
    
    for (page_idx, top_y, bot_y) in q_pages:
        page = doc[page_idx]
        for b in page.get_text('blocks'):
            # check if block intersects [top_y, bot_y]
            if b[3] > top_y and b[1] < bot_y:
                all_text.append(b[4].strip())
        
        for img in page.get_images():
            xref = img[0]
            for r in page.get_image_rects(xref):
                if r.y1 > top_y and r.y0 < bot_y:
                    if r.height < 30:
                        # option icon
                        option_icons.append({'page': page_idx, 'y0': r.y0, 'xref': xref, 'is_green': xref in green_xrefs})
    
    # Sort option icons by page, then y0
    option_icons.sort(key=lambda x: (x['page'], x['y0']))
    
    full_str = "\n".join(all_text)
    
    if q_type == 'NAT':
        # Find Correct Answer :
        m = re.search(r'Correct Answer\s*:\s*([^\n]+)', full_str)
        if not m:
            m = re.search(r'Correct Answer\s*\n([^\n]+)', full_str)
        ans = m.group(1).strip() if m else None
        processed_keys[f"AE2015-Q{q_num:02d}"] = {
            "questionNumber": q_num,
            "type": "NAT",
            "rawKey": ans,
            "pages": [p[0] + 1 for p in q_pages]
        }
    else: # MCQ
        correct_letter = None
        for opt_idx, opt in enumerate(option_icons):
            if opt['is_green']:
                correct_letter = chr(ord('A') + opt_idx)
                break
        processed_keys[f"AE2015-Q{q_num:02d}"] = {
            "questionNumber": q_num,
            "type": "MCQ",
            "numOptionIcons": len(option_icons),
            "correctOption": correct_letter,
            "pages": [p[0] + 1 for p in q_pages]
        }

print("Accurate Answer Key for AE2015:")
for qid in sorted(processed_keys.keys()):
    print(f"{qid}: {processed_keys[qid]}")

with open('internal/ae/AE2015-key.json', 'w', encoding='utf-8') as f:
    json.dump(processed_keys, f, indent=2)
