import os
from PIL import Image

os.makedirs('figures/ae/2021', exist_ok=True)

# Page image path helper
def page_path(num):
    return f'tmp/ae2021_pages/page_{num:02d}.png'

def crop_and_save(page_num, box, out_name):
    img = Image.open(page_path(page_num))
    w, h = img.size
    # box is in normalized coords [left, top, right, bottom] or pixel coords
    # If float, convert to pixels
    if isinstance(box[0], float):
        l = int(box[0] * w)
        t = int(box[1] * h)
        r = int(box[2] * w)
        b = int(box[3] * h)
    else:
        l, t, r, b = box
    cropped = img.crop((l, t, r, b))
    out_path = os.path.join('figures/ae/2021', out_name)
    cropped.save(out_path)
    print(f"Saved {out_path} ({cropped.size})")

# Let's define the crops based on the page images
# Each page image is 1654 x 2339 (or similar)
# Let's inspect page 2 for GA Q2
img2 = Image.open(page_path(2))
w2, h2 = img2.size
print(f"Page 2 size: {w2}x{h2}")

# GA Q2 main figure:
# Inside Q.2 box:
# main figure is below Q.2 header and above "The mirror image of the above text..."
crop_and_save(2, (0.24, 0.13, 0.65, 0.36), 'ga_q2_main.png')
crop_and_save(2, (0.24, 0.395, 0.60, 0.445), 'ga_q2_opt_a.png')
crop_and_save(2, (0.24, 0.455, 0.60, 0.505), 'ga_q2_opt_b.png')
crop_and_save(2, (0.24, 0.515, 0.60, 0.565), 'ga_q2_opt_c.png')
crop_and_save(2, (0.24, 0.575, 0.60, 0.625), 'ga_q2_opt_d.png')

# GA Q9 (Page 5)
crop_and_save(5, (0.35, 0.41, 0.70, 0.615), 'ga_q9.png')

# AE Q4 (Page 8)
crop_and_save(8, (0.28, 0.18, 0.80, 0.465), 'ae_q4.png')

# AE Q10 (Page 10)
crop_and_save(10, (0.30, 0.42, 0.78, 0.605), 'ae_q10.png')

# AE Q11 (Page 11)
crop_and_save(11, (0.32, 0.175, 0.72, 0.395), 'ae_q11.png')

# AE Q13 (Page 12)
crop_and_save(12, (0.35, 0.17, 0.72, 0.385), 'ae_q13.png')

# AE Q14 (Page 13)
crop_and_save(13, (0.33, 0.27, 0.76, 0.555), 'ae_q14.png')

# AE Q21 (Page 16)
crop_and_save(16, (0.28, 0.18, 0.80, 0.425), 'ae_q21.png')

# AE Q26 (Page 18)
crop_and_save(18, (0.38, 0.28, 0.72, 0.48), 'ae_q26.png')

# AE Q27 (Page 19)
crop_and_save(19, (0.31, 0.22, 0.78, 0.41), 'ae_q27.png')

# AE Q29 (Page 20)
crop_and_save(20, (0.28, 0.20, 0.80, 0.43), 'ae_q29.png')

# AE Q33 (Page 22)
crop_and_save(22, (0.26, 0.25, 0.82, 0.445), 'ae_q33.png')

# AE Q40 (Page 25)
crop_and_save(25, (0.28, 0.30, 0.80, 0.475), 'ae_q40.png')

# AE Q46 (Page 27)
crop_and_save(27, (0.38, 0.565, 0.70, 0.755), 'ae_q46.png')

# AE Q49 (Page 29)
crop_and_save(29, (0.28, 0.315, 0.79, 0.63), 'ae_q49.png')

# AE Q50 (Page 30)
crop_and_save(30, (0.29, 0.20, 0.78, 0.485), 'ae_q50.png')

# AE Q51 (Page 30)
crop_and_save(30, (0.29, 0.63, 0.77, 0.76), 'ae_q51.png')

# AE Q52 (Page 31)
crop_and_save(31, (0.28, 0.255, 0.79, 0.54), 'ae_q52.png')

# AE Q53 (Page 31)
crop_and_save(31, (0.32, 0.74, 0.78, 0.88), 'ae_q53.png')

print("All figure crops saved successfully.")
