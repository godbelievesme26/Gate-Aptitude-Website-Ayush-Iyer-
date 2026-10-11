// Numeric input has no option-click action. Persist its string value on input,
// without rerendering the control or creating an attempt before submission.
export function saveNumericAnswer(application,session,question,value){
 if(!session||question?.type!=='NAT'||session.questionIds[session.currentPosition]!==question.id)throw Error('Numeric answer is unavailable for this question.');
 if(application.progress.attempts.some(attempt=>attempt.attemptId===session.id+':'+question.id))throw Error('This response is already recorded. Continue with the session.');
 if(typeof value!=='string')throw Error('Enter a valid number.');
 const trimmed=value.trim();
 const isIntermediate=trimmed==='-'||trimmed==='+'||trimmed==='.'||trimmed==='-.'||trimmed==='+.';
 if(trimmed!==''&&!isIntermediate&&(!Number.isFinite(Number(trimmed))||Number.isNaN(Number(trimmed))))throw Error('Enter a valid number.');
 const nextValue=trimmed===''? '':trimmed;
 if(session.answers[question.id]===nextValue)return false;
 application.updateProgress(()=>{session.answers[question.id]=nextValue;});return true;
}
