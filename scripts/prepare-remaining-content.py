"""Prepare the 90 records explicitly authorized in the current full-corpus brief.
The preceding 70 verified questions and all source PDFs stay unchanged.
Vector crops omit only the identified watermark/logo objects before rendering.
"""
import io,json
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream
import pypdfium2 as pdfium
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent.parent
CROPS={
 (2,4):[(3,[140,160,460,385],'')],(2,10):[(9,[125,178,486,391],'')],
 (10,5):[(3,[118,151,500,279],'')],(11,10):[(9,[125,209,345,351],'')],
 (12,5):[(5,[155,190,440,445],'')],(12,7):[(7,[214,203,350,333],'')],(12,9):[(9,[120,190,474,285],'')],
 (13,4):[(4,[226,189,369,295],'')],(13,9):[(9,[225,220,345,337],'')],(13,10):[(10,[163,205,426,365],'')],
 (14,4):[(3,[190,174,371,201],'Iteration 0'),(3,[190,225,371,299],'Iteration 1 · Length of each segment: 1/3'),(3,[190,320,371,407],'Iteration 2 · Length of each segment: 1/9')],
 (14,8):[(7,[215,242,385,414],'')],(15,3):[(3,[127,195,477,403],'')],
 (15,4):[(4,[389,285,450,341],'Column-II · (P)'),(4,[389,358,450,416],'Column-II · (Q)'),(4,[389,432,450,482],'Column-II · (R)'),(4,[389,505,450,565],'Column-II · (S)')],
 (15,7):[(7,[188,161,394,364],'')],(16,8):[(8,[213,207,384,335],'')]
}
OPTION_CROPS={
 (10,5):[(3,[127,290,232,394]),(3,[125,403,231,509]),(3,[125,516,231,623]),(3,[125,633,231,740])],
 (10,10):[(8,[118,227,211,323]),(8,[118,329,211,423]),(8,[118,429,211,523]),(8,[118,529,211,622])],
 (11,5):[(4,[233,257,396,420]),(4,[220,452,386,618]),(5,[219,113,381,272]),(5,[219,307,381,466])],
 (12,9):[(9,[120,298,214,388]),(9,[120,392,214,480]),(9,[120,484,214,571]),(9,[120,575,214,663])],
 (13,4):[(4,[118,303,182,359]),(4,[118,363,182,417]),(4,[116,421,179,473]),(4,[116,478,179,532])],
 (14,5):[(4,[118,168,251,288]),(4,[118,294,248,416]),(4,[118,425,248,541]),(4,[118,547,244,662])],
 (16,8):[(8,[116,349,210,435]),(8,[116,441,210,530]),(8,[116,537,210,627]),(8,[116,635,210,721])]
}
EMBED={
 (2,8):(7,['Image49.jpg'],[]),
 (9,2):(2,['Im1.png'],['Im2.png','Im3.png','Im4.png','Im5.png']),
 (9,3):(3,['Im1.png'],[]),(9,5):(5,['Im1.png'],[]),(9,10):(10,['Im1.png'],[]),
 (10,8):(6,['Image67.jpg'],['Image71.jpg','Image68.jpg','Image69.jpg','Image70.jpg']),
 (11,7):(7,['Image44.jpg'],[]),(14,7):(6,['Image84.png'],[]),(15,10):(10,['Image62.png'],[])
}
XE_CUBE=[([0,55,394,580],'Panel I'),([500,207,688,392],'Panel II · (i)'),([734,207,920,392],'Panel II · (ii)')]
def trim(im):
 rgba=im.convert('RGBA');flat=Image.new('RGBA',rgba.size,'white');flat.alpha_composite(rgba);im=flat.convert('RGB')
 b=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
 return im.crop(b) if b else im
