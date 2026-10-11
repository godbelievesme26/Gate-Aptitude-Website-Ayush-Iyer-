import test from 'node:test';
import assert from 'node:assert/strict';
import {ApplicationState} from '../js/state.js';
import {Store,STORAGE_KEY,defaults} from '../js/storage.js';
import {achievements,createAttemptEvent,generateSession,submit} from '../js/domain.js';

function countingAdapter(raw=null){let writes=0;return {getItem:key=>key===STORAGE_KEY?raw:null,setItem(key,value){if(key===STORAGE_KEY){raw=value;writes++;}},raw:()=>raw,writes:()=>writes};}
const question={id:'q-1',type:'MCQ',answer:'A',marks:1,negativeMarks:1/3,year:2026,paper:'AE'};
const content={questions:[question],byId:new Map([[question.id,question]])};

test('repeated session completion keeps one session, attempt and XP award',()=>{
 const adapter=countingAdapter(),state=new ApplicationState(new Store(adapter));state.initializeContent(content);
 const session=generateSession(content.questions,state.progress,{ids:['q-1']},'stable-session');session.answers['q-1']='A';
 state.addDraft(session);const first=state.completeSession(session,content.byId,new Date('2026-09-28T08:00:00.000Z')),writes=adapter.writes();const second=state.completeSession(session,content.byId,new Date('2026-09-28T09:00:00.000Z'));
 assert.equal(second,first);assert.equal(adapter.writes(),writes);assert.equal(state.progress.sessions.length,1);assert.equal(state.progress.attempts.length,1);assert.deepEqual(Object.keys(state.progress.xpEvents),['question:q-1']);assert.equal(state.progress.xpEvents['question:q-1'].id,'question:q-1');
});

test('rapid pointer or keyboard completion repeats cannot append attempts',()=>{
 const adapter=countingAdapter(),state=new ApplicationState(new Store(adapter));state.initializeContent(content);
 const session=generateSession(content.questions,state.progress,{ids:['q-1']},'rapid-session');session.answers['q-1']='A';state.addDraft(session);
 const records=Array.from({length:20},()=>state.completeSession(session,content.byId,new Date('2026-09-28T08:00:00.000Z')));
 assert.ok(records.every(record=>record===records[0]));assert.equal(state.progress.sessions.length,1);assert.equal(state.progress.attempts.length,1);assert.equal(state.progress.attempts[0].selectedAnswer,'A');
});

test('canonical keys grade selected answers and missing keys remain ungraded',()=>{
 const state=defaults(),questions=[question,{...question,id:'q-2',answer:'B'},{id:'q-3',type:'MCQ',marks:1,negativeMarks:1/3,year:2026,paper:'AE'}],byId=new Map(questions.map(item=>[item.id,item]));
 const session=generateSession(questions,state,{},'grading-session');session.answers={'q-1':'A','q-2':'A','q-3':'C'};submit(state,session,byId,new Date('2026-09-28T08:00:00.000Z'));
 assert.deepEqual(state.attempts.map(item=>item.selectedAnswer),['A','A','C']);assert.deepEqual(state.attempts.map(item=>item.correctness),['correct','incorrect','ungraded']);
});

test('stable attempt ID prevents duplication during partial-state recovery',()=>{
 const state=defaults(),session=generateSession(content.questions,state,{ids:['q-1']},'recovery-session');session.answers['q-1']='A';
 const row={questionId:'q-1',answer:'A',result:'correct'},stamp='2026-09-28T08:00:00.000Z';state.attempts.push(createAttemptEvent(session,row,question,stamp));
 submit(state,session,content.byId,new Date(stamp));
 assert.equal(state.sessions.length,1);assert.equal(state.attempts.length,1);assert.equal(state.attempts[0].attemptId,'recovery-session:q-1');
});

test('repeated bookmark add and remove are no-op writes',()=>{
 const adapter=countingAdapter(),state=new ApplicationState(new Store(adapter));
 assert.equal(state.setBookmark('q-1','Saved'),true);const afterAdd=adapter.writes();assert.equal(state.setBookmark('q-1','Saved'),false);assert.equal(adapter.writes(),afterAdd);assert.equal(Object.keys(state.progress.bookmarks).length,1);
 assert.equal(state.setBookmark('q-1',''),true);const afterRemove=adapter.writes();assert.equal(state.setBookmark('q-1',''),false);assert.equal(adapter.writes(),afterRemove);assert.deepEqual(state.progress.bookmarks,{});
});

test('achievement evaluation is repeatable and does not unlock duplicate records',()=>{
 const state=defaults();state.attempts.push({questionId:'q-1',selectedAnswer:'A',localDate:'2026-09-28'});
 const first=achievements(state),second=achievements(state);
 assert.deepEqual(first,second);assert.equal(new Set(first).size,first.length);assert.deepEqual(state.xpEvents,{});
});

test('reimporting identical state and repeated initialization do not rewrite storage',()=>{
 const adapter=countingAdapter(JSON.stringify(defaults())),firstStore=new Store(adapter);assert.equal(adapter.writes(),0);
 const state=new ApplicationState(firstStore);state.setNote('q-1','keep');const snapshot=JSON.parse(adapter.raw()),beforeImport=adapter.writes();state.replaceProgress(snapshot);state.replaceProgress(snapshot);assert.equal(adapter.writes(),beforeImport);
 new Store(adapter);new Store(adapter);assert.equal(adapter.writes(),beforeImport);
});
