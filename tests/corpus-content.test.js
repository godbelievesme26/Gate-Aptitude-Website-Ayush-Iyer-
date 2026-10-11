import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {questionContent,optionContent,questionPreview} from '../js/question-content.js';
import {questionDetail,quiz,result,bank,review,daily,attemptFeedback} from '../js/views.js';
import {defaults,serializeState,deserializeState} from '../js/storage.js';
import {generateSession,submit,commitQuestionAttempt} from '../js/domain.js';
import {scoreQuestion,scoreSession} from '../js/scoring.js';
import {applyQuestionMarking} from '../js/loader.js';
import {QuizTimer} from '../js/timer.js';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const sets=read('data/registry.json').map(e=>read(e.path));
const questions=sets.flatMap(s=>s.questions.map((q,i)=>({...applyQuestionMarking(q,i),day:s.day,search:q.question.toLowerCase()})));
const a={sets,questions,byId:new Map(questions.map(q=>[q.id,q]))};
const remaining=read('tests/fixtures/official-remaining-ga-keys.json');

test('all 160 records have verified content, an official key or ruling, and an editorial solution',()=>{
 assert.equal(questions.length,160);assert.equal(new Set(questions.map(q=>q.id)).size,160);
 for(const q of questions){
  assert.equal(q.transcriptionStatus,'source-verified',q.id);assert.ok(q.solution.length>80,q.id);
  assert.match(q.solutionStatus,/not an official solution/);assert.equal(q.type,'MCQ');
  assert.ok(['A','B','C','D','MTA'].includes(q.answer));assert.equal(q.options.map(o=>o.label).join(''),'ABCD');
  assert.equal(q.marks,q.number<=5?1:2);assert.ok(q.options.every(o=>o.text||o.figure));
  assert.equal(q.answerSource.paper,q.paper);assert.equal(q.answerSource.questionNumber,q.number);
 }
 assert.equal(questions.filter(q=>q.answer==='MTA').length,1);
 for(const [day,expected] of Object.entries(remaining)){
  const set=sets.find(s=>s.day===Number(day));assert.equal(set.paper,expected.paper);
  for(const row of expected.questions){const q=set.questions[row.number-1];
   for(const field of ['number','answer','type','marks'])assert.equal(q[field],row[field],q.id+' '+field);
   assert.equal(q.answerSource.url,expected.keyUrl);assert.equal(q.answerSource.sha256,expected.keySha256);
   assert.equal(q.answerSource.masterPaperUrl,expected.masterUrl);assert.ok(expected.masterUrl);
   assert.equal(q.answerSource.session,row.session);assert.equal(q.answerSource.mappingStatus,'master-order-verified');
  }
 }
});

test('every question surface uses selectable structured content without paper screenshots',()=>{
 for(const q of questions){
  const s=defaults();s.bookmarks[q.id]='Saved';s.notes[q.id]='QA note';
  const d=generateSession([q],s,{ids:[q.id]},'render-'+q.id);s.drafts[d.id]=d;
  const surfaces=[questionContent(q),questionPreview(q),questionDetail(s,a,q.id),quiz(s,a,d,new QuizTimer(d))];
  d.mode='test';surfaces.push(quiz(s,a,d,new QuizTimer(d)));
  d.answers[q.id]='A';submit(s,d,a.byId);surfaces.push(result(s,a,d.id));
  for(const html of surfaces){assert.ok(!html.includes(q.sourceImage),q.id);assert.doesNotMatch(html,/enlarge-source|source-image|search transcript|<iframe/i);}
  assert.match(questionContent(q),/question-stem|figure-sequence/);
  for(const o of q.options)assert.ok(optionContent(q,o).includes(o.figure?o.figure.src:'option-copy'));
 }
 const s=defaults();s.bookmarks[questions[10].id]='Saved';s.notes[questions[10].id]='note';
 for(const html of [bank(s,a,new URLSearchParams()),review(s,a,'bookmarks'),review(s,a,'notes'),daily(s,a,2)])assert.doesNotMatch(html,/enlarge-source|source-image|source-crops/);
 const broken={...questions[0],transcriptionStatus:'pending'};
 assert.match(questionContent(broken),/content is being verified/);assert.doesNotMatch(questionContent(broken),/<img/);
 const unsafe={...questions[0],figures:[{src:questions[0].sourceImage,source:{},alt:'bad'}]};assert.doesNotMatch(questionContent(unsafe),/<img/);
});

