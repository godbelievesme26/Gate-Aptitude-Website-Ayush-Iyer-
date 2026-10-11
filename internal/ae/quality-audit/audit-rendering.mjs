// Read-only corpus audit. Uses the production loader and student-facing views.
// DOM evidence is deliberately kept separate from PDF and browser visual review.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {JSDOM} from 'jsdom';
import {loadArchive} from '../../../js/loader.js';
import {questionAssets} from '../../../js/corpus.js';
import {questionDetail,quiz,result} from '../../../js/views.js';
import {generateSession,submit} from '../../../js/domain.js';
import {defaults} from '../../../js/storage.js';

const phase=process.argv[2]||'initial';
if(!['initial','post-repair'].includes(phase))throw Error('Unknown audit phase');
const directory=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(.:)/,'$1'));
const output=path.join(decodeURIComponent(directory),`${phase}-automated.json`);
if(fs.existsSync(output))throw Error('Refusing to replace audit evidence: '+output);
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const originalFetch=globalThis.fetch;
globalThis.fetch=async p=>({ok:fs.existsSync(p),json:async()=>read(p)});
let archive;
try{archive=await loadArchive();}finally{globalThis.fetch=originalFetch;}
const manifest=read('data/ae/manifest.json');
const prior=read('internal/ae/forensic_audit_2007_2026.json');
const dom=new JSDOM('<!doctype html><body></body>');
const document=dom.window.document;
// Exam mode includes a hidden whole-paper dialog. Its repeated content is not
// part of the active solving surface and must not inflate option counts.
const isExposed=element=>{for(let p=element;p&&p!==document;p=p.parentElement)if(p.hidden||p.style?.display==='none'||p.style?.visibility==='hidden')return false;return true;};
const issues=[],records=[],fileHashes={};
const checksum=p=>fileHashes[p]??=(fs.existsSync(p)?hash(p):null);
const pdfEvidence=q=>({file:q.source?.file,pages:q.source?.pages??[],sha256:q.source?.sha256});
const membership=new Map();
for(const paper of archive.papers)for(const q of paper.questions){const rows=membership.get(q.id)||[];rows.push({paperId:paper.id,year:paper.year,position:paper.questionOrder.indexOf(q.id)+1,reference:paper.questionRefs.find(r=>r.id===q.id)});membership.set(q.id,rows);}
const sorted=[...archive.questions].sort((a,b)=>(b.paper==='AE')-(a.paper==='AE')||b.year-a.year||a.paper.localeCompare(b.paper)||a.number-b.number);
for(const q of sorted){
 const record={questionId:q.id,year:q.year,paper:q.paper,number:q.number,printedNumber:q.displayNumber??q.number,section:q.section,source:pdfEvidence(q),paperMembership:membership.get(q.id)||[],type:q.type,marks:q.marks,groupId:q.groupId??null,options:q.options.map(o=>o.label),assets:[...new Set(questionAssets(q).map(a=>a.src))],loaded:'PASS',domRendering:{},sourceComparison:'NOT YET AUDITED',browserLayout:'NOT YET AUDITED',visualInspection:'NOT YET AUDITED',issueIds:[]};
 const add=(category,field,observed,expected,{severity='high',safe=false,review=true,route=null}={})=>{
  const old=issues.find(i=>i.questionId===q.id&&i.category===category&&i.field===field&&i.observed===observed);
  if(old){if(route&&!old.routes.includes(route))old.routes.push(route);return;}
  const issue={id:`${phase}-${String(issues.length+1).padStart(5,'0')}`,questionId:q.id,year:q.year,paper:q.paper,printedQuestionNumber:record.printedNumber,field,category,severity,observed,expected,evidence:pdfEvidence(q),safeSourceSupportedFix:safe,requiresFurtherReview:review,routes:route?[route]:[],status:'OPEN'};
  issues.push(issue);record.issueIds.push(issue.id);
 };
 if(!q.source?.file||!checksum(q.source.file))add('missing source','source.file',String(q.source?.file),'An existing authoritative source PDF');
 else if(q.source.sha256!==checksum(q.source.file))add('source hash mismatch','source.sha256',String(q.source.sha256),'Stored source hash matches original PDF');
 for(const asset of questionAssets(q))if(!checksum(asset.src))add('missing figure',asset.src,'File does not exist','Question-specific image loads');
 const state=defaults(),draft=generateSession([q],state,{ids:[q.id],count:1},'audit-'+q.id);
 const timer={visit:0,remaining:()=>60000};
 const routes={detail:()=>questionDetail(state,archive,q.id),practice:()=>quiz(state,archive,draft,timer),exam:()=>quiz(state,archive,{...draft,index:0,origin:'paper',mode:'test'},timer),result:()=>{draft.answers[q.id]=q.type==='NAT'?'0':q.type==='MSQ'?[q.options[0]?.label]:q.options[0]?.label;submit(state,draft,archive.byId,new Date('2026-10-10T00:00:00Z'));return result(state,archive,draft.id);}};
 for(const [route,render] of Object.entries(routes)){
  try{
   document.body.innerHTML=render();
   const root=document.body,text=root.textContent;
   const surface=root.querySelector('.question-content');
   if(route!=='result'&&!surface)add('missing rendered content','question','No question-content element','Complete question body',{route});
   const options=[...root.querySelectorAll('.option-copy')].filter(isExposed);
   if(route!=='result'&&options.length!==q.options.length)add('missing rendered options','options',`${options.length} rendered / ${q.options.length} stored`,'All stored options rendered once',{route});
   const fields=[...root.querySelectorAll('.question-stem,.content-math,.content-table td,.content-table th,.option-copy,.prose')].filter(isExposed);
   for(const element of fields){
    const visible=element.textContent;
    const field=element.closest('.option-copy')?'options':element.matches('.prose')?'solution':'content';
    const raw=visible.match(/\\[A-Za-z]+(?:\*?\{|\b)|\/(?:frac|sqrt|begin)\b|\\[()[\]]/g);
    if(raw)add('visible mathematical markup',field,visible,'Supported mathematical notation renders without visible source commands',{safe:false,review:true,route});
    if(/[\uFFFD\u0008\u000C]/.test(visible))add('corrupted displayed characters',field,visible,'Source-faithful characters without replacement/control characters',{route});
   }
   for(const image of root.querySelectorAll('img'))if(!checksum(image.getAttribute('src')))add('missing rendered image',image.getAttribute('src'),'Image file does not exist','Image loads',{route});
   if(root.querySelector('iframe,object,embed')||[...root.querySelectorAll('img')].some(i=>/source-page|page-\d/.test(i.getAttribute('src'))))add('source page fallback','rendering','Full source-page element in rendered HTML','Question-specific structured rendering',{route});
   record.domRendering[route]={status:issues.some(i=>i.questionId===q.id&&i.routes.includes(route))?'FAIL':'PASS',characters:text.length,optionCount:options.length,images:root.querySelectorAll('img').length,scope:'Production view invoked in JSDOM; no layout engine or visual judgment'};
  }catch(error){record.domRendering[route]={status:'FAIL',error:String(error)};add('rendering exception','rendering',String(error),'Production view renders successfully',{safe:false,route});}
 }
 records.push(record);
}
const papers=archive.papers.sort((a,b)=>b.year-a.year).map(p=>{
 const raw=read(manifest.years.find(e=>e.year===p.year).path);
 return {year:p.year,paperId:p.id,declaredSourceQuestions:p.totalQuestions,sourceCountStatus:'NOT YET INDEPENDENTLY CHECKED',storedRecords:raw.questions.length,resolvedReferences:p.questions.length,reusedReferences:p.questions.length-raw.questions.length,loadedQuestions:p.questionOrder.filter(id=>archive.byId.has(id)).length,options:p.questions.reduce((n,q)=>n+q.options.length,0),uniqueAssets:new Set(p.questions.flatMap(q=>questionAssets(q).map(a=>a.src))).size,groups:p.questionGroups.length,questionIds:p.questionOrder,source:p.source,recordsWithDomIssues:p.questions.filter(q=>issues.some(i=>i.questionId===q.id&&i.routes.length)).length};
});
const summary={generatedAt:new Date().toISOString(),phase,method:'Production loadArchive plus detail/practice/exam/result in JSDOM. Source comparison and real-browser layout are separate pending gates.',earlierForensicReport:'internal/ae/forensic_audit_2007_2026.json',earlierForensicSummary:prior.summary??null,canonicalAERecords:papers.reduce((n,p)=>n+p.storedRecords,0),resolvedAEReferences:papers.reduce((n,p)=>n+p.resolvedReferences,0),existingGARecords:archive.sets.reduce((n,s)=>n+s.questions.length,0),reusedGAReferences:papers.reduce((n,p)=>n+p.reusedReferences,0),uniqueLoadedRecords:archive.questions.length,uniqueLoadedIds:archive.byId.size,domViewInvocations:records.length*4,recordsWithIssues:new Set(issues.map(i=>i.questionId)).size,issueCount:issues.length,sourceComparison:'NOT YET AUDITED',browserLayout:'NOT YET AUDITED',explanation:'AE2026 and AE2025 reuse ten existing GA records each. Count each stable ID once in the union; count shared references in each full paper. Previous forensic audit only enumerated directly stored AE records.'};
fs.writeFileSync(output,JSON.stringify({summary,papers,records,issues,fileHashes},null,2)+'\n');
dom.window.close();
console.log(JSON.stringify(summary,null,2));
