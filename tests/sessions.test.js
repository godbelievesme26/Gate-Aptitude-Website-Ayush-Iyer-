import test from 'node:test';
import assert from 'node:assert/strict';
import {defaults} from '../js/storage.js';
import {abandonSession,generateSession,interruptSession,move,resumeSession,submit} from '../js/domain.js';

const questions=[{id:'q-1',type:'MCQ',answer:'A',marks:1,negativeMarks:1/3,year:2026,paper:'AE'},{id:'q-2',type:'MCQ',answer:'B',marks:1,negativeMarks:1/3,year:2026,paper:'AE'}];
const byId=new Map(questions.map(question=>[question.id,question]));

test('new session has canonical identity, timing, queue, position and state',()=>{
 const session=generateSession(questions,defaults(),{mode:'test',minutes:30},'new-session');
 assert.equal(session.id,'new-session');
 assert.ok(Number.isFinite(Date.parse(session.startedAt)));
 assert.equal(session.endedAt,null);
 assert.equal(session.mode,'test');
 assert.equal(session.plannedDuration,1800000);
 assert.deepEqual(session.questionIds,['q-1','q-2']);
 assert.equal(session.currentPosition,0);
 assert.equal(session.status,'active');
});

test('active session tracks its current position without changing question order',()=>{
 const session=generateSession(questions,defaults(),{},'active-session'),order=[...session.questionIds];
 move(session,1);
 assert.equal(session.status,'active');
 assert.equal(session.currentPosition,1);
 assert.deepEqual(session.questionIds,order);
});

test('completed session stores metadata and summary while attempts own question details',()=>{
 const state=defaults(),session=generateSession(questions,state,{},'completed-session');
 session.answers['q-1']='A';session.times['q-1']=4000;
 const completed=submit(state,session,byId,new Date('2026-09-28T10:00:00.000Z'));
 assert.equal(completed.status,'completed');
 assert.equal(completed.endedAt,'2026-09-28T10:00:00.000Z');
 assert.equal(completed.result.correct,1);
 assert.equal(completed.result.rows,undefined);
 for(const field of ['answers','times','review','visited'])assert.equal(completed[field],undefined);
 assert.equal(state.attempts[0].sessionId,completed.id);
 assert.equal(state.attempts[0].selectedAnswer,'A');
});

test('interrupted session can resume without an end time',()=>{
 const session=generateSession(questions,defaults(),{},'interrupted-session');
 interruptSession(session);
 assert.equal(session.status,'interrupted');
 assert.equal(session.endedAt,null);
 resumeSession(session);
 assert.equal(session.status,'active');
 assert.equal(session.endedAt,null);
});

test('abandoned session records its terminal state and end time',()=>{
 const session=generateSession(questions,defaults(),{},'abandoned-session');
 abandonSession(session,new Date('2026-09-28T11:00:00.000Z'));
 assert.equal(session.status,'abandoned');
 assert.equal(session.endedAt,'2026-09-28T11:00:00.000Z');
});
