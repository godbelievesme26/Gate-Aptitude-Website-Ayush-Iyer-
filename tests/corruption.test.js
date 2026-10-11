import test from 'node:test';
import assert from 'node:assert/strict';
import {Store,STORAGE_KEY,defaults} from '../js/storage.js';

function guardedAdapter(raw){let writes=0;return {getItem:key=>key===STORAGE_KEY?raw:null,setItem(){writes++;throw Error('must not overwrite');},writes:()=>writes};}

test('invalid JSON preserves the raw record and starts safe defaults',()=>{
 const raw='{"schemaVersion":5,"notes":',adapter=guardedAdapter(raw),store=new Store(adapter);
 assert.deepEqual(store.state,defaults());
 assert.equal(store.readOnly,true);
 assert.equal(store.recovery.kind,'invalid-state');
 assert.equal(store.recovery.rawAvailable,true);
 assert.equal(store.raw(),raw);
 assert.equal(adapter.writes(),0);
 assert.match(store.error,/safe defaults/);
 assert.throws(()=>store.save());
});

test('valid JSON with a corrupted state shape is preserved without overwrite',()=>{
 const raw=JSON.stringify({schemaVersion:5,stateKind:'gate-user-progress',sessions:'broken'}),adapter=guardedAdapter(raw),store=new Store(adapter);
 assert.deepEqual(store.state,defaults());
 assert.equal(store.readOnly,true);
 assert.equal(store.raw(),raw);
 assert.equal(adapter.writes(),0);
 assert.match(store.diagnostic,/Invalid backup/);
});

test('storage access failure still produces usable defaults and safe diagnostics',()=>{
 const adapter={getItem(){throw Error('access denied');},setItem(){throw Error('access denied');}},store=new Store(adapter);
 assert.deepEqual(store.state,defaults());
 assert.equal(store.readOnly,true);
 assert.equal(store.recovery.kind,'storage-unavailable');
 assert.equal(store.recovery.rawAvailable,false);
 assert.equal(store.raw(),null);
 assert.match(store.error,/safe temporary workspace/);
});

test('a readable unsupported future state is retained for recovery',()=>{
 const raw=JSON.stringify({schemaVersion:999,stateKind:'gate-user-progress'}),adapter=guardedAdapter(raw),store=new Store(adapter);
 assert.deepEqual(store.state,defaults());
 assert.equal(store.raw(),raw);
 assert.equal(adapter.writes(),0);
 assert.match(store.diagnostic,/Unsupported backup version/);
});
