import requests, json
res = requests.get('http://127.0.0.1:4174/api/question/gate-2021-ae-ga-07')
q = res.json()
old_q = q['question']
# first  is open quote, second  is close quote
# just replace both with standard straight quotes for safety, or smart quotes
new_q = old_q.replace(chr(0xfffd), '\"')
payload = {
    'id': 'gate-2021-ae-ga-07',
    'field': 'question',
    'previousValue': old_q,
    'newValue': new_q,
    'reviewerAction': 'HUMAN_CORRECTED',
    'sourcePage': 4
}
r = requests.post('http://127.0.0.1:4174/api/update-canonical', json=payload)
print('Status:', r.json())
