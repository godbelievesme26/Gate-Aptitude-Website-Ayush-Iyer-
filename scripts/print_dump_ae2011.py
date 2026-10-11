import re

with open('tmp/ae2011_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Print the pages or breakdown
pages = text.split('=== PAGE ')
for p in pages[1:]:
    p_num = p.split(' ===')[0]
    content = p.split(' ===\n', 1)[1] if ' ===\n' in p else p
    print(f"\n==================== PAGE {p_num} ====================")
    print(content)
