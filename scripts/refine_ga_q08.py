from PIL import Image

im_q08 = Image.open('tmp/ae2015_clean_crops/q08.png')
# crop with y0=158
fig_q08 = im_q08.crop((360, 158, 780, 455))
fig_q08.save('figures/gate-2015-ae-ga-q08.png')
print("Successfully refined gate-2015-ae-ga-q08.png.")
