import requests

batch = ['gate-2021-ae-ga-02', 'gate-2021-ae-ga-09', 'gate-2021-ae-ae-14', 'gate-2021-ae-ae-20', 'gate-2021-ae-ae-21', 
          'gate-2021-ae-ae-22', 'gate-2021-ae-ae-23', 'gate-2021-ae-ae-24', 'gate-2021-ae-ae-25', 'gate-2021-ae-ae-26', 
          'gate-2021-ae-ae-27', 'gate-2021-ae-ae-28', 'gate-2021-ae-ae-29', 'gate-2021-ae-ae-30', 'gate-2021-ae-ae-31', 
          'gate-2021-ae-ae-32', 'gate-2021-ae-ae-33', 'gate-2021-ae-ae-34', 'gate-2021-ae-ae-35', 'gate-2021-ae-ae-36']

has_fig = ['gate-2021-ae-ga-02', 'gate-2021-ae-ga-09', 'gate-2021-ae-ae-14', 'gate-2021-ae-ae-20', 'gate-2021-ae-ae-21',
           'gate-2021-ae-ae-23', 'gate-2021-ae-ae-24', 'gate-2021-ae-ae-31', 'gate-2021-ae-ae-36']

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

print('Batch 2 updated.')
