import json
import fitz

batch2 = ['gate-2021-ae-ga-02', 'gate-2021-ae-ga-09', 'gate-2021-ae-ae-14', 'gate-2021-ae-ae-20', 'gate-2021-ae-ae-21', 
          'gate-2021-ae-ae-22', 'gate-2021-ae-ae-23', 'gate-2021-ae-ae-24', 'gate-2021-ae-ae-25', 'gate-2021-ae-ae-26', 
          'gate-2021-ae-ae-27', 'gate-2021-ae-ae-28', 'gate-2021-ae-ae-29', 'gate-2021-ae-ae-30', 'gate-2021-ae-ae-31', 
          'gate-2021-ae-ae-32', 'gate-2021-ae-ae-33', 'gate-2021-ae-ae-34', 'gate-2021-ae-ae-35', 'gate-2021-ae-ae-36']

docs = fitz.open('internal/ae/AE2021.pdf')
with open('data/ae/2021.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for qid in batch2:
    qjson = next(x for x in d['questions'] if x['id'] == qid)
    page_num = qjson['source']['pages'][0]['page']
    pix = docs[page_num-1].get_pixmap(dpi=72)
    pix.save(f'internal/ae/audit_renders/batch2_{qid}.png')
print('Batch 2 renders generated.')
