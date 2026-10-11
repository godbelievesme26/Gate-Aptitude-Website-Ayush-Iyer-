import json

with open("tmp/ae2020_text.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

for p in pages:
    print(f"=== PAGE {p['page']} ===")
    lines = p['text'].split('\n')
    for line in lines[:10]:
        print(line)
    print("...")
