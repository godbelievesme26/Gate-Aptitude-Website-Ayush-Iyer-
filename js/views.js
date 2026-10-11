import {revisionState} from './revision.js';
import {revisionLibrary,reviewTabs,revisionSummary,dueLabel} from './revision-view.js';
import {notation,verifiedText,questionContent,questionPreview,optionContent,questionAnswer} from './question-content.js';
import {esc,head,link,button,empty,metric,formatDate} from './ui.js';
import {answered} from './scoring.js';
import {completedDays,questionStats,localDay,streak,xp,level,achievements} from './domain.js';
import {clock} from './timer.js';
const unavailable='<div class="notice warning">Questions without verified keys are saved without a grade. A total score is available only when every question in a session has a verified key.</div>';
export function daily(s,a,day){
 const done=completedDays(s),sets=day?a.sets.filter(x=>x.day===Number(day)):a.sets;
 return head(day?'Day '+esc(day):'Daily practice',day?'Ten questions. One focused session.':`${a.sets.length} available sets in your 118-day journey.`)+(sets.some(set=>set.questions.some(q=>q.answer===undefined))?unavailable:'')+`<div class="${day?'stack':'grid3'}">`+sets.map(set=>{const draft=Object.values(s.drafts).find(d=>d.origin==='daily'&&d.configuration.day===set.day);const previous=s.sessions.filter(x=>x.origin==='daily'&&x.configuration.day===set.day);return `<section class="panel set-card"><div class="section-head"><span class="eyebrow">Day ${String(set.day).padStart(2,'0')}</span><span class="pill">${done.has(set.day)?'Completed':draft?'In progress':'Available'}</span></div><h2>${set.year} · ${esc(set.paper)}</h2><p>General Aptitude</p><div class="caption">10 questions · 15 marks · ${previous.length} submitted sessions</div><div class="actions">${draft?link('Continue practice','#/quiz/'+draft.id,'button primary'):button(done.has(set.day)?'Practice again':'Start practice','start-day',set.day,'primary')}${!day?link('View set','#/day/'+set.day,'text-link'):''}</div>${day?`<p class="caption">Completion means submitting responses to all 10 questions. A partial submission remains in history without completing the day.</p><div>${set.questions.map(q=>questionRow({...q,day:set.day},s)).join('')}</div>${previous.length?'<h3>Previous sessions</h3>'+previous.map(x=>sessionRow(x)).join(''):''}`:''}</section>`}).join('')+'</div>'+(sets.length?'':empty('Set unavailable','This day has no source dataset yet.',link('Available sets','#/daily')));
}
export function questionRow(q,s){return `<article class="question-row"><div class="question-meta"><span class="pill">${q.year} · ${esc(q.paper)}</span><span>${q.day?'Day '+q.day:q.section||q.subject} · </span><span>${q.marks} ${q.marks===1?'mark':'marks'}</span>${s.bookmarks[q.id]?'<span>☆ '+esc(s.bookmarks[q.id])+'</span>':''}</div>${questionPreview(q)}<div class="actions">${link('Open question →','#/question/'+q.id,'text-link')}<span class="caption">${revisionState(s,q.id).label}</span></div></article>`;}
export function bank(s,a,query){const search=query.get('q')||'',year=query.get('year')||'',paper=query.get('paper')||'',status=query.get('status')||'',page=Math.max(1,Number(query.get('page'))||1);const normalized=search.normalize('NFKC').toLowerCase().trim();
 const availableYears=[...new Set(a.questions.map(q=>q.year).filter(Boolean))].sort((x,y)=>y-x);
 const list=a.questions.filter(q=>(!year||q.year===Number(year))&&(!paper||q.paper===paper)&&(!normalized||(q.search+' '+(s.notes[q.id]||'').normalize('NFKC').toLowerCase()).includes(normalized))&&(!status||status==='saved'&&s.bookmarks[q.id]||status==='new'&&!questionStats(s,q.id).attempts.length||status==='attempted'&&questionStats(s,q.id).attempts.length));
 const pageCount=Math.max(1,Math.ceil(list.length/12)),current=Math.min(page,pageCount);const pageLink=n=>{const p=new URLSearchParams(query);p.set('page',n);return '#/bank?'+p;};
 return head('The PYQ bank','Search your source papers. Save the questions you want to return to.')+`<form id="bank-form" class="filters"><label class="search">Search questions or personal notes<input name="q" placeholder="A word, phrase, or personal note…" value="${esc(search)}"></label><label>Year<select name="year"><option value="">All years</option>${availableYears.map(y=>`<option value="${y}" ${year==y?'selected':''}>${y}</option>`).join('')}</select></label><label>Paper<select name="paper"><option value="">All papers</option>${[...new Set(a.questions.map(q=>q.paper))].map(p=>`<option ${p===paper?'selected':''}>${p}</option>`).join('')}</select></label><label>Status<select name="status">${[['','All questions'],['new','Unattempted'],['attempted','Attempted'],['saved','Bookmarked']].map(([v,l])=>`<option value="${v}" ${status===v?'selected':''}>${l}</option>`).join('')}</select></label><button class="primary">Search</button></form><div class="section-head"><span class="caption">${list.length} question records · Source-verified question text</span><span class="caption">${[...new Set(list.map(q=>q.subject||'General Aptitude'))].map(esc).join(' · ')}</span></div><div class="question-list">${list.slice((current-1)*12,current*12).map(q=>questionRow(q,s)).join('')||empty('No matching questions','Try another phrase or reset a filter.')}</div><div class="pagination">${current>1?link('← Previous',pageLink(current-1)):''}<span class="caption">Page ${current} of ${pageCount}</span>${current<pageCount?link('Next →',pageLink(current+1)):''}</div>`;
}
export const sourceQuestion=questionContent;
export function questionDetail(s,a,id){const q=a.byId.get(id);if(!q)return head('Question not found')+link('Open the bank','#/bank');const stats=questionStats(s,id);const isAe=q.paper==='AE'||q.id?.includes('-ae-');const isVerified=a.verification?.[id]?.status==='verified';const verifyBadge=isAe?`<span class="pill ${isVerified?'primary':''}" style="margin-left:8px; vertical-align:middle;">${isVerified?'✓ Verified':'Unverified'}</span>`:'';const verifiedDate=isAe&&isVerified&&a.verification?.[id]?.verifiedAt?`<span class="caption" style="margin-left:8px;">Verified on ${esc(a.verification[id].verifiedAt)}</span>`:'';return head(`${q.year} ${esc(q.paper)} · Question ${q.number}`,esc(q.subject||'General Aptitude')+' · '+q.marks+(q.marks===1?' mark':' marks'))+`<div class="detail">${revisionSummary(s,id)}<div class="actions">${button('Practice question','practice-one',id,'primary')}${verifyBadge}${button(s.bookmarks[id]?'☆ '+esc(s.bookmarks[id]):'☆ Bookmark','bookmark',id)}${button('Add to notebook','add-notebook',id)}${button('Create flashcard','new-card',id)}${button('Share','share',id)}${button('Report source issue','report',id)}${verifiedDate}</div>${sourceQuestion(q)}<p class="source-note">Original source: ${q.year} ${esc(q.paper)} · Question ${q.number}</p><section class="panel" style="margin-top:24px"><h2>My note</h2><p class="caption">Personal notes are separate from source material.</p><form id="note-form" data-id="${id}"><label class="sr-only" for="note">My note</label><textarea id="note" name="note" maxlength="20000" placeholder="What would help you approach this question again?">${esc(s.notes[id]||'')}</textarea><button class="primary">Save note</button></form></section><section class="panel" style="margin-top:24px"><h2>Answer & solution</h2><p>${q.gradingRule==='marks-to-all'?'Official ruling: marks to all. No option is designated correct.':q.answer!==undefined?'Answer: '+esc(questionAnswer(q)):'No verified answer key in the supplied source.'}</p>${q.answerSource?`<p class="caption">${link('Official '+esc(q.paper)+' answer key',q.answerSource.url,'text-link')} · ${esc(q.answerSource.section||'GA')}  · ${esc(q.type)} · ${q.marks} ${q.marks===1?'mark':'marks'}</p>`:''}<p class="prose">${q.solution?notation(q.solution):'No source solution available.'}</p>${q.solutionStatus?'<p class="caption">Editorial solution, checked against the source question. The linked official key supplies the answer.</p>':''}</section><section class="panel" style="margin-top:24px"><h2>Question history</h2><p class="caption">${revisionState(s,id).label} · ${stats.attempts.length} answered attempts · ${clock(stats.totalTime)} total answering time</p>${stats.attempts.length?stats.attempts.slice().reverse().map(x=>`<div class="row"><span>${formatDate(x.timestamp)} · Response ${esc(x.selectedAnswer)}</span><span class="pill">${x.correctness}</span></div>`).join(''):empty('No attempts yet','Practice this question to begin its history.')}</section></div>`;}
export function quiz(s,a,d,timer){
 if(d.origin==='paper'&&d.mode==='test') return renderExamMode(s,a,d,timer);
 const q=a.byId.get(d.questionIds[d.index]),count=d.questionIds.filter(id=>answered(d.answers[id])).length,isTest=d.mode==='test',last=d.index===d.questionIds.length-1;
 const selected=value=>q.type==='MSQ'?(d.answers[q.id]||[]).includes(value):d.answers[q.id]===value;
 const choices=!verifiedText(q)?'<p class="caption">Answer controls are unavailable until this content has been verified.</p>':q.type==='NAT'?`<input type="number" step="any" id="nat-answer" aria-label="Numeric answer" placeholder="Enter your answer" value="${esc(d.answers[q.id]??'')}">`:q.options.map(({label:v})=>`<button class="option ${selected(v)?'selected':''}" data-action="answer" data-value="${v}" aria-pressed="${selected(v)}" ><span class="option-letter"><span class="sr-only">Option </span>${v}</span>${optionContent(q,q.options.find(o=>o.label===v))}<span class="option-state" aria-hidden="true">${selected(v)?'Selected':''}</span><span class="option-indicator" aria-hidden="true">${selected(v)?'✓':''}</span></button>`).join('');
 const penalty=q.negativeMarks??q.marks/3;
 return `<div class="solve-experience"><header class="solve-header"><div><p class="solve-mode">${isTest?'Timed test':d.origin==='revision'?'Review session':'Practice session'} <span>· ${esc(q.subject||'General Aptitude')}</span></p><div class="solve-position"><h1 id="solve-title" tabindex="-1">Question ${String(d.index+1).padStart(2,'0')}</h1><span>of ${d.questionIds.length}</span></div></div><div class="solve-header-actions">${button(s.settings.focus?'Exit focus':'Focus mode','focus','','quiet')}<progress class="session-progress" value="${d.index+1}" max="${d.questionIds.length}" aria-label="Question position"></progress></div></header>
 <div class="quiz-grid"><article class="question-surface" aria-labelledby="solve-title"><div class="question-heading"><div><span class="source-label">${verifiedText(q)?'Source-verified question':'Content unavailable'}</span><span class="source-context">${q.year} ${esc(q.paper)} <span>· Question ${q.number}</span></span>${(q.paper==='AE'||q.id?.includes('-ae-')) ? `<span class="pill ${a.verification?.[q.id]?.status==='verified'?'primary':''}" style="margin-left:12px; font-size:12px; vertical-align:middle;">${a.verification?.[q.id]?.status==='verified'?'✓ Verified':'Unverified'}</span>` : ''}</div><div class="marking"><strong>${q.marks} ${q.marks===1?'mark':'marks'}</strong><span>${q.gradingRule==='marks-to-all'?'Official ruling: marks to all':penalty===0?'No negative marking':'−'+Number(penalty.toFixed(2))+' for an incorrect answer'}</span></div></div><div class="question-document">${sourceQuestion(q,true)}</div>
 <section class="response-section" aria-labelledby="response-title"><div class="section-head"><h2 id="response-title">Your answer</h2><span class="caption">${q.type==='NAT'?'Enter a number':q.type==='MSQ'?'Select all that apply':'Choose one option'}</span></div><fieldset class="answer-panel"><legend class="sr-only">Select your answer</legend>${choices}</fieldset><div class="solve-actions"><button class="quiet" data-action="previous" ${d.index===0?'disabled':''}>← Previous</button>${last?button('Submit session','submit','','primary'):button('Continue →','next','','primary')}</div><p class="answer-save-note">Responses save automatically.${q.answer===undefined?' Without an answer key, the response is recorded as ungraded.':''}</p><div class="solve-tools" aria-label="Question tools">${button('Clear','clear','','quiet')}${button(d.review[q.id]?'Unmark review':'Mark for review','review-question','','quiet')}${button(s.bookmarks[q.id]?'Saved question':'Save question','quick-bookmark',q.id,'quiet')}</div></section></article>
 <aside class="quiz-aside quiz-support" aria-label="Session support"><div class="status-summary"><strong><span id="answered-count">${count}</span> / ${d.questionIds.length}</strong><span>answered</span></div><div class="timing" data-mode="${isTest?'test':'practice'}"><div><span>${isTest?'Time remaining':'Session time'}</span><strong id="session-time">${clock(isTest?timer.remaining():d.elapsed)}</strong></div><div><span>Current question</span><strong id="question-time">${clock(d.times[q.id]||0)}</strong></div><small>Current visit <span id="visit-time">${clock(timer.visit)}</span></small></div><div id="checkpoint" role="status" aria-live="polite"></div><details class="question-navigation"><summary>Question navigation</summary><div class="palette">${d.questionIds.map((id,i)=>`<button class="${i===d.index?'current ':''}${answered(d.answers[id])?'answered ':''}${d.review[id]?'review':''}" data-action="jump" data-value="${i}" aria-label="Question ${i+1}, ${answered(d.answers[id])?'answered':d.visited[id]?'visited':'unvisited'}${d.review[id]?', marked for review':''}" ${i===d.index?'aria-current="step"':''}>${i+1}</button>`).join('')}</div><p class="caption">Filled: answered · underline: review</p></details><p class="keyboard">${q.type==='NAT'?'':'1–'+q.options.length+' Answer · '}← → Navigate<br>R Review · C Clear · S Submit</p></aside></div></div>`;
}
const answerText=value=>answered(value)?Array.isArray(value)?value.join(', '):String(value):'No answer';
export function attemptFeedback(attempt,question){
 if(attempt.correctness==='awarded')return {status:'Marks awarded',message:'The official key awards full marks to everyone for this question, including unanswered responses.',selectedAnswer:answerText(attempt.selectedAnswer),correctAnswer:'MTA — marks to all',nextAction:{label:'Read the official ruling',href:'#/question/'+attempt.questionId}};
 const selectedAnswer=answerText(attempt.selectedAnswer),correctAnswer=question?.answer===undefined?null:questionAnswer(question);
 const status=attempt.correctness==='correct'?'Correct':attempt.correctness==='incorrect'?'Incorrect':attempt.correctness==='blank'?'Not answered':'Not graded';
 const message=attempt.correctness==='correct'?'Your selected answer is correct.':attempt.correctness==='incorrect'?'Your selected answer is incorrect.':attempt.correctness==='blank'?'No answer was selected.':question?.answer!==undefined?'This response was saved without a grade. A verified key is now available; the original result is unchanged.':'The answer key is unavailable, so this response was saved without a grade.';
 const nextAction=attempt.correctness==='incorrect'||attempt.correctness==='blank'?{label:'Try this question again',href:'#/question/'+attempt.questionId}:attempt.correctness==='correct'?{label:'Continue practice',href:'#/home'}:{label:'Review your response',href:'#/question/'+attempt.questionId};
 return {status,message,selectedAnswer,correctAnswer,nextAction};
}
export function result(s,a,id){
 const r=s.sessions.find(x=>x.id===id);if(!r)return head('Session not found')+link('Back to history','#/history');
 const z=r.result,events=s.attempts.filter(x=>x.sessionId===id),rows=r.questionIds.map(questionId=>events.find(x=>x.questionId===questionId)).filter(Boolean);
 const feedback=rows.map((attempt,index)=>{const question=a.byId.get(attempt.questionId),item=attemptFeedback(attempt,question),mark=attempt.correctness==='correct'?'✓':attempt.correctness==='incorrect'?'×':attempt.correctness==='blank'?'—':'i';return `<article class="feedback-row" data-result="${attempt.correctness}" tabindex="-1"><div class="feedback-copy"><span class="feedback-mark" aria-hidden="true">${mark}</span><div><strong>Question ${index+1}: ${item.status}</strong><p>${item.message}</p><span class="caption">Selected: ${esc(item.selectedAnswer)}${item.correctAnswer===null?' · Correct answer unavailable':(question?.gradingRule==='marks-to-all'?' · Official ruling: ':' · Correct answer: ')+esc(item.correctAnswer)} · ${clock(attempt.timeSpent)}</span></div></div>${attempt.correctness==='incorrect'?button('Try this question again','review-one',attempt.questionId,'quiet'):link(item.nextAction.label,item.nextAction.href,'text-link')}${attempt.correctness==='correct'&&revisionState(s,attempt.questionId).learningState==='recovered'&&revisionState(s,attempt.questionId).lastAttempt?.attemptId===attempt.attemptId?'<p class="revision-result-context">Recovered · '+dueLabel(revisionState(s,attempt.questionId))+'</p>':''}${question?.solution?`<details class="feedback-solution"><summary>View question &amp; solution</summary>${questionContent(question)}<h3>Editorial solution</h3><p class="prose">${notation(question.solution)}</p><p class="caption">Checked against the source question. ${question.answerSource?link('Official answer key',question.answerSource.url,'text-link'):''}</p></details>`:''}</article>`;}).join('');
 return `<div role="status" aria-live="polite" tabindex="-1">${head('Session recorded.',`${r.origin==='daily'?'Day '+r.configuration.day:'Practice'} · ${formatDate(r.endedAt)}`,link('Back to Home','#/home'))}</div>`+(z.score===null?unavailable:'')+`<div class="metrics">${metric(z.answered+' / '+r.questionIds.length,'Answered')}${metric(z.score===null?'—':z.score.toFixed(2)+' / '+z.maxMarks,'Score')}${metric(z.accuracy===null?'—':z.accuracy.toFixed(0)+'%','Graded accuracy')}${metric(clock(r.elapsed),'Session time')}</div><div class="grid2" style="margin:24px 0"><section class="panel"><h2>Your practice summary</h2><div class="row"><span>Correct / incorrect</span><strong>${z.correct} / ${z.incorrect}</strong></div><div class="row"><span>Unattempted / ungraded</span><strong>${r.questionIds.length-z.answered} / ${z.ungraded}</strong></div>${z.awarded?`<div class="row"><span>Marks-to-all questions</span><strong>${z.awarded}</strong></div>`:''}<div class="row"><span>Average time per question</span><strong>${clock(r.elapsed/r.questionIds.length)}</strong></div></section><section class="panel"><h2>Next step</h2><p style="margin:14px 0">${z.incorrect?`${z.incorrect} incorrect responses are ready for another attempt.`:z.ungraded?'Review any response you want to revisit while the source question is fresh.':'Continue when you are ready.'}</p><div class="actions">${button('Retry session','retry',id,'primary')}${z.incorrect?button('Retry incorrect','retry-wrong',id):''}${link('Open review library','#/review')}</div></section></div><section class="panel"><h2>Answer feedback</h2><div class="feedback-list">${feedback}</div></section>`;
}
export function sessionRow(x){return `<a href="#/result/${x.id}" class="row"><div><strong class="row-title">${x.origin==='daily'?'Day '+x.configuration.day:esc(x.origin)+' session'}</strong><small>${formatDate(x.endedAt)} · ${x.result.answered}/${x.questionIds.length} answered · ${clock(x.elapsed)}</small></div><span class="pill">${x.result.score===null?'Ungraded':x.result.score.toFixed(2)+' marks'} →</span></a>`;}
export const history=(s)=>head('Session history','Every submitted session, with its original answers and timing.')+`<section class="panel">${s.sessions.length?s.sessions.slice().reverse().map(sessionRow).join(''):empty('No history yet','Finish a daily set or custom session to start your practice record.',link('Start daily practice','#/daily','button primary'))}</section>`;
export function practice(s,a){const availableYears=[...new Set(a.questions.map(q=>q.year).filter(Boolean))].sort((x,y)=>y-x);return head('Make this session yours.','Choose a source, set your time, and start solving.')+`<div class="grid2"><section class="panel"><h2>Build a session</h2><form id="practice-form" class="form-grid" style="margin-top:20px"><label>Question source<select name="source"><option value="all">All available questions</option><option value="unattempted">Unattempted</option><option value="incorrect">Unresolved mistakes</option><option value="bookmarked">Bookmarked</option><option value="notebook">Notebook</option></select></label><label>Notebook<select name="notebook"><option value="">Choose a notebook</option>${s.notebooks.map(n=>`<option value="${n.id}">${esc(n.name)}</option>`).join('')}</select></label><label>Year<select name="year"><option value="">All years</option>${availableYears.map(y=>`<option value="${y}">${y}</option>`).join('')}</select></label><label>Paper<select name="paper"><option value="">All papers</option>${[...new Set(a.questions.map(q=>q.paper))].map(p=>`<option>${p}</option>`).join('')}</select></label><label>Question count<input name="count" type="number" value="10" min="1" max="160" required></label><label>Mode<select name="mode"><option value="practice" ${s.settings.preferredMode==='practice'?'selected':''}>Unlimited practice</option><option value="test" ${s.settings.preferredMode==='test'?'selected':''}>Timed test</option></select></label><label>Session study time (minutes)<input name="minutes" type="number" value="30" min="1" max="360" required></label><label>Blueprint name (optional)<input name="name" maxlength="80" placeholder="My morning practice"></label><p class="caption wide">Practice counts up without a limit. Timed tests count down and submit at expiry, including time away. Fewer matching questions means a shorter question queue.</p><div class="actions wide"><button class="primary" name="intent" value="start">Build & start</button><button name="intent" value="save">Save blueprint</button></div></form></section><div class="stack"><section class="panel"><h2>A session for the time you have</h2><p style="margin:12px 0">Prioritize unresolved mistakes, must-revise bookmarks, then unattempted questions.</p><div class="actions">${[10,30,60].map(n=>button(n+' minutes','time-session',n)).join('')}</div><p class="source-note">Estimated at 2 minutes per question. This is an unlimited practice queue, not a time limit.</p></section><section class="panel"><h2>Saved blueprints</h2>${s.blueprints.length?s.blueprints.map(b=>`<div class="row"><div><strong>${esc(b.name)}</strong><small>${b.count} questions · ${b.mode}</small></div><div class="actions">${button('Start','blueprint',b.id,'small')}${button('Delete','delete-blueprint',b.id,'quiet small')}</div></div>`).join(''):empty('No saved blueprints','Save a session configuration to use it again.')}</section><section class="panel"><h2>Question of the day</h2><p class="caption" style="margin:12px 0">One source question, selected by calendar date.</p>${button('Solve one question','question-day','','primary')}</section></div></div>`;}
export function review(s,a,tab='due',query=new URLSearchParams()){
 if(['due','mistakes','recovered','all'].includes(tab))return revisionLibrary(s,a,tab,query);
 let content='';
 if(tab==='bookmarks'){const qs=a.questions.filter(q=>s.bookmarks[q.id]);content=(qs.length?button('Practice saved questions','practice-ids',qs.map(q=>q.id).join(','),'primary'):'')+qs.map(q=>questionRow(q,s)).join('')||empty('No bookmarks yet','Save questions from a quiz or the PYQ bank.');}
 else if(tab==='notes'){const qs=a.questions.filter(q=>s.notes[q.id]);content=qs.map(q=>`<section class="panel"><h3>${q.year} ${q.paper} · </h3><p class="prose">${esc(s.notes[q.id])}</p>${link('Edit note','#/question/'+q.id,'text-link')}</section>`).join('')||empty('No personal notes yet','Open a question to capture your reasoning or a reminder.');}
 else {content=button('Create notebook','new-notebook','','primary')+`<div class="grid2" style="margin-top:20px">`+s.notebooks.map(n=>{const qs=n.questionIds.filter(id=>a.byId.has(id));const seen=qs.filter(id=>questionStats(s,id).attempts.length).length;return `<section class="panel"><h2>${esc(n.name)}</h2><p class="caption">${qs.length} questions · ${seen} attempted · Updated ${formatDate(n.updatedAt)}</p><progress value="${seen}" max="${Math.max(1,qs.length)}" aria-label="Notebook coverage"></progress><div class="actions">${qs.length?button('Practice all','notebook-practice',n.id+'|all')+button('Unattempted','notebook-practice',n.id+'|new')+button('Mistakes','notebook-practice',n.id+'|wrong'):''}${button('Rename','rename-notebook',n.id,'small')}${button('Delete','delete-notebook',n.id,'quiet small')}</div>${qs.map(id=>`<div class="row">${link(esc(a.byId.get(id).paper)+' Q'+a.byId.get(id).number,'#/question/'+id,'text-link')}${button('Remove','remove-notebook-question',n.id+'|'+id,'quiet small')}</div>`).join('')}</section>`}).join('')+'</div>'+(s.notebooks.length?'':empty('Your own question collections','Create a notebook, then add questions from their detail pages.'));}
 return head('Your review library','Keep useful questions and your own reasoning close.')+`${reviewTabs(tab)}<div class="stack">${content}</div>`;
}
export function flashcards(s,revealed){const due=s.flashcards.filter(c=>c.due<=Date.now());const card=due[0];return head('Keep it fresh.',`${due.length} due · ${s.flashcards.length} personal flashcards`,button('Create flashcard','new-card'))+`<div class="grid2"><section class="panel flash">${card?`<span class="eyebrow">${revealed?'Your answer':'Recall before you reveal'}</span><p>${esc(revealed?card.back:card.front)}</p>${revealed?`<div class="actions" style="justify-content:center">${['Again','Hard','Good','Easy'].map(r=>button(r,'rate-card',card.id+'|'+r)).join('')}</div>`:button('Reveal answer','reveal-card','','primary')}<span class="caption" style="margin-top:18px">${card.reviewCount||0} reviews</span>`:empty(s.flashcards.length?'You’re up to date.':'Your revision starts here.','Create a card from a question or write your own prompt and answer.')}</section><section class="panel"><h2>Your cards</h2>${s.flashcards.map(c=>`<div class="row"><div><strong class="row-title">${esc(c.front.slice(0,90))}</strong><small>Due ${formatDate(c.due)} · ${c.reviewCount||0} reviews · ${c.reviewCount?Math.round(100*c.successes/c.reviewCount)+'% recall':'Not reviewed'}</small></div>${button('Delete','delete-card',c.id,'quiet small')}</div>`).join('')||'<p class="caption">No cards created yet.</p>'}<p class="source-note">Again: 10 minutes. Hard: 1 day. Good: at least 2 days, doubling. Easy: at least 4 days, tripling. Recall is self-rated.</p></section></div><section class="panel" style="margin-top:24px"><h2>Quick revision & formula library</h2><p style="margin:12px 0">No source revision material is available. Your own flashcards and notes can be used for revision.</p>${link('Open personal notes','#/review/notes','text-link')}</section>`;}
export function analytics(s,a){const attempts=s.attempts.filter(x=>answered(x.selectedAnswer));const groups=new Map();for(const x of attempts){if(!groups.has(x.questionId))groups.set(x.questionId,[]);groups.get(x.questionId).push(x);}const first=[...groups.values()].map(x=>x[0]),latest=[...groups.values()].map(x=>x.at(-1));const accuracy=list=>{const known=list.filter(x=>['correct','incorrect'].includes(x.correctness));return known.length?Math.round(100*known.filter(x=>x.correctness==='correct').length/known.length)+'%':'—';};const recovered=a.questions.filter(q=>questionStats(s,q.id).recovered).length;const st=streak(s.attempts);const total=s.sessions.reduce((v,x)=>v+x.elapsed,0);const daily=new Map();for(const x of attempts)daily.set(x.localDate,(daily.get(x.localDate)||0)+1);const recent=[...daily].sort().slice(-14);const maximum=Math.max(1,...recent.map(x=>x[1]));const today=new Date(),cutoff=days=>{const d=new Date(today);d.setDate(d.getDate()-days);return localDay(d);};const weekly=attempts.filter(x=>x.localDate>=cutoff(6)),monthly=attempts.filter(x=>x.localDate>=cutoff(29));
 const availableYears=[...new Set(a.questions.map(q=>q.year).filter(Boolean))].sort((x,y)=>y-x);
 return head('Know your practice.','Descriptive progress from your own activity. No predicted scores or ranks.')+`<div class="metrics">${metric(groups.size+' / '+a.questions.length,'Question coverage')}${metric(attempts.length,'Answered attempts')}${metric(accuracy(first),'First-attempt accuracy')}${metric(accuracy(latest),'Latest accuracy')}</div><div class="grid2" style="margin-top:24px"><section class="panel"><h2>Questions answered by day</h2>${recent.length?recent.map(([d,n])=>`<div class="chart-row"><span>${formatDate(d+'T12:00:00')}</span><div><i style="width:${100*n/maximum}%"></i></div><strong>${n}</strong></div>`).join(''):empty('No activity yet','Submit your first session to begin tracking real practice.')}</section><section class="panel"><h2>Consistency & effort</h2><div class="row"><span>Current / longest streak</span><strong>${st.current} / ${st.longest} days</strong></div><div class="row"><span>Study time</span><strong>${clock(total)}</strong></div><div class="row"><span>Recovered mistakes</span><strong>${recovered}</strong></div><div class="row"><span>Practice XP / level</span><strong>${xp(s)} / ${level(xp(s))}</strong></div><p class="caption">XP rewards participation, not performance. Correctness requires a verified answer key.</p></section><section class="panel"><h2>Coverage by year</h2>${availableYears.map(year=>{const qs=a.questions.filter(q=>q.year===year),ids=new Set(qs.map(q=>q.id));return `<div class="row"><span>${year}</span><strong>${[...groups.keys()].filter(id=>ids.has(id)).length} / ${qs.length}</strong></div>`}).join('')}<p class="source-note">Descriptive question coverage across historical source papers. Topic, chapter, and difficulty analysis are unavailable because these labels are absent from the sources.</p></section><section class="panel"><h2>Weekly & monthly review</h2><div class="row"><span>Last 7 days</span><strong>${weekly.length} answers · ${accuracy(weekly)}</strong></div><div class="row"><span>Last 30 days</span><strong>${monthly.length} answers · ${new Set(monthly.map(x=>x.localDate)).size} active days</strong></div><div class="row"><span>Most answers in a day</span><strong>${Math.max(0,...daily.values())}</strong></div><div class="row"><span>Longest session</span><strong>${clock(Math.max(0,...s.sessions.map(x=>x.elapsed)))}</strong></div></section><section class="panel"><h2>Achievements earned</h2><div class="badge-list" style="margin-top:16px">${achievements(s).map(x=>`<span>${x}</span>`).join('')||'<p class="caption">Your first submitted answer earns First PYQ.</p>'}</div></section><section class="panel"><h2>Historical comparison</h2><p style="margin-top:12px">${first.some(x=>x.result==='correct'||x.result==='incorrect')?'Compare first-attempt and latest accuracy above. Period comparisons require at least five graded attempts in each period.':'Accuracy trends need graded attempts. None are available from the current source papers.'}</p></section></div>`;
}
export function planner(s,a){let left=null;if(s.planner.date){left=Math.ceil((Date.parse(s.planner.date+'T00:00:00')-new Date(new Date().getFullYear(),new Date().getMonth(),new Date().getDate()).getTime())/86400000);}const remaining=a.questions.filter(q=>!questionStats(s,q.id).attempts.length).length;const phase=left===null?'Set your exam date':left<0?'Exam date has passed':left<=7?'Final revision':left<=21?'Revision':left<=45?'Mixed practice':left<=90?'Strengthening':'Foundation & coverage';return head('Plan around your real life.','Calendar days until your exam and minutes for today’s session are separate.')+`<div class="grid2"><section class="panel"><h2>Your preparation plan</h2><form id="planner-form" class="form-grid" style="margin-top:20px"><label>Target exam<input name="exam" value="${esc(s.planner.exam)}" maxlength="80" required></label><label>Exam date<input type="date" name="date" value="${esc(s.planner.date)}"></label><label>Daily question goal<input name="goal" type="number" min="1" max="160" value="${s.settings.goal}" required></label><label>Daily study minutes<input name="minutes" type="number" min="1" max="600" value="${s.planner.minutes}" required></label><button class="primary">Save plan</button></form></section><section class="panel"><span class="eyebrow">Calendar time</span><div class="goal-number">${left===null?'—':Math.max(0,left)} <small>days remaining</small></div><h2>${phase}</h2><p style="margin-top:12px">${remaining} of ${a.questions.length} available question records are unattempted.</p><p class="source-note">Phases use days remaining: over 90 foundation, 46–90 strengthening, 22–45 mixed practice, 8–21 revision, 0–7 final revision.</p></section><section class="panel"><h2>Coverage scenarios</h2><p class="caption">Based only on the ${remaining} unattempted records in your available archive.</p>${[['Minimum',.25],['Balanced',.5],['Full',1]].map(([label,part])=>{const count=Math.ceil(remaining*part),days=Math.ceil(count/s.settings.goal);return `<div class="row"><div><strong>${label}</strong><small>${count} questions · ${days} study days at your goal</small></div><span class="pill">${left===null?'No date set':days<=Math.max(0,left)?'Fits current goal':'Beyond current goal'}</span></div>`}).join('')}<p class="source-note">These are archive coverage fractions, not curriculum completeness or outcome predictions. Missed activity stays in history; no automatic catch-up workload is added.</p></section><section class="panel"><h2>What fits today?</h2><p style="margin:15px 0">${s.planner.minutes} minutes of study time ≈ ${Math.min(a.questions.length,Math.floor(s.planner.minutes/2)||1)} questions at an estimated 2 minutes each.</p>${button('Build today’s practice','time-session',s.planner.minutes,'primary')}<p class="source-note">Priority order: unresolved mistakes, must-revise bookmarks, unattempted questions. Topic priorities need verified topic metadata.</p></section></div>`;}
export function settings(s,offlineReady,installable){return head('Your workspace, your way.','Preferences and progress are stored in this browser.')+`<div class="grid2"><section class="panel"><h2>Practice preferences</h2><form id="settings-form" class="form-grid" style="margin-top:20px"><label>Your name<input name="name" value="${esc(s.profile.name)}" maxlength="60"></label><label>Theme<select name="theme"><option value="light" ${s.settings.theme==='light'?'selected':''}>Light</option><option value="dark" ${s.settings.theme==='dark'?'selected':''}>Dark</option></select></label><label>Daily question goal<input name="goal" type="number" min="1" max="160" value="${s.settings.goal}" required></label><label>Preferred mode<select name="preferredMode"><option value="practice" ${s.settings.preferredMode==='practice'?'selected':''}>Unlimited practice</option><option value="test" ${s.settings.preferredMode==='test'?'selected':''}>Timed test</option></select></label><label>Checkpoint volume<select name="volume">${[[.025,'Low'],[.04,'Medium'],[.08,'High']].map(([v,l])=>`<option value="${v}" ${s.settings.volume===v?'selected':''}>${l}</option>`).join('')}</select></label>${[['sound','Sound'],['checkpointSound','Checkpoint sound'],['checkpoint','2-minute checkpoint'],['shortcuts','Keyboard shortcuts']].map(([v,l])=>`<label class="check-label"><input name="${v}" type="checkbox" ${s.settings[v]?'checked':''}>${l}</label>`).join('')}<button class="primary wide">Save preferences</button></form></section><div class="stack"><section class="panel"><h2>Your data</h2><p style="margin:12px 0">Export a backup before moving browsers or resetting progress. No cloud sync is connected.</p><div class="actions">${button('Export progress','export')}${button('Import backup','import')}</div><input id="import-file" type="file" accept=".json,application/json" hidden><p class="source-note">Import validates the backup and asks before replacing current data. Existing progress is exported first.</p></section><section class="panel"><h2>Offline workspace</h2><p style="margin:12px 0">${offlineReady?'App shell, question datasets, and source crops are saved for offline practice.':'Preparing offline availability. Keep this page open while question assets are cached.'}</p>${installable?button('Install workspace','install'):'<p class="caption">Installation is available through your browser when supported.</p>'}<p class="source-note">Source PDFs are retained internally. Browser storage can be cleared by the browser.</p></section><section class="panel"><h2>Reset controls</h2><div class="actions" style="margin:15px 0">${button('Reset quiz progress','reset','progress')}${button('Reset XP','reset','xp')}${button('Reset everything','reset','all','danger')}</div><p class="caption">Every reset requires confirmation and downloads a backup first.</p></section></div></div>`;}


