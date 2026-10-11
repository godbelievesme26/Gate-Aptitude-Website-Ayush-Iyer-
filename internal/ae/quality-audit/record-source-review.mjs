// Persist the explicitly inspected AE2026 source evidence from this audit.
// This is an agent audit, separate from the user's manual verification records.
import fs from 'node:fs';
const root='internal/ae/quality-audit/';
const baseline=JSON.parse(fs.readFileSync(root+'initial-automated.json','utf8'));
const affected=new Set([12,18,21,25,27,28,38,40,42,46,47,59,60,64]);
const reviewedAt=new Date().toISOString();
const records=baseline.records.filter(q=>q.year===2026&&q.paper==='AE').map(q=>({
 questionId:q.questionId,year:q.year,paper:q.paper,printedQuestionNumber:q.printedNumber,
 reviewedAt,reviewer:'agent-source-audit',phase:'initial',source:q.source,
 method:'Visual comparison of all 39 original PDF pages with current canonical statements/options; current figure contact sheets inspected separately. Not a user manual verification.',
 evidence:{sourceSheets:'tmp/ae2026/review-01.png through review-37.png, in steps of 3',assetSheets:'internal/ae/quality-audit/visual/2026-current-assets-1.png through -5.png'},
 statement:'PASS',options:'PASS',valuesUnitsAndMathStructure:'PASS',tables:'PASS',numbering:'PASS',marks:'PASS',groupRelationships:'PASS',figureAssociation:'PASS',
 figureCrop:affected.has(q.number)?'FAIL':'PASS',
 officialKeyAndType:'NOT YET AUDITED',studentFacingVisualInspection:'NOT YET AUDITED',
 qualification:'Math structure compared with source; this does not certify the browser renderer. Table status means not applicable when absent. No common-data or linked-answer groups in this paper.'
}));
const issues=records.filter(q=>q.figureCrop==='FAIL').map(q=>({
 id:`initial-source-${q.questionId}-crop`,questionId:q.questionId,year:q.year,paper:q.paper,printedQuestionNumber:q.printedQuestionNumber,
 field:`figures/${q.questionId}-figure-1.png`,category:'figure crop contamination',severity:'medium',
 observed:'Figure contains clipped or duplicated surrounding question text'+(q.printedQuestionNumber===64?' and partial table headings':q.printedQuestionNumber===47?' and a repeated final prompt':''),
 expected:'Complete source diagram and labels without adjacent question text or table fragments',
 evidence:q.source,visualEvidence:q.evidence.assetSheets,safeSourceSupportedFix:false,requiresFurtherReview:true,
 nextStep:'After the complete initial baseline, localize the diagram in the original source, preserve the old asset, and visually validate a replacement crop. Coordinates not yet established.',
 status:'OPEN',recordedAt:reviewedAt
}));
for(const [name,rows] of [['initial-source-review.jsonl',records],['initial-source-issues.jsonl',issues]]){
 if(fs.existsSync(root+name))throw Error('Evidence already exists: '+name);
 fs.writeFileSync(root+name,rows.map(r=>JSON.stringify(r)).join('\n')+'\n');
}
console.log({sourceRecords:records.length,cropIssues:issues.length});
