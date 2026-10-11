import os
from PIL import Image

os.makedirs('figures', exist_ok=True)

def crop_and_save(page_num, box, filename, pad=10):
    im = Image.open(f'tmp/ae2019_pages/page_{page_num:02d}.png')
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

# 1. Page 5: Q9 (Paper Q19) - 4 option graphs
crop_and_save(5, (330, 500, 750, 830), 'gate-2019-ae-ae-19-option-A.png')
crop_and_save(5, (880, 500, 1300, 830), 'gate-2019-ae-ae-19-option-B.png')
crop_and_save(5, (330, 880, 750, 1200), 'gate-2019-ae-ae-19-option-C.png')
crop_and_save(5, (880, 880, 1300, 1200), 'gate-2019-ae-ae-19-option-D.png')

# 2. Page 7: Q23 (Paper Q33) - plate
crop_and_save(7, (550, 780, 1250, 1420), 'gate-2019-ae-ae-33-figure-1.png')

# 3. Page 7: Q24 (Paper Q34) - wedge at 45 deg
crop_and_save(7, (550, 1560, 1250, 1980), 'gate-2019-ae-ae-34-figure-1.png')

# 4. Page 8: Q25 (Paper Q35) - spring-mass system
crop_and_save(8, (450, 250, 1350, 520), 'gate-2019-ae-ae-35-figure-1.png')

# 5. Page 9: Q27 (Paper Q37) - shock in duct + theta-beta-M plot
crop_and_save(9, (300, 725, 1450, 1120), 'gate-2019-ae-ae-37-figure-1.png')

# 6. Page 10: Q30 (Paper Q40) - beam and 4 option BMDs
crop_and_save(10, (450, 265, 1350, 445), 'gate-2019-ae-ae-40-figure-1.png')
crop_and_save(10, (350, 530, 1000, 715), 'gate-2019-ae-ae-40-option-A.png')
crop_and_save(10, (350, 765, 1000, 935), 'gate-2019-ae-ae-40-option-B.png')
crop_and_save(10, (350, 985, 1000, 1175), 'gate-2019-ae-ae-40-option-C.png')
crop_and_save(10, (350, 1225, 1000, 1415), 'gate-2019-ae-ae-40-option-D.png')

# 7. Page 11: Q34 (Paper Q44) - cylinder in flow
crop_and_save(11, (550, 340, 1250, 680), 'gate-2019-ae-ae-44-figure-1.png')

# 8. Page 11: Q35 (Paper Q45) - rotating cylindrical container
crop_and_save(11, (650, 1080, 1150, 1520), 'gate-2019-ae-ae-45-figure-1.png')

# 9. Page 12: Q40 (Paper Q50) - pull-up aircraft
crop_and_save(12, (450, 1180, 1350, 1480), 'gate-2019-ae-ae-50-figure-1.png')

# 10. Page 13: Q48 (Paper Q58) - compressor velocity triangles
crop_and_save(13, (300, 1560, 1350, 2000), 'gate-2019-ae-ae-58-figure-1.png')

# 11. Page 14: Q49 (Paper Q59) - rigid slab CD hung by 3 cables
crop_and_save(14, (600, 380, 1200, 680), 'gate-2019-ae-ae-59-figure-1.png')

# 12. Page 14: Q50 (Paper Q60) - truss ABC
crop_and_save(14, (600, 880, 1200, 1300), 'gate-2019-ae-ae-60-figure-1.png')

# 13. Page 14: Q51 (Paper Q61) - solid and hollow shafts
crop_and_save(14, (600, 1510, 1200, 1800), 'gate-2019-ae-ae-61-figure-1.png')

# 14. Page 15: Q52 (Paper Q62) - L-bracket ABC
crop_and_save(15, (600, 320, 1200, 760), 'gate-2019-ae-ae-62-figure-1.png')

# 15. Page 15: Q53 (Paper Q63) - thin-walled tube cross-section
crop_and_save(15, (500, 970, 1300, 1240), 'gate-2019-ae-ae-63-figure-1.png')

# 16. Page 15: Q55 (Paper Q65) - 2-DOF spring mass system
crop_and_save(15, (450, 1580, 1350, 1860), 'gate-2019-ae-ae-65-figure-1.png')

print("All AE2019 figures re-extracted with precision crops!")
