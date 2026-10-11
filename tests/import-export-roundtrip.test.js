import test from 'node:test';
import assert from 'node:assert/strict';
import {defaults,deserializeState,LATEST_SCHEMA_VERSION,serializeState} from '../js/storage.js';
import {generateSession,submit} from '../js/domain.js';

const questions=[
 {id:'roundtrip-q1',type:'MCQ',answer:'A',marks:1,negativeMarks:1/3,year:2026,paper:'AE',source:{file:'paper.pdf'}},
 {id:'roundtrip-q2',type:'MCQ',answer:'B',marks:2,negativeMarks:2/3,year:2026,paper:'AE',source:{file:'paper.pdf'}}
];
const byId=new Map(questions.map(question=>[question.id,question]));

test('representative persisted state survives an internal export/import round trip',()=>{
 const original=defaults();
 original.revision=9;
 original.profile.name='Round Trip Learner';
 original.settings.theme='dark';
 original.settings.goal=14;
 original.bookmarks['roundtrip-q1']='Must Revise';
 original.notes['roundtrip-q1']='Check the units before answering.';
 original.notebooks.push({id:'notebook-1',name:'Revision',questionIds:['roundtrip-q1'],updatedAt:'2026-09-28T07:00:00.000Z'});
 original.flashcards.push({id:'card-1',questionId:'roundtrip-q1',front:'Prompt',back:'Answer',due:1790553600000,reviewCount:2,successes:1});
 original.planner={exam:'GATE 2027',date:'2027-02-07',minutes:45};

 const completed=generateSession(questions,original,{ids:['roundtrip-q1'],origin:'daily',day:1,mode:'test',minutes:30},'session-completed');
 completed.startedAt='2026-09-28T08:00:00.000Z';completed.answers['roundtrip-q1']='A';completed.times['roundtrip-q1']=42000;completed.elapsed=42000;
 submit(original,completed,byId,new Date('2026-09-28T08:30:00.000Z'));

 const active=generateSession(questions,original,{ids:['roundtrip-q2'],origin:'custom',mode:'practice'},'session-active');
 active.startedAt='2026-09-28T09:00:00.000Z';active.answers['roundtrip-q2']='B';active.times['roundtrip-q2']=7000;active.elapsed=7000;
 original.drafts[active.id]=active;

 const serialized=serializeState(original),restored=deserializeState(serialized);
 const important=['schemaVersion','stateKind','revision','profile','settings','planner','drafts','sessions','attempts','bookmarks','notes','notebooks','flashcards','xpEvents'];
 for(const field of important)assert.deepEqual(restored[field],original[field],field);
 assert.equal(restored.schemaVersion,LATEST_SCHEMA_VERSION);

 const ids=[...restored.sessions.map(session=>session.id),...Object.values(restored.drafts).map(session=>session.id),...restored.attempts.map(attempt=>attempt.attemptId),...restored.notebooks.map(notebook=>notebook.id),...restored.flashcards.map(card=>card.id),...Object.keys(restored.xpEvents)];
 assert.equal(new Set(ids).size,ids.length);
 for(const id of ids)assert.match(id,/^[a-zA-Z0-9:_-]{1,180}$/);

 const timestamps=[...restored.sessions.flatMap(session=>[session.startedAt,session.endedAt]),...Object.values(restored.drafts).map(session=>session.startedAt),...restored.attempts.map(attempt=>attempt.timestamp),...Object.values(restored.xpEvents).map(event=>event.timestamp)];
 for(const timestamp of timestamps)assert.ok(Number.isFinite(Date.parse(timestamp)),timestamp);
 assert.equal(restored.attempts[0].sessionId,restored.sessions[0].id);
});
