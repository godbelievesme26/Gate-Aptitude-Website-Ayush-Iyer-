import json
import re

with open('internal/ae/AE2023-pages.json', encoding='utf-8') as f:
    pages = json.load(f)

full_text = ""
for p in pages:
    full_text += f"\n--- PAGE {p['page']} ---\n" + p['text']

with open('scratch/ae2023_all_text.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Saved scratch/ae2023_all_text.txt")
