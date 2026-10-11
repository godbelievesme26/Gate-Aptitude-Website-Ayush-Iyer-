import json

with open('data/ae/2010.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['questions']:
    num = q['number']
    qtext = q['question']
    if '\\' in qtext and '$' not in qtext:
        print(f'Q{num} text missing $: {qtext}')
    for opt in q['options']:
        otext = opt['text']
        if '\\' in otext and '$' not in otext:
            print(f'Q{num} opt {opt["label"]} missing $: {otext}')

for group in d.get('questionGroups', []):
    for c in group.get('content', []):
        if c.get('type') == 'text':
            t = c['text']
            if '\\' in t and '$' not in t:
                print(f'Group {group["id"]} text missing $: {t}')
