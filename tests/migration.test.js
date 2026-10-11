import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {LATEST_SCHEMA_VERSION,STORAGE_KEY,Store,defaults,migrateState,validateState} from '../js/storage.js';

const fixture=name=>fs.readFileSync(new URL(`./fixtures/state/${name}.json`,import.meta.url),'utf8');
const parsed=name=>JSON.parse(fixture(name));
const adapter=(raw,{writable=false}={})=>({getItem:key=>key===STORAGE_KEY?raw:null,setItem(key,value){if(!writable)throw Error('unexpected write');if(key===STORAGE_KEY)raw=value;},value:()=>raw});

test('latest-state fixture validates without changing its data',()=>{
 const input=parsed('latest-state'),result=validateState(input);
 assert.deepEqual(result,input);
 assert.equal(result.schemaVersion,LATEST_SCHEMA_VERSION);
});

test('previous-version fixture migrates deterministically without losing progress',()=>{
 const input=parsed('previous-version-state');
 const first=migrateState(input),second=migrateState(input);
 assert.deepEqual(first,second);
 assert.equal(first.schemaVersion,LATEST_SCHEMA_VERSION);
 assert.equal(first.stateKind,'gate-user-progress');
 for(const key of Object.keys(input).filter(key=>!['schemaVersion','attempts','drafts','sessions'].includes(key)))assert.deepEqual(first[key],input[key],key);
 assert.equal(first.drafts['draft-1'].startedAt,input.drafts['draft-1'].createdAt);
 assert.equal(first.drafts['draft-1'].currentPosition,input.drafts['draft-1'].index);
 assert.deepEqual(first.drafts['draft-1'].answers,input.drafts['draft-1'].answers);
 assert.equal(first.sessions[0].startedAt,input.sessions[0].createdAt);
 assert.equal(first.sessions[0].endedAt,input.sessions[0].completedAt);
 assert.equal(first.attempts[0].selectedAnswer,'A');
 assert.equal(first.attempts[0].correctness,'ungraded');
 assert.equal(first.attempts[0].timeSpent,9000);
 assert.equal(first.attempts[0].mode,'practice');
 assert.deepEqual(first.attempts[0].sourceContext,{origin:'daily',day:1,year:2026,paper:'AE'});
 for(const key of ['answer','result','questionTime','sessionOrigin','attemptNumber'])assert.equal(key in first.attempts[0],false,key);
 for(const key of ['createdAt','completedAt','index'])assert.equal(key in first.sessions[0],false,key);
 assert.equal('rows' in first.sessions[0].result,false);
 for(const key of ['createdAt','completedAt','index'])assert.equal(key in first.drafts['draft-1'],false,key);
 const validated=validateState(input);
 assert.equal(validated.notes['question-1'],'Preserve this note');
 assert.equal(validated.drafts['draft-1'].answers['question-1'],'A');
 assert.deepEqual(validated.extensionData,{preserve:true});
});

test('migration retains legacy session detail when canonical attempts cannot preserve it',()=>{
 const state=parsed('previous-version-state');
 state.attempts=[];
 state.sessions[0].answers={'question-1':'A'};
 state.sessions[0].times={'question-1':9000};
 state.sessions[0].result.rows=[{questionId:'question-1',selectedAnswer:'A'}];
 const migrated=migrateState(state);
 assert.deepEqual(migrated.sessions[0].answers,{'question-1':'A'});
 assert.deepEqual(migrated.sessions[0].times,{'question-1':9000});
 assert.deepEqual(migrated.sessions[0].result.rows,[{questionId:'question-1',selectedAnswer:'A'}]);
});

test('malformed-state fixture falls back safely and preserves original storage',()=>{
 const raw=fixture('malformed-state'),store=new Store(adapter(raw));
 assert.equal(store.readOnly,true);
 assert.ok(store.error);
 assert.deepEqual(store.state,defaults());
 assert.throws(()=>store.save());
 assert.equal(store.raw(),raw);
});

test('empty-state fixture initializes a new install at the latest schema',()=>{
 const empty=parsed('empty-state');
 const store=new Store(adapter(empty));
 assert.deepEqual(store.state,defaults());
 assert.equal(store.state.schemaVersion,LATEST_SCHEMA_VERSION);
 assert.equal(store.readOnly,false);
});

test('known previous state is upgraded during store initialization',()=>{
 const storage=adapter(fixture('previous-version-state'),{writable:true}),store=new Store(storage);
 assert.equal(store.state.schemaVersion,LATEST_SCHEMA_VERSION);
 assert.equal(store.state.profile.name,'Returning Learner');
 assert.equal(store.readOnly,false);
 assert.equal(JSON.parse(storage.value()).schemaVersion,LATEST_SCHEMA_VERSION);
});

test('migration write failure retains valid progress in protected memory',()=>{
 const store=new Store(adapter(fixture('previous-version-state')));
 assert.equal(store.state.profile.name,'Returning Learner');
 assert.equal(store.state.schemaVersion,LATEST_SCHEMA_VERSION);
 assert.equal(store.readOnly,true);
 assert.match(store.error,/upgraded safely in memory/);
});
