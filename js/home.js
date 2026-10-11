import {dueReviewQueue} from './revision.js';
import {esc,link,empty,formatDate,button} from './ui.js';
import {recommendation,startNowPlan,completedDays,streak,xp,level,localDay,achievements} from './domain.js';
import {answered} from './scoring.js';

const stat=(value,label,kind)=>`<div class="home-stat home-stat--${kind}"><strong>${value}</strong><span>${label}</span></div>`;

export function home(s,a){
 const plan=startNowPlan(s,a),available=plan.kind!=='unavailable';
 const rec=!available?{title:'Study session unavailable',reason:plan.reason}:plan.kind==='resume'?recommendation(s,a):{title:'Your study session is ready',reason:'Prioritizes unresolved mistakes, due review items, then questions you have not attempted.'};
 const done=completedDays(s),st=streak(s.attempts),today=localDay();
 const todayCount=s.attempts.filter(x=>x.localDate===today&&answered(x.selectedAnswer)).length;
 const seen=new Set(s.attempts.filter(x=>answered(x.selectedAnswer)).map(x=>x.questionId));
 const reviewDue=dueReviewQueue(a.questions,s).length;
 const due=s.flashcards.filter(f=>f.due<=Date.now()).length;
 const week=Array.from({length:7},(_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);return `<div>${d.toLocaleDateString(undefined,{weekday:'narrow'})}<i class="${st.days.includes(localDay(d))?'done':''}">${st.days.includes(localDay(d))?'✓':d.getDate()}</i></div>`}).join('');
 const draft=plan.kind==='resume'?s.drafts[plan.sessionId]:null;
 const count=draft?.questionIds.length||plan.questionIds?.length||0;
 const estimate=plan.kind==='resume'?`<strong>Question ${Math.min((draft?.currentPosition||0)+1,count)} of ${count}</strong>Continue where you stopped`:`<strong id="start-estimate" data-available="${a.questions.length}">${Math.min(a.questions.length,12)} questions</strong>Planned for 25 minutes`;
 const budget=available&&plan.kind==='new'?`<label class="budget-label">Available time<select id="start-budget" aria-describedby="start-estimate"><option value="10">10 minutes</option><option value="25" selected>25 minutes</option><option value="45">45 minutes</option><option value="60">60 minutes</option><option value="custom">Custom</option></select></label><label class="custom-budget-label" for="start-budget-custom">Custom minutes · 1–360</label><input id="start-budget-custom" aria-label="Custom minutes · 1–360" type="number" min="1" max="360" step="1" inputmode="numeric" value="30" hidden>`:'';
 const startAction=available?button(plan.kind==='resume'?'Continue session':'Start now','start-now','','primary'):'<button class="primary" disabled aria-disabled="true">Start now</button>';
 const journey=Array.from({length:118},(_,i)=>i<a.sets.length?`<a href="#/day/${i+1}" class="${done.has(i+1)?'complete':''}" aria-label="Day ${i+1}, ${done.has(i+1)?'completed':'available'}" title="Day ${i+1}">${i+1}${done.has(i+1)?'<span class="sr-only"> ✓</span>':''}</a>`:'').join('');
 const laterDays=Array.from({length:Math.max(0,118-a.sets.length)},(_,i)=>`<span title="Day ${a.sets.length+i+1}: unavailable" aria-label="Day ${a.sets.length+i+1}: unavailable">${a.sets.length+i+1}</span>`).join('');
 const recent=s.sessions.length?s.sessions.slice(-3).reverse().map(x=>`<a class="row" href="#/result/${x.id}"><div class="row-main"><span class="number-box" aria-label="${x.result.answered} answered">${x.result.answered}</span><div><div class="row-title">${x.origin==='daily'?'Day '+x.configuration.day:x.origin==='start-now'?'Study session':esc(x.origin)+' session'}</div><small>${formatDate(x.completedAt)} · ${x.questionIds.length} questions</small></div></div><span class="pill">${x.result.score===null?'Ungraded':x.result.score.toFixed(2)+' marks'}</span></a>`).join(''):empty('Your first session starts a new record.','Finish a practice session to see your activity here.');
 return `<div class="home-command">
 <header class="home-intro"><p>${s.sessions.length||draft?'Welcome back':'Your study space'}${s.profile.name?', '+esc(s.profile.name):''}.</p><span class="date">${new Date().toLocaleDateString(undefined,{weekday:'long',day:'numeric',month:'long'})}</span></header>
 <section class="home-action" aria-labelledby="recommended-title">
  <div class="home-invitation"><span class="eyebrow">General Aptitude · Recommended next</span><h1 id="recommended-title">${plan.kind==='new'?'Make room for your<br class="home-title-break"> next question.':rec.title}</h1></div>
  <div class="session-plan">${budget}${available?`<div class="session-estimate">${estimate}</div>`:''}${startAction}<p class="caption save-context">${available?(plan.kind==='resume'&&plan.mode==='test'?'Timed test · its deadline continues while away':'Progress is saved on this browser'):'No valid questions are currently loaded'}</p></div>
  <p class="home-reason">${rec.reason}</p>
 </section>
 <section class="home-progress" aria-label="Your progress">
  <div class="home-goal"><div><h2>Today’s goal</h2><p><strong>${todayCount}</strong> / ${s.settings.goal} questions <span class="goal-edit">${link('Edit','#/settings','text-link')}</span></p><progress value="${Math.min(todayCount,s.settings.goal)}" max="${s.settings.goal}" aria-label="Daily question goal"></progress><p class="caption">${todayCount>=s.settings.goal?'Daily goal reached.':'A small, consistent step is a good start.'}</p></div><div class="home-week"><span class="caption">Your past seven days</span><div class="week">${week}</div></div></div>
  <div class="home-stats" aria-label="Practice summary">${stat(done.size,'Sets completed','sets')}${stat(seen.size,'Questions attempted','questions')}${stat('<svg class="home-streak-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2c1 5-4 6-4 10 0 1 .5 2 1.5 2.5C9 11 12 10 13 8c0 4 5 5 5 9a6 6 0 0 1-12 0C3 11 8 8 8 5c1 2 1 3 2 3 2-2 2-4 2-6Z"/></svg>'+st.current,'day streak','streak')}${stat(xp(s),'Practice XP','xp')}</div>
 </section>
 <div class="home-study-grid">
  <section class="home-section home-journey"><div class="section-head"><div><h2>Your 118-day journey</h2><p class="caption">${a.sets.length} source sets available · ${done.size} / 118 completed</p></div></div>${journey?`<div class="journey">${journey}</div><div class="legend"><span><i class="journey-complete"></i>Completed</span><span><i></i>Available</span></div>`:'<p class="caption">Your journey will be available when source sets are loaded.</p>'}${laterDays?`<details class="journey-later"><summary>${Math.max(0,118-a.sets.length)} later days · not yet available</summary><div class="journey-future">${laterDays}</div></details>`:''}</section>
  <section class="home-section home-review"><div class="section-head"><div><h2>Return to your material</h2><p class="caption">Your review library, ready when you are.</p></div></div><a class="row" href="#/review/due"><span class="row-title">Questions due for review</span><span>${reviewDue} <span aria-hidden="true">↗</span></span></a><a class="row" href="#/review/bookmarks"><span class="row-title">Saved questions</span><span>${Object.keys(s.bookmarks).length} <span aria-hidden="true">↗</span></span></a><a class="row" href="#/flashcards"><span class="row-title">Flashcards due</span><span>${due} <span aria-hidden="true">↗</span></span></a><a class="row" href="#/review/notes"><span class="row-title">Personal notes</span><span>${Object.values(s.notes).filter(Boolean).length} <span aria-hidden="true">↗</span></span></a></section>
  <section class="home-section home-recent"><div class="section-head"><h2>Recent practice</h2>${link('View history →','#/history','text-link')}</div>${recent}</section>
  <section class="home-section home-record"><div class="section-head"><h2>Practice record</h2><span class="caption">${level(xp(s))}</span></div><p class="caption">${xp(s)} XP · ${st.longest} day longest streak</p><progress value="${xp(s)%500}" max="500" aria-label="Experience toward next level"></progress><p class="caption">${achievements(s).join(' · ')||'Your first achievement begins with your first submitted answer.'}</p></section>
 </div>
 <p class="home-source caption"><strong>From your source papers</strong><span>${a.questions.length} question records · 2025–2026<br>${a.questions.filter(q=>q.answer!==undefined).length} questions with verified official keys and checked editorial solutions.</span></p>
 <div class="footer"><span>GATE / General Aptitude</span><span>Focus on the next question.</span></div></div>`;
}
