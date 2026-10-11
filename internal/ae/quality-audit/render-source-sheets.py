"""Read-only source evidence sheets. No question/crop files are changed."""
import sys
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
year=int(sys.argv[1])
out=Path('internal/ae/quality-audit/visual')/str(year)
out.mkdir(exist_ok=True)
doc=pdfium.PdfDocument(f'internal/ae/AE{year}.pdf')
for start in range(0,len(doc),3):
    pages=[]
    for i in range(start,min(start+3,len(doc))):
        im=doc[i].render(scale=1.5).to_pil().convert('RGB')
        im.thumbnail((780,1150))
        page=Image.new('RGB',(800,1180),'#dddddd')
        page.paste(im,((800-im.width)//2,25))
        ImageDraw.Draw(page).text((10,7),f'AE {year} / PDF page {i+1}',fill='black')
        pages.append(page)
    sheet=Image.new('RGB',(800*len(pages),1180),'white')
    for i,page in enumerate(pages):sheet.paste(page,(i*800,0))
    sheet.save(out/f'source-{start+1:02}.png')
print(f'{year}: {len(doc)} source pages rendered')
