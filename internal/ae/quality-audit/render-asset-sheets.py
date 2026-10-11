"""Make evidence contact sheets from current, referenced assets only."""
import json,sys
from pathlib import Path
from PIL import Image, ImageDraw
year=int(sys.argv[1]); root=Path('internal/ae/quality-audit')
records=json.loads((root/'initial-automated.json').read_text(encoding='utf-8'))['records']
assets=[(q['questionId'],src) for q in records if q['paper']=='AE' and q['year']==year for src in q['assets']]
for start in range(0,len(assets),6):
    sheet=Image.new('RGB',(1600,1440),'#dddddd'); draw=ImageDraw.Draw(sheet)
    for offset,(qid,src) in enumerate(assets[start:start+6]):
        x=(offset%2)*800;y=(offset//2)*480
        im=Image.open(src).convert('RGB');im.thumbnail((770,430))
        sheet.paste(im,(x+15,y+45));draw.text((x+15,y+8),qid,fill='black');draw.text((x+15,y+24),Path(src).name,fill='black')
    sheet.save(root/'visual'/f'{year}-current-assets-{start//6+1}.png')
print(f'{year}: {len(assets)} referenced assets')
