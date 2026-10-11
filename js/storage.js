export const STORAGE_KEY='gate-preparation-v1';
export const LATEST_SCHEMA_VERSION=6;
export function defaults(){return {schemaVersion:LATEST_SCHEMA_VERSION,stateKind:'gate-user-progress',revision:0,profile:{name:''},settings:{theme:'light',sound:true,checkpointSound:true,volume:0.04,checkpoint:true,shortcuts:true,goal:10,focus:false,preferredMode:'practice'},drafts:{},sessions:[],attempts:[],bookmarks:{},notes:{},notebooks:[],flashcards:[],planner:{exam:'GATE',date:'',minutes:30},blueprints:[],reports:[],xpEvents:{},momentReceipts:{}};}

const migrations=new Map([
 [1,value=>({...value,schemaVersion:2,stateKind:'gate-user-progress'})],
 [2,value=>{
  const sessions=new Map((value.sessions||[]).map(session=>[session.id,session]));
  const attempts=(value.attempts||[]).map(attempt=>{
   const session=sessions.get(attempt.sessionId),configuration=session?.configuration||{};
   const sourceContext={origin:attempt.sessionOrigin??session?.origin??null};
   for(const key of ['day','year','paper','source'])if(configuration[key]!==undefined&&configuration[key]!=='')sourceContext[key]=configuration[key];
   return {...attempt,selectedAnswer:attempt.selectedAnswer??attempt.answer??null,correctness:attempt.correctness??attempt.result,timeSpent:attempt.timeSpent??attempt.questionTime??0,mode:attempt.mode??session?.mode??'practice',sourceContext:attempt.sourceContext??sourceContext,localDate:attempt.localDate??null};
  });
  return {...value,schemaVersion:3,attempts};
 }],
 [3,value=>{
  const canonical=session=>({...session,startedAt:session.startedAt??session.createdAt,endedAt:session.endedAt??session.completedAt??null,plannedDuration:session.plannedDuration??(Number(session.configuration?.minutes)>0?Number(session.configuration.minutes)*60000:null),currentPosition:session.currentPosition??session.index??0,status:session.status??(session.completedAt?'completed':'interrupted')});
  return {...value,schemaVersion:4,sessions:(value.sessions||[]).map(canonical),drafts:Object.fromEntries(Object.entries(value.drafts||{}).map(([id,session])=>[id,canonical(session)]))};
 }],
 [4,value=>{
  const attempts=(value.attempts||[]).map(attempt=>{
   const {answer,result,questionTime,totalQuestionTime,attemptNumber,sessionOrigin,...canonical}=attempt;
   return canonical;
  });
  const attemptsBySession=new Map();
  for(const attempt of attempts){const records=attemptsBySession.get(attempt.sessionId)||[];records.push(attempt);attemptsBySession.set(attempt.sessionId,records);}
  const session=session=>{
   const {createdAt,completedAt,index,...canonical}=session;
   const recorded=new Set((attemptsBySession.get(session.id)||[]).map(attempt=>attempt.questionId));
   const fullyRecorded=Array.isArray(session.questionIds)&&session.questionIds.every(id=>recorded.has(id));
   if(!fullyRecorded)return canonical;
   const {answers,times,review,visited,deadline,...withoutQuestionState}=canonical;
   if(!withoutQuestionState.result)return withoutQuestionState;
   const {rows,...summary}=withoutQuestionState.result;
   return {...withoutQuestionState,result:summary};
  };
  const draft=session=>{const {createdAt,completedAt,index,...canonical}=session;return canonical;};
  return {...value,schemaVersion:5,attempts,sessions:(value.sessions||[]).map(session),drafts:Object.fromEntries(Object.entries(value.drafts||{}).map(([id,value])=>[id,draft(value)]))};
 }],
 [5,value=>({...value,schemaVersion:6,momentReceipts:{}})]
]);

export function migrateState(value){
 if(!value||typeof value!=='object'||Array.isArray(value))throw Error('Invalid saved state. Your existing data has not been changed.');
 if(!Number.isInteger(value.schemaVersion))throw Error('Saved state has no valid schema version. Your existing data has not been changed.');
 if(value.schemaVersion>LATEST_SCHEMA_VERSION||value.schemaVersion<1)throw Error('Unsupported backup version. Your existing data has not been changed.');
 let next=JSON.parse(JSON.stringify(value));
 while(next.schemaVersion<LATEST_SCHEMA_VERSION){
  const migrate=migrations.get(next.schemaVersion);
  if(!migrate)throw Error('No migration is available for this backup version. Your existing data has not been changed.');
  const before=next.schemaVersion;
  next=migrate(next);
  if(!next||next.schemaVersion!==before+1)throw Error('Saved-state migration failed. Your existing data has not been changed.');
 }
 return next;
}

