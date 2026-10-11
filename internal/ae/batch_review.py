import json
import fitz
import re

with open('internal/ae/ocr_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)
with open('internal/ae/forensic_review_state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

batch = []
for q in queue:
    s = state.get(q['id'], {}).get('state')
    if s not in ['HUMAN_REVIEWED', 'SOURCE_UNCLEAR', 'CORRECTION_REQUIRED']:
        batch.append(q)
    if len(batch) >= 20: break

year_data = {}
for q in batch:
    y = q['year']
    if y not in year_data:
        with open(f'data/ae/{y}.json', 'r', encoding='utf-8') as f:
            year_data[y] = json.load(f)

doc = fitz.open('internal/ae/AE2021.pdf')

for q in batch:
    qid = q['id']
    y = q['year']
    qjson = next(x for x in year_data[y]['questions'] if x['id'] == qid)
    page_num = qjson['source']['pages'][0]['page']
    
    # Text from fitz
    text = doc[page_num-1].get_text('text')
    # Basic cleanup
    text = text.replace(chr(0xFFFD), "'")
    
    print(f"--- {qid} ---")
    print("CANONICAL:")
    print(qjson.get('question', '')[:200])
    print("FITZ PDF TEXT (snippet):")
    # find the text in fitz roughly matching the start
    start_str = qjson.get('question', '')[:20].replace('\\n', ' ')
    print("PDF contains?", start_str in text.replace('\n', ' '))
    print()
