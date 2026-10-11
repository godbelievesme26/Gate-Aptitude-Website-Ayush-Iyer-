import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-raw-extracted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('internal/ae/AE2025-key.json', 'r', encoding='utf-8') as f:
    key_data = json.load(f)

key_map = {r['number']: r for r in key_data['rows']}

for qnum in range(11, 66):
    qstr = str(qnum)
    body = data['questions'][qstr]
    k = key_map[qnum]
    print(f"\n{'='*70}\n[Q.{qnum:02d}] Type: {k['type']}, Marks: {k['marks']}, Key: {k['rawKey']}")
    print(body)
