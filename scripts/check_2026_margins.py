import json
from pathlib import Path
from PIL import Image, ImageChops

data_2026 = json.loads(Path('data/ae/2026.json').read_text(encoding='utf-8'))
data_day01 = json.loads(Path('data/day01.json').read_text(encoding='utf-8'))
all_qs = data_day01['questions'] + data_2026['questions']

for q in all_qs:
    q_num = q['number']
    figs = q.get('figures', [])
    for idx, f in enumerate(figs):
        src = f['src']
        im = Image.open(src)
        # Check margins (distance from non-white pixels to edge)
        diff = ImageChops.difference(im.convert('RGB'), Image.new('RGB', im.size, 'white'))
        bbox = diff.getbbox()
        if bbox:
            left_m = bbox[0]
            top_m = bbox[1]
            right_m = im.size[0] - bbox[2]
            bottom_m = im.size[1] - bbox[3]
            print(f"Q{q_num:02d} fig {idx+1}: size={im.size}, margins=(L:{left_m}, T:{top_m}, R:{right_m}, B:{bottom_m})")
        else:
            print(f"Q{q_num:02d} fig {idx+1}: all white?")

    for opt in q.get('options', []):
        if 'figure' in opt:
            src = opt['figure']['src']
            im = Image.open(src)
            diff = ImageChops.difference(im.convert('RGB'), Image.new('RGB', im.size, 'white'))
            bbox = diff.getbbox()
            if bbox:
                left_m = bbox[0]
                top_m = bbox[1]
                right_m = im.size[0] - bbox[2]
                bottom_m = im.size[1] - bbox[3]
                print(f"Q{q_num:02d} opt {opt['label']}: size={im.size}, margins=(L:{left_m}, T:{top_m}, R:{right_m}, B:{bottom_m})")
