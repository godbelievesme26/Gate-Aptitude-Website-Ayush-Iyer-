import {esc} from './ui.js';
import {clock} from './timer.js';
import {MOTION_LEVELS} from './moments.js';

const ring='<svg class="moment-orbit" viewBox="0 0 220 220" aria-hidden="true"><circle class="moment-orbit-track" cx="110" cy="110" r="99"/><circle class="moment-orbit-fill" cx="110" cy="110" r="99" pathLength="100"/></svg>';
export function insightCard(insight){return insight?`<aside class="moment-story" aria-label="From your practice"><span class="eyebrow">From your practice</span><p>${esc(insight.text)}</p></aside>`:'';}
export function momentMarkup(moment){
 const p=moment.primary,s=moment.summary,isStreak=p.kind==='streak',goal=moment.events.find(e=>e.kind==='goal'),session=moment.events.find(e=>e.kind==='session');
 const visual=isStreak?`<div class="moment-counter" role="img" aria-label="${p.value} day streak">${ring}<div class="moment-number-window" aria-hidden="true"><span class="moment-number-old">${p.previous}</span><span class="moment-number-new">${p.value}</span></div><span class="moment-unit" aria-hidden="true">Day streak</span></div>`:p.kind==='goal'?`<div class="moment-counter moment-goal-symbol" aria-hidden="true">${ring}<span>✓</span></div>`:`<div class="moment-counter" aria-hidden="true">${ring}<span class="moment-number-new">${p.value||s.answered}</span><span class="moment-unit">${p.kind==='journey'?'Daily sets':p.kind==='questions'?'Questions':'Answered'}</span></div>`;
 return `<div class="moment-layout moment-${p.kind} moment-level-${p.level}" style="--moment-duration:${MOTION_LEVELS[p.level]}ms"><section class="moment-stage"><span class="eyebrow">${isStreak?'Consistency in motion':p.kind==='goal'?"Today's work":'A step forward'}</span>${visual}<h2 id="moment-title">${esc(p.title)}</h2><p id="moment-context">${esc(p.context)}</p><span class="moment-stage-rule" aria-hidden="true"></span></section><section class="moment-details"><div><span class="eyebrow">Session complete</span><h3>${esc(session.title==='Session complete'?'Time well spent.':session.title)}</h3><p class="moment-saved">${esc(session.context)}</p></div><dl class="moment-facts"><div><dt>Answered</dt><dd>${s.answered}</dd></div><div><dt>Correct</dt><dd>${s.correct}</dd></div><div><dt>Study time</dt><dd>${clock(s.elapsed)}</dd></div>${s.xp?`<div><dt>Practice XP</dt><dd>+${s.xp}</dd></div>`:''}</dl>${s.ungraded?`<p class="caption">${s.ungraded} response${s.ungraded===1?' is':'s are'} ungraded or awarded without a correctness judgment.</p>`:''}${goal?`<div class="moment-goal-progress"><strong>Today's goal complete</strong><span>${goal.value} / ${goal.target} questions</span><div class="moment-goal-line" aria-hidden="true"><i></i></div></div>`:''}${moment.events.filter(e=>['questions','journey'].includes(e.kind)&&e!==p).map(e=>`<p class="moment-landmark">${esc(e.title)}</p>`).join('')}${insightCard(moment.insight)}<div class="moment-actions"><button class="primary" data-moment-continue autofocus>Continue</button><button data-moment-review>Review answers</button></div><p class="moment-dismiss-hint">You can continue at any time. Esc closes this moment.</p></section></div>`;
}

/** An independent dialog host reuses the native overlay mechanism without racing
 * the asynchronous Submit confirmation's close handler. Never reads storage. */
export function showProductMoment(moment,{onContinue=()=>{},onReview=()=>{}}={}){
 if(!moment)return;
 document.querySelector('#product-moment')?.close();
 const before=document.activeElement,d=document.createElement('dialog');d.id='product-moment';d.className='product-moment';d.setAttribute('aria-labelledby','moment-title');d.setAttribute('aria-describedby','moment-context');d.innerHTML=momentMarkup(moment);document.body.append(d);document.documentElement.classList.add('moment-open');
 const cleanup=()=>{window.removeEventListener('hashchange',dismiss);window.removeEventListener('popstate',dismiss);d.remove();if(!document.querySelector('#product-moment'))document.documentElement.classList.remove('moment-open');if(before?.isConnected)before.focus({preventScroll:true});else document.querySelector('#main')?.focus({preventScroll:true});};
 const dismiss=()=>d.close();d.addEventListener('close',cleanup,{once:true});window.addEventListener('hashchange',dismiss);window.addEventListener('popstate',dismiss);
 d.querySelector('[data-moment-continue]').onclick=()=>{d.close();onContinue();};d.querySelector('[data-moment-review]').onclick=()=>{d.close();onReview();};d.showModal();
 return d;
}
