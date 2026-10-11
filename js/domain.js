import {answered,scoreQuestion,scoreSession} from './scoring.js';
export const localDay=(date=new Date())=>`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
const dayNumber=day=>Math.round(Date.parse(day+'T00:00:00Z')/86400000);
export function streak(attempts,now=new Date()){
 const days=[...new Set(attempts.filter(a=>answered(a.selectedAnswer)).map(a=>a.localDate||localDay(new Date(a.timestamp))))].sort();
 let longest=0,run=0,previous;for(const d of days){const v=dayNumber(d);run=previous===v-1?run+1:1;longest=Math.max(longest,run);previous=v;}
 const today=dayNumber(localDay(now));return {current:previous>=today-1?run:0,longest,days};
}
export function questionStats(state,id){
 const attempts=state.attempts.filter(a=>a.questionId===id&&answered(a.selectedAnswer));const wrong=attempts.filter(a=>a.correctness==='incorrect');const correct=attempts.filter(a=>a.correctness==='correct');const latest=attempts.at(-1);
 const recovered=wrong.length>0&&latest?.correctness==='correct';
 // Mastery: three consecutive correct attempts across at least three local dates.
 const last=attempts.slice(-3);const mastered=last.length===3&&last.every(a=>a.correctness==='correct')&&new Set(last.map(a=>a.localDate)).size===3;
 return {attempts,wrong:wrong.length,correct:correct.length,latest,recovered,unresolved:wrong.length>0&&latest?.correctness!=='correct',totalTime:attempts.reduce((v,a)=>v+a.timeSpent,0),mastery:mastered?'Mastered':latest?.correctness==='incorrect'?'Needs review':correct.length>=2?'Strong':attempts.length?'Learning':'New'};
}
export const completedDays=state=>new Set(state.sessions.filter(s=>s.origin==='daily'&&s.result.answered===s.questionIds.length).map(s=>s.configuration.day));
export const xp=state=>Object.values(state.xpEvents).reduce((sum,e)=>sum+e.amount,0);
export const level=points=>['Beginner','Learner','Practitioner','Solver','Advanced Solver','Expert'][Math.min(5,Math.floor(points/500))];
export function generateSession(questions,state,config={},id=globalThis.crypto.randomUUID()){
 const pool=questions.filter(q=>(!config.year||q.year===Number(config.year))&&(!config.paper||q.paper===config.paper)&&(!config.ids||config.ids.includes(q.id))&&
  (!config.source||config.source==='all'||config.source==='unattempted'&&!state.attempts.some(a=>a.questionId===q.id&&answered(a.selectedAnswer))||config.source==='bookmarked'&&!!state.bookmarks[q.id]||config.source==='incorrect'&&questionStats(state,q.id).unresolved||config.source==='notebook'&&state.notebooks.find(n=>n.id===config.notebook)?.questionIds.includes(q.id)));
 if(config.prioritize)pool.sort((a,b)=>priority(b,state)-priority(a,state));
 const selected=pool.slice(0,Math.max(1,Math.min(160,Number(config.count)||pool.length)));
 if(!selected.length)throw Error('No questions match these choices. Change the filters and try again.');
 const mode=config.mode||'practice',plannedDuration=Number(config.minutes)>0?Number(config.minutes)*60000:null,startedAt=new Date().toISOString();
 const session={id,startedAt,endedAt:null,mode,plannedDuration,questionIds:selected.map(q=>q.id),currentPosition:0,status:'active',origin:config.origin||'custom',configuration:config,answers:{},review:{},visited:{[selected[0].id]:true},times:{},elapsed:0,deadline:mode==='test'?Date.now()+(plannedDuration||1800000):null};
 Object.defineProperty(session,'index',{configurable:true,get(){return this.currentPosition;},set(value){this.currentPosition=value;}});
 return session;
}
function priority(q,s){return (questionStats(s,q.id).unresolved?100:0)+(s.bookmarks[q.id]==='Must Revise'?50:0)+(!s.attempts.some(a=>a.questionId===q.id&&answered(a.selectedAnswer))?20:0);}
export function move(session,index){session.currentPosition=Math.max(0,Math.min(session.questionIds.length-1,index));session.visited[session.questionIds[session.currentPosition]]=true;}
export function interruptSession(session){if(session.status==='active')session.status='interrupted';return session;}
export function resumeSession(session){if(session.status==='interrupted')session.status='active';return session;}
export function abandonSession(session,now=new Date()){if(session.status!=='completed'){session.status='abandoned';session.endedAt=now.toISOString();}return session;}
export function createAttemptEvent(session,row,question,timestamp){
 const configuration=session.configuration||{},sourceContext={origin:session.origin};
 const context={day:configuration.day??question?.day,year:question?.year??configuration.year,paper:question?.paper??configuration.paper,source:configuration.source,sourceFile:question?.source?.file};
 for(const [key,value] of Object.entries(context))if(value!==undefined&&value!==null&&value!=='')sourceContext[key]=value;
 return {attemptId:`${session.id}:${row.questionId}`,questionId:row.questionId,sessionId:session.id,selectedAnswer:structuredClone(row.answer),correctness:row.result,timeSpent:session.times[row.questionId]||0,timestamp,mode:session.mode,sourceContext,markedForReview:!!session.review[row.questionId],localDate:localDay(new Date(timestamp))};
}
export function commitQuestionAttempt(state,session,question,now=new Date()){
 const attemptId=`${session.id}:${question.id}`,existing=state.attempts.find(attempt=>attempt.attemptId===attemptId);if(existing)return existing;
 const answer=structuredClone(session.answers[question.id]??null),scored=scoreQuestion(question,answer),row={questionId:question.id,answer,result:scored.result};
 const event=createAttemptEvent(session,row,question,now.toISOString());state.attempts.push(event);return event;
}
export function submit(state,session,byId,now=new Date()){
 const existing=state.sessions.find(s=>s.id===session.id);if(existing)return existing;
 const result=scoreSession(session.questionIds.map(id=>byId.get(id)),session.answers);const stamp=now.toISOString();
 const {rows,...summary}=result;
 const record={id:session.id,startedAt:session.startedAt,endedAt:stamp,mode:session.mode,plannedDuration:session.plannedDuration,questionIds:[...session.questionIds],currentPosition:session.currentPosition,status:'completed',origin:session.origin,configuration:structuredClone(session.configuration),elapsed:session.elapsed,localDate:localDay(now),result:summary};
 Object.defineProperty(record,'completedAt',{configurable:true,get(){return this.endedAt;}});
 for(const row of result.rows){const event=createAttemptEvent(session,row,byId.get(row.questionId),stamp);if(!state.attempts.some(attempt=>attempt.attemptId===event.attemptId))state.attempts.push(event);
  // Once per question, participation XP. Correctness remains separate from effort.
  const awardId='question:'+row.questionId;if(answered(row.answer)&&!state.xpEvents[awardId])state.xpEvents[awardId]={id:awardId,amount:10,timestamp:stamp};
 }
 state.sessions.push(record);delete state.drafts[session.id];return record;
}
export function recommendation(state,archive){
 const draft=Object.values(state.drafts).at(-1);if(draft)return {title:'Pick up where you left off',reason:`${Object.keys(draft.answers).filter(k=>answered(draft.answers[k])).length} of ${draft.questionIds.length} answered. Your draft is saved.`,href:'#/quiz/'+draft.id,label:'Continue practice'};
 const done=completedDays(state),day=archive.registry.find(s=>!done.has(s.day));if(day)return {title:`Make time for Day ${day.day}`,reason:`${day.year} ${day.paper} · 10 questions · 15 marks`,href:'#/day/'+day.day,label:`Start Day ${day.day}`};
 const wrong=archive.questions.filter(q=>questionStats(state,q.id).unresolved).length;if(wrong)return {title:'Return to your mistakes',reason:`${wrong} questions have an unresolved incorrect attempt.`,href:'#/review/mistakes',label:'Review mistakes'};
 const due=state.flashcards.filter(f=>f.due<=Date.now()).length;if(due)return {title:'A little revision goes a long way',reason:`${due} flashcards are due.`,href:'#/flashcards',label:'Review flashcards'};
 return {title:'Keep your practice moving',reason:'Choose questions from the available archive.',href:'#/bank',label:'Explore PYQs'};
}
export function deterministicSessionQuestions(questions,budgetMinutes,state,now=Date.now()){
 const minutes=Number(budgetMinutes);
 if(!Number.isInteger(minutes)||minutes<1||minutes>360)throw Error('Session budget must be from 1 to 360 whole minutes.');
 const progress=state||{attempts:[],flashcards:[]};
 const available=[],seenIds=new Set();
 for(const question of Array.isArray(questions)?questions:[])if(question&&typeof question.id==='string'&&!seenIds.has(question.id)){available.push(question);seenIds.add(question.id);}
 const limit=Math.min(available.length,Math.max(1,Math.floor(minutes/2)));
 const attempted=new Set((progress.attempts||[]).filter(attempt=>answered(attempt.selectedAnswer)).map(attempt=>attempt.questionId));
 const mistakes=new Set(available.filter(question=>questionStats(progress,question.id).unresolved).map(question=>question.id));
 const due=new Set((progress.flashcards||[]).filter(card=>card.questionId&&Number.isFinite(card.due)&&card.due<=now&&seenIds.has(card.questionId)).map(card=>card.questionId));
 const groups=[['recoverableMistakes',question=>mistakes.has(question.id)],['dueReviewItems',question=>due.has(question.id)],['unattempted',question=>!attempted.has(question.id)],['available',()=>true]],ordered=[],selected=new Set(),counts={recoverableMistakes:0,dueReviewItems:0,unattempted:0,available:0};
 for(const [kind,matches] of groups)for(const question of available)if(ordered.length<limit&&!selected.has(question.id)&&matches(question)){ordered.push(question.id);selected.add(question.id);counts[kind]++;}
 return {questionIds:ordered,reason:{code:'priority-fill-v1',counts,budgetMinutes:minutes,minutesPerQuestion:2,topicDataUsed:false}};
}
export function startNowPlan(state,archive,budgetMinutes=25){
 const questions=Array.isArray(archive?.questions)?archive.questions.filter(question=>question&&typeof question.id==='string'):[];
 const availableIds=new Set(questions.map(question=>question.id));
 const draft=Object.values(state.drafts).reverse().find(session=>Array.isArray(session.questionIds)&&session.questionIds.length&&session.questionIds.every(id=>availableIds.has(id)));
 if(draft)return {kind:'resume',sessionId:draft.id,mode:draft.mode};
 if(!questions.length)return {kind:'unavailable',reason:'Study questions are unavailable right now. Reload the page after the content archive is restored.'};
 const selection=deterministicSessionQuestions(questions,budgetMinutes,state);
 return {kind:'new',questionIds:selection.questionIds,reason:selection.reason,config:{origin:'start-now',ids:selection.questionIds,count:selection.questionIds.length,minutes:Number(budgetMinutes),selectionReason:selection.reason}};
}
export function sessionBudget(preset,custom){
 const fixed=new Set(['10','25','45','60']);
 const raw=fixed.has(String(preset))?preset:preset==='custom'?custom:null,value=Number(raw);
 if(!Number.isInteger(value)||value<1||value>360)throw Error('Choose a study budget from 1 to 360 whole minutes.');
 return value;
}
export function reviewCard(card,rating,now=Date.now()){
 const intervals={Again:1/144,Hard:1,Good:Math.max(2,(card.interval||1)*2),Easy:Math.max(4,(card.interval||1)*3)};
 card.interval=intervals[rating];card.due=now+card.interval*86400000;card.reviewCount=(card.reviewCount||0)+1;card.successes=(card.successes||0)+(rating==='Again'?0:1);card.lastReviewed=now;
}
export function achievements(state){const count=new Set(state.attempts.filter(a=>answered(a.selectedAnswer)).map(a=>a.questionId)).size;const days=completedDays(state).size;const st=streak(state.attempts);return [...new Set([count>0&&'First PYQ',days>0&&'First daily set',count>=100&&'100 questions',st.longest>=7&&'7 day streak',days>=25&&'25 days completed'].filter(Boolean))];}
