import json
from pathlib import Path
from PIL import Image

data_2026 = json.loads(Path('data/ae/2026.json').read_text(encoding='utf-8'))
data_day01 = json.loads(Path('data/day01.json').read_text(encoding='utf-8'))

all_qs = data_day01['questions'] + data_2026['questions']

fig_list = []
for q in all_qs:
    q_num = q['number']
    figs = q.get('figures', [])
    for idx, f in enumerate(figs):
        fig_list.append((q_num, f'figure-{idx+1}', f['src'], f.get('alt', '')))
    for opt in q.get('options', []):
        if 'figure' in opt:
            fig_list.append((q_num, f"option-{opt['label']}", opt['figure']['src'], opt['figure'].get('alt', '')))

print(f"Total figures in AE2026: {len(fig_list)}")
for q_num, kind, src, alt in fig_list:
    p = Path(src)
    exists = p.exists()
    size = Image.open(p).size if exists else (0, 0)
    print(f"Q{q_num:02d} [{kind}]: {src} -> exists={exists}, size={size}")
