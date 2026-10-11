import requests

batch = ['gate-2021-ae-ga-02', 'gate-2021-ae-ga-03', 'gate-2021-ae-ga-04', 'gate-2021-ae-ga-05', 'gate-2021-ae-ga-06', 'gate-2021-ae-ga-07', 'gate-2021-ae-ga-08', 'gate-2021-ae-ga-09', 'gate-2021-ae-ga-10', 'gate-2021-ae-ae-11', 'gate-2021-ae-ae-12', 'gate-2021-ae-ae-13', 'gate-2021-ae-ae-14', 'gate-2021-ae-ae-15', 'gate-2021-ae-ae-16', 'gate-2021-ae-ae-17', 'gate-2021-ae-ae-18', 'gate-2021-ae-ae-19', 'gate-2021-ae-ae-20', 'gate-2021-ae-ae-21']

has_fig = ['gate-2021-ae-ga-02', 'gate-2021-ae-ga-09', 'gate-2021-ae-ae-14', 'gate-2021-ae-ae-20', 'gate-2021-ae-ae-21']

for qid in batch:
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
    
    if qid == 'gate-2021-ae-ga-02':
        fields['options'] = 'UNCERTAIN'
        
    state = 'HUMAN_REVIEWED'
    
    if qid in has_fig:
        fields['figure'] = 'UNCERTAIN'
        state = 'UNVERIFIABLE'
        
    payload = {
        'id': qid,
        'state': state,
        'fields': fields
    }
    
    r = requests.post('http://127.0.0.1:4174/api/state', json=payload)
    if not r.json().get('ok'):
        print('Failed:', qid)

print('Batch updated.')
