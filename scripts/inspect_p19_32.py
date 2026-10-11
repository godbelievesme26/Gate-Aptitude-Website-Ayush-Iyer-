import pymupdf
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('internal/ae/AE2025-pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

print("=== PAGE 19 ===")
print(pages[18]['text'])

print("=== PAGE 32 ===")
print(pages[31]['text'])
