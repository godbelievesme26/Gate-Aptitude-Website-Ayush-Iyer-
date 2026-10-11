import fitz
from PIL import Image
import os

# Let's see what is drawn or rendered in these icons
# We can crop the non-white parts of each icon and check their appearance
for icon in sorted(os.listdir('tmp/ae2015_icons')):
    if icon.endswith('.png'):
        im = Image.open(os.path.join('tmp/ae2015_icons', icon))
        # find bounding box of non-white pixels
        bg = Image.new(im.mode, im.size, (255, 255, 255) if im.mode == 'RGB' else 255)
        diff = ImageChops.difference(im, bg) if 'ImageChops' in globals() else None
        # let's find unique colors
        colors = im.getcolors(maxcolors=2000)
        # sample some colors
        print(f"{icon}: num_unique_colors={len(colors) if colors else '>2000'}")