def run():
 edits=json.loads((ROOT/'scripts/verified-remaining-transcriptions.json').read_text(encoding='utf8'))
 keys=json.loads((ROOT/'tests/fixtures/official-remaining-ga-keys.json').read_text())
 for daystr,questions in edits.items():
  day=int(daystr);path=ROOT/f'data/day{day:02}.json';data=json.loads(path.read_text(encoding='utf8'));reader=PdfReader(ROOT/data['source']);writer=PdfWriter()
  for original in reader.pages[:10]:
   page=writer.add_page(original);stream=ContentStream(page.get_contents(),writer)
   if data['year']==2025:stream.operations=[(args,op) for args,op in stream.operations if not(op==b'Do' and str(args[0]) in ['/Image5','/Image15'])]
   page.replace_contents(stream)
  buf=io.BytesIO();writer.write(buf);doc=pdfium.PdfDocument(buf.getvalue());rendered={}
  def save(q,im,page,suffix,source,caption=''):
   rel=f"figures/{q['id']}-{suffix}.png";trim(im).save(ROOT/rel)
   asset={'src':rel,'alt':f"{q['year']} {q['paper']} question {q['number']}, {suffix.replace('-',' ')}: original diagram",'source':{'file':q['source']['file'],'page':page,'sha256':q['source']['sha256'],**source}}
   if caption:asset['caption']=caption
   return asset
  def crop(q,item,suffix):
   page,box,*captions=item
   if page not in rendered:rendered[page]=doc[page-1].render(scale=3).to_pil()
   return save(q,rendered[page].crop(tuple(round(v*3) for v in box)),page,suffix,{'pdfCrop':box,'dpi':216,'omittedBackgroundObjects':['Image5','Image15']},captions[0] if captions else '')
  def embedded(q,page,name,suffix):
   im=next(x for x in reader.pages[page-1].images if x.name==name)
   return save(q,im.image,page,suffix,{'image':name})
  for q in data['questions']:
   n=q['number'];edit=questions[str(n)];key=next(k for k in keys[daystr]['questions'] if k['number']==n)
   q['question']=edit['question'];q['options']=[{'label':l,'text':t} for l,t in zip('ABCD',edit['options'])]
   for name in ['table','afterTable']:
    if name in edit:q[name]=edit[name]
   q['solution']=edit['solution'];q['solutionStatus']='independently checked editorial solution; not an official solution';q['type']=key['type'];q['marks']=key['marks'];q['answer']=key['answer']
   if key['answer']=='MTA':q['gradingRule']='marks-to-all'
   q['answerSource']={'url':keys[daystr]['keyUrl'],'paper':data['paper'],'questionNumber':n,'section':'GA','session':key['session'],'verifiedOn':'2026-10-05','sha256':keys[daystr]['keySha256'],'masterPaperUrl':keys[daystr]['masterUrl'],'mappingStatus':'master-order-verified'}
   q['transcriptionStatus']='source-verified';q['gradingStatus']='official key verified';q['figures']=[]
   for f in ['figure','figureSource']:q.pop(f,None)
   for i,item in enumerate(CROPS.get((day,n),[])):q['figures'].append(crop(q,item,f'figure-{i+1}'))
   for o,item in zip(q['options'],OPTION_CROPS.get((day,n),[])):o['text']='';o['figure']=crop(q,item,'option-'+o['label'])
   if (day,n) in EMBED:
    page,stems,opts=EMBED[day,n]
    for i,name in enumerate(stems):q['figures'].append(embedded(q,page,name,f'figure-{i+1}'))
    for o,name in zip(q['options'],opts):o['text']='';o['figure']=embedded(q,page,name,'option-'+o['label'])
   if (day,n)==(9,7):
    im=next(x.image for x in reader.pages[6].images if x.name=='Im1.png')
    for i,(box,caption) in enumerate(XE_CUBE):q['figures'].append(save(q,im.crop(box),7,f'figure-{i+1}',{'image':'Im1.png','pixelCrop':box},caption))
   for f,alt in zip(q['figures'],edit.get('figureAlts',[])):f['alt']=alt
   for o,alt in zip(q['options'],edit.get('optionAlts',[])):
    if 'figure' in o:o['figure']['alt']=alt
   q['hasFigure']=bool(q['figures'] or any(o.get('figure') for o in q['options']))
  data['answerKeyStatus']=f"official GATE {data['year']} final key verified for GA questions 1–10"
  path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 assets=[]
 for day in edits:
  for q in json.loads((ROOT/f'data/day{int(day):02}.json').read_text(encoding='utf8'))['questions']:
   assets.extend({'questionId':q['id'],**a} for a in q['figures']+[o['figure'] for o in q['options'] if 'figure' in o])
 (ROOT/'docs/corpus-pass/asset-manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(f'Prepared {sum(len(q) for q in edits.values())} questions and {len(assets)} figure assets')
if __name__=='__main__':run()
