import {resolvePaper} from './corpus.js';
let cache;
export const normalize=text=>String(text??'').normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
export function applyQuestionMarking(question,index){const marks=index<5?1:2;return {...question,exam:'GATE',section:'GA',marks,negativeMarks:marks/3,markingRule:'gate-ga-one-third-negative'};}
async function json(url){const r=await fetch(url);if(!r.ok)throw Error(`Could not load ${url}`);return r.json();}
export async function loadArchive(){
 if(cache)return cache;
 const registry=await json('data/registry.json');const sets=await Promise.all(registry.map(s=>json(s.path)));
 const questions=sets.flatMap(s=>s.questions.map((q,index)=>({...applyQuestionMarking(q,index),day:s.day,search:normalize([q.question,...q.options.map(o=>o.text),q.solution,q.topic,q.chapter].join(' '))})));
 const byId=new Map(questions.map(q=>[q.id,q]));if(byId.size!==questions.length)throw Error('Duplicate question IDs');
 const corpusManifest=await json('data/ae/manifest.json'),papers=[];
 for(const entry of corpusManifest.years.filter(entry=>entry.ingestionStatus==='complete')){
  const paper=resolvePaper(await json(entry.path),byId);papers.push(paper);
  for(const q of paper.questions)if(!byId.has(q.id)){const record={...q,search:normalize([q.question,...(q.content?q.content.filter(b=>b.text).map(b=>b.text):[]),...q.options.map(o=>o.text),q.subject,q.year,q.paper].join(' '))};questions.push(record);byId.set(q.id,record);}
 }
 let verification={};
 try{const v=await json('data/ae/verification.json');if(v&&typeof v==='object'&&!Array.isArray(v))verification=v;}catch{}
 return cache={registry,sets,questions,byId,papers,corpusManifest,verification};
}
