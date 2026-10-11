import {streak,completedDays,localDay,xp,questionStats} from './domain.js';
import {answered} from './scoring.js';

// Definitions are shared by derivation, rendering and tests. No progress lives here.
export const STREAK_MILESTONES=Object.freeze({3:'First rhythm',7:'One week',14:'Two weeks',30:'One month',50:'Sustained momentum',100:'Serious consistency',365:'One year'});
export const QUESTION_MILESTONES=Object.freeze([25,50,100,150]);
export const JOURNEY_MILESTONES=Object.freeze([1,7,14,30,50,100,118]);
export const MOTION_LEVELS=Object.freeze({normal:1200,milestone:2400,major:3400});
const responses=s=>s.attempts.filter(a=>answered(a.selectedAnswer));
const uniqueCount=s=>new Set(responses(s).map(a=>a.questionId)).size;
export const legitimateSession=s=>s?.status==='completed'&&s.questionIds.length>0&&s.result?.answered===s.questionIds.length;

export function storyInsight(state,session,now=new Date()){
 const ids=new Set(state.attempts.filter(a=>a.sessionId===session.id&&a.correctness==='correct').map(a=>a.questionId));
 const previous={...state,attempts:state.attempts.filter(a=>a.sessionId!==session.id)};
 const recovered=[...ids].filter(id=>questionStats(previous,id).unresolved&&questionStats(state,id).recovered).length;
 if(recovered)return {kind:'recovery',text:`You answered ${recovered} previously missed question${recovered===1?'':'s'} correctly in this session.`};
 const start=new Date(now);start.setDate(start.getDate()-6);const first=localDay(start),last=localDay(now);
 const count=state.sessions.filter(s=>legitimateSession(s)&&s.localDate>=first&&s.localDate<=last).length;
 return count>1?{kind:'weekly-sessions',text:`You've completed ${count} fully answered study sessions in the past seven days.`}:null;
}

/** Called only after a new completion has been committed in memory, before its save. */
export function completionMoment(state,session,previousXp,now=new Date()){
 const own=responses(state).filter(a=>a.sessionId===session.id);
 if(!legitimateSession(session)||!session.questionIds.every(id=>own.some(a=>a.questionId===id)))return null;
 const receipts=state.momentReceipts||{},events=[];
 const add=event=>{if(!receipts[event.id])events.push(event);};
 const today=localDay(now),prior={...state,attempts:state.attempts.filter(a=>a.sessionId!==session.id),sessions:state.sessions.filter(s=>s.id!==session.id)};
 add({id:`session:${session.id}`,kind:'session',title:prior.sessions.some(legitimateSession)?'Session complete':'Your preparation starts here.',context:prior.sessions.some(legitimateSession)?'Your answers and study time are saved.':'Your first fully answered study session is saved.',level:'normal'});
 // Attempts can already have been saved by Next. Compare against the same canonical
 // history excluding this session, never an independently maintained streak value.
 const before=streak(prior.attempts,now),after=streak(state.attempts,now);
 if(own.some(a=>a.localDate===today)&&!before.days.includes(today)&&after.current>before.current){
  const milestone=STREAK_MILESTONES[after.current],freshMilestone=milestone&&!receipts[`streak-milestone:${after.current}`];
  add({id:`streak:${today}`,kind:'streak',previous:before.current,value:after.current,title:freshMilestone?milestone:after.current===1?'A day of focused study':'Another day of study',context:`${after.current} consecutive study day${after.current===1?'':'s'}.`,level:freshMilestone?(after.current>=100?'major':'milestone'):'normal',milestoneId:freshMilestone?`streak-milestone:${after.current}`:null});
 }
 const count=s=>responses(s).filter(a=>a.localDate===today).length,goal=state.settings.goal;
 if(count(prior)<goal&&count(state)>=goal)add({id:`goal:${today}`,kind:'goal',title:"Today's goal complete",context:`${count(state)} / ${goal} questions answered today.`,value:count(state),target:goal,level:'normal'});
 const crossed=QUESTION_MILESTONES.filter(n=>uniqueCount(prior)<n&&uniqueCount(state)>=n).at(-1);
 if(crossed)add({id:`questions:${crossed}`,kind:'questions',value:crossed,title:`${crossed} questions explored`,context:`You've answered ${crossed} different questions.`,level:'milestone'});
 const sets=completedDays(state).size,oldSets=completedDays(prior).size;
 if(JOURNEY_MILESTONES.includes(sets)&&sets>oldSets)add({id:`journey:${sets}`,kind:'journey',value:sets,title:sets===1?'Your first daily set':`${sets} daily sets complete`,context:'Progress through your source-paper journey.',level:sets===1?'normal':'milestone'});
 if(!events.some(e=>e.kind==='session'))return null;
 const primary=events.find(e=>e.kind==='streak')||events.find(e=>e.kind==='goal')||events.find(e=>e.kind==='questions'||e.kind==='journey')||events[0];
 return {sessionId:session.id,timestamp:now.toISOString(),events,primary,insight:storyInsight(state,session,now),summary:{answered:session.result.answered,correct:own.filter(a=>a.correctness==='correct').length,ungraded:own.filter(a=>a.correctness==='ungraded'||a.correctness==='awarded').length,elapsed:session.elapsed,xp:Math.max(0,xp(state)-previousXp)}};
}

export function receiptMoment(state,moment){
 if(!moment)return;
 for(const event of moment.events){state.momentReceipts[event.id]=moment.timestamp;if(event.milestoneId)state.momentReceipts[event.milestoneId]=moment.timestamp;}
}
