// Paper configuration is content, never persisted learner state. GA daily sets
// remain their own source records; paper references reuse their existing IDs.
import {generateSession} from './domain.js';

export const assetPath=path=>typeof path==='string'&&/^figures\/gate-\d{4}-[a-z0-9]+-(?:ga|ae)-\d{2,3}-(?:figure-\d+|option-[A-Z0-9]+)\.png$/.test(path);
export function contentAssets(blocks=[]){return blocks.filter(b=>b.type==='figure').map(b=>b.asset);}
export function questionAssets(q){return [...(q.figures||[]),...contentAssets(q.content),...(q.options||[]).flatMap(o=>[...(o.figure?[o.figure]:[]),...contentAssets(o.content)]),...contentAssets(q.group?.content)];}
const fail=message=>{throw Error('Invalid corpus: '+message);};
function validateAsset(asset){
 if(!assetPath(asset?.src)||!asset.alt||!asset.source?.file||!Number.isInteger(asset.source.page)||asset.source.page<1||!asset.source.sha256)fail('figure lineage');
 if(asset.verificationStatus!==undefined&&asset.verificationStatus!=='source-verified')fail('unverified figure');
}
export function validateBlocks(blocks){
 if(!Array.isArray(blocks)||!blocks.length)fail('empty structured content');
 for(const block of blocks){
  if(['text','math'].includes(block.type)){if(typeof block.text!=='string'||!block.text.trim())fail('empty text/math');}
  else if(block.type==='figure')validateAsset(block.asset);
  else if(block.type==='table'){
   const width=block.headers?.length||block.rows?.[0]?.length;
   if(!width||!block.rows?.length||block.rows.some(row=>!Array.isArray(row)||row.length!==width||row.some(cell=>typeof cell!=='string')))fail('table shape');
  }else fail('unsupported content block');
 }
}
export function resolvePaper(paper,existing=new Map()){
 if(paper.schemaVersion!==1||!paper.id||!paper.exam||!Number.isInteger(paper.year)||!paper.paper)fail('paper identity/version');
 if(!Number.isInteger(paper.totalQuestions)||paper.totalQuestions<1||!(paper.totalMarks>0))fail('paper totals');
 if(paper.durationMinutes!==null&&(!(paper.durationMinutes>0)||!Number.isFinite(paper.durationMinutes)))fail('duration');
 const records=new Map(existing),newIds=new Set();
 for(const q of paper.questions){if(records.has(q.id)||newIds.has(q.id))fail('duplicate question '+q.id);newIds.add(q.id);records.set(q.id,q);}
 const order=paper.questionOrder;
 if(!Array.isArray(order)||order.length!==paper.totalQuestions||new Set(order).size!==order.length)fail('question order/count');
 const refs=new Map(paper.questionRefs.map(ref=>[ref.id,ref]));
 if(refs.size!==order.length||paper.questionRefs.length!==order.length||[...newIds].some(id=>!order.includes(id)))fail('question references');
 const sections=new Map(paper.sections.map(section=>[section.id,section]));
 if(sections.size!==paper.sections.length||paper.sectionOrder.length!==sections.size||new Set(paper.sectionOrder).size!==sections.size||paper.sectionOrder.some(id=>!sections.has(id)))fail('section order');
 const sectionMembers=paper.sectionOrder.flatMap(id=>sections.get(id).questionIds);
 if(JSON.stringify(sectionMembers)!==JSON.stringify(order))fail('section membership/order');
 const numbers=new Set(),groups=new Map();
 for(const group of paper.questionGroups||[]){
  if(!group.id||groups.has(group.id)||!['common-data','linked-answer'].includes(group.type)||!group.questionIds?.length||new Set(group.questionIds).size!==group.questionIds.length||group.questionIds.some(id=>!order.includes(id)))fail('question group');
  validateBlocks(group.content);groups.set(group.id,group);
  if(group.type==='linked-answer'){
   if(!Array.isArray(group.dependencies))fail('linked dependencies');
   for(const dependency of group.dependencies)if(!group.questionIds.includes(dependency.questionId)||!group.questionIds.includes(dependency.dependsOn)||group.questionIds.indexOf(dependency.dependsOn)>=group.questionIds.indexOf(dependency.questionId))fail('linked dependency order');
  }
 }
 const questions=order.map(id=>{
  const q=records.get(id),ref=refs.get(id);
  if(!q||!ref||q.year!==paper.year||q.paper!==paper.paper||q.number!==ref.number||numbers.has(q.number)||!Number.isInteger(q.number)||q.number<1)fail('question identity '+id);
  numbers.add(q.number);
  if(!sections.get(ref.section)?.questionIds.includes(id)||(q.section&&q.section!==ref.section))fail('question section');
  if(!['MCQ','MSQ','NAT'].includes(q.type)||!(q.marks>0)||!Array.isArray(q.options))fail('question type/marks');
  if(q.transcriptionStatus!=='source-verified'||!q.source?.sha256||!q.source.pages?.length)fail('question provenance');
  if(q.content)validateBlocks(q.content);else if(!q.question)fail('question content');
  const labels=q.options.map(o=>o.label);
  if(new Set(labels).size!==labels.length||labels.some(label=>typeof label!=='string'||!/^[A-Za-z0-9]+$/.test(label)))fail('option labels');
  if(q.type==='NAT'?labels.length!==0:labels.length<2)fail('options for type');
  for(const option of q.options){if(option.content)validateBlocks(option.content);else if(!option.text&&!option.figure)fail('empty option');}
  for(const asset of questionAssets(q))validateAsset(asset);
  if(q.answer!==undefined){
   if(q.gradingRule==='marks-to-all'){if(q.answer!=='MTA')fail('MTA ruling');}
   else if(q.type==='MCQ'){if(Array.isArray(q.answer)?(!q.answer.length||q.answer.some(v=>!labels.includes(v))):!labels.includes(q.answer))fail('MCQ key');}
   else if(q.type==='MSQ'){if(!Array.isArray(q.answer)||!q.answer.length||new Set(q.answer).size!==q.answer.length||q.answer.some(v=>!labels.includes(v)))fail('MSQ key');}
   else if(!(typeof q.answer==='number'&&Number.isFinite(q.answer))&&!(Array.isArray(q.answer)&&q.answer.length===2&&q.answer.every(Number.isFinite)&&q.answer[0]<=q.answer[1])&&!(Array.isArray(q.answer)&&q.answer.length>0&&q.answer.every(item=>(typeof item==='number'&&Number.isFinite(item))||(Array.isArray(item)&&item.length===2&&item.every(Number.isFinite)&&item[0]<=item[1]))))fail('NAT key');
  }
  const group=q.groupId?groups.get(q.groupId):null;
  if(q.groupId&&!group?.questionIds.includes(id))fail('group reference');
  for(const g of groups.values())if(g.questionIds.includes(id)&&g.id!==q.groupId)fail('group membership');
  // Preserve existing GA object identity. Additional section metadata lives in refs.
  return group?{...q,group}:q;
 });
 if(questions.reduce((sum,q)=>sum+q.marks,0)!==paper.totalMarks)fail('total marks');
 for(const section of sections.values())if(questions.filter(q=>section.questionIds.includes(q.id)).reduce((sum,q)=>sum+q.marks,0)!==section.totalMarks)fail('section marks');
 for(const q of questions.filter(q=>newIds.has(q.id))){const fraction=paper.marking?.negativeFraction?.[q.type];if(!Number.isFinite(fraction)||fraction<0||q.negativeMarks!==q.marks*fraction)fail('marking configuration');}
 return {...paper,questions};
}

export function orderedSessionQuestions(questions,ids){
 if(!Array.isArray(ids))return questions;
 const byId=new Map(questions.map(q=>[q.id,q])),seen=new Set();
 return ids.map(id=>{if(seen.has(id))throw Error('Duplicate session question ID.');seen.add(id);const q=byId.get(id);if(!q)throw Error('A selected question is unavailable.');return q;});
}
export function generatePaperSession(paper,state,config={},id){
 // Callers pass a resolved paper; ordering is explicit and never an archive filter.
 const ordered=orderedSessionQuestions(paper.questions,config.ids||paper.questionOrder);
 return generateSession(ordered,state,{...config,paper:paper.paper,year:paper.year,origin:config.origin||'paper',count:config.count||ordered.length,minutes:config.minutes??paper.durationMinutes,ids:ordered.map(q=>q.id),paperId:paper.id},id);
}