test('all 153 figure assets have question-specific paths and source lineage',()=>{
 const assets=questions.flatMap(q=>[...(q.figures||[]),...q.options.flatMap(o=>o.figure?[o.figure]:[])].map(f=>({q,f})));
 assert.equal(assets.length,153);
 for(const {q,f} of assets){assert.ok(f.src.startsWith('figures/'+q.id+'-'));assert.ok(fs.statSync(f.src).size>100);assert.ok(f.alt);assert.equal(f.source.file,q.source.file);assert.equal(f.source.sha256,q.source.sha256);assert.ok(f.source.page>0);}
 const xe=a.byId.get('gate-2026-xe-ga-02');assert.deepEqual(xe.options.map(o=>o.figure.source.image),['Im2.png','Im3.png','Im4.png','Im5.png']);
 const ce=a.byId.get('gate-2025-ce1-ga-08');assert.deepEqual(ce.options.map(o=>o.figure.source.image),['Image71.jpg','Image68.jpg','Image69.jpg','Image70.jpg']);
});

test('official MTA awards full marks for every response including blank without claiming correctness',()=>{
 const q=a.byId.get('gate-2025-ec-ga-08');
 for(const answer of [undefined,null,'','A','B','C','D'])assert.deepEqual(scoreQuestion(q,answer),{result:'awarded',marks:2,penalty:0});
 const summary=scoreSession([q],{});assert.equal(summary.score,2);assert.equal(summary.accuracy,null);assert.equal(summary.correct,0);assert.equal(summary.incorrect,0);assert.equal(summary.answered,0);assert.equal(summary.awarded,1);
 const s=defaults(),d=generateSession([q],s,{},'mta-test');s.drafts[d.id]=d;
 const event=commitQuestionAttempt(s,d,q);submit(s,d,a.byId);submit(s,d,a.byId);
 assert.equal(s.attempts.length,1);assert.equal(event.correctness,'awarded');assert.equal(s.sessions.length,1);
 const restored=deserializeState(serializeState(s));assert.deepEqual(restored.attempts,s.attempts);assert.equal(restored.sessions[0].result.awarded,1);
 assert.match(attemptFeedback(event,q).message,/including unanswered/);assert.doesNotMatch(questionDetail(s,a,q.id),/Answer: MTA/);
});

test('adding keys never rewrites previous ungraded attempts or stored results',()=>{
 const q=a.byId.get('gate-2025-ae-ga-01'),old={...q};delete old.answer;
 const s=defaults(),d=generateSession([old],s,{},'historical');d.answers[q.id]='A';submit(s,d,new Map([[q.id,old]]));
 const before=serializeState(s);questionDetail(s,a,q.id);result(s,a,d.id);
 assert.equal(serializeState(s),before);assert.equal(s.attempts[0].correctness,'ungraded');assert.equal(s.sessions[0].result.score,null);
 assert.match(attemptFeedback(s.attempts[0],q).message,/original result is unchanged/);
 const fresh=generateSession([q],s,{},'new');fresh.answers[q.id]='A';submit(s,fresh,a.byId);assert.equal(s.attempts[1].correctness,'correct');
});

test('independent arithmetic and enumerations check remaining numerical solutions',()=>{
 let exactlyOneSix=0;for(let x=1;x<=6;x++)for(let y=1;y<=6;y++)for(let z=1;z<=6;z++)if([x,y,z].filter(n=>n===6).length===1)exactlyOneSix++;
 assert.equal(exactlyOneSix,75);
 let scoops=0;for(let a=0;a<=3;a++)for(let b=0;b<=3;b++)for(let c=0;c<=3;c++)for(let d=0;d<=3;d++)if(a+b+c+d===3)scoops++;
 assert.equal(scoops,20);
 const covers=[];for(let mask=0;mask<32;mask++)if([0,1,2,3,4].every(i=>(mask&(1<<i))||(mask&(1<<((i+1)%5)))))covers.push(mask.toString(2).replaceAll('0','').length);
 assert.equal(Math.min(...covers),3);
 const h=Math.sqrt(13**2-5**2);assert.equal(h,12);assert.equal(14*h/2,84);
 const root=(-3+Math.sqrt(17))/2;assert.ok(Math.abs(root**2+3*root-2)<1e-12);
 assert.ok(Math.abs(3*(.8**2)*.2-48/125)<1e-12);
});
