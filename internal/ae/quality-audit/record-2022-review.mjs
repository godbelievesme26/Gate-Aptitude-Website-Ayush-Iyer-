import fs from 'node:fs';
import crypto from 'node:crypto';
const root='internal/ae/quality-audit/', qs=JSON.parse(fs.readFileSync('data/ae/2022.json','utf8')).questions, issues=[], now=new Date().toISOString();
function add(n,field,category,expected,safe=true){const q=qs.find(q=>q.number===n);issues.push({id:`initial-source-${q.id}-${issues.length+1}`,questionId:q.id,year:2022,paper:'AE',printedQuestionNumber:n,field,category,severity:'high',observed:{question:q.question,options:q.options,figures:q.figures,answer:q.answer},expected,evidence:q.source,safeSourceSupportedFix:safe,requiresFurtherReview:!safe,status:'OPEN',recordedAt:now});}
add(5,'content order','source figure ordering','Source page 5 places the target shape before the phrase shown above. Canonical content places it after the statement. Restore figure-before-statement order.');
add(27,'options.C','source symbol mismatch','Source page 21 uses sea-level subscripts s in p_s, T_s and rho_s, not 0. Values and units are otherwise faithful.');
for(const [n,expected] of [
 [10,'Source page 10 has complete case M and case N labels. Both are cut off at the bottom of the current figure.'],
 [16,'Source page 14 has P and S labels above the control volume. The current crop excludes them.'],
 [17,'Source page 15 has a downward-pointing vertical axis arrow. The current crop cuts off its lower end.'],
 [22,'Source page 19 figure crop includes a clipped duplicate line of question text at its top.'],
 [33,'Source page 24 figure crop includes a clipped fragment of the preceding prompt at its top.'],
 [52,'Source page 35 includes the full 2 m height label and 5 mm gap label. Current crop cuts off the left height label and right gap label.']
])add(n,'figures and content figure assets','incorrect crop',expected,false);
add(53,'figures and content','missing source figure','Source page 36 contains a converging duct diagram with P and Q sections. The canonical question has no figure at all. Restore the source diagram with source coordinates and preserved provenance.',false);
add(65,'answer and extracted key row','key transcription mismatch','The locally preserved key PDF page 2 explicitly accepts 6 or greater than 6. The extracted key JSON says 6 to 6 and canonical answer is [6,6]. Preserve the original key and investigate the existing grading representation for the open-ended accepted range; do not silently constrain it to six.',false);
const records=qs.map(q=>({questionId:q.id,year:2022,paper:'AE',printedQuestionNumber:q.number,source:q.source,reviewedAt:now,reviewer:'agent-source-audit',phase:'initial',method:'All 42 original PDF pages visually compared with all 65 canonical statements/options; all 32 referenced current assets compared with source; both local key PDF pages visually read.',evidence:{sourceSheets:'visual/2022/source-01.png through source-40.png, step 3',assetSheets:'visual/2022-current-assets-1.png through -6.png',keySheets:['visual/2022-key-1.png','visual/2022-key-2.png'],browserReports:['initial-browser-1440-light.json','initial-browser-1440-dark.json','initial-browser-390-light.json','initial-browser-390-dark.json']},sourceComparison:issues.some(i=>i.questionId===q.id)?'FAIL':'PASS',numbering:'PASS',marks:'PASS',groupRelationships:'PASS: no linked/common-data groups',figureAssociation:q.number===53?'FAIL: missing duct figure':'PASS',figureCrop:[10,16,17,22,33,52].includes(q.number)?'FAIL':q.number===53?'NOT APPLICABLE: missing':'PASS',officialKeyAndType:'See initial-key-comparison-2022.json',studentFacingVisualInspection:'NOT YET AUDITED',renderingReview:{automated:'See existing four browser reports by questionId; flags are not a visual pass',visual:'NOT YET AUDITED'},issueIds:issues.filter(i=>i.questionId===q.id).map(i=>i.id),qualification:'Mathematical meaning of stored LaTeX was compared with PDF independently of renderer support. Existing browser markup flags remain open. Source-sheet inspection is not student-facing browser inspection. No manual user verification changed.'}));
const key=JSON.parse(fs.readFileSync('internal/ae/AE2022-key.json','utf8'));
const hash=crypto.createHash('sha256').update(fs.readFileSync(key.source)).digest('hex');
if(hash!==key.sha256)throw Error('Key hash mismatch');
const keys=key.rows.map(row=>{const q=qs.find(q=>q.number===row.number);let expected=row.rawKey;
 if(row.type==='MSQ'||row.type==='MCQ'&&expected.includes(';'))expected=expected.split(';');
 if(row.type==='NAT'){expected=expected.split(' OR ').map(s=>{const r=s.split(/\s+to\s+/).map(Number);return r.length===1?[r[0],r[0]]:r;});if(expected.length===1)expected=expected[0];}
 let actual=row.type==='NAT'&&typeof q.answer==='number'?[q.answer,q.answer]:q.answer;
 if(row.number===65)expected={minimum:6,maximum:null,sourceText:'6 or greater than 6'};
 return{questionId:q.id,year:2022,number:q.number,status:JSON.stringify(expected)===JSON.stringify(actual)&&q.type===row.type&&q.marks===row.marks?'PASS':'FAIL',source:key.source,sha256:hash,page:q.number<=44?1:2,type:row.type,marks:row.marks,expected,actual:q.answer,reviewedAt:now,method:'Both preserved key PDF pages visually read. Special alternatives Q5 and Q55 retained; Q65 extraction discrepancy checked directly against PDF.',remotePublication:'NOT RE-FETCHED'};});
for(const name of ['initial-source-review.jsonl','initial-source-issues.jsonl'])if(fs.readFileSync(root+name,'utf8').includes('"year":2022'))throw Error('Evidence already recorded');
if(fs.existsSync(root+'initial-key-comparison-2022.json'))throw Error('Key evidence exists');
fs.appendFileSync(root+'initial-source-review.jsonl',records.map(JSON.stringify).join('\n')+'\n');
fs.appendFileSync(root+'initial-source-issues.jsonl',issues.map(JSON.stringify).join('\n')+'\n');
fs.writeFileSync(root+'initial-key-comparison-2022.json',JSON.stringify(keys,null,2));
console.log({reviewed:records.length,issues:issues.length,keyFailures:keys.filter(k=>k.status==='FAIL').map(k=>k.number)});
