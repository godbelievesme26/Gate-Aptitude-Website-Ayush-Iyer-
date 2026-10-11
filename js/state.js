import {commitQuestionAttempt,move,submit} from './domain.js';
import {xp} from './domain.js';
import {completionMoment,receiptMoment} from './moments.js';

/**
 * Canonical application state boundary.
 *
 * content  - immutable source archive loaded from JSON
 * progress - persisted user-owned data managed by Store
 * session  - current session identity and runtime-only timer
 * ui       - temporary presentation state that is never persisted
 */
export class ApplicationState {
 constructor(store){
  if(!store)throw Error('Application state requires a progress store.');
  this.store=store;
  this.content=null;
  this.session={activeId:null,timer:null};
  this.ui={revealedFlashcard:false,offlineReady:false,installEvent:null,saveTick:0,conflict:false};
 }
 get progress(){return this.store.state;}
 get activeSession(){return this.session.activeId?this.progress.drafts[this.session.activeId]||null:null;}
 initializeContent(content){
  if(!content||!Array.isArray(content.questions)||!(content.byId instanceof Map))throw Error('Invalid content archive.');
  this.content=content;
  return content;
 }
 activateSession(id,timerFactory){
  const draft=this.progress.drafts[id]||null;
  if(!draft){this.clearSession();return null;}
  if(this.content&&!draft.questionIds.every(questionId=>this.content.byId.has(questionId))){this.clearSession();return null;}
  this.clearSession();
  this.session.activeId=id;
  draft.status='active';
  if(!Object.getOwnPropertyDescriptor(draft,'index'))Object.defineProperty(draft,'index',{configurable:true,get(){return this.currentPosition;},set(value){this.currentPosition=value;}});
  this.session.timer=timerFactory?timerFactory(draft):null;
  return draft;
 }
 clearSession(){
  this.session.timer?.stop?.();
  this.session.activeId=null;
  this.session.timer=null;
 }
 save(){if(this.ui.conflict)throw Error('Another tab changed your progress. Reload this tab before continuing.');this.store.save();return this.progress;}
 updateProgress(change){change(this.progress);this.save();return this.progress;}
 addDraft(draft){this.updateProgress(progress=>{progress.drafts[draft.id]=draft;});return draft;}
 commitAndMove(session,byId,nextPosition,now=new Date()){let attempt;this.updateProgress(progress=>{const question=byId.get(session.questionIds[session.currentPosition]);if(!question)throw Error('The current question is unavailable.');attempt=commitQuestionAttempt(progress,session,question,now);move(session,nextPosition);});return attempt;}
 completeSession(session,byId,now=new Date()){
  const existing=this.progress.sessions.find(record=>record.id===session.id);if(existing)return existing;
  // submit only appends records, deletes its draft and adds XP keys. Copy those
  // collections while preserving existing record identities and runtime aliases.
  const original=this.progress,next={...original,sessions:[...original.sessions],attempts:[...original.attempts],drafts:{...original.drafts},xpEvents:{...original.xpEvents},momentReceipts:{...original.momentReceipts}},previousXp=xp(original);
  const record=submit(next,session,byId,now),moment=['active','interrupted'].includes(session.status)?completionMoment(next,record,previousXp,now):null;
  receiptMoment(next,moment);this.store.state=next;
  try{this.save();}catch(error){this.store.state=original;throw error;}
  // Display is a one-shot runtime effect, never a side effect of loading a page.
  this.ui.productMoment=moment;return record;
 }
 takeProductMoment(sessionId){const moment=this.ui.productMoment;this.ui.productMoment=null;return moment?.sessionId===sessionId?moment:null;}
 setBookmark(questionId,kind){const current=this.progress.bookmarks[questionId]||'';if(current===kind)return false;this.updateProgress(progress=>{if(kind)progress.bookmarks[questionId]=kind;else delete progress.bookmarks[questionId];});return true;}
 setNote(questionId,note){this.updateProgress(progress=>{progress.notes[questionId]=note;});}
 clearQuizProgress(){this.clearSession();this.updateProgress(progress=>{progress.sessions=[];progress.attempts=[];progress.drafts={};});}
 replaceProgress(value){this.clearSession();this.ui.productMoment=null;this.store.replace(value);return this.progress;}
 raw(){return this.store.raw();}
 get error(){return this.store.error;}
 get recovery(){return this.store.recovery;}
 get readOnly(){return this.store.readOnly;}
}

