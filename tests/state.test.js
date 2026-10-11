import test from 'node:test';
import assert from 'node:assert/strict';
import {Store,defaults,STORAGE_KEY} from '../js/storage.js';
import {ApplicationState} from '../js/state.js';
import {generateSession} from '../js/domain.js';

function memoryAdapter(raw=null){
 return {getItem:key=>key===STORAGE_KEY?raw:null,setItem:(key,value)=>{if(key===STORAGE_KEY)raw=value;},value:()=>raw};
}
function archive(){const questions=[{id:'question-1',type:'MCQ',answer:'A',marks:1,negativeMarks:1/3},{id:'question-2',type:'MCQ',answer:'B',marks:1,negativeMarks:1/3},{id:'question-3',type:'MCQ',answer:'C',marks:1,negativeMarks:1/3}];return {questions,byId:new Map(questions.map(question=>[question.id,question]))};}
function draft(id='draft-1',questionId='question-1'){return {id,startedAt:'2026-09-28T08:00:00.000Z',endedAt:null,mode:'practice',plannedDuration:null,questionIds:[questionId],currentPosition:0,status:'active',origin:'custom',configuration:{},answers:{},times:{},visited:{[questionId]:true},review:{},elapsed:0,deadline:null};}

test('application state initializes four separate state compartments',()=>{
 const state=new ApplicationState(new Store(memoryAdapter()));
 assert.equal(state.content,null);
 assert.deepEqual(state.progress,defaults());
 assert.deepEqual(state.session,{activeId:null,timer:null});
 assert.deepEqual(state.ui,{revealedFlashcard:false,offlineReady:false,installEvent:null,saveTick:0,conflict:false});
 const content=archive();
 assert.equal(state.initializeContent(content),content);
 assert.equal(state.content,content);
 assert.notEqual(state.progress,state.ui);
});

test('progress writes persist and a new state reads the saved value',()=>{
 const adapter=memoryAdapter(),state=new ApplicationState(new Store(adapter));
 state.updateProgress(progress=>{progress.notes['question-1']='Remember this';});
 const restored=new ApplicationState(new Store(adapter));
 assert.equal(restored.progress.notes['question-1'],'Remember this');
 assert.equal(restored.progress.revision,1);
});

test('active session resolves from the canonical persisted draft',()=>{
 const state=new ApplicationState(new Store(memoryAdapter()));
 state.initializeContent(archive());
 state.progress.drafts['draft-1']=draft();
 let stopped=0;
 assert.equal(state.activateSession('draft-1',()=>({stop:()=>stopped++})),state.progress.drafts['draft-1']);
 state.activeSession.answers['question-1']='A';
 assert.equal(state.progress.drafts['draft-1'].answers['question-1'],'A');
 state.clearSession();
 assert.equal(stopped,1);
 assert.equal(state.activeSession,null);
});

test('session initialization rejects missing and unavailable drafts without deleting progress',()=>{
 const state=new ApplicationState(new Store(memoryAdapter()));
 state.initializeContent(archive());
 state.progress.drafts.bad=draft('bad','missing-question');
 assert.equal(state.activateSession('missing'),null);
 assert.equal(state.activateSession('bad'),null);
 assert.ok(state.progress.drafts.bad);
 assert.deepEqual(state.session,{activeId:null,timer:null});
});

test('replacing progress clears runtime session and leaves UI state temporary',()=>{
 const state=new ApplicationState(new Store(memoryAdapter()));
 state.initializeContent(archive());
 state.progress.drafts['draft-1']=draft();
 state.activateSession('draft-1',()=>({stop(){}}));
 state.ui.revealedFlashcard=true;
 const replacement=defaults();replacement.profile.name='Learner';
 state.replaceProgress(replacement);
 assert.equal(state.progress.profile.name,'Learner');
 assert.equal(state.activeSession,null);
 assert.equal(state.ui.revealedFlashcard,true);
});

test('browser refresh restores persistent progress, attempts, sessions, bookmarks and notes',()=>{
 const adapter=memoryAdapter(),contentQuestion={id:'question-1',type:'MCQ',answer:'A',marks:1,negativeMarks:1/3,year:2026,paper:'AE'},content={questions:[contentQuestion],byId:new Map([['question-1',contentQuestion]])};
 const beforeRefresh=new ApplicationState(new Store(adapter));
 beforeRefresh.initializeContent(content);
 beforeRefresh.setBookmark('question-1','Important');
 beforeRefresh.setNote('question-1','Persistent note');
 const session=generateSession(content.questions,beforeRefresh.progress,{ids:['question-1'],origin:'daily',day:1},'refresh-session');
 beforeRefresh.addDraft(session);
 session.answers['question-1']='A';session.times['question-1']=6500;
 beforeRefresh.completeSession(session,content.byId,new Date('2026-09-28T09:00:00.000Z'));
 beforeRefresh.ui.revealedFlashcard=true;

 const afterRefresh=new ApplicationState(new Store(adapter));
 afterRefresh.initializeContent(content);
 assert.equal(afterRefresh.progress.bookmarks['question-1'],'Important');
 assert.equal(afterRefresh.progress.notes['question-1'],'Persistent note');
 assert.equal(afterRefresh.progress.sessions.length,1);
 assert.equal(afterRefresh.progress.sessions[0].id,'refresh-session');
 assert.equal(afterRefresh.progress.attempts.length,1);
 assert.equal(afterRefresh.progress.attempts[0].selectedAnswer,'A');
 assert.deepEqual(afterRefresh.progress.drafts,{});
 assert.equal(afterRefresh.ui.revealedFlashcard,false);
 assert.equal(afterRefresh.activeSession,null);
});

test('committing a question persists its attempt before advancing exactly once',()=>{
 const adapter=memoryAdapter(),content=archive(),state=new ApplicationState(new Store(adapter));state.initializeContent(content);
 const session=generateSession(content.questions,state.progress,{ids:content.questions.map(question=>question.id)},'transition-session');state.addDraft(session);session.answers['question-1']='A';session.times['question-1']=4200;
 const attempt=state.commitAndMove(session,content.byId,1,new Date('2026-09-28T08:00:00.000Z'));
 assert.equal(attempt.selectedAnswer,'A');assert.equal(attempt.correctness,'correct');assert.equal(session.currentPosition,1);
 const refreshed=new ApplicationState(new Store(adapter));refreshed.initializeContent(content);assert.equal(refreshed.progress.attempts.length,1);assert.equal(refreshed.progress.drafts[session.id].currentPosition,1);
 const restored=refreshed.progress.drafts[session.id];refreshed.commitAndMove(restored,content.byId,2,new Date('2026-09-28T08:01:00.000Z'));assert.equal(refreshed.progress.attempts.length,2);assert.deepEqual(refreshed.progress.attempts.map(item=>item.questionId),['question-1','question-2']);assert.equal(restored.currentPosition,2);
});

test('repeating a committed transition does not duplicate its attempt',()=>{
 const content=archive(),state=new ApplicationState(new Store(memoryAdapter()));state.initializeContent(content);const session=generateSession(content.questions,state.progress,{ids:content.questions.map(question=>question.id)},'repeat-transition');state.addDraft(session);session.answers['question-1']='A';state.commitAndMove(session,content.byId,1);session.currentPosition=0;state.commitAndMove(session,content.byId,1);assert.equal(state.progress.attempts.length,1);assert.equal(session.currentPosition,1);
});
