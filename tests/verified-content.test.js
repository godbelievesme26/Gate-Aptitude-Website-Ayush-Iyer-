import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {notation,questionContent} from '../js/question-content.js';
import {sourceQuestion,quiz} from '../js/views.js';
import {defaults} from '../js/storage.js';
import {generateSession,submit} from '../js/domain.js';
import {applyQuestionMarking} from '../js/loader.js';
import {QuizTimer} from '../js/timer.js';
const read=path=>JSON.parse(fs.readFileSync(path,'utf8'));
const official=read('tests/fixtures/official-2026-ga-keys.json');
const sets=Object.values(official.papers).map(({day})=>read(`data/day${String(day).padStart(2,'0')}.json`));
const questions=sets.flatMap(s=>s.questions);

test('70 exact GA records agree with their own official key, type, marks and provenance',()=>{
 assert.equal(questions.length,70);
 for(const set of sets){
  const expected=official.papers[set.paper];assert.equal(set.day,expected.day);
  assert.deepEqual(set.questions.map(q=>q.number),official.questionNumbers);
  assert.equal(set.questions.map(q=>q.answer).join(''),expected.key);
  assert.deepEqual(set.questions.map(q=>q.marks),official.marks);
  for(const q of set.questions){
   assert.equal(q.id,`gate-2026-${set.paper.toLowerCase()}-ga-${String(q.number).padStart(2,'0')}`);
   assert.equal(q.type,official.questionType);assert.equal(q.transcriptionStatus,'source-verified');
   assert.equal(q.answerSource.url,official.sourceBase+set.paper+'_Keys.pdf');
   assert.equal(q.answerSource.questionNumber,q.number);assert.ok(q.solution.length>80);
   assert.match(q.solutionStatus,/not an official solution/);
  }
 }
});

test('all out-of-scope data and canonical engines retain their pre-task bytes',()=>{
 for(const [path,hash] of Object.entries(read('tests/fixtures/corpus-preservation.json'))){
  // MTA requires an additive result enum and scoring branch; dedicated tests cover those two modules.
  if(['js/scoring.js','js/storage.js'].includes(path))continue;
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex'),hash,path);
 }
});

test('verified questions render text and figure assets, never full source screenshots',()=>{
 assert.equal(questions.filter(q=>q.hasFigure).length,25);
 for(const q of questions){
  const html=sourceQuestion(q,true);assert.ok(!html.includes(q.sourceImage),q.id);
  assert.equal(q.hasFigure,q.figures.length>0);
  for(const asset of [...q.figures,...q.options.flatMap(o=>o.figure?[o.figure]:[])]){
   assert.ok(fs.existsSync(asset.src));assert.equal(asset.source.sha256,q.source.sha256);assert.ok(asset.alt);
  }
  const detail=questionContent(q);for(const o of q.options)assert.ok(o.text||o.figure,q.id+o.label);
  assert.equal([...detail.matchAll(/class="option-letter"/g)].length,4);
 }
 const legacy={...read('data/day02.json').questions[0],transcriptionStatus:'unverified'};assert.ok(!sourceQuestion(legacy,true).includes(legacy.sourceImage));assert.match(sourceQuestion(legacy,true),/content is being verified/);
});

test('notation renders nested bases and exponents safely and leaves blanks intact',()=>{
 assert.equal(notation('log_{p^{1/n}} y'), 'log<sub>p<sup>1/n</sup></sub> y');
 assert.equal(notation('x = n^{log₁₀(m)}'), 'x = n<sup>log₁₀(m)</sup>');
 assert.equal(notation('_____ <img src=x>'), '_____ &lt;img src=x&gt;');
 assert.equal(notation('^{<script>}'), '<sup>&lt;script&gt;</sup>');
 assert.equal(notation('x^{unfinished'), 'x^{unfinished');
 assert.equal(notation('\\overline{PQ}'), '<span class="math-overline">PQ</span>');
});

test('verified answer controls expose full option content, selection and existing actions',()=>{
 for(const raw of [questions[0],questions[1]]){
  const q=applyQuestionMarking(raw,0),s=defaults(),d=generateSession([q],s,{ids:[q.id]},'content-test'),a={byId:new Map([[q.id,q]])};
  d.answers[q.id]='B';const html=quiz(s,a,d,new QuizTimer(d));
  assert.equal([...html.matchAll(/data-action="answer"/g)].length,4);
  assert.match(html,/data-value="B" aria-pressed="true"/);assert.match(html,/Selected/);
  for(const o of q.options)assert.ok(html.includes(o.figure?o.figure.src:notation(o.text)));
  assert.ok(!html.includes(q.solution));assert.ok(!html.includes('Correct answer:'));
  submit(s,d,a.byId);assert.equal(s.attempts[0].selectedAnswer,'B');assert.equal(s.attempts[0].correctness,q.answer==='B'?'correct':'incorrect');
 }
});

