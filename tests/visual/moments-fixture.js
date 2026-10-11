import {loadArchive} from '../../js/loader.js';
import {Store,STORAGE_KEY} from '../../js/storage.js';
import {ApplicationState} from '../../js/state.js';
import {generateSession} from '../../js/domain.js';
import {showProductMoment} from '../../js/moment-view.js';
const archive=await loadArchive(),motionStyle=document.createElement('style');document.head.append(motionStyle);
document.querySelector('#home-link').href='/#/home';
function fixture(){
 let raw=null;const adapter={getItem:()=>raw,setItem(k,v){raw=v;}},state=new ApplicationState(new Store(adapter)),scenario=document.querySelector('#scenario').value,now=new Date();
 const q=archive.questions[0],historyCount={ordinary:1,seven:6,hundred:99,goal:1,session:1}[scenario]||0;
 state.progress.settings.theme=document.querySelector('#theme').value;state.progress.settings.goal=scenario==='goal'?2:1000;state.initializeContent(archive);
 const draft=(id,date)=>{const d=generateSession([q],state.progress,{ids:[q.id],count:1},id);d.startedAt=date.toISOString();d.answers[q.id]=q.answer;d.elapsed=84000;state.addDraft(d);return d;};
 for(let i=0;i<historyCount;i++){const date=new Date(now);if(!['goal','session'].includes(scenario))date.setDate(date.getDate()-historyCount+i);const d=draft(`qa-history-${i}`,date);state.completeSession(d,archive.byId,date);state.takeProductMoment(d.id);}
 const d=draft('qa-current',now);delete d.answers[q.id];state.save();return {state,d,now,q};
}
function appearance(){document.documentElement.dataset.theme=document.querySelector('#theme').value;const rules=[...document.styleSheets].filter(s=>s!==motionStyle.sheet).flatMap(s=>[...s.cssRules]).filter(r=>r.conditionText?.replaceAll(' ','').includes('prefers-reduced-motion:reduce'));motionStyle.textContent=document.querySelector('#reduce').checked?rules.flatMap(r=>[...r.cssRules].map(x=>x.cssText)).join('\n'):'';}
document.querySelector('#theme').onchange=appearance;document.querySelector('#reduce').onchange=appearance;
document.querySelector('#preview').onclick=()=>{appearance();const {state,d,now,q}=fixture();d.answers[q.id]=q.answer;const r=state.completeSession(d,archive.byId,now);showProductMoment(state.takeProductMoment(r.id));document.querySelector('#status').textContent='Preview derived through ApplicationState.completeSession; memory-only storage.';};
document.querySelector('#launch').onclick=()=>{if(location.port!=='4186'){document.querySelector('#status').textContent='Blocked: only the disposable test server on port 4186 may prepare app state.';return;}const {state,d}=fixture();localStorage.setItem(STORAGE_KEY,JSON.stringify(state.progress));location.href='/#/quiz/'+d.id;};appearance();

document.querySelectorAll("#preview,#launch").forEach(b=>b.disabled=false);
document.querySelector("#status").textContent="Ready — isolated fixture controls loaded.";
