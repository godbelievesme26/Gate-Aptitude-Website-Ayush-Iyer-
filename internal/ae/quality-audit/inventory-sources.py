"""Read-only source inventory. Extracted text is candidate evidence, not verification."""
import hashlib
import json
import pathlib
import re
import zipfile
from datetime import datetime, timezone
from pypdf import PdfReader

root=pathlib.Path.cwd()
out=root/'internal/ae/quality-audit'
target=out/'initial-source-inventory.json'
if target.exists():
    raise RuntimeError('Refusing to replace baseline source inventory')
baseline=json.loads((out/'initial-automated.json').read_text(encoding='utf-8'))
paths={r['source']['file'] for r in baseline['records']}
paths.update(p['source']['file'] for p in baseline['papers'])
archive=zipfile.ZipFile(r'C:\Users\godbe\Desktop\Gate Aerospace\AE.zip')
sources=[]
textdir=out/'source-text'
textdir.mkdir(exist_ok=True)
for source in sorted(paths):
    file=root/source
    if not file.exists():
        sources.append({'file':source,'status':'MISSING'})
        continue
    digest=hashlib.sha256(file.read_bytes()).hexdigest()
    doc=PdfReader(file)
    pages=[]
    for number,page in enumerate(doc.pages,1):
        text=page.extract_text() or ''
        pages.append({'page':number,'width':float(page.mediabox.width),'height':float(page.mediabox.height),'textCharacters':len(text.strip()),'questionNumberCandidates':[int(n) for n in re.findall(r'(?:^|\n)\s*Q\.?\s*(\d+)\b',text)],'text':text})
    textfile=textdir/(digest+'.json')
    if not textfile.exists():
        textfile.write_text(json.dumps({'source':source,'sha256':digest,'pages':pages},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    year=re.fullmatch(r'internal/ae/AE(\d{4})\.pdf',source)
    archive_match=None
    if year:
        member='AE/AE'+year[1]+'.pdf'
        archive_match=hashlib.sha256(archive.read(member)).hexdigest()==digest
    sources.append({'file':source,'sha256':digest,'pageCount':len(pages),'archiveMatch':archive_match,'textEvidence':textfile.relative_to(root).as_posix(),'pagesWithoutExtractedText':[p['page'] for p in pages if p['textCharacters']<20],'questionNumberCandidates':sorted(set(n for p in pages for n in p['questionNumberCandidates'])),'sourceQuestionCount':'NOT YET INDEPENDENTLY CHECKED','sourceFidelity':'NOT YET AUDITED'})
    print(source,len(pages),'pages',flush=True)
target.write_text(json.dumps({'createdAt':datetime.now(timezone.utc).isoformat(),'method':'Original PDFs read with pypdf. Text extraction, numbering candidates and scan hints do not certify fidelity. Original archive compared by hash for every AE year.','sources':sources},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
