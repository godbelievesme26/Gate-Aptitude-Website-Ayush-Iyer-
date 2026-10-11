import {answered} from './scoring.js';
import {generateSession,localDay} from './domain.js';

export const REVIEW_POLICY=Object.freeze({id:'revision-v1',firstWrong:1,wrongAgain:3,recovered:7,correctAgain:14});
export const REVISION_LABELS=Object.freeze({never:'Never attempted',ungraded:'Not graded',correct:'Correct',wrong:'Wrong',repeated:'Repeated mistake',recovered:'Recovered'});
const compareText=(a,b)=>a<b?-1:a>b?1:0;
// UTC is used only for arithmetic on date-only calendar components, never to
// choose the learner's date. Captured localDate remains stable after travel/DST.
export function validLocalDate(day){
 if(typeof day!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(day))return false;
 const date=new Date(day+'T12:00:00Z');return Number.isFinite(date.getTime())&&date.toISOString().slice(0,10)===day;
}
export function addLocalDays(day,days){if(!validLocalDate(day))return null;const date=new Date(day+'T12:00:00Z');date.setUTCDate(date.getUTCDate()+days);return date.toISOString().slice(0,10);}
export function attemptLocalDate(attempt){if(validLocalDate(attempt.localDate))return attempt.localDate;const date=new Date(attempt.timestamp);return Number.isFinite(date.getTime())?localDay(date):null;}
export function revisionState(state,questionId,now=new Date()){
 const attempts=(state.attempts||[]).filter(a=>a.questionId===questionId&&answered(a.selectedAnswer)).map((a,index)=>({a,index})).sort((x,y)=>Date.parse(x.a.timestamp)-Date.parse(y.a.timestamp)||x.index-y.index).map(x=>x.a);
 let wrongCount=0,wrongRun=0,successRun=0,dueDate=null,interval=null,reason=null,recoveryAttemptNumber=null,lastGraded=null;
 for(const [index,a] of attempts.entries()){
  if(a.correctness==='incorrect'){
   wrongCount++;wrongRun++;successRun=0;recoveryAttemptNumber=null;
   interval=wrongRun===1?REVIEW_POLICY.firstWrong:REVIEW_POLICY.wrongAgain;
   reason=wrongRun===1?(wrongCount===1?'First incorrect response.':'New mistake after recovery.'):'Another incorrect response before recovery.';
  }else if(a.correctness==='correct'){
   wrongRun=0;successRun++;
   if(wrongCount){if(successRun===1)recoveryAttemptNumber=index+1;interval=successRun===1?REVIEW_POLICY.recovered:REVIEW_POLICY.correctAgain;reason=successRun===1?'Correct after an earlier mistake.':'Correct again after recovery.';}
   else{interval=null;reason=null;}
  }else continue;
  lastGraded=a;dueDate=interval?addLocalDays(attemptLocalDate(a),interval):null;
 }
 const learningState=!attempts.length?'never':!lastGraded?'ungraded':lastGraded.correctness==='incorrect'?(wrongCount>=2?'repeated':'wrong'):wrongCount?'recovered':'correct';
 const today=localDay(now),lastAttempt=attempts.at(-1)||null;
 return {questionId,learningState,label:REVISION_LABELS[learningState],attempts,attemptCount:attempts.length,wrongCount,wrongRun,recoveryAttemptNumber,lastAttempt,lastAttemptDate:lastAttempt?attemptLocalDate(lastAttempt):null,lastGraded,dueDate,interval,reason,due:!!dueDate&&dueDate<=today,overdue:!!dueDate&&dueDate<today};
}
export function revisionPriority(item){return item.learningState==='repeated'?0:item.overdue?1:item.learningState==='wrong'?2:3;}
export function revisionItems(questions,state,now=new Date()){
 const seen=new Set();return questions.filter(q=>q?.id&&!seen.has(q.id)&&seen.add(q.id)).map(question=>({...revisionState(state,question.id,now),question})).filter(item=>item.attemptCount>0);
}
export function dueReviewQueue(questions,state,now=new Date()){
 return revisionItems(questions,state,now).filter(item=>item.due).sort((a,b)=>revisionPriority(a)-revisionPriority(b)||compareText(a.dueDate,b.dueDate)||compareText(a.questionId,b.questionId));
}
export function generateReviewSession(questions,state,{capacity=10,questionId=null}={},now=new Date(),id){
 if(!Number.isInteger(capacity)||capacity<1||capacity>160)throw Error('Choose a review capacity from 1 to 160 questions.');
 const queue=questionId?revisionItems(questions,state,now).filter(item=>item.questionId===questionId):dueReviewQueue(questions,state,now);
 const selected=queue.slice(0,questionId?1:capacity);
 if(!selected.length)throw Error(questionId?'This question has no answered history to review.':'No questions are due for review right now.');
 const ordered=selected.map(item=>item.question);
 return generateSession(ordered,state,{origin:'revision',mode:'practice',ids:ordered.map(q=>q.id),count:ordered.length,minutes:ordered.length*2,reviewPolicy:REVIEW_POLICY.id},id);
}
