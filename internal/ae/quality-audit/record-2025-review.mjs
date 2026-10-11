// Records observations from the 34 pages and 18 current assets inspected by the agent.
// It does not perform or claim automatic source verification.
import fs from 'node:fs';
const root='internal/ae/quality-audit/';
const qs=JSON.parse(fs.readFileSync(root+'2025-canonical-review.json','utf8'));
const now=new Date().toISOString(),issues=[];
const add=(n,field,category,observed,expected,safe=true)=>{
 const q=qs.find(q=>q.number===n);
 issues.push({id:`initial-source-${q.id}-${issues.length+1}`,questionId:q.id,year:2025,paper:'AE',printedQuestionNumber:n,field,category,severity:category==='source transcription mismatch'?'high':'medium',observed,expected,evidence:q.source,safeSourceSupportedFix:safe,requiresFurtherReview:!safe,status:'OPEN',recordedAt:now});
};
for(const n of [12,14,16,33,43,59]){
 const q=qs.find(q=>q.number===n);
 add(n,'question and content text','source transcription mismatch',q.question,'Remove the spurious n/nn at the equation boundary; use the line layout shown on the original PDF. Q12 also has an added introductory sentence not printed in the source.');
}
add(21,'options A-D','malformed mathematics',qs.find(q=>q.number===21).options.map(o=>o.text),'Four square roots of fractions: inertia/viscous, inertia/elastic, elastic/viscous, viscous/inertia. Repair unbalanced fraction braces and root grouping.');
add(42,'question and content text','source transcription mismatch',qs.find(q=>q.number===42).question,'The source equation is r = (2 / sqrt(pi)) times (1 - sin(theta)). The (1 - sin(theta)) factor is outside the denominator.');
add(61,'question and content text','malformed mathematics',qs.find(q=>q.number===61).question,'The three mass-flow terms have a dot above m and subscript a,c, as shown on PDF page 33.');
add(19,'options[].figure.alt','incorrect accessible figure description',qs.find(q=>q.number===19).options.map(o=>o.figure.alt),'Describe the actual four airfoil/flow-direction/moment-arrow diagrams. These are not pitching-moment-versus-alpha curves.');
for(const n of [20,27,29,30,49,53,56,57,58,59,60])add(n,`figures/gate-2025-ae-ae-${n}-figure-1.png`,'figure contamination','Red and blue audit rectangles are baked into the current asset; they are absent from the original source. Source page borders are also included.','Use a clean source crop containing the complete diagram and all labels, without diagnostic rectangles.',false);
const textFailures=new Set([12,14,16,33,42,43,59,61]);
const cropFailures=new Set([20,27,29,30,49,53,56,57,58,59,60]);
const records=qs.map(q=>({questionId:q.id,year:2025,paper:'AE',printedQuestionNumber:q.number,reviewedAt:now,reviewer:'agent-source-audit',phase:'initial',source:q.source,
 method:'Visual comparison of all 34 original PDF pages with loaded canonical statements/options/tables; all 18 referenced assets visually compared with source diagrams. No user verification changed.',
 evidence:{sourceSheets:'internal/ae/quality-audit/visual/2025/source-01.png through source-34.png, step 3',assetSheets:'internal/ae/quality-audit/visual/2025-current-assets-1.png through -3.png'},
 statement:textFailures.has(q.number)?'FAIL':'PASS',options:q.number===21?'FAIL':'PASS',tables:'PASS',numbering:'PASS',marks:'PASS',groupRelationships:'PASS',figureAssociation:'PASS',figureCrop:cropFailures.has(q.number)?'FAIL':'PASS',accessibleFigureDescription:q.number===19?'FAIL':'NOT YET AUDITED',
 officialKeyAndType:'PASS against locally preserved key PDF',studentFacingVisualInspection:q.number===21?'FAIL: malformed options visible in desktop practice screenshot':'NOT YET AUDITED',
 issueIds:issues.filter(i=>i.questionId===q.id).map(i=>i.id),qualification:'No groups in this paper. Mathematical browser rendering and editorial solutions remain separate checks. Original watermark is not itself a defect. Key PDF was visually read; its current remote publication was not re-fetched.'}));
for(const [name,rows] of [['initial-source-review.jsonl',records],['initial-source-issues.jsonl',issues]]){
 const old=fs.readFileSync(root+name,'utf8');
 if(old.includes('"year":2025'))throw Error('2025 evidence already exists');
 fs.appendFileSync(root+name,rows.map(r=>JSON.stringify(r)).join('\n')+'\n');
}
console.log({reviewed:records.length,issues:issues.length});
