from pathlib import Path
import pypdf, json
rows=[]
for p in sorted(Path('Aptitude Sets').rglob('*.pdf')):
 d=pypdf.PdfReader(p).pages
 text='\n'.join(f'\n=== PAGE {i+1} ===\n'+page.extract_text() for i,page in enumerate(d))
 out=Path('tmp/pdfs')/(p.parent.name+'-'+p.stem+'.txt')
 out.write_text(text,encoding='utf-8')
 rows.append({'file':str(p),'pages':len(d),'text':str(out),'first':text[:850],'last':text[-500:]})
print(json.dumps(rows,ensure_ascii=True,indent=2))


