"""Reproducible, source-reviewed transcription/figure preparation for Days 1, 3–8.
Requires pypdf and Pillow. No source PDF, question ID, or ordering is changed.
"""
import json
import re
from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
KEYS = {1:'ABABCDADCC',3:'AAACBABABD',4:'CAADCBBCBB',5:'BCCDCBDAAC',6:'ACAA CAAABC'.replace(' ',''),7:'BBACDABDCC',8:'BADBBACCCC'}
# page, stem XObjects, option XObjects. P/Q/R/S are ordered visually, not by PDF resource order.
FIGURES = {
 (1,2):(2,[1],[2,3,4,5]), (1,8):(7,[1],[]),(1,10):(9,[1],[]),
 (3,2):(2,[1],[2,4,3,5]),(3,5):(5,[1],[2,4,3,5]),(3,7):(7,[1],[]),(3,8):(8,[1],[]),(3,9):(9,[1],[]),
 (4,3):(3,[1],[2,3,4,5]),(4,8):(8,[1],[]),(4,9):(9,[1],[]),(4,10):(10,[1],[2,4,3,5]),
 (5,2):(2,[1,2],[3,4,5,6]),(5,8):(7,[1],[]),(6,8):(7,[1],[]),
 (7,3):(2,[1,2,3,4],[5,7,6,8]),(7,10):(7,[1],[]),
 (8,3):(3,[1],[2,4,3,5]),(8,9):(9,[1],[]),(8,10):(10,[1,2],[3,5,4,6]),
}
# Pixel bounds within the original embedded image; exclude panel rules and unrelated candidates.
COMPOSITES = {
 (1,7):(6,[(0,55,390,577),(518,229,699,412),(795,230,976,413)],[],['Panel I','Panel II — (i)','Panel II — (ii)']),
 (5,7):(6,[(100,154,225,554)],[(390,40,660,330),(690,40,940,330),(390,340,660,625),(690,340,940,625)],['Panel I']),
 (6,2):(2,[(12,181,298,490)],[(480,81,707,265),(790,82,1013,265),(480,364,707,546),(790,364,1013,546)],['Panel I']),
 (6,7):(6,[(0,227,339,535)],[(489,115,611,325),(786,115,908,325),(489,444,611,655),(786,444,908,655)],['Panel I']),
 (6,9):(8,[(15,213,329,531)],[(388,55,677,343),(733,55,1019,343),(388,410,677,699),(733,410,1019,699)],['Panel I']),
}

def clean_image(page, number, box=None):
    source = next(im for im in page.images if im.name.split('.')[0] == f'Im{number}')
    rgba=source.image.convert('RGBA')
    image=Image.new('RGBA',rgba.size,'white');image.alpha_composite(rgba);image=image.convert('RGB')
    if box: image=image.crop(box)
    # Remove only empty white perimeter; leave labels, axes and diagram geometry intact.
    bounds=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox()
    if bounds: image=image.crop(bounds)
    return image,source.name

def asset(q,page,pdf_page,number,suffix,box=None,caption=''):
    im,name=clean_image(page,number,box)
    path=f"figures/{q['id']}-{suffix}.png";im.save(ROOT/path)
    return {'src':path,'alt':f"{q['paper']} question {q['number']}: {caption or suffix.replace('-', ' ')} from the source paper",'caption':caption,
      'source':{'file':q['source']['file'],'page':pdf_page,'image':name,'pixelCrop':box,'sha256':q['source']['sha256']}}

def set_options(q,texts):
    q['options']=[{'label':label,'text':text} for label,text in zip('ABCD',texts)]

def run():
 for day,key in KEYS.items():
    path=ROOT/f'data/day{day:02}.json'; data=json.loads(path.read_text(encoding='utf8'));pdf=PdfReader(ROOT/data['source'])
    edits=json.loads((ROOT/'scripts/verified-2026-transcriptions.json').read_text(encoding='utf8'))[str(day)]
    for q,answer in zip(data['questions'],key):
      n=q['number'];edit=edits[str(n)]
      q['question']=re.sub(r'^Q\.\s*\d+\s*','',q['question']).replace('\uf0b7','•')
      # Reflow PDF line wraps; keep list/clue/paragraph boundaries.
      q['question']=re.sub(r'\n(?![ivx]+\.|\([ivx]+\)|\(S\d\)|•|[PQ]:|Clue |Choose |Based |Which |The student|The number|The value)', ' ', q['question'])
      q['question']=re.sub(r'\s+P Q\s+R S(?:\s+P)?$','',q['question'])
      if (day,n)==(3,5): q['question']=q['question'].removesuffix(' (I)')
      if 'question' in edit:q['question']=edit['question']
      if (day,n)==(8,10):q['figureSequence']=True
      if 'options' in edit:set_options(q,edit['options'])
      else:
       for o in q['options']:o['text']=o['text'].replace('\n',' ')
      for field in ['table','afterTable']:
       if field in edit:q[field]=edit[field]
      q['answer']=answer;q['type']='MCQ';q['marks']=1 if n<=5 else 2
      q['solution']=edit['solution'];q['solutionStatus']='independently checked editorial solution; not an official solution'
      q['answerSource']={'url':f"https://gate2026.iitg.ac.in/doc/download/2026/Keys/{data['paper']}_Keys.pdf",'paper':data['paper'],'questionNumber':n,'section':'GA','verifiedOn':'2026-10-04'}
      q['transcriptionStatus']='source-verified';q['gradingStatus']='official key verified'
      for field in ['figure','figureSource']:q.pop(field,None)
      q['figures']=[]
      if (day,n) in FIGURES:
       page,stems,opts=FIGURES[day,n]
       for i,im in enumerate(stems):
        caption=['If','Then'][i] if (day,n)==(8,10) else '(I)' if (day,n)==(3,5) else ''
        q['figures'].append(asset(q,pdf.pages[page-1],page,im,f'figure-{i+1}',caption=caption))
       for o,im in zip(q['options'],opts):o['figure']=asset(q,pdf.pages[page-1],page,im,'option-'+o['label'])
      if (day,n) in COMPOSITES:
       page,stems,opts,captions=COMPOSITES[day,n]
       for i,box in enumerate(stems):q['figures'].append(asset(q,pdf.pages[page-1],page,1,f'figure-{i+1}',box,captions[i]))
       for o,box in zip(q['options'],opts):o['figure']=asset(q,pdf.pages[page-1],page,1,'option-'+o['label'],box)
      for f,alt in zip(q['figures'],edit.get('figureAlts',[])):f['alt']=alt
      for o,alt in zip(q['options'],edit.get('optionAlts',[])):
       if 'figure' in o:o['figure']['alt']=alt
      q['hasFigure']=bool(q['figures'])
    data['answerKeyStatus']='official GATE 2026 key verified for GA questions 1–10'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':run()
