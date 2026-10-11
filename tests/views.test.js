import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import * as views from '../js/views.js';import {defaults} from '../js/storage.js';import {normalize} from '../js/loader.js';import {home} from '../js/home.js';import {generateSession,submit} from '../js/domain.js';import {QuizTimer} from '../js/timer.js';
const registry=JSON.parse(fs.readFileSync('data/registry.json','utf8')),sets=registry.map(x=>JSON.parse(fs.readFileSync(x.path,'utf8'))),questions=sets.flatMap(s=>s.questions.map(q=>({...q,day:s.day,search:normalize(q.question)}))),byId=new Map(questions.map(q=>[q.id,q]));const archive={registry,sets,questions,byId};
test('every route renders against real source data and empty state',()=>{const s=defaults();for(const html of [home(s,archive),views.daily(s,archive),views.daily(s,archive,1),views.bank(s,archive,new URLSearchParams()),views.questionDetail(s,archive,questions[0].id),views.history(s),views.practice(s,archive),views.review(s,archive),views.flashcards(s,false),views.analytics(s,archive),views.planner(s,archive),views.settings(s,false,false)])assert.ok(html.length>100);});
test('populated bookmark, notebook, note, session and quiz views render',()=>{const s=defaults(),id=questions[0].id;s.bookmarks[id]='Must Revise';s.notes[id]='<unsafe>';s.notebooks.push({id:'test-notebook',name:'<notebook>',questionIds:[id],updatedAt:new Date().toISOString()});const d=generateSession(questions,s,{ids:[id]},'test-session');d.answers[id]='A';const timer=new QuizTimer(d);assert.ok(views.quiz(s,archive,d,timer).includes('aria-pressed="true"'));submit(s,d,byId);for(const tab of ['bookmarks','notes','notebooks']){const html=views.review(s,archive,tab);assert.ok(html.length>100);assert.ok(!html.includes('<unsafe>'));assert.ok(!html.includes('<notebook>'));}assert.ok(views.result(s,archive,d.id).includes('ungraded'));});
test('question screen prioritizes question, response, primary action, then supporting status',()=>{const s=defaults(),d=generateSession(questions,s,{ids:questions.slice(0,2).map(q=>q.id)},'hierarchy'),timer=new QuizTimer(d),first=views.quiz(s,archive,d,timer);const positions=['question-content','response-section','Continue →','status-summary'].map(value=>first.indexOf(value));assert.ok(positions.every((value,index)=>value>=0&&(index===0||value>positions[index-1])));assert.match(first,/−0.33 for an incorrect answer/);d.currentPosition=1;const last=views.quiz(s,archive,d,timer);assert.match(last,/data-action="submit"/);assert.doesNotMatch(last,/Continue →/);});
test('answer feedback is concise, honest, and includes a useful next action',()=>{const keyed={id:'keyed',answer:'B'},missing={id:'missing'};assert.deepEqual(views.attemptFeedback({questionId:'keyed',selectedAnswer:'A',correctness:'incorrect'},keyed),{status:'Incorrect',message:'Your selected answer is incorrect.',selectedAnswer:'A',correctAnswer:'B',nextAction:{label:'Try this question again',href:'#/question/keyed'}});const unknown=views.attemptFeedback({questionId:'missing',selectedAnswer:'C',correctness:'ungraded'},missing);assert.equal(unknown.status,'Not graded');assert.equal(unknown.selectedAnswer,'C');assert.equal(unknown.correctAnswer,null);assert.match(unknown.message,/answer key is unavailable/);assert.equal(unknown.nextAction.label,'Review your response');});
test('submitted result announces feedback with selected and correct answers',()=>{const q={...questions[0],id:'feedback-q',type:'MCQ',answer:'B',negativeMarks:1/3},a={...archive,questions:[q],byId:new Map([[q.id,q]])},s=defaults(),d=generateSession([q],s,{ids:[q.id]},'feedback-session');d.answers[q.id]='A';submit(s,d,a.byId,new Date('2026-09-28T08:00:00.000Z'));const html=views.result(s,a,d.id);assert.match(html,/role="status" aria-live="polite" tabindex="-1"/);assert.match(html,/Question 1: Incorrect/);assert.match(html,/Selected: A · Correct answer: B/);assert.match(html,/Try this question again/);});
test('latest mistakes are derived from canonical attempts',()=>{const s=defaults(),question=questions[0],timestamp=new Date().toISOString();s.sessions.push({id:'graded-session',startedAt:timestamp,endedAt:timestamp,mode:'practice',plannedDuration:null,questionIds:[question.id],currentPosition:0,status:'completed',origin:'custom',configuration:{},elapsed:1000,result:{correct:0,incorrect:1,ungraded:0,blank:0,answered:1,maxMarks:question.marks,score:0}});s.attempts.push({attemptId:'graded-session:'+question.id,questionId:question.id,sessionId:'graded-session',selectedAnswer:'A',correctness:'incorrect',timeSpent:1000,timestamp,mode:'practice',sourceContext:{origin:'custom'},localDate:'2026-09-28'});const html=views.review(s,archive,'mistakes',new URLSearchParams('mode=latest'));assert.ok(html.includes(question.id));});
test('home shows a one-click start action, simple budgets, and a clear unavailable state',()=>{const available=home(defaults(),archive);assert.match(available,/data-action="start-now"/);for(const label of ['10 minutes','25 minutes','45 minutes','60 minutes','Custom'])assert.match(available,new RegExp(label));assert.match(available,/Available time/);assert.match(available,/Planned for 25 minutes/);const unavailable=home(defaults(),{sets:[],questions:[],byId:new Map()});assert.match(unavailable,/Study session unavailable/);assert.match(unavailable,/<button class="primary" disabled aria-disabled="true">Start now<\/button>/);assert.doesNotMatch(unavailable,/data-action="start-now"/);});

