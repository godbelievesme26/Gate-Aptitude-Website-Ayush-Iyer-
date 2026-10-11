// Companion to the agent's visual reading of both key PDF pages for 2025/2026.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {loadArchive} from '../../../js/loader.js';
globalThis.fetch=async p=>({ok:fs.existsSync(p),json:async()=>JSON.parse(fs.readFileSync(p,'utf8'))});
const archive=await loadArchive(),records=[];
const years=process.argv.slice(2).map(Number);
for(const year of years.length?years:[2026,2025]){
 const key=JSON.parse(fs.readFileSync(`internal/ae/AE${year}-key.json`,'utf8'));
 const separateSource=`internal/ae/AE${year}-key.pdf`,source=fs.existsSync(separateSource)?separateSource:key.source;
 const sha256=crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex');
 if(key.sha256!==sha256)throw Error('Key PDF hash differs from preserved extraction');
 for(const row of key.rows){
  const q=archive.questions.find(q=>q.paper==='AE'&&q.year===year&&q.number===row.number);
  let expected=row.rawKey.replace(/\*/g,'');
  if(expected!=='MTA'&&row.type==='NAT'){
   const ranges=expected.split(/\s+OR\s+/i).map(part=>{const values=part.trim().split(/\s+to\s+/).map(Number);if(values.length===1)values.push(values[0]);if(values.length!==2||values.some(v=>!Number.isFinite(v)))throw Error(`Unsupported key ${year}/${row.number}: ${part}`);return values;});
   expected=ranges.length===1?ranges[0]:ranges;
  }
  if(row.type==='MSQ'&&expected!=='MTA')expected=expected.split(';');
  if(row.type==='MCQ'&&/^[A-D](?:\s+or\s+[A-D])+$/i.test(expected))expected=expected.split(/\s+or\s+/i);
  const actual=q?.type==='NAT'&&typeof q.answer==='number'?[q.answer,q.answer]:q?.answer;
  const pass=q&&q.type===row.type&&q.marks===row.marks&&JSON.stringify(actual)===JSON.stringify(expected);
  records.push({questionId:q?.id,year,number:row.number,status:pass?'PASS':'FAIL',source,sha256,page:row.page,type:row.type,marks:row.marks,expected,actual:q?.answer,reviewedAt:new Date().toISOString(),method:source===separateSource?'All local key PDF pages visually read before running this companion comparison; extracted rows reconciled against loaded canonical records. Separate from manual user verification.':'All embedded answer annotations in the original local question PDF visually read; no separate key PDF available. Extracted rows compared with loaded canonical records; this is not independent official publication verification.',remotePublication:'NOT RE-FETCHED'});
 }
}
const output=`internal/ae/quality-audit/initial-key-comparison${years.length?'-'+years.join('-'):''}.json`;
if(fs.existsSync(output))throw Error('Evidence already exists');
fs.writeFileSync(output,JSON.stringify(records,null,2));
console.log({rows:records.length,failed:records.filter(r=>r.status!=='PASS').length});