export function aerospace(s,a,id){
 const aeManifest=a.corpusManifest;
 if(!aeManifest)return head('Aerospace PYQs','Aerospace engineering previous year questions.')+'<p>Aerospace manifest not found.</p>';
 if(id){
  const paper=a.papers.find(p=>p.id===id||String(p.year)===id);
  if(!paper)return head('Paper not found')+link('Back to Aerospace PYQs','#/aerospace');
  const typeCounts=paper.questionTypeCounts||(paper.questions?paper.questions.reduce((acc,q)=>{acc[q.type]=(acc[q.type]||0)+1;return acc;},{}):{MCQ:29,MSQ:14,NAT:22});
  const verifiedCount=paper.questionOrder.filter(qId=>a.verification?.[qId]?.status==='verified').length;
  return head(`GATE Aerospace ${paper.year}`,`Complete paper · ${paper.totalQuestions} questions · ${paper.totalMarks} marks`)+
  `<div class="grid2"><section class="panel">
    <h2>Paper summary</h2>
    <div class="row"><span>Duration</span><strong>${paper.durationMinutes} minutes</strong></div>
    <div class="row"><span>Manual verification</span><strong>${verifiedCount} / ${paper.totalQuestions} verified</strong></div>
    <div class="row"><span>Question types</span><strong>${Object.entries(typeCounts).map(([k,v])=>`${k}: ${v}`).join(', ')}</strong></div>
    ${paper.sections.map(sec=>`<div class="row"><span>${esc(sec.title)}</span><strong>${sec.questionIds.length} questions, ${sec.totalMarks} marks</strong></div>`).join('')}
    <div class="actions" style="margin-top:20px;">
      ${button('Start PYQ','start-paper',paper.id,'primary')}
      ${button('Timed Test','time-paper',paper.id)}
    </div>
  </section>
  <section class="panel">
    <h2>Questions & Verification Status</h2>
    <p class="caption">Direct access to all ${paper.totalQuestions} questions. Open any question to review and verify.</p>
    <div style="max-height: 380px; overflow-y: auto; padding-right: 4px; display: flex; flex-direction: column; gap: 4px; margin-top: 12px;">
      ${paper.questionOrder.map(qId => {
        const item = a.byId.get(qId);
        if (!item) return '';
        const isV = a.verification?.[qId]?.status === 'verified';
        return `<div class="row" style="padding: 6px 0; border-bottom: 1px solid var(--border, #eee);">
          <span><strong></strong> · ${esc(item.section || 'AE')} · ${esc(item.type)} · ${item.marks}M</span>
          <span style="display:flex; align-items:center; gap:8px;">
            <span class="pill" style="${isV ? 'background: #2b669a; color: white;' : ''}">${isV ? '✓ Verified' : 'Unverified'}</span>
            ${link('Open', '#/question/' + item.id, 'button quiet small')}
          </span>
        </div>`;
      }).join('')}
    </div>
  </section></div>`;
 }
 const yearsList=aeManifest.years.slice().reverse().map(yearInfo=>{
  const isAvailable=yearInfo.ingestionStatus==='complete';
  const paper=a.papers.find(p=>p.year===yearInfo.year);
  const verifiedCount=paper?paper.questionOrder.filter(qId=>a.verification?.[qId]?.status==='verified').length:0;
  const metadata=isAvailable?`<div class="caption">${yearInfo.questionCount} questions · ${yearInfo.totalMarks} marks<br><strong style="color:var(--text-accent, #2b669a);">${verifiedCount} / ${yearInfo.questionCount} verified</strong></div>`:`<div class="caption">Coming soon</div>`;
  const action=isAvailable?link('View Paper',`#/aerospace/${yearInfo.year}`,'button primary'):`<button class="ghost" disabled>Not available</button>`;
  return `<section class="panel set-card"><div class="section-head"><span class="eyebrow">GATE ${yearInfo.year}</span><span class="pill">${isAvailable?'Available':'Unavailable'}</span></div>
    <h2>${yearInfo.year} · ${esc(yearInfo.paper)}</h2>
    <p>Aerospace Engineering</p>
    ${metadata}
    <div class="actions">${action}</div>
    </section>`;
 }).join('');
 return head('Aerospace PYQs','Practice actual GATE Aerospace questions.')+`<div class="grid3">${yearsList}</div>`;
}


