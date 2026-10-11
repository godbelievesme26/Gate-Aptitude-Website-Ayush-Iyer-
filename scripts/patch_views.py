from pathlib import Path

path = Path('c:/Users/godbe/Desktop/Aptitude Website/js/views.js')
content = path.read_text(encoding='utf-8')

old_part = """export function aerospace(s,a,id){
 const aeManifest=a.corpusManifest;
 if(!aeManifest)return head('Aerospace PYQs','Aerospace engineering previous year questions.')+'<p>Aerospace manifest not found.</p>';
 if(id){
  const paper=a.papers.find(p=>p.id===id||String(p.year)===id);
  if(!paper)return head('Paper not found')+link('Back to Aerospace PYQs','#/aerospace');
  const typeCounts=paper.questionTypeCounts||{MCQ:29,MSQ:14,NAT:22};
  return head(`GATE Aerospace ${paper.year}`,`Complete paper · ${paper.totalQuestions} questions · ${paper.totalMarks} marks`)+
  `<div class="grid2"><section class="panel">
    <h2>Paper summary</h2>
    <div class="row"><span>Duration</span><strong>${paper.durationMinutes} minutes</strong></div>
    <div class="row"><span>Question types</span><strong>${Object.entries(typeCounts).map(([k,v])=>`${k}: ${v}`).join(', ')}</strong></div>
    ${paper.sections.map(sec=>`<div class="row"><span>${esc(sec.title)}</span><strong>${sec.questionIds.length} questions, ${sec.totalMarks} marks</strong></div>`).join('')}
    <div class="actions" style="margin-top:20px;">
      ${button('Start PYQ','start-paper',paper.id,'primary')}
      ${button('Timed Test','time-paper',paper.id)}
    </div>
  </section></div>`;
 }
 const yearsList=aeManifest.years.slice().reverse().map(yearInfo=>{
  const isAvailable=yearInfo.ingestionStatus==='complete';
  const metadata=isAvailable?`<div class="caption">${yearInfo.questionCount} questions · ${yearInfo.totalMarks} marks</div>`:`<div class="caption">Coming soon</div>`;
  const action=isAvailable?link('View Paper',`#/aerospace/${yearInfo.year}`,'button primary'):`<button class="ghost" disabled>Not available</button>`;
  return `<section class="panel set-card"><div class="section-head"><span class="eyebrow">GATE ${yearInfo.year}</span><span class="pill">${isAvailable?'Available':'Unavailable'}</span></div>
    <h2>${yearInfo.year} · ${esc(yearInfo.paper)}</h2>
    <p>Aerospace Engineering</p>
    ${metadata}
    <div class="actions">${action}</div>
    </section>`;
 }).join('');
 return head('Aerospace PYQs','Practice actual GATE Aerospace questions.')+`<div class="grid3">${yearsList}</div>`;
}"""

new_part = """export function aerospace(s,a,id){
 const aeManifest=a.corpusManifest;
 if(!aeManifest)return head('Aerospace PYQs','Aerospace engineering previous year questions.')+'<p>Aerospace manifest not found.</p>';
 if(id){
  const paper=a.papers.find(p=>p.id===id||String(p.year)===id);
  if(!paper)return head('Paper not found')+link('Back to Aerospace PYQs','#/aerospace');
  const typeCounts=paper.questionTypeCounts||{MCQ:29,MSQ:14,NAT:22};
  const verifiedCount=paper.questionOrder.filter(qId=>a.verification?.[qId]?.status==='verified').length;
  return head(`GATE Aerospace ${paper.year}`,`Complete paper · ${paper.totalQuestions} questions · ${paper.totalMarks} marks`)+
  `<div class="grid2"><section class="panel">
    <h2>Paper summary</h2>
    <div class="row"><span>Duration</span><strong>${paper.durationMinutes} minutes</strong></div>
    <div class="row"><span>Manual verification</span><strong>${verifiedCount} / ${paper.totalQuestions} verified</strong></div>
    <div class="row"><span>Question types</span><strong>${Object.entries(typeCounts).map(([k,v])=>`${k}: ${v}`).join(', ')}</strong></div>
    ${paper.sections.map(sec=>`<div class="row"><span>${esc(sec.title)}</span><strong>${sec.questionIds.length} questions, ${sec.totalMarks} marks</strong></div>`).join('')}
    <div class="actions" style="margin-top:20px;">
      ${button('Start PYQ','start-paper',paper.id,'primary')}
      ${button('Timed Test','time-paper',paper.id)}
    </div>
  </section></div>`;
 }
 const yearsList=aeManifest.years.slice().reverse().map(yearInfo=>{
  const isAvailable=yearInfo.ingestionStatus==='complete';
  const paper=a.papers.find(p=>p.year===yearInfo.year);
  const verifiedCount=paper?paper.questionOrder.filter(qId=>a.verification?.[qId]?.status==='verified').length:0;
  const metadata=isAvailable?`<div class="caption">${yearInfo.questionCount} questions · ${yearInfo.totalMarks} marks<br><strong style="color:var(--text-accent, #2b669a);">${verifiedCount} / ${yearInfo.questionCount} verified</strong></div>`:`<div class="caption">Coming soon</div>`;
  const action=isAvailable?link('View Paper',`#/aerospace/${yearInfo.year}`,'button primary'):`<button class="ghost" disabled>Not available</button>`;
  return `<section class="panel set-card"><div class="section-head"><span class="eyebrow">GATE ${yearInfo.year}</span><span class="pill">${isAvailable?'Available':'Unavailable'}</span></div>
    <h2>${yearInfo.year} · ${esc(yearInfo.paper)}</h2>
    <p>Aerospace Engineering</p>
    ${metadata}
    <div class="actions">${action}</div>
    </section>`;
 }).join('');
 return head('Aerospace PYQs','Practice actual GATE Aerospace questions.')+`<div class="grid3">${yearsList}</div>`;
}"""

assert old_part in content, "old_part not found"
updated = content.replace(old_part, new_part, 1)
path.write_text(updated, encoding='utf-8')
print("Successfully updated views.js with aerospace verification counts!")
