import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {resolvePaper,generatePaperSession,orderedSessionQuestions,questionAssets,validateBlocks} from '../js/corpus.js';
import {loadArchive,applyQuestionMarking} from '../js/loader.js';
import {questionContent,notation,optionShortcut,questionAnswer} from '../js/question-content.js';
import {questionDetail,bank,quiz,result,review} from '../js/views.js';
import {generateSession,submit} from '../js/domain.js';
import {scoreQuestion,scoreSession} from '../js/scoring.js';
import {revisionState,generateReviewSession} from '../js/revision.js';
import {Store,defaults,validateState} from '../js/storage.js';
import {ApplicationState} from '../js/state.js';
import {saveNumericAnswer} from '../js/answer-input.js';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const registry=read('data/registry.json'),sets=registry.map(e=>read(e.path)),ga=sets.flatMap(s=>s.questions.map(applyQuestionMarking)),gaById=new Map(ga.map(q=>[q.id,q]));
const raw=read('data/ae/2026.json'),paper=resolvePaper(raw,gaById),qs=paper.questions,manifest=read('data/ae/manifest.json');
const archive={registry,sets,questions:[...ga,...qs.slice(10)],byId:new Map([...ga,...qs.slice(10)].map(q=>[q.id,q]))};
const q=n=>qs[n-1],timer={visit:0,remaining:()=>60000};
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

