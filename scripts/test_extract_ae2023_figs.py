import pymupdf
from PIL import Image, ImageChops
from io import BytesIO
from pathlib import Path

doc = pymupdf.open('internal/ae/AE2023.pdf')

def extract_clean(xref):
    d = doc.extract_image(xref)
    sm = d.get('smask')
    if sm:
        smd = doc.extract_image(sm)
        mask = Image.open(BytesIO(smd['image'])).convert('L')
        base = Image.open(BytesIO(d['image'])).convert('RGB')
        if base.getextrema() == ((0, 0), (0, 0), (0, 0)):
            out = Image.new('RGB', mask.size, 'white')
            out.paste(Image.new('RGB', mask.size, 'black'), mask=mask)
            return out
        else:
            rgba = base.convert('RGBA')
            rgba.putalpha(mask)
            bg = Image.new('RGBA', rgba.size, 'white')
            bg.alpha_composite(rgba)
            return bg.convert('RGB')
    else:
        im = Image.open(BytesIO(d['image']))
        if im.mode == 'RGBA':
            bg = Image.new('RGBA', im.size, 'white')
            bg.alpha_composite(im)
            return bg.convert('RGB')
        return im.convert('RGB')

out_dir = Path('scratch/extracted_figs')
out_dir.mkdir(parents=True, exist_ok=True)

test_xrefs = {
    'q14': 51,
    'q18_A': 70, 'q18_B': 72, 'q18_C': 74, 'q18_D': 76,
    'q19_A': 82, 'q19_B': 84, 'q19_C': 86, 'q19_D': 88,
    'q23': 101,
    'q24_A': 106, 'q24_B': 108, 'q24_C': 110, 'q24_D': 112,
    'q30': 123,
    'q32': 130,
    'q37': 148,
    'q41': 178,
    'q44': 211,
    'q49': 234,
    'q50': 236,
    'q52': 247
}

for name, xref in test_xrefs.items():
    im = extract_clean(xref)
    bbox = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
    if bbox:
        im = im.crop(bbox)
    im.save(out_dir / f"{name}.png")
    print(f"Extracted {name} (xref {xref}): size {im.size}")

print("All raster figures extracted to scratch/extracted_figs/")
