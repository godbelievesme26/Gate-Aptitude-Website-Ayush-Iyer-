import pdfplumber,re,json
from pathlib import Path
for path in sorted(Path('Aptitude Sets').rglob('*.pdf')):
 with pdfplumber.open(path) as pdf:
  markers=[]
  for i,p in enumerate(pdf.pages[:13]):
   for line in p.extract_text_lines():
    if re.match(r'^Q\.\s*\d+\b',line['text']) and not re.search(r'Carry|[–−]',line['text'][:22]):
     n=int(re.match(r'^Q\.\s*(\d+)',line['text'])[1])
     if n<=11:markers.append((n,i+1,round(line['top']),line['text'][:60]))
  print(str(path),json.dumps(markers,ensure_ascii=True))
