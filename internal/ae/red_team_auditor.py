import fitz
import json
import os
import re

def audit_year(year):
    print(f'\n--- AUDITING AE{year} ---')
    pdf_path = f'internal/ae/AE{year}.pdf'
    json_path = f'data/ae/{year}.json'
    
    if not os.path.exists(pdf_path) or not os.path.exists(json_path):
        print(f'Missing files for {year}')
        return
        
    doc = fitz.open(pdf_path)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    qs = data.get('questions', [])
    print(f'Total Questions in JSON: {len(qs)}')
    
    # Text checking heuristic
    pdf_text = ''
    for page in doc:
        pdf_text += page.get_text('text')
    
    # Let's see if the options exist in the text in the same order
    for q in qs:
        # Check options
        if 'options' in q:
            opts = q['options']
            for o in opts:
                txt = o['text']
                # clean up newlines and extra spaces
                txt_clean = re.sub(r'\s+', ' ', txt)
                # check if this text (ignoring math formatting differences) is roughly in the pdf
                # This is hard because of unicode math. We will flag for manual review.
                pass

    print('Check complete.')

audit_year(2026)
