import fs from 'node:fs';
import crypto from 'node:crypto';
import {resolvePaper,questionAssets} from '../js/corpus.js';
import {applyQuestionMarking} from '../js/loader.js';

const read=path=>JSON.parse(fs.readFileSync(path,'utf8'));
const hash=path=>crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
const registry=read('data/registry.json'),existing=new Map(registry.flatMap(entry=>read(entry.path).questions.map(applyQuestionMarking)).map(q=>[q.id,q]));
const manifest=read('data/ae/manifest.json');

const completedYears=manifest.years.filter(row=>row.ingestionStatus==='complete');
if(completedYears.length<1)throw Error('No complete AE years in manifest');

const reports=[];

for(const entry of completedYears){
 const raw=read(entry.path),paper=resolvePaper(raw,existing),keys=read(`internal/ae/AE${entry.year}-key.json`);
 const totalQ = entry.totalQuestions || paper.totalQuestions || 65;
 const totalMarks = entry.totalMarks || paper.totalMarks || 100;
 if(paper.questions.length!==totalQ||paper.totalMarks!==totalMarks||paper.questions.some((q,i)=>q.number!==i+1))throw Error(`AE${entry.year} numbering/totals`);
 if(hash(paper.source.file)!==paper.source.sha256||hash(keys.source)!==keys.sha256)throw Error(`AE${entry.year} source hash mismatch`);
 const typeCounts={},assets=new Map();
 for(const q of paper.questions){
  typeCounts[q.type]=(typeCounts[q.type]||0)+1;
  const key=keys.rows.find(row=>row.number===q.number),ref=paper.questionRefs.find(row=>row.id===q.id);
  if(!key||key.type!==q.type||key.marks!==q.marks||key.section!==ref.section)throw Error(`Key metadata ${q.id}`);
  const expected=key.rawKey==='MTA*'?'MTA':q.type==='NAT'?(key.rawKey.includes(' OR ')?key.rawKey.split(' OR ').map(p=>p.includes(' to ')?p.split(' to ').map(Number):Number(p)):key.rawKey.includes(' to ')?key.rawKey.split(' to ').map(Number):Number(key.rawKey)):(q.type==='MSQ'||key.rawKey.includes(';')||/\b(?:OR|or)\b/.test(key.rawKey))?(/\b(?:OR|or)\b/.test(key.rawKey)?key.rawKey.split(/\s+(?:OR|or)\s+/).map(s=>s.trim()):key.rawKey.split(';').map(s=>s.trim())):key.rawKey;
  if(JSON.stringify(expected)!==JSON.stringify(q.answer))throw Error(`Key answer mismatch ${q.id}: expected ${JSON.stringify(expected)} vs got ${JSON.stringify(q.answer)}`);
  for(const asset of questionAssets(q)){
   if(!fs.existsSync(asset.src)||hash(asset.source.file)!==asset.source.sha256)throw Error(`Asset lineage ${asset.src}`);
   assets.set(asset.src,asset);
  }
  if(q.number>10&&(q.topic!==undefined||q.subtopic!==undefined||q.sourceImage!==undefined||q.solution!==null))throw Error(`Unapproved AE metadata ${q.id}`);
 }
 for(const [type,count] of Object.entries(entry.questionTypeCounts))if((typeCounts[type]||0)!==count)throw Error(`Type count mismatch ${type} in AE${entry.year}`);
 if(assets.size!==entry.figureAssetCount)throw Error(`Asset manifest count mismatch in AE${entry.year}: expected ${entry.figureAssetCount} vs actual ${assets.size}`);
 const report={paper:paper.id,year:entry.year,questions:totalQ,marks:totalMarks,typeCounts,assets:assets.size,newAssets:entry.newFigureAssetCount,officialAnswers:entry.answerAvailability.gradedAnswers,marksToAll:entry.answerAvailability.marksToAll,technicalSolutions:'not provided',verified:true};
 reports.push(report);
 console.log(`PASS: AE${entry.year}: ${totalQ} questions / ${totalMarks} marks; ${typeCounts.MCQ||0} MCQ, ${typeCounts.MSQ||0} MSQ, ${typeCounts.NAT||0} NAT; ${assets.size} figure assets. Official key/rulings, source lineage, sections and scope valid.`);
}

fs.writeFileSync('docs/ae-validation-report.json',JSON.stringify(reports,null,2)+'\n');
