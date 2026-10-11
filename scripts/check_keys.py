import json

for y in [2026, 2025, 2024, 2023]:
    with open(f'internal/ae/AE{y}-key.json', 'r') as f:
        d = json.load(f)
    for r in d['rows']:
        rk = str(r.get('rawKey', ''))
        if 'OR' in rk or ';' in rk or ' to ' in rk or ' ' in rk:
            print(f'{y} Q{r["number"]}: type={r["type"]}, rawKey={rk}')
