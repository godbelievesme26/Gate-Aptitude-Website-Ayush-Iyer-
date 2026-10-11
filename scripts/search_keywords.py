import json
import re

with open('internal/ae/AE2023-pages.json', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    t = p['text']
    for kw in ['Table', 'Group I', 'Column I', 'Match', 'matrix', 'following']:
        if kw.lower() in t.lower():
            # find question number on this page
            q_matches = list(re.finditer(r'(?:^|\n)Q\.(\d+)', t))
            q_nums = [m.group(1) for m in q_matches]
            print(f"Page {p['page']} has '{kw}' in Qs {q_nums}")
