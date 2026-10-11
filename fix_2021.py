import requests, json
res = requests.get('http://127.0.0.1:4174/api/question/gate-2021-ae-ga-01')
q = res.json()
old_q = q['question']
new_q = old_q.replace(chr(0xfffd), "'")
print('Before:', repr(old_q))
print('After:', repr(new_q))
payload = {
    'id': 'gate-2021-ae-ga-01',
    'field': 'question',
    'previousValue': old_q,
    'newValue': new_q,
    'reviewerAction': 'HUMAN_CORRECTED',
    'sourcePage': 1
}
r = requests.post('http://127.0.0.1:4174/api/update-canonical', json=payload)
print('Status:', r.json())
