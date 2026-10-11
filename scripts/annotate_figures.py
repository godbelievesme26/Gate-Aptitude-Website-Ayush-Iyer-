"""Figure mappings verified visually against local source pages, not inferred from keywords."""
import json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
figures={1:[2,7,8,10],2:[3,4,8,10],3:[2,5,7,8,9],4:[3,8,9,10],5:[2,7,8],6:[2,7,8,9],7:[3,10],8:[3,9,10],9:[2,3,5,7,10],10:[5,8,10],11:[4,5,7,10],12:[5,7,9],13:[4,9,10],14:[4,5,7,8],15:[3,4,7,10],16:[8]}
bounds={(1,2):(140,250),(1,7):(150,452),(1,8):(168,412),(1,10):(181,550),(2,3):(122,240),(2,4):(135,410),(2,8):(213,387),(2,10):(164,413)}
preview=Image.new('RGB',(1200,2000),'#eee');idx=0
for day,nums in figures.items():
 path=Path(f'data/day{day:02d}.json');s=json.loads(path.read_text(encoding='utf-8'));doc=pdfium.PdfDocument(s['source'])
 for q in s['questions']:
  q['hasFigure']=q['number'] in nums
  if (day,q['number']) in bounds:
   y0,y1=bounds[day,q['number']];page=q['source']['pages'][0]['page'];bbox=[100,y0,550,y1]
   img=doc[page-1].render(scale=2).to_pil().convert('RGB').crop(tuple(v*2 for v in bbox))
   asset=f"figures/day{day:02d}-q{q['number']:02d}-diagram.png";img.save(asset)
   q['figure']=asset;q['figureSource']={'page':page,'bbox':bbox}
   img.thumbnail((560,450));preview.paste(img,((idx%2)*600+20,(idx//2)*500+30));ImageDraw.Draw(preview).text(((idx%2)*600+20,(idx//2)*500+5),f"Day {day} Q{q['number']}",fill='black');idx+=1
 path.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
Path('docs/figure-map.json').write_text(json.dumps({'questionsWithFigures':sum(map(len,figures.values())),'byDay':figures,'standaloneCrops':len(bounds),'remainingFigures':'Preserved within their original complete question crops.'},indent=2),encoding='utf-8')
preview.save('tmp/pdfs/diagram-audit.jpg')
