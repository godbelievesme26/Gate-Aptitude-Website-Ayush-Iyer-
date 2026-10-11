import json

with open('internal/ae/forensic_audit_granular.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

ocr_queue = []

for q in audit_data['questions']:
    if q['overall'] == 'UNVERIFIABLE':
        ocr_queue.append({
            'id': q['id'],
            'year': q['year'],
            'status': 'UNVERIFIABLE',
            'required_verification_fields': [
                'question_text', 'mathematics', 'numerical_values', 'options', 'type', 'marks'
            ]
        })

with open('internal/ae/ocr_queue.json', 'w', encoding='utf-8') as f:
    json.dump(ocr_queue, f, indent=2)

print('OCR Queue length:', len(ocr_queue))
