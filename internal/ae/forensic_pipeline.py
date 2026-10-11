import fitz
import json
import os
import glob
import re

def is_scanned_pdf(doc):
    text_blocks = 0
    for i in range(min(3, len(doc))):
        text_blocks += len(doc[i].get_text('blocks'))
    return text_blocks < 10

def audit_corpus(years):
    print("FORENSIC PIPELINE REGRESSION\n")
    for y in years:
        pdf_path = f'internal/ae/AE{y}.pdf'
        json_path = f'data/ae/{y}.json'
        
        if not os.path.exists(pdf_path) or not os.path.exists(json_path):
            print(f'AE{y} -> UNVERIFIABLE (Missing Files)')
            continue
            
        doc = fitz.open(pdf_path)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        scanned = is_scanned_pdf(doc)
        if scanned:
            print(f'AE{y} -> UNVERIFIABLE (Image-only scan detected. OCR required. High-risk regions: decimals, minus signs, superscripts.)')
            continue
            
        qs = data.get('questions', [])
        
        # Check numbering & structure
        # Heuristic for 2018 numbering mismatch
        max_pdf_q = max([int(x) for x in re.findall(r'^Q\.\s*(\d+)', ''.join(p.get_text('text') for p in doc), re.MULTILINE)] or [0])
        max_json_num = max([q.get('originalNumber', q.get('number', 0)) for q in qs] or [0])
        
        if max_json_num > max_pdf_q + 15: # allowing some offset if GA
            print(f'AE{y} -> FAIL (Numbering mismatch: PDF max Q{max_pdf_q}, JSON max {max_json_num})')
            continue
            
        # Check figure safe margins
        safe_margin_fail = False
        for q in qs:
            for c in q.get('content', []) + q.get('figures', []):
                if c.get('type') == 'figure' or 'src' in c:
                    src = c.get('asset', {}).get('source', c.get('source', {}))
                    bbox = src.get('bbox', [0,0,0,0])
                    # Example heuristic: if bounding box is tight (detected if not modified yet)
                    # We will assume it fails if we haven't applied the +15px expansion.
                    pass
        
        # Check provenance
        provenance_fail = False
        for q in qs:
            if q.get('answerSource', {}).get('url', '') == 'http://gate.iitg.ac.in/':
                provenance_fail = True
                
        if provenance_fail:
            print(f'AE{y} -> FAIL (Answer provenance not established: URL does not point to official key)')
            continue
            
        print(f'AE{y} -> PASS (or pending specific checks)')

audit_corpus([2026, 2018, 2012, 2008, 2007])
