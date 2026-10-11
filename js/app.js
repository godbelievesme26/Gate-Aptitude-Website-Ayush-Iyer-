import {saveNumericAnswer} from './answer-input.js';
import {optionShortcut} from './question-content.js';
import {orderedSessionQuestions,generatePaperSession} from './corpus.js';
import {generateReviewSession} from './revision.js';
import {Store,defaults,validateState,STORAGE_KEY} from './storage.js';
import {loadArchive} from './loader.js';
import {home} from './home.js';
import * as views from './views.js';
import {xp,level,generateSession,move,interruptSession,questionStats,reviewCard,startNowPlan,sessionBudget} from './domain.js';
import {answered} from './scoring.js';
import {createSessionTimer,clock} from './timer.js';
import {esc,button,toast,modal,link} from './ui.js';
import {ApplicationState} from './state.js';
import {showProductMoment} from './moment-view.js';
let store;try{store=new Store(localStorage);}catch(error){store=new Store({getItem:()=>{throw error;},setItem:()=>{throw error;}});}
const state=new ApplicationState(store); window.state=state;
let audioContext=null;
const progress=()=>state.progress,active=()=>state.activeSession,timer=()=>state.session.timer,ui=state.ui;
const navGroups=[['Study',[['home','Today','home'],['daily','Daily sets','calendar'],['bank','Question bank','book'],['practice','Build a session','timer'],['aerospace','Aerospace PYQs','plan']]],['Review',[['review','Review library','review'],['flashcards','Flashcards','cards']]],['Progress',[['analytics','Analytics','chart'],['planner','Study plan','plan']]]];
const nav=navGroups.flatMap(([,items])=>items);
const iconPaths={home:'<path d="M3 10.5 9 4l6 6.5V16H4v-5.5Z"/><path d="M7 16v-5h4v5"/>',calendar:'<rect x="3" y="4.5" width="12" height="11" rx="2"/><path d="M6 2.5v4M12 2.5v4M3 8h12"/>',book:'<path d="M3 4.5A2.5 2.5 0 0 1 5.5 2H9v13H5.5A2.5 2.5 0 0 0 3 17.5v-13ZM15 4.5A2.5 2.5 0 0 0 12.5 2H9v13h3.5a2.5 2.5 0 0 1 2.5 2.5v-13Z"/>',timer:'<circle cx="9" cy="10" r="6"/><path d="M9 7v3l2 1M7 2h4"/>',review:'<path d="m3 9 3 3 7-7"/><path d="M15 9v6H3V3h7"/>',cards:'<rect x="3" y="5" width="11" height="10" rx="2"/><path d="M6 5V3h9v9h-1"/>',chart:'<path d="M3 15V9M8 15V5M13 15V2M2 15.5h14"/>',plan:'<path d="M5 3h10v13H3V5l2-2Z"/><path d="M5 3v3H3M7 9h5M7 12h5"/>',history:'<path d="M3 5v4h4"/><path d="M4.5 12.5A6 6 0 1 0 4 6l-1 3M9 6v4l2.5 1.5"/>',settings:'<circle cx="9" cy="9" r="2.5"/><path d="M9 2.5v2M9 13.5v2M2.5 9h2M13.5 9h2M4.4 4.4l1.4 1.4M12.2 12.2l1.4 1.4M13.6 4.4l-1.4 1.4M5.8 12.2l-1.4 1.4"/>',search:'<circle cx="8" cy="8" r="4.5"/><path d="m11.5 11.5 3 3"/>',theme:'<path d="M9 2.5a6.5 6.5 0 1 0 0 13V2.5Z"/>',menu:'<path d="M3 5h12M3 9h12M3 13h12"/>',play:'<path d="m6.5 4 7 5-7 5V4Z"/>'};
const icon=name=>`<svg class="ui-icon" viewBox="0 0 18 18" aria-hidden="true">${iconPaths[name]||''}</svg>`;
const route=()=>{const [path,search='']=(location.hash.slice(1)||'/home').split('?');return {parts:path.split('/').filter(Boolean),query:new URLSearchParams(search)};};
function persist(){state.save();}
function go(hash){if(location.hash===hash)navigate();else {history.pushState(null,'',hash);navigate();}}
function animateView(kind='view'){if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;const target=kind==='question'?document.querySelector('.question-surface,.quiz-main'):document.querySelector('#main > *');if(target){target.classList.remove('view-enter','question-enter');void target.offsetWidth;target.classList.add(kind==='question'?'question-enter':'view-enter');}}
function render(){
 if(!state.content)return;const {parts,query}=route(),[page='home',id]=parts,s=progress(),archive=state.content;
 const isExam = page==='quiz'&&active()&&active().mode==='test';
 document.documentElement.dataset.theme=isExam?'light':s.settings.theme;document.body.classList.toggle('focus',page==='quiz'&&s.settings.focus);document.body.classList.toggle('solving',page==='quiz');document.body.classList.toggle('home-view',page==='home');
 let body;
 if(page==='home')body=home(s,archive);
 else if(page==='daily'||page==='day')body=views.daily(s,archive,page==='day'?id:null);
 else if(page==='bank')body=views.bank(s,archive,query);
 else if(page==='aerospace')body=views.aerospace(s,archive,id);
 else if(page==='question')body=views.questionDetail(s,archive,id);
 else if(page==='quiz')body=active()&&timer()?views.quiz(s,archive,active(),timer()):'<h1>No saved session here.</h1>'+link('Start daily practice','#/daily');
 else if(page==='result')body=views.result(s,archive,id);
 else if(page==='history')body=views.history(s);
 else if(page==='practice')body=views.practice(s,archive);
 else if(page==='review')body=views.review(s,archive,id||'due',query);
 else if(page==='flashcards')body=views.flashcards(s,ui.revealedFlashcard);
 else if(page==='analytics')body=views.analytics(s,archive);
 else if(page==='planner')body=views.planner(s,archive);
 else if(page==='settings')body=views.settings(s,ui.offlineReady,!!ui.installEvent);
 else body='<h1>Page not found.</h1>'+link('Return home','#/home');
 const label=nav.find(n=>n[0]===page)?.[1]||({day:'Daily practice',quiz:'Practice session',question:'Question detail',result:'Session result',settings:'Settings',history:'Session history',aerospace:'Aerospace PYQs'}[page]||'Home');
 document.title=label+' / GATE';
 const navMarkup=navGroups.map(([group,items])=>`<div class="nav-group"><div class="nav-group-label">${group}</div>${items.map(([v,l,i])=>`<a class="nav-link ${page===v||(v==='daily'&&page==='day')?'active':''}" href="#/${v}" ${page===v?'aria-current="page"':''}><span class="icon">${icon(i)}</span>${l}</a>`).join('')}</div>`).join('');
 const hasDraft=Object.keys(s.drafts).length>0;
 document.querySelector('#app').innerHTML=`<aside class="sidebar"><a class="brand" href="#/home"><span class="brand-mark">G</span><span>GATE<small>STUDY WORKSPACE</small></span></a><button class="sidebar-action primary" data-action="start-now">${icon('play')}${hasDraft?'Continue session':'Start a session'}</button><nav class="nav-groups" aria-label="Primary navigation">${navMarkup}</nav><div class="sidebar-bottom"><a class="nav-link ${page==='history'?'active':''}" href="#/history"><span class="icon">${icon('history')}</span>Session history</a><a class="nav-link ${page==='settings'?'active':''}" href="#/settings"><span class="icon">${icon('settings')}</span>Settings</a><div class="local-note">Personal workspace<br><span id="connection">${navigator.onLine?'Saved on this browser':'Offline · Local workspace'}</span></div></div></aside><div class="workspace"><header class="topbar"><button class="mobile-menu icon-button ghost" data-action="menu" aria-label="Toggle navigation">${icon('menu')}</button><span class="crumb">Workspace / ${label}</span><div class="top-actions">${button(icon('search')+' Search <span class="caption">⌘ K</span>','commands','','ghost small')}<span class="caption">${level(xp(s))}</span><span class="pill">${xp(s)} XP</span><button class="icon-button ghost" data-action="theme" aria-label="Switch color theme">${icon('theme')}</button><span class="avatar">${esc(s.profile.name.slice(0,1).toUpperCase()||'G')}</span></div></header><main id="main" tabindex="-1">${state.error?`<div class="notice warning">Existing data could not be read and is protected. ${esc(state.error)} ${button('Export original data','export-raw')}</div>`:''}${ui.conflict?'<div class="notice warning">Progress changed in another tab. Reload this tab to continue safely.</div>':''}${body}</main></div>`;
 if(active()&&timer())updateTimer();
}
function navigate(){
 document.querySelector('#product-moment')?.close();
 if(timer()){timer().stop();interruptSession(active());try{persist();}catch(e){toast(e.message);}state.clearSession();}
 const {parts}=route();if(parts[0]==='quiz'){
  const draft=state.activateSession(parts[1],value=>createSessionTimer(value));
  if(!draft&&progress().drafts[parts[1]])toast('This draft references unavailable questions. Its data is preserved.');
  if(draft&&!document.hidden)timer().start();
 }
 render();animateView();window.scrollTo(0,0);document.querySelector('#main')?.focus({preventScroll:true});
}
function unlockSound(){try{audioContext??=new (window.AudioContext||window.webkitAudioContext)();if(audioContext.state==='suspended')audioContext.resume();}catch{}}
function ting(){const s=progress();if(!s.settings.sound||!s.settings.checkpointSound||!audioContext)return;try{const o=audioContext.createOscillator(),g=audioContext.createGain();o.type='sine';o.frequency.value=880;g.gain.setValueAtTime(s.settings.volume,audioContext.currentTime);g.gain.exponentialRampToValueAtTime(.001,audioContext.currentTime+.45);o.connect(g);g.connect(audioContext.destination);o.start();o.stop(audioContext.currentTime+.45);}catch{}}
function start(config){state.clearSession();const d=generateSession(orderedSessionQuestions(state.content.questions,config.ids),progress(),config);state.addDraft(d);unlockSound();go('#/quiz/'+d.id);}
function startReview(questionId=null){const draft=generateReviewSession(state.content.questions,progress(),{questionId,capacity:Number(document.querySelector('#review-capacity')?.value||10)});state.clearSession();state.addDraft(draft);go('#/quiz/'+draft.id);}
let submittingSessionId=null;
function finish(){const draft=active();if(!draft||submittingSessionId===draft.id)return;submittingSessionId=draft.id;try{timer()?.stop();const record=state.completeSession(draft,state.content.byId);state.clearSession();document.querySelector('#dialog').close();const moment=state.takeProductMoment(record.id);go('#/result/'+record.id);showProductMoment(moment,{onContinue:()=>go('#/home'),onReview:()=>document.querySelector('#main')?.focus()});}finally{submittingSessionId=null;}}
function requestSubmit(){const draft=active();if(!draft)return;const count=draft.questionIds.filter(id=>answered(draft.answers[id])).length;modal('Submit this session?',`<p>${count} of ${draft.questionIds.length} questions answered. ${draft.questionIds.length-count} left blank.</p><p>Your responses and time will be added to history. Questions without keys remain ungraded.</p>`,finish,'Submit session');}
function updateTimer(){const draft=active(),clockState=timer();if(!clockState||!draft)return;const current=draft.questionIds[draft.currentPosition];const text=(id,v)=>{const el=document.getElementById(id);if(el)el.textContent=v;};text('session-time',clock(draft.mode==='test'?clockState.remaining():draft.elapsed));text('visit-time',clock(clockState.visit));text('question-time',clock(draft.times[current]||0));const checkpointEnabled=draft.mode==='practice'&&progress().settings.checkpoint,triggered=checkpointEnabled&&clockState.checkpoint();if(triggered)ting();const checkpoint=document.querySelector('#checkpoint');if(checkpoint){checkpoint.className=clockState.checkpointVisible()?'checkpoint':'';checkpoint.textContent=clockState.checkpointVisible()?'02:00 — Is your approach clear? Consider moving to the next question.':'';}
}
function answer(value){const draft=active();if(!draft)return;const q=state.content.byId.get(draft.questionIds[draft.currentPosition]);if(progress().attempts.some(attempt=>attempt.attemptId===draft.id+':'+q.id)){toast('This response is already recorded. Continue with the session.');return;}if(q.type==='MSQ'){const current=draft.answers[q.id]||[];draft.answers[q.id]=current.includes(value)?current.filter(x=>x!==value):[...current,value];}else draft.answers[q.id]=value;persist();const y=scrollY;cbtRender();if(q.type==='NAT')document.querySelector('#nat-answer')?.focus({preventScroll:true});else document.querySelector(`[data-action="answer"][data-value="${CSS.escape(String(value))}"]`)?.focus({preventScroll:true});scrollTo(0,y);}
function jump(index){const draft=active();if(!draft)return;const from=draft.currentPosition,target=(draft.mode==='test'||index<=from)?index:from+1;timer().leave();if(draft.mode!=='test'&&target>from)state.commitAndMove(draft,state.content.byId,target);else{move(draft,target);persist();}ui.examModal=null;render();animateView('question');window.scrollTo(0,0);document.querySelector('#solve-title')?.focus({preventScroll:true});}
function exportData(value=progress(),name='gate-progress'){const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name+'-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function openBookmark(id){modal('Save this question',`<label>Collection<select id="bookmark-kind"><option>Saved</option><option>Important</option><option>Must Revise</option><option value="">Remove bookmark</option></select></label>`,d=>{state.setBookmark(id,d.querySelector('select').value);render();},'Save');}
function notebookModal(id){if(!state.progress.notebooks.length){modal('Create a notebook',`<label>Name<input id="new-name" maxlength="80" placeholder="Must revise"></label>`,d=>{const name=d.querySelector('input').value.trim();if(!name)throw Error('Enter a notebook name.');state.progress.notebooks.push({id:crypto.randomUUID(),name,questionIds:id?[id]:[],updatedAt:new Date().toISOString()});persist();render();},'Create notebook');return;}
 modal('Add to notebook',`<label>Notebook<select>${state.progress.notebooks.map(n=>`<option value="${n.id}">${esc(n.name)}</option>`).join('')}</select></label>`,d=>{const n=state.progress.notebooks.find(n=>n.id===d.querySelector('select').value);if(!n.questionIds.includes(id))n.questionIds.push(id);n.updatedAt=new Date().toISOString();persist();toast('Added to notebook.');},'Add question');}
function newCard(id){const q=state.content.byId.get(id);modal('Create a personal flashcard',`<label>Front<textarea id="card-front" maxlength="4000">${esc(q?q.question:'')}</textarea></label><label>Back · your own explanation<textarea id="card-back" maxlength="8000">${esc(progress().notes[id]||'')}</textarea></label><p class="caption">This is your revision material, not an official solution.</p>`,d=>{const front=d.querySelector('#card-front').value.trim(),back=d.querySelector('#card-back').value.trim();if(!front||!back)throw Error('Add both a prompt and an answer.');progress().flashcards.push({id:crypto.randomUUID(),questionId:id||null,front,back,due:Date.now(),reviewCount:0,successes:0});persist();ui.revealedFlashcard=false;render();},'Create card');}
function commands(){const d=document.querySelector('#dialog'),before=document.activeElement;const items=[['Start today’s set','#/daily'],['Search PYQs','#/bank'],['Open mistakes','#/review/mistakes'],['Open bookmarks','#/review/bookmarks'],['Open notebooks','#/review/notebooks'],['Open flashcards','#/flashcards'],['Open analytics','#/analytics'],...state.content.registry.map(x=>['Go to Day '+x.day,'#/day/'+x.day])];d.setAttribute('aria-labelledby','dialog-title');d.innerHTML='<h2 id="dialog-title">Command center</h2><label>Find a page or day<input id="command-search" autofocus placeholder="Try Day 2 or bookmarks"></label><div class="command-list"></div><div class="actions">'+button('Switch theme','theme')+'<button data-close>Close</button></div>';const list=d.querySelector('.command-list'),input=d.querySelector('input');const draw=()=>{list.innerHTML=items.filter(([l])=>l.toLowerCase().includes(input.value.toLowerCase())).map(([l,h])=>link(l,h,'')).join('');};input.oninput=draw;list.onclick=e=>{if(e.target.closest('a'))d.close();};d.querySelector('[data-close]').onclick=()=>d.close();d.onclose=()=>before?.focus();draw();d.showModal();}
function cbtRender() {
  const cbtBody = document.querySelector('.cbt-question-body');
  const cbtPalette = document.querySelector('.cbt-palette');
  const scrollCache = {
    body: cbtBody ? cbtBody.scrollTop : 0,
    palette: cbtPalette ? cbtPalette.scrollTop : 0
  };
  render();
  const newCbtBody = document.querySelector('.cbt-question-body');
  const newCbtPalette = document.querySelector('.cbt-palette');
  if (newCbtBody) newCbtBody.scrollTop = scrollCache.body;
  if (newCbtPalette) newCbtPalette.scrollTop = scrollCache.palette;
}
const actions={
 'start-review':()=>startReview(),'review-one':v=>startReview(v),
 'start-now':()=>{let plan=startNowPlan(progress(),state.content);if(plan.kind==='resume'){go('#/quiz/'+plan.sessionId);return;}if(plan.kind==='new'){const minutes=sessionBudget(document.querySelector('#start-budget')?.value||'25',document.querySelector('#start-budget-custom')?.value);plan=startNowPlan(progress(),state.content,minutes);start(plan.config);return;}toast(plan.reason);},
 theme:()=>{state.progress.settings.theme=state.progress.settings.theme==='light'?'dark':'light';persist();render();},menu:()=>document.querySelector('.sidebar').classList.toggle('open'),commands,
 'start-day':v=>start({origin:'daily',day:Number(v),ids:state.content.sets.find(s=>s.day===Number(v)).questions.map(q=>q.id),count:10}),
 'start-paper':v=>{const p=state.content.papers.find(x=>x.id===v);state.clearSession();const draft=generatePaperSession(p,progress(),{mode:'practice'});state.addDraft(draft);unlockSound();go('#/quiz/'+draft.id);},
 'time-paper':v=>{const p=state.content.papers.find(x=>x.id===v);state.clearSession();const draft=generatePaperSession(p,progress(),{mode:'test'});state.addDraft(draft);unlockSound();go('#/quiz/'+draft.id);},
 'practice-one':v=>start({origin:'question',ids:[v],count:1}),
 'practice-ids':v=>start({origin:'review',ids:v.split(','),count:v.split(',').length}),
 answer,clear:()=>{const draft=active();if(draft){const id=draft.questionIds[draft.currentPosition];if(progress().attempts.some(attempt=>attempt.attemptId===draft.id+':'+id)){toast('This response is already recorded. Continue with the session.');return;}delete draft.answers[id];persist();cbtRender();}},
 'review-question':()=>{const draft=active();if(draft){const id=draft.questionIds[draft.currentPosition];draft.review[id]=!draft.review[id];persist();cbtRender();}},
 'exam-submit-confirm':()=>{const d=active();if(d){d.showSubmitConfirm=true;cbtRender();}},
 'nat-key':v=>{const d=active();if(d){const id=d.questionIds[d.currentPosition];let val=d.answers[id]||'';if(v==='Backspace')val=val.slice(0,-1);else if(v==='Clear All')val='';else val+=v;d.answers[id]=val;persist();cbtRender();}},
 'exam-modal':v=>{ui.examModal=ui.examModal===v?null:v;cbtRender();},
 'exam-submit-cancel':()=>{const d=active();if(d){d.showSubmitConfirm=false;cbtRender();}},
 'exam-submit-final': finish,
 previous:()=>jump(active().currentPosition-1),next:()=>jump(active().currentPosition+1),jump:v=>jump(Number(v)),submit:requestSubmit,
 focus:()=>{state.progress.settings.focus=!state.progress.settings.focus;persist();render();},
 'toggle-verify-question':async v=>{
    if(!v)return;
    if(!state.content.verification)state.content.verification={};
    const current=state.content.verification[v]?.status;
    const nextStatus=current==='verified'?'unverified':'verified';
    if(nextStatus==='verified'){
      state.content.verification[v]={status:'verified',verifiedAt:new Date().toISOString().slice(0,10)};
    } else {
      delete state.content.verification[v];
    }
    render();
    try{
      const res=await fetch('/api/ae/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({questionId:v,status:nextStatus})});
      const data=await res.json();
      if(data.ok){
        state.content.verification=data.verification;
        render();
        toast(nextStatus==='verified'?'Question marked as verified.':'Verification removed.');
      } else {
        toast(data.error||'Could not update verification.');
      }
    }catch(err){
      toast('Verification saved locally.');
    }
  },
 bookmark:openBookmark,'quick-bookmark':v=>{state.setBookmark(v,state.progress.bookmarks[v]?'':'Saved');render();},
 'add-notebook':notebookModal,'new-notebook':()=>{const old=state.progress.notebooks;modal('New notebook','<label>Name<input maxlength="80"></label>',d=>{const name=d.querySelector('input').value.trim();if(!name)throw Error('Enter a name.');old.push({id:crypto.randomUUID(),name,questionIds:[],updatedAt:new Date().toISOString()});persist();render();},'Create');},
 'rename-notebook':v=>{const n=state.progress.notebooks.find(n=>n.id===v);modal('Rename notebook',`<label>Name<input maxlength="80" value="${esc(n.name)}"></label>`,d=>{const name=d.querySelector('input').value.trim();if(!name)throw Error('Enter a name.');n.name=name;n.updatedAt=new Date().toISOString();persist();render();},'Save');},
 'delete-notebook':v=>modal('Delete notebook?','<p>Question history and personal notes will be kept.</p>',()=>{state.progress.notebooks=state.progress.notebooks.filter(n=>n.id!==v);persist();render();},'Delete notebook'),
 'remove-notebook-question':v=>{const [id,q]=v.split('|'),n=state.progress.notebooks.find(n=>n.id===id);n.questionIds=n.questionIds.filter(x=>x!==q);n.updatedAt=new Date().toISOString();persist();render();},
 'notebook-practice':v=>{const [id,mode]=v.split('|'),n=state.progress.notebooks.find(n=>n.id===id);const ids=n.questionIds.filter(q=>mode==='all'||mode==='new'&&!questionStats(state.progress,q).attempts.length||mode==='wrong'&&questionStats(state.progress,q).unresolved);start({origin:'notebook',ids,count:ids.length});},
 'new-card':newCard,'reveal-card':()=>{ui.revealedFlashcard=true;render();},'rate-card':v=>{const [id,rating]=v.split('|');reviewCard(progress().flashcards.find(c=>c.id===id),rating);persist();ui.revealedFlashcard=false;render();},
 'delete-card':v=>modal('Delete flashcard?','<p>This removes the card and its review schedule.</p>',()=>{state.progress.flashcards=state.progress.flashcards.filter(c=>c.id!==v);persist();render();},'Delete card'),
 retry:v=>{const r=state.progress.sessions.find(s=>s.id===v);start({origin:'retry',ids:r.questionIds,count:r.questionIds.length});},
 'retry-wrong':v=>{const ids=state.progress.attempts.filter(x=>x.sessionId===v&&x.correctness==='incorrect').map(x=>x.questionId);start({origin:'mistakes',ids,count:ids.length});},
 'time-session':v=>start({origin:'time-plan',prioritize:true,count:Math.max(1,Math.floor(Number(v)/2)),minutes:Number(v),mode:'practice'}),
 'question-day':()=>{const index=Math.floor(Date.now()/86400000)%state.content.questions.length;start({origin:'question-of-day',ids:[state.content.questions[index].id],count:1});},
 blueprint:v=>{const b=state.progress.blueprints.find(b=>b.id===v);start({...b,origin:'blueprint'});},
 'delete-blueprint':v=>{state.progress.blueprints=state.progress.blueprints.filter(b=>b.id!==v);persist();render();},
 share:async v=>{const url=location.href.split('#')[0]+'#/question/'+v;try{await navigator.clipboard.writeText(url);toast('Question link copied. Localhost links work on this computer.');}catch{modal('Question link',`<input aria-label="Question link" value="${esc(url)}" readonly>`,()=>{},'Done');}},
 report:v=>modal('Record a source issue','<p>This report is saved locally and included in your export. It is not sent anywhere.</p><label>What needs checking?<textarea maxlength="2000"></textarea></label>',d=>{const text=d.querySelector('textarea').value.trim();if(!text)throw Error('Describe the issue.');state.progress.reports.push({id:crypto.randomUUID(),questionId:v,text,createdAt:new Date().toISOString()});persist();toast('Source issue recorded locally.');},'Save report'),
 export:()=>exportData(),'export-raw':()=>{const raw=state.raw();if(raw===null)throw Error('No raw browser record is available to export.');const blob=new Blob([raw],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='gate-original-storage.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);},
 import:()=>document.querySelector('#import-file').click(),
 reset:v=>modal(v==='all'?'Reset everything?':'Reset '+(v==='xp'?'practice XP':'quiz progress')+'?',`<p>A backup will download first. ${v==='all'?'All progress, notes, bookmarks, cards, and settings will be removed from this browser.':'Your notes, cards, and bookmarks will stay.'}</p><label>Type RESET to confirm<input autocomplete="off"></label>`,d=>{if(d.querySelector('input').value!=='RESET')throw Error('Type RESET to confirm.');exportData();const fresh=defaults();if(v==='all')state.replaceProgress(fresh);else if(v==='xp'){progress().xpEvents=Object.fromEntries(Object.entries(progress().xpEvents).map(([k,x])=>[k,{...x,amount:0}]));persist();}else state.clearQuizProgress();navigate();},'Download backup & reset'),
 install:async()=>{if(ui.installEvent){await ui.installEvent.prompt();await ui.installEvent.userChoice;ui.installEvent=null;render();}}
};
document.addEventListener('click',async e=>{if(e.target.closest('.skip')){e.preventDefault();document.querySelector('#main')?.focus();document.querySelector('#main')?.scrollIntoView();return;}const el=e.target.closest('[data-action]');if(!el)return;try{unlockSound();await actions[el.dataset.action]?.(el.dataset.value);}catch(error){console.error(error);toast(error.message||'This action could not be completed.');}});
function updateBudgetPreview(e){if(e.target.id==='review-capacity'){const el=document.querySelector('#review-estimate');if(el){const n=Math.min(Number(el.dataset.dueCount),Number(e.target.value));el.textContent=n+' questions · about '+(n*2)+' min';}return;}if(!['start-budget','start-budget-custom'].includes(e.target.id))return;const select=document.querySelector('#start-budget'),custom=document.querySelector('#start-budget-custom'),show=select?.value==='custom';if(custom)custom.hidden=!show;if(e.target.id==='start-budget'&&show)custom?.focus();const minutes=show?Number(custom?.value):Number(select?.value),estimate=document.querySelector('#start-estimate'),available=Number(estimate?.dataset.available||0);if(estimate&&Number.isFinite(minutes)&&minutes>0)estimate.parentElement.innerHTML=`<strong id="start-estimate" data-available="${available}">${Math.min(available,Math.max(1,Math.floor(minutes/2)))} questions</strong>Planned for ${minutes} minutes`;}
document.addEventListener('change',updateBudgetPreview);
document.addEventListener('input',e=>{if(e.target.id==='start-budget-custom')updateBudgetPreview(e);if(e.target.id==='nat-answer'&&active()){try{const d=active();saveNumericAnswer(state,d,state.content.byId.get(d.questionIds[d.currentPosition]),e.target.value);const count=document.querySelector('#answered-count');if(count)count.textContent=d.questionIds.filter(id=>answered(d.answers[id])).length;}catch(error){toast(error.message);}}});
document.addEventListener('submit',e=>{const f=e.target;if(!['practice-form','settings-form','planner-form','note-form','bank-form'].includes(f.id))return;e.preventDefault();try{const data=Object.fromEntries(new FormData(f));if(f.id==='bank-form'){go('#/bank?'+new URLSearchParams(data));return;}if(f.id==='note-form'){state.setNote(f.dataset.id,data.note);toast('Note saved.');return;}if(f.id==='settings-form'){Object.assign(state.progress.settings,{theme:data.theme,goal:Number(data.goal),volume:Number(data.volume),preferredMode:data.preferredMode,...Object.fromEntries(['sound','checkpointSound','checkpoint','shortcuts'].map(k=>[k,!!data[k]]))});state.progress.profile.name=data.name;persist();render();toast('Preferences saved.');return;}if(f.id==='planner-form'){state.progress.planner={exam:data.exam,date:data.date,minutes:Number(data.minutes)};state.progress.settings.goal=Number(data.goal);persist();render();toast('Plan saved.');return;}if(f.id==='practice-form'){const config={...data,count:Number(data.count),minutes:Number(data.minutes),origin:'custom'};if(e.submitter?.value==='save'){if(!data.name.trim())throw Error('Give this blueprint a name.');state.progress.blueprints.push({...config,id:crypto.randomUUID()});persist();render();toast('Blueprint saved.');}else start(config);}}catch(error){toast(error.message);}});
document.addEventListener('change',async e=>{try{if(e.target.id==='import-file'){const file=e.target.files[0];if(!file)return;if(file.size>20*1024*1024)throw Error('Backup exceeds the 20 MB limit.');const next=validateState(JSON.parse(await file.text()));const known=new Set(state.content.questions.map(q=>q.id));if(next.attempts.some(x=>!known.has(x.questionId))||Object.values(next.drafts).some(d=>d.questionIds.some(id=>!known.has(id))))throw Error('Backup references questions outside this archive. Existing data is unchanged.');modal('Replace local progress?',`<p>This backup contains ${next.sessions.length} sessions, ${next.attempts.length} attempt records, and ${Object.keys(next.notes).length} notes. Your current data will download before replacement.</p>`,()=>{exportData();state.replaceProgress(next);navigate();toast('Backup imported.');},'Back up & import');}}catch(error){toast(error.message||'Could not read this backup.');}});
document.addEventListener('keydown',e=>{if(document.querySelector('#product-moment[open]'))return;if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();commands();return;}if(e.target.closest('input,textarea,select,[contenteditable="true"]')||document.querySelector('dialog[open]')||!active()||!progress().settings.shortcuts||e.ctrlKey||e.metaKey||e.altKey)return;const k=e.key.toLowerCase(),q=state.content.byId.get(active().questionIds[active().currentPosition]),choice=optionShortcut(q,k);const map={...(choice?{[k]:()=>answer(choice)}:{}),arrowleft:actions.previous,arrowright:actions.next,r:actions['review-question'],c:actions.clear,s:actions.submit};if(map[k]){e.preventDefault();try{map[k]();}catch(error){toast(error.message);}}});
window.addEventListener('hashchange',()=>{try{navigate();}catch(error){console.error(error);toast('This page could not be opened. Return Home or reload.');}});
window.addEventListener('popstate',()=>{try{navigate();}catch(error){toast('Could not restore this page.');}});
document.addEventListener('visibilitychange',()=>{const clockState=timer();if(!clockState)return;if(document.hidden){clockState.stop();try{persist();}catch(e){toast(e.message);}}else{clockState.start();if(active()?.mode==='test'&&clockState.expired())finish();}});
window.addEventListener('pagehide',()=>{if(timer()){timer().stop();try{persist();}catch{}}});
window.addEventListener('storage',e=>{if(e.key===STORAGE_KEY){ui.conflict=true;timer()?.stop();render();}});
for(const event of ['online','offline'])window.addEventListener(event,()=>{const el=document.querySelector('#connection');if(el)el.textContent=navigator.onLine?'Saved on this browser':'Offline · Local workspace';});
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();ui.installEvent=e;if(route().parts[0]==='settings')render();});
setInterval(()=>{if(!state.content||ui.conflict)return;try{
 for(const draft of Object.values(progress().drafts))if(draft.mode==='test'&&draft.deadline<=Date.now()){
  if(active()?.id===draft.id){finish();toast('Time is up. Your session was submitted.');return;}
  state.completeSession(draft,state.content.byId);state.takeProductMoment(draft.id);render();toast('A timed test reached its deadline and was saved to history.');
 }
 if(active()&&timer()&&!document.hidden){timer().flush();updateTimer();if(++ui.saveTick%5===0)persist();}
}catch(e){toast(e.message);}},1000);
async function registerOffline(){if(!('serviceWorker' in navigator))return;try{const reg=await navigator.serviceWorker.register('sw.js');const ready=()=>{ui.offlineReady=true;if(route().parts[0]==='settings')render();};navigator.serviceWorker.addEventListener('message',e=>{if(e.data==='OFFLINE_READY')ready();});navigator.serviceWorker.controller?.postMessage('STATUS');reg.active?.postMessage('STATUS');}catch(e){console.warn('Offline caching unavailable',e);}}

loadArchive().then(a=>{state.initializeContent(a);navigate();registerOffline();}).catch(e=>{console.error(e);document.querySelector('#app').innerHTML='<main><h1>Could not load the question archive.</h1><p>Open this project with a local web server, then reload.</p><button onclick="location.reload()">Retry</button></main>';});
