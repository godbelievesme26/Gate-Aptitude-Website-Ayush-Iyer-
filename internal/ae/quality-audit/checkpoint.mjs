import fs from 'node:fs';
const root='internal/ae/quality-audit/';
const read=name=>JSON.parse(fs.readFileSync(root+name,'utf8'));
const lines=name=>fs.readFileSync(root+name,'utf8').trim().split('\n').map(JSON.parse);
const base=read('initial-automated.json'),reviews=lines('initial-source-review.jsonl'),issues=lines('initial-source-issues.jsonl');
const years=Array.from({length:20},(_,i)=>2026-i).map(year=>({year,
 canonicalAndLoadedUniqueRecords:base.records.filter(r=>r.paper==='AE'&&r.year===year).length,
 sourceCompared:reviews.filter(r=>r.year===year).length,
 recordedSourceIssues:issues.filter(r=>r.year===year).length,
 sourceAffectedQuestions:new Set(issues.filter(r=>r.year===year).map(r=>r.questionId)).size,
 automatedVisibleMarkupIssues:base.issues.filter(r=>r.year===year&&r.paper==='AE').length,
 fixes:0,postRepairAudit:'NOT YET AUDITED'}));
const browserReports=['1440-light','390-light','390-dark','1440-dark'].map(key=>{const d=read(`initial-browser-${key}.json`);return{file:`initial-browser-${key}.json`,viewport:d.viewport,theme:d.theme,...d.summary};});
const sourceYearsCompleted=years.filter(y=>y.sourceCompared===y.canonicalAndLoadedUniqueRecords).map(y=>y.year);
const nextYear=years.find(y=>y.sourceCompared<y.canonicalAndLoadedUniqueRecords)?.year;
const keys=fs.readdirSync(root).filter(name=>/^initial-key-comparison(?:-\d+)*\.json$/.test(name)).flatMap(read);
const checkpoint={updatedAt:new Date().toISOString(),phase:'Full initial baseline - incomplete; canonical repairs not started',uniqueLoadedQuestions:base.records.length,
 sourceComparisonRecords:reviews.length,sourceYearsCompleted,nextSourceQuestion:`gate-${nextYear}-ae-ga-01`,sourceIssues:issues.length,
 nextSteps:[`Continue all source questions from AE${nextYear} Q1 through AE2007, then remaining GA papers.`,'Finish per-question complex browser visual review and classify mobile overflow findings.','After complete baseline, repair shared rendering/data/assets with old/new evidence, then repeat full independent audit.'],
 browserReports,years,protection:read('integrity-checkpoint.json'),
 qualifications:['No final source or rendering pass is claimed.',`Local key comparisons cover ${keys.length} rows: ${keys.filter(k=>k.status==='PASS').length} PASS, ${keys.filter(k=>k.status==='FAIL').length} FAIL, ${keys.filter(k=>k.status==='UNVERIFIABLE').length} UNVERIFIABLE; remote publication not re-fetched.`,'A passing load/DOM check is not source fidelity.','Source statuses are agent audit evidence, never user manual verification.','Additional browser inspection is pending: selecting the audit tab was rejected by browser URL security policy on 2026-10-11; no alternative control path was used. Existing browser reports remain preserved.']};
fs.writeFileSync(root+'checkpoint.json',JSON.stringify(checkpoint,null,2));
console.log({reviewed:reviews.length,issues:issues.length,next:checkpoint.nextSourceQuestion});
