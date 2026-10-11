import fs from 'node:fs';
import path from 'node:path';
import './validate-ae.mjs';
const registry=JSON.parse(fs.readFileSync('data/registry.json','utf8'));
const ids=new Set();let count=0,graded=0,solutions=0,figureCount=0;const warnings=[];
for(const entry of registry){
 const set=JSON.parse(fs.readFileSync(entry.path,'utf8'));
 if(set.day!==entry.day||set.questions.length!==10)throw Error(`Invalid set ${entry.path}`);
 for(const q of set.questions){
  if(!q.id||ids.has(q.id))throw Error(`Duplicate/missing ID ${q.id}`);ids.add(q.id);
  if(!q.question||q.number<1||q.number>10||q.year!==set.year||q.marks!==(q.number<=5?1:2))throw Error(`Invalid question ${q.id}`);
  if(!fs.existsSync(q.sourceImage)||!fs.existsSync(q.source.file)||q.figure&&!fs.existsSync(q.figure))throw Error(`Broken source ${q.id}`);
  if(q.options.length!==4||q.options.map(o=>o.label).join('')!=='ABCD')(()=>{throw Error(`Invalid option labels ${q.id}`)})();
  if(q.type&&!['MCQ','MSQ','NAT'].includes(q.type))throw Error(`Invalid type ${q.id}`);
  if(q.answer!==undefined&&q.type==='MCQ'&&!(q.answer==='MTA'&&q.gradingRule==='marks-to-all')&&!q.options.some(o=>o.label===q.answer))throw Error(`Invalid answer ${q.id}`);
  if(q.answer!==undefined)graded++;
  if(q.solution)solutions++;
  if(q.transcriptionStatus==='source-verified'){
   if(!q.answerSource?.url||q.answerSource.paper!==q.paper||q.answerSource.questionNumber!==q.number||!q.solution)throw Error(`Missing verification ${q.id}`);
   for(const o of q.options)if(!o.text&&!o.figure)throw Error(`Empty option ${q.id} ${o.label}`);
   for(const asset of [...q.figures,...q.options.flatMap(o=>o.figure?[o.figure]:[])]){
    if(!fs.existsSync(asset.src)||!asset.alt||asset.source.sha256!==q.source.sha256||asset.source.file!==q.source.file)throw Error(`Broken figure lineage ${q.id}`);
    figureCount++;
   }
  }
  for(const key of ['subject','chapter','topic','subtopic','difficulty','solution'])if(q[key]!==undefined&&typeof q[key]!=='string')throw Error(`Invalid ${key}`);
  count++;
 }
}
console.log(`PASS: ${registry.length} datasets, ${count} unique questions, source and image paths valid.`);
console.log(`${graded} questions have official keys and ${solutions} editorial solutions; ${count-graded} remain ungraded. ${figureCount} source figure assets verified. The user-supplied one-third negative-mark rule is unchanged.`);
console.log(warnings.join('\n')||'All questions contain four extracted option labels.');
fs.writeFileSync('docs/validation-report.json',JSON.stringify({sets:registry.length,questions:count,warnings,graded,solutions,figureAssets:figureCount,ungraded:count-graded},null,2));
