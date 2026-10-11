from PIL import Image

# 1. GA Q8: Trim the stray line at top
im_q08 = Image.open('tmp/ae2015_clean_crops/q08.png')
w, h = im_q08.size
fig_q08 = im_q08.crop((int(0.20 * w), int(0.20 * h), int(0.55 * w), int(0.85 * h)))
fig_q08.save('figures/gate-2015-ae-ga-q08.png')

# 2. AE Q26: Trim top line
im_q26 = Image.open('tmp/ae2015_clean_crops/q26.png')
w, h = im_q26.size
fig_q26 = im_q26.crop((int(0.02 * w), int(0.44 * h), int(0.95 * w), int(0.78 * h)))
fig_q26.save('figures/gate-2015-ae-q26.png')

print("Refined crops for GA Q8 and AE Q26.")
