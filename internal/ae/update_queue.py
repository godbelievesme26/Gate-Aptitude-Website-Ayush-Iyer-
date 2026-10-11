import json

with open('internal/ae/ocr_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

with open('internal/ae/forensic_audit_granular.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

for q in audit['questions']:
    if q['overall'] == 'REQUIRES_HUMAN_REVIEW':
        queue.append({
            'id': q['id'],
            'year': q['year'],
            'status': 'REQUIRES_HUMAN_REVIEW',
            'required_verification_fields': ['figure_bbox']
        })

with open('internal/ae/ocr_queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2)

print('Updated queue length:', len(queue))