test('Home presentation keeps existing progress, destinations and the resumable session',()=>{
 const s=defaults(),d=generateSession(questions,s,{origin:'daily',day:1,ids:questions.slice(0,10).map(q=>q.id)},'home-complete');
 d.answers[d.questionIds[0]]='B';submit(s,d,byId);
 const draft=generateSession(questions,s,{count:3},'home-resume');draft.currentPosition=1;s.drafts[draft.id]=draft;
 s.bookmarks[questions[0].id]='Saved';s.notes[questions[0].id]='My note';s.profile.name='<student>';
 const before=JSON.stringify(s),html=home(s,archive);
 assert.equal(JSON.stringify(s),before,'rendering must never mutate progress');
 assert.match(html,/Continue session/);assert.match(html,/Question 2 of 3/);assert.doesNotMatch(html,/id="start-budget"/);
 assert.match(html,/Welcome back, &lt;student&gt;/);assert.doesNotMatch(html,/<student>/);
 assert.match(html,/<strong>0<\/strong><span>Sets completed/);assert.match(html,/<strong>1<\/strong><span>Questions attempted/);
 for(const href of ['#/settings','#/history','#/review/bookmarks','#/review/notes','#/flashcards','#/result/home-complete',...archive.sets.map(x=>'#/day/'+x.day)])assert.ok(html.includes('href="'+href+'"'),href);
 assert.equal([...html.matchAll(/<h1\b/g)].length,1);
});

test('Home custom budget exposes the numeric input expected by the existing handler',()=>{
 const html=home(defaults(),archive);
 assert.match(html,/<input id="start-budget-custom"[^>]*aria-label="Custom minutes · 1–360"[^>]*type="number"[^>]*min="1" max="360" step="1"[^>]*hidden>/);
 assert.ok(html.indexOf('data-action="start-now"')<html.indexOf('aria-label="Your progress"'));
});

test('solving presentation preserves authentic source, answer values and supporting actions',()=>{
 const s=defaults(),d=generateSession(questions,s,{count:2},'visual-contract');d.answers[d.questionIds[0]]='C';
 const html=views.quiz(s,archive,d,new QuizTimer(d));
 assert.ok(!html.includes('src="'+questions[0].sourceImage+'"'));assert.ok(html.includes('question-stem'));assert.ok(html.includes('exaggerates; engenders'));
 assert.deepEqual([...html.matchAll(/data-action="answer" data-value="([A-D])" aria-pressed="(true|false)"/g)].map(x=>x.slice(1)),[['A','false'],['B','false'],['C','true'],['D','false']]);
 for(const action of ['focus','previous','next','clear','review-question','quick-bookmark','jump'])assert.ok(html.includes('data-action="'+action+'"'),action);
 for(const id of ['session-time','question-time','visit-time','checkpoint'])assert.ok(html.includes('id="'+id+'"'),id);
 assert.match(html,/Source-verified question/);
 assert.match(html,/Selected<\/span>/);
});
test('solving presentation retains MSQ and numeric semantics without leaking grading',()=>{
 for(const type of ['MSQ','NAT']){
  const q={...questions[0],type,answer:type==='NAT'?12:['A','C']},a={...archive,byId:new Map([[q.id,q]])},s=defaults(),d=generateSession([q],s,{},'typed-visual');d.answers[q.id]=type==='NAT'?7:['A','C'];
  const html=views.quiz(s,a,d,new QuizTimer(d));
  if(type==='NAT'){assert.match(html,/id="nat-answer" aria-label="Numeric answer"[^>]*value="7"/);assert.doesNotMatch(html,/data-action="answer"/);}
  else{assert.match(html,/Select all that apply/);assert.equal([...html.matchAll(/aria-pressed="true"/g)].length,2);}
  assert.doesNotMatch(html,/Correct answer:|data-feedback="correct"/);
 }
});
