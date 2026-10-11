"""Independent pixel checks for the rotation, tiling and assembly solutions.
Run after prepare-2026-content.py; uses only source-extracted images.
"""
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parent.parent
def image(name):return Image.open(ROOT/'figures'/name).convert('L')
def mask(im,size=(240,240)):
    return im.resize(size).point(lambda v:255 if v>128 else 0)
def error(a,b):
    return sum(ImageChops.difference(mask(a),mask(b)).getdata())/(240*240*255)
def choose(name,reference):
    scores={letter:error(reference,image(f'{name}-option-{letter}.png')) for letter in 'ABCD'}
    winner=min(scores,key=scores.get);print(name,winner,scores)
    return winner

# Rotation: Pillow positive angles are anticlockwise, hence -45.
name='gate-2026-ce1-ga-05'
rotated=image(f'{name}-figure-1.png').rotate(-45,expand=True,fillcolor=255)
rotated=rotated.crop(ImageChops.invert(rotated).getbbox())
assert choose(name,rotated)=='B'

# Three repeated square blocks in the long source pattern.
name='gate-2026-ce2-ga-10';strip=image(f'{name}-figure-1.png')
for i in range(3):
    tile=strip.crop((round(i*strip.width/3),0,round((i+1)*strip.width/3),strip.height))
    assert choose(name,tile)=='B'

# Assemble the black puzzle pieces at their shared square boundary.
name='gate-2026-da-ga-03'
pieces=[mask(image(f'{name}-figure-{i}.png')) for i in range(1,5)]
assembled=pieces[0]
for p in pieces[1:]:assembled=ImageChops.darker(assembled,p)
assert choose(name,assembled)=='A'
print('PASS: clockwise rotation, all three repeated tiles, and four-piece assembly.')
