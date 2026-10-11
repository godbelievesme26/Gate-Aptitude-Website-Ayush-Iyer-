import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

print("=== PAGE 25 (Q.37) ===")
print(pages[24]['text'])
