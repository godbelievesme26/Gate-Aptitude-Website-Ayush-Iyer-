import re

f = open('scripts/build_ae2013_dataset.py', 'r', encoding='utf-8').read()
f = f.replace(
    'if q["type"] == "MCQ" and q.get("gradingRule") != "marks-to-all":',
    'if q["type"] == "MCQ":'
)
open('scripts/build_ae2013_dataset.py', 'w', encoding='utf-8').write(f)
