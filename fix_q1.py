import requests

fields = {
    'question': 'MATCH',
    'math': 'MATCH',
    'options': 'MATCH',
    'type': 'MATCH',
    'marks': 'MATCH',
    'groups': 'MATCH',
    'answer': 'MATCH',
    'solution': 'MATCH'
}
payload = {
    'id': 'gate-2021-ae-ga-01',
    'state': 'HUMAN_REVIEWED',
    'fields': fields
}
r = requests.post('http://127.0.0.1:4174/api/state', json=payload)
print('Q1 resolved:', r.json())