test('AE2026 has 65 uniquely numbered records, 100 marks, configured GA then AE sections',()=>{
 assert.equal(qs.length,65);assert.equal(new Set(qs.map(q=>q.id)).size,65);
 assert.deepEqual(qs.map(q=>q.number),Array.from({length:65},(_,i)=>i+1));
 assert.deepEqual(raw.sectionOrder,['GA','AE']);assert.deepEqual(raw.sections.map(s=>[s.questionIds.length,s.totalMarks]),[[10,15],[55,85]]);
 assert.equal(qs.reduce((s,q)=>s+q.marks,0),100);
 assert.deepEqual(qs.map(q=>q.marks),qs.map(q=>q.number<=5||q.number>=11&&q.number<=35?1:2));
 assert.equal(raw.durationMinutes,180);assert.equal(raw.questionGroups.length,0);
});
test('AE2026 official question types include 29 MCQ, 14 MSQ and 22 NAT',()=>{
 const expected=n=>n<=21||n>=36&&n<=43?'MCQ':n<=30||n>=44&&n<=48?'MSQ':'NAT';
 for(const item of qs)assert.equal(item.type,expected(item.number));
 assert.deepEqual(manifest.years.at(-1).questionTypeCounts,{MCQ:29,MSQ:14,NAT:22});
});
test('AE official answers, numeric intervals and MTA rulings match checked key rows',()=>{
 assert.equal(qs.slice(0,21).map(q=>q.answer).join(''),'ABABCDADCCACACCBBBDCA');
 assert.deepEqual(qs.slice(21,30).map(q=>q.answer),[['A','B'],['B','C','D'],['A','B'],['A','C'],['A','B','C'],['A','D'],['A','C','D'],['A','B'],['B','C']]);
 assert.equal(qs.slice(35,43).map(q=>q.answer).join(''),'BDAADCAB');
 assert.deepEqual(qs.slice(43,48).map(q=>q.answer),[['A','C','D'],['A','B','C'],'MTA',['B','D'],['C','D']]);
 assert.deepEqual(qs.filter(q=>q.type==='NAT').map(q=>q.answer),[[60,60],[1,1],[.440,.450],[50,50],'MTA',[.151,.155],[.67,.71],[1.5,1.5],[-645.50,-645.44],[513270,513272],[.2,.2],[.167,.169],[.43,.45],[.860,.890],[197,202],[1000,1000],[.9,1.1],[39,41],[.26,.29],[-5.5,-5],[27.2,27.6],[4.5,5]]);
});
test('existing GA records are reused by identity, with no duplicate attempt identities or data edits',()=>{
 for(const item of qs.slice(0,10))assert.strictEqual(item,gaById.get(item.id));
 assert.equal(archive.byId.size,215);assert.equal(ga.length,160);
 for(const [path,expected] of Object.entries(read('docs/home-colour-pass/preservation.json')))if(path.startsWith('data/'))assert.equal(hash(path),expected,path);
});
test('all figures/options resolve to question-specific assets with reproducible source lineage',()=>{
 const assets=new Map();
 for(const item of qs){
  assert.equal(item.options.length,item.type==='NAT'?0:4);
  for(const option of item.options)assert.ok(option.text||option.figure||option.content);
  for(const asset of questionAssets(item)){assert.ok(fs.statSync(asset.src).size>0);assert.equal(hash(asset.source.file),asset.source.sha256);assert.ok(asset.alt);assets.set(asset.src,asset);}
 }
 assert.equal(assets.size,25);assert.equal(qs.slice(10).flatMap(q=>q.figures).length,15);
 for(const asset of qs.slice(10).flatMap(q=>q.figures)){assert.equal(asset.verificationStatus,'source-verified');assert.equal(asset.source.bbox.length,4);assert.equal(asset.source.pixelCrop.length,4);assert.match(asset.source.image,/^Im1\./);}
});
test('all 65 questions render through the canonical renderer without PDF page fallback',()=>{
 for(const item of qs){
  const html=questionContent(item);assert.match(html,/question-content/);assert.doesNotMatch(html,/source-reader|source-frame|question-image|<iframe|<object|\.pdf|content is being verified|Verified figure unavailable/);
  if(item.sourceImage)assert.ok(!html.includes(item.sourceImage));
  assert.equal([...html.matchAll(/class="option-letter"/g)].length,item.options.length);
 }
 for(const n of [54,64,65])assert.match(questionContent(q(n)),/<table/);
 assert.match(questionContent(q(49)),/math-fraction/);assert.match(questionContent(q(37)),/math-matrix/);
 assert.match(questionContent(q(35)),/induced drag it incurs/);assert.match(questionContent(q(39)),/specific impulse due to gravity/);
});
test('notation extensions preserve nested fractions, matrices, scripts and text escaping',()=>{
 const html=notation('\\frac{τ_{r}}{τ_{λ}} + \\matrix{a & b; c & d}');
 assert.match(html,/τ<sub>r<\/sub>/);assert.match(html,/--matrix-columns:2/);assert.doesNotMatch(html,/\\frac|\\matrix/);
 assert.doesNotMatch(notation('\\frac{<img>}{<script>}'),/<img>|<script>/);
 assert.match(notation('\\frac{unclosed'),/\\frac/);
});
test('numeric shortcuts cannot inject option letters into NAT answers and option labels are data-driven',()=>{
 assert.equal(optionShortcut(q(31),'1'),null);assert.equal(optionShortcut(q(11),'1'),'A');
 assert.equal(optionShortcut({type:'MCQ',options:[{label:'X'},{label:'Y'}]},'2'),'Y');
 assert.equal(optionShortcut({type:'MCQ',options:[{label:'X'}]},'4'),null);
 assert.equal(questionAnswer(q(33)),'0.44 to 0.45');assert.equal(questionAnswer(q(31)),'60');
});
test('MCQ penalties, exact MSQ sets, NAT boundaries and both MTA types use existing scoring',()=>{
 assert.equal(scoreQuestion(q(11),'B').marks,-1/3);assert.equal(scoreQuestion(q(36),'A').marks,-2/3);
 assert.equal(scoreQuestion(q(22),['A']).marks,0);assert.equal(scoreQuestion(q(22),['B','A']).marks,1);
 assert.equal(scoreQuestion(q(33),'0.440').result,'correct');assert.equal(scoreQuestion(q(33),'0.450').result,'correct');assert.equal(scoreQuestion(q(33),'0.451').marks,0);
 for(const n of [35,46])for(const answer of [null,'',0,['A']])assert.equal(scoreQuestion(q(n),answer).result,'awarded');
 const answers=Object.fromEntries(qs.map(q=>[q.id,q.type==='NAT'&&Array.isArray(q.answer)?q.answer[0]:q.answer]));assert.equal(scoreSession(qs,answers).score,100);
});
test('AE detail, bank, solver and result use truthful subject, controls and solution availability',()=>{
 const s=defaults();
 assert.match(questionDetail(s,archive,q(38).id),/Aerospace Engineering/);assert.match(questionDetail(s,archive,q(38).id),/No source solution available/);
 assert.match(bank(s,archive,new URLSearchParams('year=2026&paper=AE&page=2')),/Aerospace Engineering/);
 for(const n of [11,22,31,35,46,64]){
  const d=generatePaperSession(paper,s,{ids:[q(n).id]},'solve-'+n),html=quiz(s,archive,d,timer);
  assert.match(html,n===31||n===35||n===64?/Numeric answer/:/data-action="answer"/);
  if(q(n).type!=='MCQ'&&q(n).answer!=='MTA')assert.match(html,/No negative marking/);
  assert.doesNotMatch(html,/Editorial solution|Answer: /);
 }
 const d=generatePaperSession(paper,s,{ids:[q(31).id]},'nat-result');d.answers[q(31).id]='60';submit(s,d,archive.byId);assert.match(result(s,archive,d.id),/Correct/);
});
test('paper and explicit retry orders survive shuffled archive order',()=>{
 const s=defaults(),reversed={...paper,questions:[...qs].reverse()};
 assert.deepEqual(generatePaperSession(reversed,s,{},'all').questionIds,raw.questionOrder);
 const ids=[q(64).id,q(22).id,q(11).id];assert.deepEqual(generateSession(orderedSessionQuestions(archive.questions,ids),s,{ids},'explicit').questionIds,ids);
 assert.throws(()=>orderedSessionQuestions(qs,[q(1).id,q(1).id]),/Duplicate/);assert.throws(()=>orderedSessionQuestions(qs,['absent']),/unavailable/);
});
test('AE attempts, review recovery, sessions, bookmarks and notes survive refresh and import/export',()=>{
 const data=new Map(),storage={getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k)},app=new ApplicationState(new Store(storage));app.initializeContent(archive);
 const d=generatePaperSession(paper,app.progress,{ids:[q(22).id,q(31).id]},'ae-original');app.addDraft(d);d.answers[q(22).id]=['A'];d.answers[q(31).id]='60';app.completeSession(d,archive.byId,new Date('2026-10-01T12:00:00Z'));
 app.setBookmark(q(22).id,'Must Revise');app.setNote(q(22).id,'Recheck the determinant.');
 const refreshed=new ApplicationState(new Store(storage));refreshed.initializeContent(archive);assert.equal(refreshed.progress.attempts.length,2);assert.equal(revisionState(refreshed.progress,q(22).id).learningState,'wrong');
 const retry=generateReviewSession(archive.questions,refreshed.progress,{capacity:5},new Date('2026-10-03T12:00:00Z'),'ae-review');assert.deepEqual(retry.questionIds,[q(22).id]);refreshed.addDraft(retry);retry.answers[q(22).id]=['A','B'];refreshed.completeSession(retry,archive.byId,new Date('2026-10-03T12:00:00Z'));
 const imported=validateState(JSON.parse(JSON.stringify(refreshed.progress)));assert.equal(imported.schemaVersion,6);assert.equal(imported.attempts.length,3);assert.equal(new Set(imported.attempts.map(a=>a.attemptId)).size,3);assert.equal(revisionState(imported,q(22).id).learningState,'recovered');assert.equal(imported.notes[q(22).id],'Recheck the determinant.');assert.equal(imported.bookmarks[q(22).id],'Must Revise');assert.match(review(imported,archive,'recovered'),/Question 22/);
});
test('numeric typing persists before blur or submission without duplicate writes or premature attempts',()=>{
 const memory=new Map(),storage={getItem:k=>memory.get(k)||null,setItem:(k,v)=>memory.set(k,v),removeItem:k=>memory.delete(k)},app=new ApplicationState(new Store(storage));app.initializeContent(archive);
 const d=generatePaperSession(paper,app.progress,{ids:[q(64).id]},'numeric-draft');app.addDraft(d);
 assert.equal(saveNumericAnswer(app,d,q(64),'27.4'),true);assert.equal(saveNumericAnswer(app,d,q(64),'27.4'),false);
 const refreshed=new Store(storage);assert.equal(refreshed.state.drafts[d.id].answers[q(64).id],'27.4');assert.equal(refreshed.state.attempts.length,0);
 assert.throws(()=>saveNumericAnswer(app,d,q(64),'A'),/valid number/);assert.throws(()=>saveNumericAnswer(app,d,q(22),'1'),/unavailable/);
 app.completeSession(d,archive.byId);assert.equal(app.progress.attempts[0].correctness,'correct');assert.throws(()=>saveNumericAnswer(app,d,q(64),'28'),/already recorded/);
});
test('year-configurable model supports GA last, non-65 totals, variable options and shared/linked content',()=>{
 const one={...structuredClone(q(11)),id:'synthetic-1',year:2011,number:20,groupId:'linked',options:[{label:'A',text:'one'},{label:'B',text:'two'},{label:'C',text:'three'}]};
 const two={...structuredClone(q(22)),id:'synthetic-2',year:2011,number:21,groupId:'linked'};
 const three={...structuredClone(q(31)),id:'synthetic-3',year:2011,number:65,section:'GA',subject:'General Aptitude',groupId:null};
 const p={...raw,id:'synthetic-paper',year:2011,totalQuestions:3,totalMarks:3,questionOrder:[one.id,two.id,three.id],questions:[one,two,three],sectionOrder:['AE','GA'],sections:[{id:'AE',questionIds:[one.id,two.id],totalMarks:2},{id:'GA',questionIds:[three.id],totalMarks:1}],questionRefs:[one,two,three].map(q=>({id:q.id,number:q.number,section:q.section})),questionGroups:[{id:'linked',type:'linked-answer',questionIds:[one.id,two.id],content:[{type:'text',text:'Shared context'}],dependencies:[{questionId:two.id,dependsOn:one.id}]}]};
 const resolved=resolvePaper(p);assert.equal(resolved.questions.length,3);assert.match(questionContent(resolved.questions[1]),/Shared context/);
 assert.equal([...questionContent(resolved.questions[0]).matchAll(/option-letter/g)].length,3);
 p.questionGroups[0].type='common-data';delete p.questionGroups[0].dependencies;assert.doesNotThrow(()=>resolvePaper(p));
});
test('invalid corpus references, groups, types, content, marking and asset paths fail explicitly',()=>{
 for(const corrupt of [p=>p.questionOrder.reverse(),p=>p.questions[0].id=p.questions[1].id,p=>p.questions[0].type='UNKNOWN',p=>p.questions[0].negativeMarks=0,p=>p.questions[0].groupId='missing',p=>p.questions[0].content=[{type:'pdf',src:'page.png'}],p=>p.questions[0].figures[0].src='internal/ae/AE2026.pdf']){const changed=structuredClone(raw);corrupt(changed);assert.throws(()=>resolvePaper(changed,gaById),/Invalid corpus/);}
 assert.throws(()=>validateBlocks([{type:'table',rows:[['a','b'],['c']]}]),/table shape/);
});
test('manifest exposes completed years as ingested and accurately reports answers/assets',()=>{
 assert.equal(manifest.years.length,20);
 const completed = manifest.years.filter(y=>y.ingestionStatus==='complete');
 assert.ok(completed.length>=2);
 const entry2026=manifest.years.find(y=>y.year===2026);assert.equal(entry2026.figureAssetCount,25);assert.equal(entry2026.optionFigureCount,4);assert.equal(entry2026.structuredTableCount,3);assert.deepEqual(entry2026.answerAvailability,{officialKey:65,gradedAnswers:63,marksToAll:2,unavailable:0});
 const entry2025=manifest.years.find(y=>y.year===2025);assert.equal(entry2025.figureAssetCount,18);assert.equal(entry2025.optionFigureCount,4);assert.equal(entry2025.structuredTableCount,2);assert.deepEqual(entry2025.answerAvailability,{officialKey:65,gradedAnswers:65,marksToAll:0,unavailable:0});
});
test('real loader adds AE technical records once and retains GA sets/identities and marking',async()=>{
 const original=globalThis.fetch;globalThis.fetch=async path=>({ok:true,json:async()=>read(path)});
 try{
  const loaded=await loadArchive();
  const completedCount = manifest.years.filter(y=>y.ingestionStatus==='complete').length;
  assert.equal(loaded.sets.length,16);
  assert.equal(loaded.papers.length,completedCount);
  for(const p of loaded.papers)assert.equal(p.questions.length,p.year<=2008?85:p.year===2009?60:65);
  assert.equal(loaded.byId.get(q(22).id).negativeMarks,0);
  assert.equal(loaded.byId.get(q(1).id).negativeMarks,1/3);
  assert.strictEqual(loaded.papers.find(p=>p.year===2026).questions[0],loaded.byId.get(q(1).id));
 }finally{globalThis.fetch=original;}
});

