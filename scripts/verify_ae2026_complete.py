import json
from pathlib import Path

ROOT = Path('c:/Users/godbe/Desktop/Aptitude Website')
KEY_JSON_PATH = ROOT / 'internal/ae/AE2026-key.json'
PAPER_JSON = ROOT / 'data/ae/2026.json'
DAY01_JSON = ROOT / 'data/day01.json'
MANIFEST_PATH = ROOT / 'data/ae/manifest.json'

paper_raw = json.loads(PAPER_JSON.read_text(encoding='utf-8'))
day01_raw = json.loads(DAY01_JSON.read_text(encoding='utf-8'))
key_raw = json.loads(KEY_JSON_PATH.read_text(encoding='utf-8'))
manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))

all_qs = day01_raw['questions'] + paper_raw['questions']
key_rows = {r['number']: r for r in key_raw['rows']}
ref_by_id = {r['id']: r for r in paper_raw['questionRefs']}

# PASS 1: QUESTION COUNT
assert len(all_qs) == 65
assert paper_raw['totalQuestions'] == 65
assert paper_raw['totalMarks'] == 100

# PASS 2: NUMBERING
nums = [q['number'] for q in all_qs]
assert nums == list(range(1, 66))

# PASS 3 & 4 & 5: QUESTION TEXT, OPTIONS, MATHEMATICS
for q in all_qs:
    n = q['number']
    assert q['question'] and len(q['question'].strip()) > 0
    assert q['type'] in ['MCQ', 'MSQ', 'NAT']
    if q['type'] in ['MCQ', 'MSQ']:
        assert len(q['options']) == 4
        labels = [o['label'] for o in q['options']]
        assert labels == ['A', 'B', 'C', 'D']
        for o in q['options']:
            has_content = bool(o.get('text')) or bool(o.get('figure')) or bool(o.get('content'))
            assert has_content
    elif q['type'] == 'NAT':
        assert len(q.get('options', [])) == 0

# PASS 6: FIGURES & ASSETS
figure_count = 0
for q in all_qs:
    n = q['number']
    for f in q.get('figures', []):
        src_path = ROOT / f['src']
        assert src_path.exists()
        assert f.get('alt')
        figure_count += 1
    for o in q.get('options', []):
        if 'figure' in o:
            src_path = ROOT / o['figure']['src']
            assert src_path.exists()
            assert o['figure'].get('alt')
            figure_count += 1
assert figure_count == 25

# PASS 7: TYPE AND MARKS
total_marks = 0
ga_marks = 0
ae_marks = 0
type_counts = {'MCQ': 0, 'MSQ': 0, 'NAT': 0}
for q in all_qs:
    n = q['number']
    k = key_rows[n]
    ref = ref_by_id[q['id']]
    section = ref['section']
    marks = 1 if (n <= 5 or (n >= 11 and n <= 35)) else 2
    assert q['type'] == k['type']
    assert marks == k['marks']
    if n <= 5:
        assert marks == 1 and section == 'GA'
    elif n <= 10:
        assert marks == 2 and section == 'GA'
    elif n <= 35:
        assert marks == 1 and section == 'AE'
    else:
        assert marks == 2 and section == 'AE'
    
    total_marks += marks
    if section == 'GA': ga_marks += marks
    else: ae_marks += marks
    type_counts[q['type']] += 1

assert total_marks == 100
assert ga_marks == 15
assert ae_marks == 85
assert type_counts == {'MCQ': 29, 'MSQ': 14, 'NAT': 22}

# PASS 8: GROUPS
assert len(paper_raw.get('questionGroups', [])) == 0

# PASS 9: ANSWER KEY
for q in all_qs:
    n = q['number']
    k = key_rows[n]
    raw_key = k['rawKey']
    if raw_key == 'MTA*':
        assert q['answer'] == 'MTA'
        assert q.get('gradingRule') == 'marks-to-all'
    elif q['type'] == 'MCQ':
        assert q['answer'] == raw_key
    elif q['type'] == 'MSQ':
        expected = raw_key.split(';')
        assert sorted(q['answer']) == sorted(expected)
    elif q['type'] == 'NAT':
        if ' to ' in raw_key:
            expected = [float(x) for x in raw_key.split(' to ')]
            assert q['answer'] == expected
        else:
            expected = float(raw_key)
            assert q['answer'] == expected

# PASS 10: MANIFEST INTEGRATION
ae_manifest = next(y for y in manifest['years'] if y['year'] == 2026)
assert ae_manifest['ingestionStatus'] == 'complete'
assert ae_manifest['verificationStatus'] == 'source-verified'
assert ae_manifest['questionCount'] == 65
assert ae_manifest['totalMarks'] == 100
assert ae_manifest['questionTypeCounts'] == {'MCQ': 29, 'MSQ': 14, 'NAT': 22}

print("ALL 10 PASSES VERIFIED FOR AE2026!")
