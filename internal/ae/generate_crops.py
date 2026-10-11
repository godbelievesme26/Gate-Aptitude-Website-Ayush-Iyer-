import json
import fitz

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

docs = {}
for q in batch:
    qid = q['id']
    y = q['year']
    if y not in docs: docs[y] = fitz.open(f'internal/ae/AE{y}.pdf')
    
    with open(f'data/ae/{y}.json', 'r', encoding='utf-8') as f:
        y_data = json.load(f)
    qjson = next(x for x in y_data['questions'] if x['id'] == qid)
    page_num = qjson['source']['pages'][0]['page']
    
    # We will just render the whole page for simplicity, scaled down slightly
    pix = docs[y][page_num-1].get_pixmap(dpi=72)
    pix.save(f'internal/ae/audit_renders/batch_{qid}.png')
    print(f'Rendered {qid}')
