import {loadArchive} from '../../js/loader.js';
import {defaults} from '../../js/storage.js';
import {generateSession,submit} from '../../js/domain.js';
import {createSessionTimer} from '../../js/timer.js';
import {quiz,result} from '../../js/views.js';

// This harness only renders in-memory scenarios. It never imports the app or Store.
const archive=await loadArchive(),questionSelect=document.querySelector('#fixture-question');
const motionToggle=document.createElement('label');motionToggle.className='check-label';motionToggle.innerHTML='<input id="fixture-reduced" type="checkbox">Test reduced motion';document.querySelector('.fixture-controls').append(motionToggle);
const motionStyle=document.createElement('style');document.head.append(motionStyle);
function reducedMotion(){
 // Apply the real reduced-motion declarations in this fixture only. The browser
 // control API cannot emulate OS media preferences; no production CSS is changed.
 const rules=[...document.styleSheets].filter(s=>s!==motionStyle.sheet).flatMap(s=>[...s.cssRules]).filter(r=>r.conditionText?.includes('prefers-reduced-motion:reduce')||r.conditionText?.includes('prefers-reduced-motion: reduce'));
 motionStyle.textContent=document.querySelector('#fixture-reduced').checked?rules.flatMap(r=>[...r.cssRules].map(x=>x.cssText)).join('\n'):'';
}
questionSelect.innerHTML=archive.questions.slice(0,10).map((q,i)=>`<option value="${i}">Source question ${q.number}</option>`).join('');
function render(){
 const state=defaults(),scenario=document.querySelector('#fixture-scenario').value;
 document.documentElement.dataset.theme=document.querySelector('#fixture-theme').value;
 const questions=archive.questions.slice(Number(questionSelect.value),Number(questionSelect.value)+4),a={...archive,questions,byId:new Map(questions.map(q=>[q.id,q]))};
 if(scenario==='feedback'){
  // Keys exist only on isolated copies for visual grading coverage.
  const qs=questions.map((q,i)=>({...q,type:'MCQ',...(i<2?{answer:'B'}:{})})),fixture={...a,questions:qs,byId:new Map(qs.map(q=>[q.id,q]))};
  const d=generateSession(qs,state,{count:4},'visual-feedback');d.answers[qs[0].id]='B';d.answers[qs[1].id]='A';d.answers[qs[2].id]='C';d.elapsed=186000;
  submit(state,d,fixture.byId);document.querySelector('#main').innerHTML=result(state,fixture,d.id);return;
 }
 const d=generateSession(questions,state,{count:4,mode:scenario==='test'?'test':'practice',minutes:25},'visual-question');
 d.elapsed=82000;d.times[questions[0].id]=42000;
 if(['selected','busy','answer-states'].includes(scenario))d.answers[questions[0].id]='B';
 const timer=createSessionTimer(d,()=>Date.now());
 document.querySelector('#main').innerHTML=quiz(state,a,d,timer);
 document.querySelector('.question-surface').classList.add('question-enter');
 if(scenario==='busy'){const action=document.querySelector('.solve-actions .primary');action.setAttribute('aria-busy','true');action.disabled=true;action.textContent='Saving…';document.querySelectorAll('.option').forEach(el=>{el.disabled=true;});}
 if(scenario==='answer-states')for(const [index,status,mark] of [[0,'correct','✓'],[1,'incorrect','×']]){const el=document.querySelectorAll('.option')[index];el.dataset.feedback=status;el.querySelector('.option-state').textContent=status==='correct'?'Correct':'Incorrect';el.querySelector('.option-indicator').textContent=mark;el.setAttribute('aria-label',`Option ${el.dataset.value}, ${status}`);}
}
document.querySelector('.fixture-controls').addEventListener('change',()=>{render();reducedMotion();});render();
