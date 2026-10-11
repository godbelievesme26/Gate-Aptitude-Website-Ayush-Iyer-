import {loadArchive} from '/js/loader.js';
import {questionDetail,quiz,result} from '/js/views.js';
import {generateSession,submit} from '/js/domain.js';
import {defaults} from '/js/storage.js';
const $=id=>document.getElementById(id),main=$('main'),errors=[];
addEventListener('error',e=>errors.push({message:e.message,source:e.filename}));
addEventListener('unhandledrejection',e=>errors.push({message:String(e.reason)}));
const archive=await loadArchive();
const questions=[...archive.questions].sort((a,b)=>(b.paper==='AE')-(a.paper==='AE')||b.year-a.year||a.paper.localeCompare(b.paper)||a.number-b.number);
for(const q of questions){const option=document.createElement('option');option.value=q.id;option.textContent=q.id;$('question').append(option);}
let report;
function render(q,view){
 const state=defaults(),draft=generateSession([q],state,{ids:[q.id],count:1},'audit-'+q.id),timer={visit:0,remaining:()=>60000};
 if(view==='detail')return questionDetail(state,archive,q.id);
 if(view==='result'){draft.answers[q.id]=q.type==='NAT'?'0':q.type==='MSQ'?[q.options[0]?.label]:q.options[0]?.label;submit(state,draft,archive.byId);return result(state,archive,draft.id);}
 if(view==='exam'){draft.origin='paper';draft.mode='test';}
 return quiz(state,archive,draft,timer);
}
async function mount(q,view){
 main.innerHTML=render(q,view);
 // Solutions must be laid out too, rather than only checked inside closed details.
 for(const details of main.querySelectorAll('.feedback-solution'))details.open=true;
 await Promise.all([...main.querySelectorAll('img')].map(img=>img.decode().catch(()=>{})));
 await document.fonts.ready;
}
function exposed(el){for(let p=el;p&&p!==document;p=p.parentElement){const s=getComputedStyle(p);if(s.display==='none'||s.visibility==='hidden')return false;}return true;}
function measure(q,view){
 const fields=[...main.querySelectorAll('.question-stem,.content-math,.content-table,.option-copy,.prose,.question-group')].filter(exposed);
 const findings=[];
 for(const el of fields){
  const text=el.textContent,rect=el.getBoundingClientRect();
  if(/\\[A-Za-z]+(?:\*?\{|\b)|\/(?:frac|sqrt|begin)\b|\\[()[\]]/.test(text))findings.push({category:'visible mathematical markup',text});
  if(rect.width===0||rect.height===0)findings.push({category:'zero-size content',text});
  // A scrollable equation/table is reachable. Hidden/clip overflow is not.
  let clipped=false;
  for(let p=el;p&&p!==main;p=p.parentElement){const s=getComputedStyle(p);if(['hidden','clip'].includes(s.overflowX)&&p.scrollWidth>p.clientWidth+2){clipped=true;break;}}
  if(clipped)findings.push({category:'possible horizontal clipping',text,requiresVisualReview:true});
  if(el.scrollWidth>el.clientWidth+2&&!el.closest('.content-table-wrap'))findings.push({category:'content overflow',text,scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,requiresVisualReview:true});
 }
 const images=[...main.querySelectorAll('img')].filter(exposed);
 for(const img of images)if(!img.complete||!img.naturalWidth)findings.push({category:'broken image',src:img.getAttribute('src')});
 const optionCount=[...main.querySelectorAll('.option-copy')].filter(exposed).length;
 if(view!=='result'&&optionCount!==q.options.length)findings.push({category:'option count mismatch',actual:optionCount,expected:q.options.length});
 return {questionId:q.id,year:q.year,paper:q.paper,number:q.number,view,optionCount,imageCount:images.length,documentOverflow:document.documentElement.scrollWidth>innerWidth+2,findings,visualInspection:'NOT YET AUDITED'};
}
$('theme').onchange=()=>document.documentElement.dataset.theme=$('theme').value;
$('show').onclick=async()=>{await mount(archive.byId.get($('question').value),$('view').value);$('audit-status').textContent='Inspecting '+$('question').value+' · '+$('view').value;};
$('run').onclick=async()=>{
 $('run').disabled=true;$('show').disabled=true;$('download').disabled=true;
 report={generatedAt:new Date().toISOString(),viewport:{width:innerWidth,height:innerHeight},theme:$('theme').value,scope:'Production loader and views mounted with production CSS; no localStorage, network writes, or app action handlers',records:[],errors};
 try{
  for(let i=0;i<questions.length;i++){
   const q=questions[i];
   for(const view of ['practice','exam','detail','result']){
    try{await mount(q,view);report.records.push(measure(q,view));}catch(error){report.records.push({questionId:q.id,view,exception:String(error)});}
   }
   $('audit-status').textContent=`Audited ${i+1} / ${questions.length}: ${q.id}`;
   if(i%10===0)await new Promise(resolve=>setTimeout(resolve,0));
  }
  report.summary={questions:questions.length,views:report.records.length,recordsWithFindings:report.records.filter(r=>r.exception||r.findings?.length).length,errors:errors.length};
  $('audit-output').textContent=JSON.stringify(report.summary,null,2);
  $('audit-json').value=JSON.stringify(report,null,2);
  $('audit-status').textContent='Audit complete';$('download').disabled=false;
 }finally{$('run').disabled=false;$('show').disabled=false;}
};
$('download').onclick=()=>{const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:'application/json'}));link.download=`initial-browser-${report.viewport.width}-${report.theme}.json`;link.click();URL.revokeObjectURL(link.href);};
await mount(questions[0],'practice');$('audit-status').textContent=`Ready: ${questions.length} questions`;
