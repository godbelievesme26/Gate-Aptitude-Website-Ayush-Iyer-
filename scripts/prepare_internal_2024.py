import sys
import os
import json
import hashlib
import shutil

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('internal/ae', exist_ok=True)

# 1. Copy PDF if not exists
shutil.copy('AE PYQ Papers/AE2024.pdf', 'internal/ae/AE2024.pdf')
shutil.copy('AE PYQ Papers/GATE-Aerospace-2024-Key.pdf', 'internal/ae/AE2024-key.pdf')

with open('internal/ae/AE2024-key.pdf', 'rb') as f:
    key_sha256 = hashlib.sha256(f.read()).hexdigest()

from prepare_ae2024_metadata import official_answers

rows = []
for qnum in range(1, 66):
    ans_info = official_answers[qnum]
    raw_key = ans_info["answer"]
    if isinstance(raw_key, list):
        if ans_info["type"] == "MSQ":
            raw_key_str = ";".join(raw_key)
        else:
            raw_key_str = f"{raw_key[0]} to {raw_key[1]}"
    else:
        raw_key_str = str(raw_key)
    
    rows.append({
        "number": qnum,
        "session": 5,
        "type": ans_info["type"],
        "section": ans_info["section"],
        "rawKey": raw_key_str,
        "marks": ans_info["marks"],
        "page": 1 if qnum <= 28 else 2
    })

key_json = {
    "source": "internal/ae/AE2024-key.pdf",
    "sha256": key_sha256,
    "url": "https://gate2024.iisc.ac.in/",
    "rows": rows
}

with open('internal/ae/AE2024-key.json', 'w', encoding='utf-8') as f:
    json.dump(key_json, f, indent=2, ensure_ascii=False)

print("Saved internal/ae/AE2024-key.json with SHA256:", key_sha256)
