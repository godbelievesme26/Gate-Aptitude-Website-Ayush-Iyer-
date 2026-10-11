export const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const button=(text,action,value='',style='')=>`<button class="${style}" data-action="${action}" data-value="${esc(value)}">${text}</button>`;
export const link=(text,href,style='button')=>`<a class="${style}" href="${esc(href)}">${text}</a>`;
export const empty=(title,text,action='')=>`<div class="empty"><strong>${title}</strong><p>${text}</p>${action}</div>`;
export const head=(title,subtitle='',extra='')=>`<div class="page-head"><div><h1>${title}</h1><p>${subtitle}</p></div>${extra}</div>`;
export const metric=(value,label)=>`<div class="metric"><strong>${value}</strong><span>${label}</span></div>`;
export const formatDate=value=>new Date(value).toLocaleDateString(undefined,{day:'numeric',month:'short',year:'numeric'});
let toastTimeout;
export function toast(message){const el=document.querySelector('#toast');el.textContent=message;el.style.display='block';clearTimeout(toastTimeout);toastTimeout=setTimeout(()=>el.style.display='none',5000);}
export function modal(title,body,action,label='Confirm'){const d=document.querySelector('#dialog');if(d.open)return;const before=document.activeElement;d.setAttribute('aria-labelledby','dialog-title');d.innerHTML=`<h2 id="dialog-title">${esc(title)}</h2>${body}<div class="actions"><button data-dialog-close>Cancel</button><button class="primary" data-dialog-confirm>${label}</button></div>`;const confirm=d.querySelector('[data-dialog-confirm]');let pending=false;d.querySelector('[data-dialog-close]').onclick=()=>d.close();confirm.onclick=async()=>{if(pending)return;pending=true;confirm.disabled=true;confirm.setAttribute('aria-busy','true');try{await action(d);d.close();}catch(e){pending=false;confirm.disabled=false;confirm.removeAttribute('aria-busy');toast(e.message);}};d.onclose=()=>before?.focus();d.showModal();}
