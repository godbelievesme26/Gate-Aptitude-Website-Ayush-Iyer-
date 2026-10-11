"""Reproduce AE2026 from the supplied PDF and reviewed transcription overrides.

Only AE2026 is extracted. Existing GA records are referenced, never rewritten.
Source PDFs stay under internal/; only individual figure XObjects are published.
"""
from pathlib import Path
import json, re, hashlib, unicodedata
from collections import Counter
from pypdf import PdfReader
import pdfplumber
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
PDF = 'internal/ae/AE2026.pdf'
KEY = 'internal/ae/AE2026-key.pdf'
KEY_URL = 'https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf'
VERIFIED = '2026-10-06'
def digest(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def write(path, value):
    target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def clean(text): return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()

FIGURES = {
11:(10,'Closed contour O–P–Q–R–O with O (0,0), P (1,1), Q (0,2), R (−1,1), arrows and coordinate axes.'),
12:(11,'Square-wave Fourier approximation with fluctuations near x = −1 and x = +1.'),
18:(15,"Temperature–entropy diagram showing cycles 1–2–3–4–1 and 1–2–3′–4′–1."),
21:(17,'Nozzle with flow arrow, converging jet boundaries and crossing waves downstream of the exit.'),
25:(19,'Figures P and Q: airfoil lift curves against angle of attack, with solid retracted and dashed deployed curves.'),
27:(21,'Rotor blade configurations I and II with flow arrows and the positive theta direction marked upward.'),
28:(22,'Compressor pressure ratio against mass flow rate: points A and B on the descending part of one speed line.'),
38:(26,'Turbofan schematic with fan and core streams, compressor, combustor, high and low pressure turbines, nozzle and stations 0, 2, 3, 4, 4.5, 5.'),
40:(28,'Unit square with one corner at the origin, aligned with the x and y axes.'),
42:(30,'Compressor stage with rotor R and stator S, stations 1 before rotor, 2 between rotor and stator, and 3 after stator.'),
46:(33,'Rotor velocity triangles labelled C1, C2, W1, W2 and U; dimensions 60, 15, 80 and 100, all in m/s.'),
47:(34,'Uniform flow U to the right past two vortices separated by a, with −Γ at the upper vortex and +Γ at the lower vortex.'),
59:(37,'Fixed support above a vertical bar labelled L, E, A, attached in series to spring k and mass M.'),
60:(38,'Stepped cantilever fixed at C, segment C–B labelled E,I2 and L2, segment B–A labelled E,I1 and L1; downward load P at A.'),
64:(39,'Centered expansion fan at a downward corner θ; ending-wave angle ψ is measured from the incoming horizontal stream.')}

def build():
    source_hash=digest(PDF); key_hash=digest(KEY)
    reader=PdfReader(ROOT/PDF); key_reader=PdfReader(ROOT/KEY)
    keys={}
    for page,p in enumerate(key_reader.pages,1):
        for line in p.extract_text().splitlines():
            m=re.match(r'^\s*(\d+)\s+2\s+(MCQ|MSQ|NAT)\s+(GA|AE)\s+(.+?)\s+([12])\s*$',line)
            if m:
                number,kind,section,value,marks=m.groups();keys[int(number)]={'number':int(number),'type':kind,'section':section,'rawKey':value,'marks':int(marks),'page':page}
    assert sorted(keys)==list(range(1,66))
    write('internal/ae/AE2026-key.json',{'source':KEY,'sha256':key_hash,'url':KEY_URL,'rows':list(keys.values())})
    overrides=json.loads((ROOT/'scripts/ae2026-transcriptions.json').read_text(encoding='utf8'))
    questions=[]; lineage=[]; assets=[]
    with pdfplumber.open(ROOT/PDF) as positioned:
        for page,p in enumerate(reader.pages,1):
            text=p.extract_text().split('Organizing Institute:')[0]
            starts=list(re.finditer(r'(?:^|\n)Q\.(\d+)\s+(?![–−-])',text))
            for index,m in enumerate(starts):
                n=int(m.group(1)); body=text[m.end():starts[index+1].start() if index+1<len(starts) else len(text)]
                # Section heading preceding Q36 is not part of the preceding question.
                body=re.sub(r'Q\.\d+\s*[–−-]\s*Q\.\d+\s+Carry.*','',body,flags=re.S)
                words=positioned.pages[page-1].extract_words()
                boundary=next(w for w in words if w['text']==f'Q.{n}')
                end=next((w['top']-4 for w in words if index+1<len(starts) and w['text']==f'Q.{starts[index+1].group(1)}'),780)
                provenance={'file':PDF,'sha256':source_hash,'pages':[{'page':page,'bbox':[70,round(boundary['top']-4,2),525,round(end,2)],'coordinateSystem':'PDF points, top-left origin'}],'verificationStatus':'source-verified','verifiedOn':VERIFIED}
                lineage.append({'questionId':f'gate-2026-ae-{"ga" if n<=10 else "ae"}-{n:02}','number':n,'source':provenance})
                if n<=10: continue
                split=re.split(r'\(([A-D])\)\s*',body)
                q={'id':f'gate-2026-ae-ae-{n:02}','exam':'GATE','year':2026,'paper':'AE','number':n,'section':'AE','subject':'Aerospace Engineering','type':keys[n]['type'],'marks':keys[n]['marks'],'question':clean(split[0]),'options':[{'label':split[i],'text':clean(split[i+1])} for i in range(1,len(split),2)],'content':[],'figures':[],'groupId':None,'source':provenance,'transcriptionStatus':'source-verified','solution':None,'solutionAvailability':'not-provided-in-source','gradingStatus':'official key verified','answerSource':{'url':KEY_URL,'paper':'AE','questionNumber':n,'section':'AE','page':keys[n]['page'],'sha256':key_hash,'verifiedOn':VERIFIED}}
                edit=overrides.get(str(n),{})
                if 'question' in edit:q['question']=edit['question']
                if 'options' in edit:q['options']=[{'label':label,'text':value} for label,value in zip('ABCD',edit['options'])]
                q['content']=edit.get('content',[{'type':'text','text':q['question']}])
                if 'optionContent' in edit:
                    for o in q['options']:
                        if o['label'] in edit['optionContent']:o['content']=edit['optionContent'][o['label']]
                raw=keys[n]['rawKey']
                if raw=='MTA*':q['answer']='MTA';q['gradingRule']='marks-to-all'
                elif q['type']=='NAT':q['answer']=[float(v) for v in raw.split(' to ')]
                elif q['type']=='MSQ':q['answer']=raw.split(';')
                else:q['answer']=raw
                # Data-driven penalties, consumed by the existing scorer unchanged.
                q['negativeMarks']=q['marks']/3 if q['type']=='MCQ' else 0
                q['markingRule']='gate-2026-official'
                if n in FIGURES:
                    expected_page,alt=FIGURES[n];assert page==expected_page
                    embedded=next(im for im in p.images if im.name.startswith('Im1.'))
                    rgba=embedded.image.convert('RGBA');im=Image.new('RGBA',rgba.size,'white');im.alpha_composite(rgba);im=im.convert('RGB')
                    bbox=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
                    im=im.crop(bbox);src=f'figures/gate-2026-ae-ae-{n:02}-figure-1.png';im.save(ROOT/src)
                    pdf_image=next(v for v in positioned.pages[page-1].images if v['name']=='Im1')
                    asset={'src':src,'alt':alt,'source':{'file':PDF,'sha256':source_hash,'page':page,'image':embedded.name,'bbox':[round(pdf_image[k],2) for k in ['x0','top','x1','bottom']],'coordinateSystem':'PDF points, top-left origin','pixelCrop':list(bbox)},'verificationStatus':'source-verified','verifiedOn':VERIFIED}
                    q['figures']=[asset];assets.append(asset)
                    marker=next((i for i,b in enumerate(q['content']) if b['type']=='figure'),None)
                    if marker is None:q['content'].append({'type':'figure','asset':asset})
                    else:q['content'][marker]={'type':'figure','asset':asset}
                q['hasFigure']=bool(q['figures']);questions.append(q)
    assert len(questions)==55
    ga=json.loads((ROOT/'data/day01.json').read_text(encoding='utf8'))['questions']
    for q in ga:
        assert q['source']['sha256']==source_hash and q['answer']==keys[q['number']]['rawKey']
    refs=[{'id':q['id'],'number':q['number'],'section':'GA','recordRef':'data/day01.json#'+q['id']} for q in ga]+[{'id':q['id'],'number':q['number'],'section':'AE'} for q in questions]
    sections=[{'id':'GA','title':'General Aptitude','questionIds':[r['id'] for r in refs if r['section']=='GA'],'totalMarks':15},{'id':'AE','title':'Aerospace Engineering','questionIds':[r['id'] for r in refs if r['section']=='AE'],'totalMarks':85}]
    paper={'schemaVersion':1,'id':'gate-2026-ae','exam':'GATE','year':2026,'paper':'AE','totalQuestions':65,'totalMarks':100,'durationMinutes':180,'sectionOrder':['GA','AE'],'sections':sections,'marking':{'id':'gate-2026-official','negativeFraction':{'MCQ':1/3,'MSQ':0,'NAT':0},'partialCredit':False,'sourceUrl':'https://gate2026.iitg.ac.in/question-paper-pattern.html'},'source':{'file':PDF,'sha256':source_hash,'archive':'AE.zip','archiveEntry':'AE/AE2026.pdf','pageCount':39},'questionOrder':[r['id'] for r in refs],'questionRefs':refs,'questionGroups':[],'questions':questions,'ingestionStatus':'complete','verificationStatus':'source-verified','verifiedOn':VERIFIED}
    write('data/ae/2026.json',paper)
    ga_assets=[f for q in ga for f in q['figures']+[o['figure'] for o in q['options'] if 'figure' in o]]
    all_assets=ga_assets+assets
    manifest={'schemaVersion':1,'exam':'GATE','paper':'AE','years':[{'year':y,'paper':'AE','sourcePdf':f'AE/AE{y}.pdf','ingestionStatus':'NOT_INGESTED','verificationStatus':'NOT_VERIFIED','path':None} for y in range(2007,2026)]+[{'year':2026,'paper':'AE','sourcePdf':PDF,'path':'data/ae/2026.json','questionCount':65,'newQuestionCount':55,'reusedGAQuestionCount':10,'totalMarks':100,'sections':sections,'questionTypeCounts':dict(Counter(v['type'] for v in keys.values())),'answerAvailability':{'officialKey':65,'gradedAnswers':63,'marksToAll':2,'unavailable':0},'figureAssetCount':len(all_assets),'newFigureAssetCount':len(assets),'reusedFigureAssetCount':len(ga_assets),'optionFigureCount':sum('figure' in o for q in ga for o in q['options']),'structuredTableCount':sum(b['type']=='table' for q in questions for b in q['content']),'questionGroupCount':0,'ingestionStatus':'complete','verificationStatus':'source-verified','verifiedOn':VERIFIED}]}
    write('data/ae/manifest.json',manifest)
    write('internal/ae/AE2026-lineage.json',{'source':paper['source'],'questions':lineage,'assets':all_assets,'review':{'pagesVisuallyChecked':list(range(1,40)),'keyPagesChecked':[1,2],'relationships':'No common-data or linked-answer groups in AE2026.','sourceWording':'Preserved, including unusual wording in Q18, Q28, Q35 and Q39.','editorialSolutions':'Existing GA solutions reused; no technical solutions supplied or invented.'}})
    print(json.dumps(manifest['years'][-1],ensure_ascii=False,indent=2))

if __name__=='__main__':build()
