import fitz
import json
import re
import os

years = [2026, 2018, 2012, 2008, 2007]

def clean_text(t):
    t = re.sub(r'\s+', ' ', t.replace('\n', ' '))
    return t.strip()

for y in years:
    print(f'==== RED TEAM AUDIT: AE{y} ====')
    pdf_path = f'internal/ae/AE{y}.pdf'
    json_path = f'data/ae/{y}.json'
    
    doc = fitz.open(pdf_path)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    qs = data.get('questions', [])
    
    # Extract PDF blocks
    pdf_text = ''
    for page in doc:
        pdf_text += page.get_text('text')
    
    # 1. Check counts
    q_matches = re.findall(r'^Q\.\s*(\d+)', pdf_text, re.MULTILINE)
    pdf_q_count = len(set(q_matches))
    print(f'PDF Question Numbers Found: {pdf_q_count} | JSON Questions: {len(qs)}')
    
    # 2. Extract numbers to check for numerical alteration
    json_numbers = []
    for q in qs:
        txt = q['question']
        if 'options' in q:
            for o in q['options']:
                txt += ' ' + o['text']
        nums = re.findall(r'\d+\.\d+|\d+', txt)
        json_numbers.extend(nums)
        
    print(f'Total Numerical Tokens in JSON: {len(json_numbers)}')
    
    # 3. Figure Crop Margin Check (Heuristic: are borders within 5px of a drawing?)
    # Since we can't do pixel gradient analysis easily in pure python here, we'll check bounding box sizes
    fig_count = 0
    small_crops = 0
    for q in qs:
        for c in q.get('content', []):
            if c['type'] == 'figure':
                fig_count += 1
                bbox = c['asset']['source'].get('bbox', [0,0,0,0])
                if bbox[2]-bbox[0] < 20 or bbox[3]-bbox[1] < 20:
                    small_crops += 1
    print(f'Figures Checked: {fig_count} | Suspicious tight crops: {small_crops}')
    
    # 4. Answers
    off_key = 0
    for q in qs:
        if q.get('answerSource', {}).get('url', '').endswith('.pdf'):
            off_key += 1
    print(f'Official Answer Provenance: {off_key}/{len(qs)}\n')

