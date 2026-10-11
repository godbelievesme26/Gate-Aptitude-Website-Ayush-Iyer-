import {loadArchive} from '../../js/loader.js';
import {Store,STORAGE_KEY} from '../../js/storage.js';
import {ApplicationState} from '../../js/state.js';
import {generateSession} from '../../js/domain.js';
import {revisionState,dueReviewQueue} from '../../js/revision.js';
const archive=await loadArchive(),status=document.querySelector('#status');
function isolated(){if(location.port!=='4186'){status.textContent='Blocked: use the disposable test origin on port 4186.';return false;}return true;}
document.querySelector('#prepare').onclick=()=>{
 if(!isolated())return;
 let raw=null;const state=new ApplicationState(new Store({getItem:()=>raw,setItem(k,v){raw=v;}})),now=new Date();state.initializeContent(archive);state.progress.settings.theme=document.querySelector('#theme').value;
 const commit=(index,daysAgo,correct,id)=>{const q=archive.questions[index],date=new Date(now);date.setDate(date.getDate()-daysAgo);const d=generateSession([q],state.progress,{count:1},id);d.startedAt=date.toISOString();d.answers[q.id]=correct?q.answer:q.options.find(o=>o.label!==q.answer).label;d.elapsed=65000;state.addDraft(d);state.completeSession(d,archive.byId,date);state.takeProductMoment(d.id);};
 if(document.querySelector('#scenario').value==='queue'){
  commit(0,5,false,'qa-repeat-first');commit(0,4,false,'qa-repeat-second');commit(1,3,false,'qa-overdue');commit(2,1,false,'qa-due');commit(3,12,false,'qa-recovery-old');commit(3,7,true,'qa-recovered-due');commit(4,2,false,'qa-recovery-recent-old');commit(4,1,true,'qa-recovered-future');commit(5,1,true,'qa-correct');
  localStorage.setItem(STORAGE_KEY,JSON.stringify(state.progress));location.href='/#/review';
 }else{const q=archive.questions[0],d=generateSession([q],state.progress,{count:1},'qa-first-practice');state.addDraft(d);localStorage.setItem(STORAGE_KEY,JSON.stringify(state.progress));location.href='/#/quiz/'+d.id;}
};
document.querySelector('#inspect').onclick=()=>{if(!isolated())return;const store=new Store(localStorage),q=archive.questions[0],r=revisionState(store.state,q.id);document.querySelector('#evidence').textContent=JSON.stringify({schemaVersion:store.state.schemaVersion,readOnly:store.readOnly,questionId:q.id,state:r.learningState,dueDate:r.dueDate,attemptCount:r.attemptCount,attempts:r.attempts.map(a=>({attemptId:a.attemptId,sessionId:a.sessionId,selectedAnswer:a.selectedAnswer,correctness:a.correctness,origin:a.sourceContext.origin,localDate:a.localDate})),dueQueue:dueReviewQueue(archive.questions,store.state).map(i=>i.questionId),sessions:store.state.sessions.map(s=>({id:s.id,origin:s.origin,questionIds:s.questionIds,answered:s.result.answered})),drafts:Object.values(store.state.drafts).map(d=>({id:d.id,origin:d.origin,questionIds:d.questionIds}))},null,2);};
document.querySelectorAll('#prepare,#inspect').forEach(b=>b.disabled=false);status.textContent='Ready — canonical content and fixture controls loaded.';
