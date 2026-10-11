import {loadArchive} from '../../js/loader.js';
import {defaults} from '../../js/storage.js';
import {generateSession} from '../../js/domain.js';
import {home} from '../../js/home.js';
// Presentation-only states: never import Store or the app; never write progress.
const archive=await loadArchive(),motionStyle=document.createElement('style');document.head.append(motionStyle);
function render(){
 const s=defaults(),scenario=document.querySelector('#scenario').value;
 if(scenario==='resume'){const draft=generateSession(archive.questions,s,{count:5,mode:'test',minutes:25},'fixture-home');draft.currentPosition=2;draft.answers[draft.questionIds[0]]='B';s.drafts[draft.id]=draft;}
 document.documentElement.dataset.theme=document.querySelector('#theme').value;
 document.querySelector('#main').innerHTML=home(s,scenario==='unavailable'?{questions:[],sets:[],byId:new Map()}:archive);
 const rules=[...document.styleSheets].filter(x=>x!==motionStyle.sheet).flatMap(x=>[...x.cssRules]).filter(x=>x.conditionText?.replaceAll(' ','').includes('prefers-reduced-motion:reduce'));
 motionStyle.textContent=document.querySelector('#reduce').checked?rules.flatMap(x=>[...x.cssRules].map(r=>r.cssText)).join('\n'):'';
}
document.querySelector('header').addEventListener('change',render);render();
