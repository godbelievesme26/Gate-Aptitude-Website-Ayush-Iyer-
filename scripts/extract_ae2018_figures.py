import os
from PIL import Image

os.makedirs('figures', exist_ok=True)

def crop_and_save(page_num, box, filename, pad=10):
    im = Image.open(f'tmp/ae2018_pages/page_{page_num:02d}.png')
    cropped = im.crop(box)
    
    gray = cropped.convert('L')
    bw = gray.point(lambda x: 0 if x < 245 else 255, '1')
    bbox = bw.getbbox()
    if bbox:
        c_bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(cropped.width, bbox[2] + pad),
            min(cropped.height, bbox[3] + pad)
        )
        final = cropped.crop(c_bbox)
    else:
        final = cropped
        
    final.save(os.path.join('figures', filename))
    print(f'Saved figures/{filename}: size {final.size}')

# 1. Page 5: AE Q8 (Paper Q18) - Boundary layer velocity profile
crop_and_save(5, (500, 565, 1000, 895), 'gate-2018-ae-ae-18-figure-1.png')

# 2. Page 7: AE Q23 (Paper Q33) - 2-block spring-mass system
crop_and_save(7, (320, 1370, 1400, 1630), 'gate-2018-ae-ae-33-figure-1.png')

# 3. Page 8: AE Q30 (Paper Q40) - Clamped-clamped beam with midspan load P
crop_and_save(8, (350, 1685, 1420, 2015), 'gate-2018-ae-ae-40-figure-1.png')

print("All AE2018 figures re-extracted with precision crops!")