export function validateState(value){
 value=migrateState(value);
 if(value.schemaVersion!==LATEST_SCHEMA_VERSION||value.stateKind!=='gate-user-progress')throw Error('Invalid application state. Your existing data has not been changed.');
 for(const k of ['sessions','attempts','notebooks','flashcards','blueprints','reports'])if(!Array.isArray(value[k]))throw Error('Invalid backup: '+k);
 for(const k of ['settings','drafts','bookmarks','notes','planner','profile','xpEvents','momentReceipts'])if(!value[k]||typeof value[k]!=='object'||Array.isArray(value[k]))throw Error('Invalid backup: '+k);
 if(!['light','dark'].includes(value.settings.theme)||!Number.isFinite(value.settings.goal)||value.settings.goal<1)throw Error('Invalid backup settings.');
 const unique=(items,key)=>new Set(items.map(x=>x[key])).size===items.length;
 if(!unique(value.sessions,'id')||!unique(value.attempts,'attemptId'))throw Error('Duplicate records in backup.');
 const validSession=s=>typeof s.id==='string'&&Array.isArray(s.questionIds)&&s.questionIds.length>0&&Number.isFinite(Date.parse(s.startedAt))&&(s.endedAt===null||Number.isFinite(Date.parse(s.endedAt)))&&['practice','test'].includes(s.mode)&&(s.plannedDuration===null||Number.isFinite(s.plannedDuration)&&s.plannedDuration>0)&&Number.isInteger(s.currentPosition)&&s.currentPosition>=0&&s.currentPosition<s.questionIds.length&&['active','completed','abandoned','interrupted'].includes(s.status);
 for(const s of value.sessions)if(!validSession(s)||s.status!=='completed'||!s.endedAt||!s.result||!Number.isFinite(s.elapsed))throw Error('Invalid session.');
 for(const a of value.attempts){
  if(typeof a.attemptId!=='string'||typeof a.questionId!=='string'||typeof a.sessionId!=='string'||!Number.isFinite(Date.parse(a.timestamp))||!['correct','incorrect','blank','ungraded','awarded'].includes(a.correctness)||!Number.isFinite(a.timeSpent)||a.timeSpent<0||!['practice','test'].includes(a.mode)||!a.sourceContext||typeof a.sourceContext!=='object'||Array.isArray(a.sourceContext))throw Error('Invalid attempt.');
  if(Array.isArray(a.selectedAnswer))a.selectedAnswer=[...new Set(a.selectedAnswer)];
 }
 for(const d of Object.values(value.drafts)){
  if(!validSession(d)||!['active','interrupted'].includes(d.status)||!d.answers||!d.times||!d.visited||!d.review||!Number.isFinite(d.elapsed))throw Error('Invalid draft.');
  for(const [k,ans] of Object.entries(d.answers)){
   if(Array.isArray(ans))d.answers[k]=[...new Set(ans)];
  }
 }
 for(const n of value.notebooks)if(typeof n.id!=='string'||typeof n.name!=='string'||!Array.isArray(n.questionIds))throw Error('Invalid notebook.');
 for(const f of value.flashcards)if(typeof f.id!=='string'||typeof f.front!=='string'||typeof f.back!=='string'||!Number.isFinite(f.due))throw Error('Invalid flashcard.');
 for(const note of Object.values(value.notes))if(typeof note!=='string')throw Error('Invalid note.');
 const id=x=>typeof x==='string'&&/^[a-zA-Z0-9:_-]{1,180}$/.test(x);
 for(const [key,stamp] of Object.entries(value.momentReceipts))if(!/^[a-zA-Z0-9:_-]{1,256}$/.test(key)||typeof stamp!=='string'||!Number.isFinite(Date.parse(stamp)))throw Error('Invalid moment receipt.');
 const number=x=>typeof x==='number'&&Number.isFinite(x)&&x>=0;
 if(typeof value.profile.name!=='string'||typeof value.planner.exam!=='string'||typeof value.planner.date!=='string'||!number(value.planner.minutes))throw Error('Invalid profile or planner.');
 for(const [key,event] of Object.entries(value.xpEvents))if(!id(key)||!event||!number(event.amount)||(event.id!==undefined&&event.id!==key))throw Error('Invalid XP event.');
 for(const [key,kind] of Object.entries(value.bookmarks))if(!id(key)||!['Saved','Important','Must Revise'].includes(kind))throw Error('Invalid bookmark.');
 for(const entry of [...value.sessions,...Object.values(value.drafts),...value.blueprints]){
  if(!id(entry.id)||!['practice','test'].includes(entry.mode))throw Error('Invalid session or blueprint identifier.');
  const config=entry.configuration||entry;
  if(config.day!==undefined&&(!Number.isInteger(config.day)||config.day<1||config.day>118))throw Error('Invalid day.');
  if(entry.questionIds&&!entry.questionIds.every(id))throw Error('Invalid question references.');
 }
 for(const session of value.sessions){for(const k of ['correct','incorrect','ungraded','blank','answered','maxMarks'])if(!number(session.result[k]))throw Error('Invalid result counts.');if(session.result.score!==null&&!Number.isFinite(session.result.score))throw Error('Invalid score.');}
 for(const entry of [...value.notebooks,...value.flashcards,...value.reports])if(!id(entry.id))throw Error('Invalid record identifier.');
 for(const card of value.flashcards)if(!number(card.reviewCount)||!number(card.successes))throw Error('Invalid review record.');
 for(const b of value.blueprints)if(typeof b.name!=='string'||!number(b.count)||b.count<1||!number(b.minutes))throw Error('Invalid blueprint.');
 return {...defaults(),...value,settings:{...defaults().settings,...value.settings}};
}
export function serializeState(value){return JSON.stringify(validateState(value));}
export function deserializeState(serialized){
 if(typeof serialized!=='string'||!serialized.trim())throw Error('Import data must be a non-empty JSON string.');
 let parsed;try{parsed=JSON.parse(serialized);}catch{throw Error('Import data is not valid JSON.');}
 return validateState(parsed);
}
function hydrateRuntimeAliases(state){
 for(const session of state.sessions)if(!Object.getOwnPropertyDescriptor(session,'completedAt'))Object.defineProperty(session,'completedAt',{configurable:true,get(){return this.endedAt;}});
 return state;
}
export class Store {
 constructor(adapter){
  this.adapter=adapter;this.error=null;this.diagnostic=null;this.recovery=null;this.originalRaw=null;this.readOnly=false;
  let raw,parsed;
  try{raw=adapter.getItem(STORAGE_KEY);this.originalRaw=typeof raw==='string'?raw:null;parsed=raw?JSON.parse(raw):null;this.state=hydrateRuntimeAliases(parsed?validateState(parsed):defaults());}
  catch(e){this.state=defaults();this.diagnostic=e.message;this.recovery={kind:raw===undefined?'storage-unavailable':'invalid-state',rawAvailable:typeof raw==='string'};this.error=raw===undefined?'Browser storage could not be accessed. The app started with a safe temporary workspace; changes are protected until storage is available.':'Your saved progress could not be opened. The app started with safe defaults, and the original browser record has not been changed.';this.readOnly=true;return;}
  if(parsed&&parsed.schemaVersion!==this.state.schemaVersion){
   try{adapter.setItem(STORAGE_KEY,JSON.stringify(this.state));}
   catch(e){this.diagnostic=e.message;this.recovery={kind:'migration-write-failed',rawAvailable:typeof raw==='string'};this.error='Progress was upgraded safely in memory, but the upgraded copy could not be saved. The original browser record has not been changed.';this.readOnly=true;}
  }
 }
 save(){if(this.readOnly)throw Error('Storage is protected because existing data could not be read. Export the original data before resetting.');
  this.state.revision++;try{const serialized=JSON.stringify(this.state);this.adapter.setItem(STORAGE_KEY,serialized);this.originalRaw=serialized;}catch(e){this.diagnostic=e.message;this.recovery={kind:'write-failed',rawAvailable:this.originalRaw!==null};this.error='Progress could not be saved. The last browser record has been left in place.';this.readOnly=true;throw Error(this.error);}}
 replace(value){const next=validateState(value),serialized=JSON.stringify(next);if(serialized===JSON.stringify(this.state)){this.readOnly=false;this.error=null;this.diagnostic=null;this.recovery=null;return this.state;}this.adapter.setItem(STORAGE_KEY,serialized);this.state=hydrateRuntimeAliases(next);this.originalRaw=serialized;this.readOnly=false;this.error=null;this.diagnostic=null;this.recovery=null;return this.state;}
 raw(){if(this.recovery?.rawAvailable)return this.originalRaw;try{return this.adapter.getItem(STORAGE_KEY);}catch{return null;}}
}
