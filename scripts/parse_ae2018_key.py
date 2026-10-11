import fitz
import json
import hashlib

doc = fitz.open('internal/ae/AE2018-key.pdf')
with open('internal/ae/AE2018-key.pdf', 'rb') as f:
    key_sha256 = hashlib.sha256(f.read()).hexdigest()

rows = []
for page_idx, page in enumerate(doc):
    text = page.get_text()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line in ['Q.No.', 'Type', 'Section', 'Key/Range', 'Marks', 'GATE 2018', 'Aerospace Engineering (AE)']:
            i += 1
            continue
        
        # We check if lines[i] is a question number
        if line.isdigit():
            qno = int(line)
            qtype = lines[i+1]
            sec = lines[i+2]
            
            # Key might span across lines if there is a newline before marks
            # Find the marks (either 1 or 2)
            # Next token is part of key
            j = i + 3
            key_parts = []
            while j < len(lines) and lines[j] not in ['1', '2']:
                key_parts.append(lines[j])
                j += 1
            
            # Now lines[j] is the marks
            if j < len(lines) and lines[j] in ['1', '2']:
                marks = int(lines[j])
                raw_key = " ".join(key_parts)
                raw_key = raw_key.replace('\u2010', '-').replace('\u2013', '-').replace('\u2014', '-').replace('\xa0', ' ')
                raw_key = raw_key.replace('(or)', 'OR').replace('(OR)', 'OR').replace('Marks-to-All', 'MTA').replace('Marks to All', 'MTA')
                
                rows.append({
                    'sectionQuestionNumber': qno,
                    'type': qtype,
                    'section': sec,
                    'rawKey': raw_key.strip(),
                    'marks': marks
                })
                i = j + 1
            else:
                i += 1
        else:
            i += 1

print(f'Parsed {len(rows)} key rows.')

paper_rows = []
for idx, r in enumerate(rows, start=1):
    r['number'] = idx
    paper_rows.append(r)
    clean_k = r['rawKey'].encode('ascii', 'replace').decode('ascii')
    print(f"Q{idx:02d} (sec {r['section']} {r['sectionQuestionNumber']:02d}): {r['type']} {r['marks']}M key={clean_k}")

key_data = {
    'exam': 'GATE',
    'year': 2018,
    'paper': 'AE',
    'source': 'internal/ae/AE2018-key.pdf',
    'sha256': key_sha256,
    'rowCount': len(paper_rows),
    'rows': paper_rows
}

with open('internal/ae/AE2018-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_data, f, indent=2, ensure_ascii=False)

print('Saved internal/ae/AE2018-key.json')
