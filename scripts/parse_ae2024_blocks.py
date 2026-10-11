import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/ae2024_full_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect each question block from Q.1 to Q.65
pattern = re.compile(r'Q\.(\d+)\s*\n')
matches = list(pattern.finditer(text))
print(f"Total Q.XX matches: {len(matches)}")

q_blocks = {}
for i in range(len(matches)):
    qnum = int(matches[i].group(1))
    start_pos = matches[i].start()
    end_pos = matches[i+1].start() if i+1 < len(matches) else len(text)
    block_text = text[start_pos:end_pos].strip()
    q_blocks[qnum] = block_text

print(f"Unique question numbers parsed: {len(q_blocks)} (keys: {min(q_blocks.keys())} to {max(q_blocks.keys())})")
for qnum in sorted(q_blocks.keys()):
    first_line = q_blocks[qnum].split('\n')[0]
    second_line = q_blocks[qnum].split('\n')[1] if len(q_blocks[qnum].split('\n')) > 1 else ''
    print(f"Q{qnum:02d}: {first_line} | {second_line[:60]}")
