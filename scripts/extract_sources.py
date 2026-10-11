from pathlib import Path
import pdfplumber,pypdfium2 as pdfium,re,json,hashlib
from PIL import Image,ImageOps,ImageChops,ImageDraw
root=Path('.')
paths=sorted(Path('Aptitude Sets').rglob('*.pdf'))
first=[Path('Aptitude Sets/2026/AE (1).pdf'),Path('Aptitude Sets/2025/AE (2).pdf')]
paths=first+sorted([p for p in paths if p not in first],key=lambda p:(-int(p.parent.name),p.name))
registry=[]; audit=[]
for day,path in enumerate(paths,1):
 year=int(path.parent.name); paper=re.sub(r' \(\d+\)','',path.stem).replace('_','')
 doc=pdfium.PdfDocument(str(path)); images=[]; questions=[]
 with pdfplumber.open(path) as pdf:
  markers=[]
  for pi,p in enumerate(pdf.pages[:13]):
   words=p.extract_words()
   for wi,w in enumerate(words):
    if w['text']=='Q.' and wi+1<len(words) and words[wi+1]['text'].isdigit():w={**w,'text':'Q.'+words[wi+1]['text']}
    if re.fullmatch(r'Q\.\d+',w['text']) and w['x0']<90:
     n=int(w['text'][2:]); following=[x['text'] for x in words if abs(x['top']-w['top'])<5 and x['x0']>w['x0']]
     if n<=11 and not any(x in ('Carry','–','—') for x in following[:5]): markers.append((n,pi,w['top']))
  # Section headings and standalone question numbers can occur on the same page.
  markers={n:(pi,top) for n,pi,top in markers}
  assert set(range(1,12)).issubset(markers),(path,markers)
  for n in range(1,11):
   pi,top=markers[n]; epi,etop=markers[n+1]; crops=[]; texts=[]; provenance=[]
   for pageidx in range(pi,epi+1):
    if pageidx==epi and epi!=pi and etop<200:break
    p=pdf.pages[pageidx]; y0=max(75,top-10) if pageidx==pi else (80 if year==2025 and paper in ['AE','EC'] else 100)
    y1=etop-16 if pageidx==epi else p.height-66
    if y1<=y0:continue
    # Trim only after the full final option row, using the actual table boundary.
    dlabels=[w for w in p.extract_words() if w['text']=='(D)' and y0<w['top']<y1 and w['x0']<110]
    if dlabels:
     borders=[edge['top'] for edge in p.edges if edge.get('orientation')=='h' and edge['width']>300 and dlabels[-1]['bottom']+4<edge['top']<y1]
     if borders:y1=min(borders)+3
    bbox=(35,y0,p.width-30,y1)
    text=p.crop(bbox).extract_text() or ''
    if not text.strip():continue
    texts.append(text)
    img=doc[pageidx].render(scale=2).to_pil().convert('RGB').crop(tuple(round(v*2) for v in bbox))
    diff=ImageChops.difference(img,Image.new('RGB',img.size,'white')).convert('L').point(lambda x:255 if x>55 else 0)
    bb=diff.getbbox()
    if bb:img=ImageOps.expand(img.crop(bb),border=20,fill='white')
    crops.append(img);provenance.append({'page':pageidx+1,'bbox':[round(v,2) for v in bbox]})
   joined=Image.new('RGB',(max(x.width for x in crops),sum(x.height for x in crops)+20*(len(crops)-1)),'white');y=0
   for im in crops:joined.paste(im,(0,y));y+=im.height+20
   asset=f'figures/day{day:02d}-q{n:02d}.png';joined.save(asset,optimize=True)
   raw='\n'.join(texts)
   parts=re.split(r'\(([ABCD])\)',raw)
   opts=[]
   if len(parts)>=9:
    for i in range(1,len(parts)-1,2):
     if parts[i] in 'ABCD':opts.append({'label':parts[i],'text':parts[i+1].strip()})
   q={'id':f'gate-{year}-{paper.lower()}-ga-{n:02d}','number':n,'year':year,'paper':paper,'subject':'General Aptitude','marks':1 if n<=5 else 2,'question':re.sub(r'^Q\.\d+\s*','',parts[0]).strip(),'options':opts,'sourceImage':asset,'source':{'file':path.as_posix(),'pages':provenance,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},'transcriptionStatus':'search-only; source image is authoritative','gradingStatus':'answer key unavailable'}
   questions.append(q);images.append(joined)
  dataset={'schemaVersion':1,'day':day,'year':year,'paper':paper,'title':f'GATE {year} · {paper} · General Aptitude','source':path.as_posix(),'answerKeyStatus':'not present in supplied PDF','questions':questions}
  target=f'data/day{day:02d}.json';Path(target).write_text(json.dumps(dataset,ensure_ascii=False,indent=2),encoding='utf-8')
  registry.append({'day':day,'path':target,'year':year,'paper':paper,'title':dataset['title'],'questionCount':10,'marks':15})
  thumbs=[]
  for n,im in enumerate(images,1):
   im=im.copy();im.thumbnail((570,650));tile=Image.new('RGB',(600,700),'#e8e8ed');tile.paste(im,(15,35));ImageDraw.Draw(tile).text((15,10),f'Day {day} / {year} {paper} / Q{n}',fill='black');thumbs.append(tile)
  sheet=Image.new('RGB',(1200,3500),'white')
  for i,tile in enumerate(thumbs):sheet.paste(tile,((i%2)*600,(i//2)*700))
  sheet.save(f'tmp/pdfs/contact-{day:02d}.jpg')
  audit.append({'day':day,'file':path.as_posix(),'pages':len(pdf.pages),'questionPages':{q['number']:[v['page'] for v in q['source']['pages']] for q in questions},'answerKeys':False})
 print(f'Extracted day {day}: {year} {paper}',flush=True)
Path('data/registry.json').write_text(json.dumps(registry,indent=2),encoding='utf-8')
Path('docs/source-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')

