// Explicit source findings from the agent's visual review of all 40 PDF pages.
import fs from 'node:fs';
const root='internal/ae/quality-audit/',qs=JSON.parse(fs.readFileSync('data/ae/2024.json','utf8')).questions;
const now=new Date().toISOString(),issues=[];
function add(q,field,category,observed,expected,safe=true){issues.push({id:`initial-source-${q.id}-${issues.length+1}`,questionId:q.id,year:2024,paper:'AE',printedQuestionNumber:q.number,field,category,severity:'high',observed,expected,evidence:q.source,recordedAt:now,status:'OPEN',safeSourceSupportedFix:safe,requiresFurtherReview:!safe});}
for(const q of qs){
 for(const [field,text] of [['question/content',q.question],...q.options.map(o=>['option '+o.label,o.text])]){
  if(text.includes('=== [PAGE'))add(q,field,'source extraction contamination',text,'Remove extraction page markers, running page headers/footers and next-section marks headings. Preserve actual question and option text.');
  if(/[\uE000-\uF8FF]/u.test(text))add(q,field,'corrupted mathematical glyph',text,'Replace private-use font glyphs with the specific source symbol: gamma in Q40/Q58; rho and subscript infinity in Q63.');
 }
}
const math={
 2:'Restore x/y as a fraction.',4:'Option B is the mixed percentage 14 + 2/7 percent.',
 5:'Restore powers p^2,q^2,p^4,q^4 and fraction (p^4+q^4)/(p^2 q^2).',
 12:'Restore C_1,C_2,v_0,v^2 and the four logarithmic fraction expressions from PDF page 9.',
 13:'Restore the six-component stress/strain vectors, 6x6 stiffness matrix and the four fractions in the options. Matrix rows: P,Q,Q,0,0,0; Q,P,Q,0,0,0; Q,Q,P,0,0,0; 0,0,0,R,0,0; 0,0,0,0,R,0; 0,0,0,0,0,R.',
 17:'Restore chemical subscripts C10H12, N2 and O2.',19:'Heating value is 43.4 times 10^6 J/kg, not 43.4 times 106; C_p is subscripted.',
 22:'Restore indices on V,T,M and option C = (1/sqrt(1.2)) M_1.',24:'Restore the pressure coefficient subscripts P_I and P_II.',28:'Option D has C_{L,max}.',
 31:'Restore definite integral from 1 to 2 of dx/(1+x^2); current separated text loses the bounds and fraction.',34:'Restore cubic/squared units kg/m^3 and m^2.',35:'The angle is 5 degrees, not the letters 5o.',
 36:'Restore e^(px), second/first derivatives and squared p,q in both the expression and option C.',37:'Restore k*pi*R^3 and option fractions 5/12,5/24,7/12,7/24.',
 39:'Restore G M_Earth = 3.98 times 10^14 m^3/s^2; current text reads 1014.',40:'Restore C_p; gamma is separately logged as a private-use glyph.',41:'Restore heating value 44 times 10^6 J/kg.',
 42:'Options B,C,D have exponents 3/2,1/2,-1/2 on U.',43:'Restore subscripts 1,2,3 on Mach numbers.',44:'Restore degree signs on 49.76 and 26.38.',45:'Restore piecewise x^2 for x<0 and x for x>=0.',
 46:'Restore subscripts I,II,Y on stresses.',48:'Restore subscript n on C_n.',51:'Restore 2x2 matrix [5,-4; k,-1].',52:'Restore squared units N/mm^2.',54:'Restore M_x and N/m^2.',
 55:'Restore double time derivatives with subscripts 1,2, and omega = alpha sqrt(k/m).',56:'Restore strain subscripts and x*y^2, x^2*y.',57:'Restore 5 times 10^6 N and m/s^2.',58:'Restore 45 degree symbol; gamma glyph separately logged.',
 61:'Restore density units kg/m^3.',63:'Restore C_d = D / ((1/2) rho U_infinity^2 c), with correct subscripts and fraction; rho/infinity glyphs separately logged.',
 64:'Restore m^2, kg/m^3 and m/s^2.',65:'Restore model drag subscript m in D_m and D/D_m.'
};
for(const [n,expected] of Object.entries(math)){const q=qs.find(q=>q.number===Number(n));add(q,'question/content and mathematical options','lost mathematical structure',{question:q.question,options:q.options.map(o=>({label:o.label,text:o.text}))},expected);}
add(qs.find(q=>q.number===6),'question/content','source transcription mismatch','Extraneous letter s before blank (iv).','Source has the fourth blank directly before “his shoulders”; remove the stray s.');
add(qs.find(q=>q.number===8),'content and option D','table/order corruption','Energy-density table flattened into prose; pie labels appended to option D; diagram occurs after the final question prompt.','Restore source order: introduction, pie chart, table introduction, two-column energy table, final prompt. Option D contains only 3,600.');
for(const [n,expected] of [[25,'Attach the first stress/strain graph to option A and second graph to option D.'],[48,'Attach the yawing-moment graph to option B.']]){const q=qs.find(q=>q.number===n);add(q,'content figure blocks / options','incorrect option-image placement','Option diagrams are inserted as unlabeled question-stem figures.',expected);}
for(const n of [8,14,28,53]){const q=qs.find(q=>q.number===n);add(q,'figure asset','figure crop contamination','Crop includes clipped fragments of adjacent question text (Q8 below; Q14/Q28/Q53 above).','Diagram and all labels without clipped surrounding body text. Source coordinates require visual localization before replacement.',false);}
const records=qs.map(q=>({questionId:q.id,year:2024,paper:'AE',printedQuestionNumber:q.number,source:q.source,reviewedAt:now,reviewer:'agent-source-audit',phase:'initial',
 method:'All 40 original PDF pages visually compared with canonical statements/options and all 22 current referenced assets; no manual user verification changed.',
 evidence:{sourceSheets:'visual/2024/source-01.png through source-40.png, step 3',assetSheets:'visual/2024-current-assets-1.png through -4.png'},
 sourceComparison:issues.some(i=>i.questionId===q.id)?'FAIL':'PASS',numbering:'PASS',marks:'PASS',groupRelationships:'PASS',
 figureAssociation:[25,48].includes(q.number)?'FAIL: option placement':'PASS',figureCrop:[8,14,28,53].includes(q.number)?'FAIL':'PASS',
 officialKeyAndType:'NOT YET AUDITED',studentFacingVisualInspection:'NOT YET AUDITED',issueIds:issues.filter(i=>i.questionId===q.id).map(i=>i.id),
 qualification:'Source count is 65 unique questions. No common-data/linked groups. Passing source comparison does not certify typography/browser rendering, official key, or accessible descriptions. Original watermarks and borders are not treated as factual defects.'}));
for(const [name,rows] of [['initial-source-review.jsonl',records],['initial-source-issues.jsonl',issues]]){
 if(fs.readFileSync(root+name,'utf8').includes('"year":2024'))throw Error('Evidence already recorded');
 fs.appendFileSync(root+name,rows.map(r=>JSON.stringify(r)).join('\n')+'\n');
}
console.log({reviewed:records.length,issues:issues.length,affected:new Set(issues.map(i=>i.questionId)).size});
