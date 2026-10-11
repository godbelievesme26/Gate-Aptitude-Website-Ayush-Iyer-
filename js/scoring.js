// Missing keys and missing penalty rules are never replaced with guessed values.
export const answered = value =>
  value !== undefined &&
  value !== null &&
  (typeof value !== 'string' || value.trim() !== '') &&
  (!Array.isArray(value) || value.length > 0);

export function matchNatRange(num, target) {
  if (typeof target === 'number') return num === target;
  if (Array.isArray(target)) {
    if (target.length === 2 && typeof target[0] === 'number' && typeof target[1] === 'number') {
      return num >= target[0] && num <= target[1];
    }
    return target.some(item => matchNatRange(num, item));
  }
  return false;
}

export function scoreQuestion(q, answer) {
  // An official marks-to-all ruling applies even to a blank response.
  if (q.gradingRule==='marks-to-all' && q.answer==='MTA') return {result:'awarded',marks:q.marks,penalty:0};
  if (!answered(answer)) return {result:'blank', marks:0, penalty:0};
  if (q.answer === undefined || !q.type) return {result:'ungraded', marks:null, penalty:null};
  let correct;
  if(q.type==='MCQ') correct=answer===q.answer;
  else if(q.type==='MSQ') correct=Array.isArray(answer)&&[...new Set(answer)].sort().join('|')===[...q.answer].sort().join('|');
  else if(q.type==='NAT') {
    const raw = typeof answer === 'string' ? answer.trim() : answer;
    const num = (typeof raw === 'string' && raw === '') ? NaN : Number(raw);
    correct = Number.isFinite(num) && matchNatRange(num, q.answer);
  }
  else return {result:'ungraded',marks:null,penalty:null};
  return {result:correct?'correct':'incorrect',marks:correct?q.marks:(q.negativeMarks===undefined?null:0-q.negativeMarks),penalty:correct?0:(q.negativeMarks??null)};
}
export function scoreSession(questions, answers) {
  const rows=questions.map(q=>({questionId:q.id,answer:answers[q.id]??null,...scoreQuestion(q,answers[q.id])}));
  const count=result=>rows.filter(r=>r.result===result).length;
  const correct=count('correct'),incorrect=count('incorrect'),ungraded=count('ungraded');
  return {rows,correct,incorrect,ungraded,...(count('awarded')?{awarded:count('awarded')}:{}),blank:count('blank'),answered:rows.filter(r=>answered(r.answer)).length,
    score:questions.some(q=>q.answer===undefined||!q.type)||rows.some(r=>r.marks===null)?null:rows.reduce((n,r)=>n+r.marks,0),
    maxMarks:questions.reduce((n,q)=>n+q.marks,0),accuracy:correct+incorrect?100*correct/(correct+incorrect):null};
}