export function renderExamMode(s,a,d,timer) {
  if (d.showSubmitConfirm) {
    const answeredCount = d.questionIds.filter(id => (Array.isArray(d.answers[id]) ? d.answers[id].length > 0 : (d.answers[id] !== undefined && d.answers[id] !== ''))).length;
    const markedCount = d.questionIds.filter(id => d.review[id]).length;
    const notVisitedCount = d.questionIds.filter(id => !d.visited[id]).length;
    const notAnsweredCount = d.questionIds.length - notVisitedCount - answeredCount;
    return `
      <div style="padding: 40px; max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 100px; border-top: 4px solid #2b669a;">
        <h2 style="margin-bottom: 20px; font-family: Arial, sans-serif; text-align: center;">Exam Summary</h2>
        <table style="width: 100%; margin: 20px 0; text-align: center; border-collapse: collapse; font-family: Arial, sans-serif;">
          <tr style="border-bottom: 1px solid #ddd; background: #f9f9f9;"><th style="padding: 12px 8px; text-align: left;">Section Name</th><th style="padding: 12px 8px;">No. of Questions</th><th style="padding: 12px 8px;">Answered</th><th style="padding: 12px 8px;">Not Answered</th><th style="padding: 12px 8px;">Marked for Review</th><th style="padding: 12px 8px;">Not Visited</th></tr>
          <tr style="border-bottom: 1px solid #ddd;"><td style="padding: 12px 8px; text-align: left;">AE Aerospace Engineering</td><td style="padding: 12px 8px;">${d.questionIds.length}</td><td style="padding: 12px 8px;">${answeredCount}</td><td style="padding: 12px 8px;">${notAnsweredCount}</td><td style="padding: 12px 8px;">${markedCount}</td><td style="padding: 12px 8px;">${notVisitedCount}</td></tr>
        </table>
        <p style="font-family: Arial, sans-serif; margin-bottom: 20px; text-align: center;">Are you sure you want to submit the exam?</p>
        <div style="display:flex; justify-content: center; gap: 16px; margin-top: 30px;">
          <button data-action="exam-submit-final" style="background: #5bc0de; color: white; border: none; padding: 10px 40px; font-weight: bold; border-radius: 4px; cursor: pointer;">Yes</button>
          <button data-action="exam-submit-cancel" style="background: #d9534f; color: white; border: none; padding: 10px 40px; font-weight: bold; border-radius: 4px; cursor: pointer;">No</button>
        </div>
      </div>
    `;
  }
  
  const q = a.byId.get(d.questionIds[d.index]);
  const sectionId = q.section || 'GA';
  
  const gaIds = [], aeIds = [];
  d.questionIds.forEach((id, i) => {
    const question = a.byId.get(id);
    if (question.section === 'GA') gaIds.push({id, index: i, number: question.number});
    else aeIds.push({id, index: i, number: question.number});
  });

  const visibleIds = sectionId === 'GA' ? gaIds : aeIds;
  const isTest = true;
  const isAe = q.paper === 'AE' || q.id?.includes('-ae-');
  const isVerified = a.verification?.[q.id]?.status === 'verified';
  const selected = value => q.type==='MSQ'?(d.answers[q.id]||[]).includes(value):d.answers[q.id]===value;
  
  let choices = '';
  if (!verifiedText(q)) {
    choices = '<p class="caption">Content unavailable.</p>';
  } else if (q.type === 'NAT') {
    choices = `
      <div class="cbt-nat-container">
        <input type="text" class="cbt-nat-input" id="nat-answer" readonly value="${esc(d.answers[q.id]??'')}">
        <div class="cbt-nat-keypad">
          <button class="cbt-nat-btn wide" data-action="nat-key" data-value="Backspace">Backspace</button>
          <div class="cbt-nat-row"><button class="cbt-nat-btn" data-action="nat-key" data-value="7">7</button><button class="cbt-nat-btn" data-action="nat-key" data-value="8">8</button><button class="cbt-nat-btn" data-action="nat-key" data-value="9">9</button></div>
          <div class="cbt-nat-row"><button class="cbt-nat-btn" data-action="nat-key" data-value="4">4</button><button class="cbt-nat-btn" data-action="nat-key" data-value="5">5</button><button class="cbt-nat-btn" data-action="nat-key" data-value="6">6</button></div>
          <div class="cbt-nat-row"><button class="cbt-nat-btn" data-action="nat-key" data-value="1">1</button><button class="cbt-nat-btn" data-action="nat-key" data-value="2">2</button><button class="cbt-nat-btn" data-action="nat-key" data-value="3">3</button></div>
          <div class="cbt-nat-row"><button class="cbt-nat-btn" data-action="nat-key" data-value="0">0</button><button class="cbt-nat-btn" data-action="nat-key" data-value=".">.</button><button class="cbt-nat-btn" data-action="nat-key" data-value="-">-</button></div>
          <div class="cbt-nat-row"><button class="cbt-nat-btn" data-action="nat-key" data-value="Left">←</button><button class="cbt-nat-btn" data-action="nat-key" data-value="Right">→</button></div>
          <button class="cbt-nat-btn wide" data-action="nat-key" data-value="Clear All">Clear All</button>
        </div>
      </div>
    `;
  } else {
    choices = q.options.map(({label:v})=>`
      <label class="cbt-option-row">
        <input type="${q.type==='MSQ'?'checkbox':'radio'}" name="q${q.id}" class="cbt-option-input" data-action="answer" data-value="${v}" ${selected(v)?'checked':''}>
        <div class="cbt-option-content">${optionContent(q,q.options.find(o=>o.label===v))}</div>
      </label>
    `).join('');
  }

  const penalty = q.negativeMarks ?? (q.type==='MCQ' ? q.marks/3 : 0);
  let formattedPenalty = penalty === 0 ? '0' : (Math.abs(penalty - 0.333) < 0.01 ? '1/3' : (Math.abs(penalty - 0.666) < 0.01 ? '2/3' : penalty));
  
  let totalAnswered = 0, totalNotAnswered = 0, totalNotVisited = 0, totalMarked = 0, totalAnsweredMarked = 0;
  
  const paletteButtons = visibleIds.map(({id, index: i, number}, localIndex) => {
    const isAnswered = Array.isArray(d.answers[id]) ? d.answers[id].length > 0 : (d.answers[id] !== undefined && d.answers[id] !== '');
    const isVisited = d.visited[id];
    const isMarkedReview = d.review[id];
    let stateClass = 'not-visited';
    if (isAnswered && isMarkedReview) { stateClass = 'answered-marked'; }
    else if (!isAnswered && isMarkedReview) { stateClass = 'not-answered-marked'; }
    else if (isAnswered) { stateClass = 'answered'; }
    else if (isVisited) { stateClass = 'not-answered'; }
    
    return `<button class="cbt-palette-btn ${stateClass} ${i===d.index?'active':''}" data-action="jump" data-value="${i}">${localIndex + 1}</button>`;
  }).join('');
  
  d.questionIds.forEach((id) => {
    const isAnswered = Array.isArray(d.answers[id]) ? d.answers[id].length > 0 : (d.answers[id] !== undefined && d.answers[id] !== '');
    const isVisited = d.visited[id];
    const isMarkedReview = d.review[id];
    if (isAnswered && isMarkedReview) totalAnsweredMarked++;
    else if (!isAnswered && isMarkedReview) totalMarked++;
    else if (isAnswered) totalAnswered++;
    else if (isVisited) totalNotAnswered++;
    else totalNotVisited++;
  });

  return `
  <style>
    body { margin: 0; background: #fff; color: #333; font-family: Arial, sans-serif; overflow: hidden; }
    .cbt-container { display: flex; flex-direction: column; height: 100vh; font-size: 14px; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 100000; background: #fff; }
    .cbt-header { background: #333; color: white; display: flex; justify-content: space-between; align-items: center; padding: 4px 16px; border-bottom: 2px solid #2b669a; }
    .cbt-title { font-weight: bold; font-size: 16px; }
    .cbt-header-tools { display: flex; gap: 16px; font-size: 13px; align-items: center; }
    .cbt-icon { background: #17a2b8; border-radius: 50%; color: white; width: 16px; height: 16px; display: inline-flex; align-items: center; justify-content: center; font-style: italic; font-weight: bold; margin-right: 4px; font-size: 11px; }
    .cbt-icon.green { background: #28a745; }
    
    .cbt-body { display: flex; flex: 1; overflow: hidden; }
    
    .cbt-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; border-right: 1px solid #ccc; }
    .cbt-sub-header { background: #f0f8ff; padding: 8px 16px; border-bottom: 1px solid #ccc; display: flex; align-items: center; gap: 8px; }
    .cbt-sub-header-btn { background: #2b669a; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold; font-size: 12px; display: flex; align-items: center; gap: 4px;}
    
    .cbt-sections-bar { display: flex; align-items: flex-end; padding: 8px 16px 0; border-bottom: 2px solid #2b669a; justify-content: space-between; }
    .cbt-tabs-container { display: flex; align-items: flex-end; gap: 8px; }
    .cbt-tabs { display: flex; gap: 4px; }
    .cbt-tab { padding: 6px 12px; border: 1px solid #ccc; border-bottom: none; border-radius: 4px 4px 0 0; cursor: pointer; background: white; font-weight: bold; color: #2b669a; display: flex; align-items: center; gap: 4px; font-size: 13px; }
    .cbt-tab.active { background: #2b669a; color: white; border-color: #2b669a; }
    .cbt-timer { font-weight: bold; padding-bottom: 4px; font-size: 13px; }
    
    .cbt-question-header { display: flex; justify-content: space-between; padding: 8px 16px; border-bottom: 1px solid #ccc; font-weight: bold; font-size: 13px; }
    .cbt-marks { font-weight: normal; }
    .cbt-marks .green { color: #28a745; font-weight: bold; }
    .cbt-marks .red { color: #dc3545; font-weight: bold; }
    
    .cbt-question-body { padding: 16px; flex: 1; overflow-y: auto; font-size: 16px; line-height: 1.5; color: #000; }
    .cbt-qno { font-weight: bold; font-size: 18px; margin-bottom: 16px; }
    
    .cbt-option-row { display: flex !important; flex-direction: row !important; align-items: center !important; gap: 8px !important; margin: 0 0 12px 0 !important; cursor: pointer; padding: 4px; color: #000; line-height: 1.2; }
    .cbt-option-row:hover { background: #f9f9f9; }
    .cbt-option-input { margin: 0 !important; padding: 0 !important; width: 16px !important; height: 16px !important; cursor: pointer; flex-shrink: 0 !important; }
    .cbt-option-content { display: flex !important; flex-direction: row !important; align-items: center !important; margin: 0 !important; padding: 0 !important; }
    .cbt-option-content > * { display: inline-block !important; vertical-align: middle !important; margin: 0 !important; padding: 0 !important; }
    
    .cbt-footer { border-top: 1px solid #ccc; padding: 12px 16px; display: flex; justify-content: space-between; background: #fff; }
    .cbt-btn-white { background: white; border: 1px solid #ccc; padding: 8px 16px; border-radius: 2px; cursor: pointer; font-size: 14px; }
    .cbt-btn-white:hover { background: #f0f0f0; }
    .cbt-btn-blue { background: #2b669a; color: white; border: 1px solid #24527a; padding: 8px 24px; border-radius: 2px; cursor: pointer; font-size: 14px; }
    .cbt-btn-blue:hover { background: #24527a; }
    
    .cbt-sidebar { width: 340px; display: flex; flex-direction: column; background: #e5f6fd; overflow: hidden; }
    .cbt-candidate { display: flex; align-items: center; padding: 12px; border-bottom: 1px solid #ccc; position: relative; background: white; }
    
    .cbt-avatar { width: 64px; height: 64px; background: #eee; margin-right: 12px; border: 1px solid #ccc; background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23999"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>'); background-size: cover; }
    .cbt-name { font-weight: bold; font-size: 16px; }
    
    .cbt-legend-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; padding: 12px; border-bottom: 1px solid #ccc; background: white; }
    .cbt-legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; line-height: 1.2; color: #000; }
    .cbt-shape { display: flex; align-items: center; justify-content: center; width: 32px; height: 28px; color: white; font-weight: bold; font-size: 12px; position: relative; }
    .cbt-shape.answered { background: #2f9a43; border-radius: 50% 50% 0 0; clip-path: polygon(50% 0%, 100% 25%, 100% 100%, 0% 100%, 0% 25%); }
    .cbt-shape.not-answered { background: #e04a22; clip-path: polygon(0% 0%, 100% 0%, 100% 75%, 50% 100%, 0% 75%); }
    .cbt-shape.not-visited { background: #efefef; border: 1px solid #ccc; color: #333; width: 26px; height: 26px; }
    .cbt-shape.marked { background: #663399; border-radius: 50%; height: 28px; width: 28px; }
    .cbt-shape.answered-marked { background: #663399; border-radius: 50%; height: 28px; width: 28px; }
    .cbt-shape.answered-marked::after { content: ''; position: absolute; bottom: 0; right: 0; width: 8px; height: 8px; background: #2f9a43; border-radius: 50%; border: 1px solid white; }
    
    .cbt-sidebar-section-title { background: #2b669a; color: white; padding: 8px 12px; font-weight: bold; font-size: 14px; }
    .cbt-sidebar-subtitle { padding: 8px 12px; font-weight: bold; background: white; border-bottom: 1px solid #ccc; font-size: 12px; }
    .cbt-palette { padding: 12px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; overflow-y: auto; flex: 1; align-content: flex-start; justify-items: center; background: #e5f6fd; }
    .cbt-palette-btn { border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; width: 44px; height: 38px; color: white; font-family: Arial; font-size: 14px; position: relative; padding: 0; }
    .cbt-palette-btn:hover { opacity: 0.9; }
    .cbt-palette-btn.active { box-shadow: inset 0 0 0 2px #000; }
    .cbt-palette-btn.answered { background: #2f9a43; border-radius: 50% 50% 0 0; clip-path: polygon(50% 0%, 100% 25%, 100% 100%, 0% 100%, 0% 25%); }
    .cbt-palette-btn.not-answered { background: #e04a22; clip-path: polygon(0% 0%, 100% 0%, 100% 75%, 50% 100%, 0% 75%); }
    .cbt-palette-btn.not-visited { background: #efefef; border: 1px solid #ccc; color: #333; width: 42px; height: 36px; }
    .cbt-palette-btn.not-answered-marked { background: #663399; border-radius: 50%; height: 42px; width: 42px; }
    .cbt-palette-btn.answered-marked { background: #663399; border-radius: 50%; height: 42px; width: 42px; }
    .cbt-palette-btn.answered-marked::after { content: ''; position: absolute; bottom: 2px; right: 2px; width: 12px; height: 12px; background: #2f9a43; border-radius: 50%; border: 1px solid white; }
    
    .cbt-submit-btn { background: #5bc0de; color: white; border: none; padding: 12px; font-weight: bold; font-size: 16px; cursor: pointer; text-align: center; border-radius: 2px; margin: 16px 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .cbt-submit-btn:hover { background: #46b8da; }
    
    /* NAT Input */
    .cbt-nat-container { margin-top: 24px; display: flex; flex-direction: column; align-items: flex-start; }
    .cbt-nat-input { width: 160px; padding: 8px; font-size: 16px; border: 1px solid #ccc; border-radius: 2px; margin-bottom: 8px; font-family: monospace; outline: none; }
    .cbt-nat-keypad { display: inline-flex; flex-direction: column; gap: 4px; background: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px; width: 160px; box-sizing: border-box; }
    .cbt-nat-row { display: flex; gap: 4px; justify-content: center; }
    .cbt-nat-btn { flex: 1; height: 32px; background: white; border: 1px solid #ccc; border-radius: 2px; font-weight: bold; font-size: 14px; cursor: pointer; color:#333; }
    .cbt-nat-btn:active { background: #e0e0e0; }
    .cbt-nat-btn.wide { flex: none; width: 100%; height: 32px; font-size: 12px; }

    
  </style>

  <div class="cbt-container">
    <header class="cbt-header">
      <div class="cbt-title">AE Aerospace Engineering Mock</div>
      <div class="cbt-header-tools">
        <span data-action="exam-modal" data-value="instructions" style="cursor:pointer; display:flex; align-items:center;"><span class="cbt-icon">i</span> Instructions</span>
        <span data-action="exam-modal" data-value="paper" style="cursor:pointer; display:flex; align-items:center;"><span class="cbt-icon green" style="background:#5cb85c;">📄</span> Question Paper</span>
      </div>
    </header>
    
    <div class="cbt-body">
      <div class="cbt-main">
        <div class="cbt-sub-header" style="justify-content: space-between;">
          <span class="cbt-sub-header-btn">AE Aerospace Engineering <span class="cbt-icon" style="background:white; color:#2b669a; cursor:pointer;" data-action="exam-modal" data-value="info">i</span></span>
            
          </div>
        
        <div class="cbt-sections-bar">
          <div class="cbt-tabs-container">
            <span style="font-weight:bold; font-size:13px; margin-bottom:10px; margin-right:8px;">Sections</span>
            <div class="cbt-tabs">
              ${gaIds.length > 0 ? `<div class="cbt-tab ${sectionId === 'GA' ? 'active' : ''}" data-action="jump" data-value="${gaIds[0].index}">General Aptitude <span class="cbt-icon" style="background:${sectionId==='GA'?'white':'#17a2b8'}; color:${sectionId==='GA'?'#2b669a':'white'}; cursor:pointer;" data-action="exam-modal" data-value="info">i</span></div>` : ''}
              ${aeIds.length > 0 ? `<div class="cbt-tab ${sectionId === 'AE' ? 'active' : ''}" data-action="jump" data-value="${aeIds[0].index}">AE Aerospace Enginee... <span class="cbt-icon" style="background:${sectionId==='AE'?'white':'#17a2b8'}; color:${sectionId==='AE'?'#2b669a':'white'}; cursor:pointer;" data-action="exam-modal" data-value="info">i</span></div>` : ''}
            </div>
          </div>
          <div class="cbt-timer">Time Left : <span id="session-time" style="font-weight:bold; font-size:16px;">${clock(timer.remaining())}</span></div>
        </div>
        
        <div class="cbt-question-header">
          <div class="cbt-qtype" style="display:flex; align-items:center; gap:12px;">
            <span>Question Type: ${q.type}</span>
            ${isAe ? `<button data-action="toggle-verify-question" data-value="${esc(q.id)}" class="${isVerified ? 'primary small' : 'quiet small'}" style="padding: 2px 10px; font-size: 12px; cursor: pointer; border-radius: 3px; font-weight: 600; ${isVerified ? 'background: #2b669a; color: #fff; border: 1px solid #2b669a;' : 'background: #fff; color: #333; border: 1px solid #999;'}">${isVerified ? '✓ Verified' : 'Mark as Verified'}</button>` : ''}
          </div>
          <div class="cbt-marks">Marks for correct answer: <span class="green">${q.marks}</span> | Negative Marks: <span class="red">${formattedPenalty}</span></div>
        </div>
        
        <div class="cbt-question-body">
          <div class="cbt-qno">Question No. </div>
          <div style="margin-bottom: 24px; color: #000;">${sourceQuestion(q, true)}</div>
          ${choices}
        </div>
        
        <div class="cbt-footer">
          <div class="cbt-footer-left">
            <button class="cbt-btn-white" data-action="review-question">Mark for Review & Next</button>
            <button class="cbt-btn-white" data-action="clear">Clear Response</button>
          </div>
          <div class="cbt-footer-right">
            <button class="cbt-btn-white" data-action="previous" ${d.index > 0 ? '' : 'disabled style="opacity:0.5; cursor:not-allowed;"'}>Previous</button>
            <button class="cbt-btn-blue" data-action="next">Save & Next</button>
          </div>
        </div>
        <div style="background: #2b669a; color: white; text-align: center; padding: 4px; font-size: 11px;">Version : 17.07.00</div>
      </div>
      
      <div class="cbt-sidebar">
        <div class="cbt-candidate">
          <div class="cbt-avatar"></div>
          <div class="cbt-name" style="color:#000;">John Smith</div>
        </div>
        
        <div class="cbt-legend-grid">
          <div class="cbt-legend-item"><div class="cbt-shape answered">${totalAnswered}</div> Answered</div>
          <div class="cbt-legend-item"><div class="cbt-shape not-answered">${totalNotAnswered}</div> Not Answered</div>
          <div class="cbt-legend-item"><div class="cbt-shape not-visited">${totalNotVisited}</div> Not Visited</div>
          <div class="cbt-legend-item"><div class="cbt-shape marked">${totalMarked}</div> Marked for Review</div>
          <div class="cbt-legend-item" style="grid-column: span 2;"><div class="cbt-shape answered-marked" style="margin-right: 8px;">${totalAnsweredMarked}</div> Answered & Marked for Review (will also be evaluated)</div>
        </div>
        
        <div class="cbt-sidebar-section-title">${sectionId === 'GA' ? 'General Aptitude' : 'AE Aerospace Engineering'}</div>
        <div class="cbt-sidebar-subtitle" style="color:#000;">Choose a Question</div>
        
        <div class="cbt-palette">
          ${paletteButtons}
        </div>
        
        <button class="cbt-submit-btn" data-action="exam-submit-confirm">Submit</button>
      </div>
    </div>
    
    
      
      <!-- Info Modal -->

    <div style="display:${globalThis.state?.ui?.examModal==='info'?'flex':'none'}; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:20000; align-items:center; justify-content:center; color:#000;">
      <div style="background:white; width: 400px; padding: 20px; border-radius:4px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
          <h3 style="margin:0; font-family:Arial;">Status</h3>
          <button data-action="exam-modal" data-value="info" style="background:none; border:none; font-size:20px; cursor:pointer;">×</button>
        </div>
        <div class="cbt-legend-item" style="margin-bottom:8px;"><div class="cbt-shape answered">${totalAnswered}</div> Answered</div>
        <div class="cbt-legend-item" style="margin-bottom:8px;"><div class="cbt-shape not-answered">${totalNotAnswered}</div> Not Answered</div>
        <div class="cbt-legend-item" style="margin-bottom:8px;"><div class="cbt-shape not-visited">${totalNotVisited}</div> Not Visited</div>
        <div class="cbt-legend-item" style="margin-bottom:8px;"><div class="cbt-shape marked">${totalMarked}</div> Marked for Review</div>
        <div class="cbt-legend-item" style="margin-bottom:8px;"><div class="cbt-shape answered-marked">${totalAnsweredMarked}</div> Answered & Marked for Review</div>
      </div>
    </div>
    
    <!-- Instructions Modal -->
    <div style="display:${globalThis.state?.ui?.examModal==='instructions'?'flex':'none'}; position:fixed; top:0; left:0; right:0; bottom:0; background:white; z-index:20000; flex-direction:column; color:#000;">
      <div class="cbt-header"><div class="cbt-title">Instructions</div><button data-action="exam-modal" data-value="instructions" style="background:none; border:none; color:white; font-size:24px; cursor:pointer; line-height:1;">×</button></div>
      <div style="padding:40px; overflow-y:auto; flex:1; font-family:Arial; line-height:1.6; max-width: 800px; margin: 0 auto;">
        <h2>General Instructions</h2>
        <p>1. Total duration of examination is 180 minutes.</p>
        <p>2. The clock will be set at the server. The countdown timer in the top right corner will display the remaining time available for you to complete the examination. When the timer reaches zero, the examination will end by itself.</p>
        <p>3. The Question Palette displayed on the right side of screen will show the status of each question using one of the following symbols:</p>
        <ul style="list-style:none; padding:0;">
          <li style="margin:8px 0; display:flex; align-items:center; gap:8px;"><div class="cbt-shape not-visited"></div> You have not visited the question yet.</li>
          <li style="margin:8px 0; display:flex; align-items:center; gap:8px;"><div class="cbt-shape not-answered"></div> You have not answered the question.</li>
          <li style="margin:8px 0; display:flex; align-items:center; gap:8px;"><div class="cbt-shape answered"></div> You have answered the question.</li>
          <li style="margin:8px 0; display:flex; align-items:center; gap:8px;"><div class="cbt-shape marked"></div> You have NOT answered the question, but have marked the question for review.</li>
          <li style="margin:8px 0; display:flex; align-items:center; gap:8px;"><div class="cbt-shape answered-marked"></div> The question(s) "Answered and Marked for Review" will be considered for evaluation.</li>
        </ul>
        <h2>Navigating to a Question</h2>
        <p>4. To answer a question, do the following:</p>
        <ul style="margin-bottom:20px;">
          <li>Click on the question number in the Question Palette at the right of your screen to go to that numbered question directly. Note that using this option does NOT save your answer to the current question.</li>
          <li>Click on <strong>Save & Next</strong> to save your answer for the current question and then go to the next question.</li>
          <li>Click on <strong>Mark for Review & Next</strong> to save your answer for the current question, mark it for review, and then go to the next question.</li>
        </ul>
        <h2>Answering a Question</h2>
        <p>5. Procedure for answering a multiple choice type question:</p>
        <ul style="margin-bottom:20px;">
          <li>To select your answer, click on the button of one of the options.</li>
          <li>To deselect your chosen answer, click on the button of the chosen option again or click on the <strong>Clear Response</strong> button.</li>
          <li>To change your chosen answer, click on the button of another option.</li>
          <li>To save your answer, you MUST click on the <strong>Save & Next</strong> button.</li>
        </ul>
      </div>
    </div>
    
    <!-- Question Paper Modal -->
    <div style="display:${globalThis.state?.ui?.examModal==='paper'?'flex':'none'}; position:fixed; top:0; left:0; right:0; bottom:0; background:white; z-index:20000; flex-direction:column; color:#000;">
      <div class="cbt-header"><div class="cbt-title">Question Paper</div><button data-action="exam-modal" data-value="paper" style="background:none; border:none; color:white; font-size:24px; cursor:pointer; line-height:1;">×</button></div>
      <div style="padding:40px; overflow-y:auto; flex:1; font-family:Arial; line-height:1.6; max-width: 900px; margin: 0 auto;">
        ${d.questionIds.map((id, index) => {
          const p = a.byId.get(id);
          return `<div style="margin-bottom: 24px; border-bottom: 1px solid #eee; padding-bottom: 24px;">
            <h3 style="margin-top:0;">Question ${index + 1} <span style="font-size:13px; font-weight:normal; color:#2b669a; cursor:pointer; background:#eee; padding:2px 8px; border-radius:2px;" data-action="jump" data-value="${index}">Jump to question</span></h3>
            ${sourceQuestion(p, true)}
            ${p.type === 'NAT' ? '<p><i>Numerical Answer Type</i></p>' : p.options.map(o => `<div>${o.label}. ${optionContent(p, o)}</div>`).join('')}
          </div>`;
        }).join('')}
      </div>
    </div>
    
  </div>
  `;
}