test('independent enumerations verify discrete numerical solutions',()=>{
 let multiples=0,primeSums=0;
 for(let a=1;a<=6;a++)for(let b=1;b<=6;b++){if(b%a===0)multiples++;if([2,3,5,7,11].includes(a+b))primeSums++;}
 assert.equal(multiples,14);assert.equal(primeSums,15);
 const picks=[];
 for(let a=0;a<=20;a++)for(let b=a;b<=20;b++)for(let d=18;d<=20;d++)for(let e=d;e<=20;e++){
  if(b>18)continue;const x=[a,b,18,d,e];if(x.reduce((s,n)=>s+n)!==60)continue;
  const counts=new Map();for(const n of x)counts.set(n,(counts.get(n)||0)+1);
  const max=Math.max(...counts.values()),modes=[...counts].filter(([,c])=>c===max).map(([n])=>n);
  if(modes.length===1&&modes[0]===20)picks.push(x);
 }
 assert.deepEqual(picks,[[0,2,18,20,20]]);
 const digits=[];
 for(let pq=10;pq<=99;pq++)for(const rs of [pq-1,pq+1]){
  const sum=pq*pq+rs*rs;if(rs<10||rs>99||sum<100||sum>999)continue;
  const p=Math.floor(pq/10),q=pq%10,r=Math.floor(rs/10),s=rs%10,x=Math.floor(sum/100),y=Math.floor(sum/10)%10;
  if(sum%10===p&&new Set([p,q,r,s,x,y]).size===6)digits.push([pq,rs,sum,y]);
 }
 assert.deepEqual(digits,[[19,20,761,6]]);
 let bulbs=[0,0,0,1,0,0,0];
 for(let step=0;step<8;step++)bulbs=bulbs.map((v,i)=>{const neighbors=(bulbs[i-1]||0)+(bulbs[i+1]||0);return !v&&neighbors===1?1:v&&neighbors===2?0:v;});
 assert.deepEqual(bulbs,[1,0,1,0,1,0,1]);
});

test('independent substitutions verify geometry, logarithms, revenue and areas',()=>{
 const r=7-4*Math.SQRT2;assert.ok(Math.abs(Math.SQRT2*(3-r)-(1+r))<1e-12);
 const ratio=Math.PI/(2*(Math.PI-1));assert.ok(Math.abs(Math.PI/2-ratio-Math.PI*(1-ratio))<1e-12);
 assert.equal(100*50+50*80+40*60+60*40+60*20,250*60);
 for(const [m,n] of [[8,3],[.8,.3],[10,1]])assert.ok(Math.abs(n**Math.log10(m)-m**Math.log10(n))<1e-12);
 assert.equal((78.25/104).toFixed(2),'0.75');
 assert.ok(Math.abs((.5*10*Math.SQRT2*(10+5*Math.SQRT2)-50)-50*Math.SQRT2)<1e-12);
});

test('independent exhaustive searches verify chess and parent-child deductions',()=>{
 const players=['Rishi','Swathi','Pavan','Tanvi'],class5=new Set(players.slice(0,2)),boys=new Set(['Rishi','Pavan']);
 const winners=new Set();let solutions=0;
 function games(remaining,history){
  if(remaining.length===1){
   if(history.filter(h=>class5.has(h.winner)).length===2&&history.filter(h=>boys.has(h.winner)).length===2){winners.add(remaining[0]);solutions++;}return;
  }
  for(let i=0;i<remaining.length;i++)for(let j=i+1;j<remaining.length;j++){
   const a=remaining[i],b=remaining[j],same=class5.has(a)===class5.has(b);
   if(same!==(history.length===0))continue;
   for(const winner of [a,b])games(remaining.filter(p=>p!==(winner===a?b:a)),[...history,{winner}]);
  }
 }
 games(players,[]);assert.ok(solutions>0);assert.deepEqual([...winners],['Tanvi']);
 const parents=[];const matches=[[['P','X'],['Q','R']],[['P','R'],['X','Y']],[['R','X'],['Q','Y']]];
 for(const x of ['P','Q','R'])for(const y of ['P','Q','R']){
  if(x===y)continue;const pairs=[['X',x],['Y',y]];
  if(matches.every(teams=>!pairs.some(pair=>teams.some(team=>pair.every(p=>team.includes(p))))&&pairs.filter(pair=>pair.every(p=>teams.flat().includes(p))).length<=1))parents.push([x,y]);
 }
 assert.deepEqual(parents,[['Q','P']]);
});
