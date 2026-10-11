import fitz
import json
import hashlib

doc = fitz.open('internal/ae/AE2017-key.pdf')
with open('internal/ae/AE2017-key.pdf', 'rb') as f:
    key_sha256 = hashlib.sha256(f.read()).hexdigest()

raw_rows = []
for page_idx, page in enumerate(doc):
    text = page.get_text()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line in ['Q. No.', 'Q.No.', 'Type', 'Section', 'Key', 'Marks', 'GATE 2017', 'Aerospace Engineering']:
            i += 1
            continue
        
        if line.isdigit():
            qno = int(line)
            qtype = lines[i+1]
            sec = lines[i+2]
            
            j = i + 3
            key_parts = []
            while j < len(lines) and lines[j] not in ['1', '2']:
                key_parts.append(lines[j])
                j += 1
            
            if j < len(lines) and lines[j] in ['1', '2']:
                marks = int(lines[j])
                raw_key = " ".join(key_parts)
                raw_key = raw_key.replace('\u2010', '-').replace('\u2013', '-').replace('\u2014', '-').replace('\xa0', ' ')
                raw_key = raw_key.replace('(or)', 'OR').replace('(OR)', 'OR').replace('Marks-to-All', 'MTA').replace('Marks to All', 'MTA').replace('MTA*', 'MTA')
                
                raw_rows.append({
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

print(f'Parsed {len(raw_rows)} raw key rows.')

# Separate GA and AE
ga_rows = [r for r in raw_rows if r['section'] == 'GA']
ae_rows = [r for r in raw_rows if r['section'] == 'AE']

# Sort GA by sectionQuestionNumber
ga_rows.sort(key=lambda x: x['sectionQuestionNumber'])
# Sort AE by sectionQuestionNumber
ae_rows.sort(key=lambda x: x['sectionQuestionNumber'])

ordered_rows = []
# 1-10: GA
for idx, r in enumerate(ga_rows, start=1):
    r_copy = dict(r)
    r_copy['number'] = idx
    ordered_rows.append(r_copy)

# 11-65: AE
for idx, r in enumerate(ae_rows, start=11):
    r_copy = dict(r)
    r_copy['number'] = idx
    ordered_rows.append(r_copy)

for r in ordered_rows:
    k = r['rawKey'].encode('ascii', 'replace').decode('ascii')
    print(f"Q{r['number']:02d} ({r['section']} {r['sectionQuestionNumber']:02d}): {r['type']} {r['marks']}M key={k}")

key_data = {
    'exam': 'GATE',
    'year': 2017,
    'paper': 'AE',
    'source': 'internal/ae/AE2017-key.pdf',
    'sha256': key_sha256,
    'totalQuestions': len(ordered_rows),
    'totalMarks': sum(r['marks'] for r in ordered_rows),
    'rows': ordered_rows
}

with open('internal/ae/AE2017-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_data, f, indent=2, ensure_ascii=False)

print('Saved internal/ae/AE2017-key.json')
