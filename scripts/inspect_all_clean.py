import json
import re

with open('internal/ae/AE2023-pages.json', encoding='utf-8') as f:
    pages = json.load(f)

# Let's parse each question block
for p in pages:
    lines = p['text'].splitlines()
    print(f"\n================ PAGE {p['page']} ================")
    for l in lines:
        if l.strip() and not any(h in l for h in ['Aerospace Engineering (AE)', 'Organizing Institute', 'Page ']):
            print(l)
