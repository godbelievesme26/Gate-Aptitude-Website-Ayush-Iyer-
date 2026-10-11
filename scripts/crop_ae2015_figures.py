import fitz
import os
from PIL import Image

os.makedirs('figures', exist_ok=True)

# 1. GA Q8
im_q08 = Image.open('tmp/ae2015_clean_crops/q08.png')
# let's crop the triangle
# size is (1190, 480)
# Triangle is roughly y: 80 to 380, x: 250 to 600
w, h = im_q08.size
fig_q08 = im_q08.crop((int(0.20 * w), int(0.15 * h), int(0.55 * w), int(0.85 * h)))
fig_q08.save('figures/gate-2015-ae-ga-q08.png')

# 2. AE Q26
im_q26 = Image.open('tmp/ae2015_clean_crops/q26.png')
w, h = im_q26.size
# In Q26 crop, top is question header, text, then 4 beams, then options
# Beams are roughly y: 0.40 * h to 0.78 * h, x: 0.02 * w to 0.95 * w
fig_q26 = im_q26.crop((int(0.02 * w), int(0.42 * h), int(0.95 * w), int(0.78 * h)))
fig_q26.save('figures/gate-2015-ae-q26.png')

# 3. AE Q41
im_q41 = Image.open('tmp/ae2015_clean_crops/q41.png')
w, h = im_q41.size
# Beam is roughly y: 0.28 * h to 0.75 * h, x: 0.20 * w to 0.75 * w
fig_q41 = im_q41.crop((int(0.22 * w), int(0.30 * h), int(0.72 * w), int(0.75 * h)))
fig_q41.save('figures/gate-2015-ae-q41.png')

# 4. AE Q56
im_q56 = Image.open('tmp/ae2015_clean_crops/q56.png')
w, h = im_q56.size
# Rankine half body is roughly y: 0.35 * h to 0.75 * h, x: 0.05 * w to 0.78 * w
fig_q56 = im_q56.crop((int(0.05 * w), int(0.38 * h), int(0.78 * w), int(0.72 * h)))
fig_q56.save('figures/gate-2015-ae-q56.png')

# 5. AE Q58
im_q58 = Image.open('tmp/ae2015_clean_crops/q58.png')
w, h = im_q58.size
# Tube is roughly y: 0.28 * h to 0.78 * h, x: 0.22 * w to 0.72 * w
fig_q58 = im_q58.crop((int(0.22 * w), int(0.30 * h), int(0.72 * w), int(0.78 * h)))
fig_q58.save('figures/gate-2015-ae-q58.png')

print("Cropped 5 figures.")
