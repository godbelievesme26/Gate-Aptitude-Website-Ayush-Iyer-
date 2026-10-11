const CACHE='gate-workspace-v31';
const SHELL=['./','index.html','css/style.css','css/quiz.css','css/home.css','css/moments.css','css/revision.css','css/system.css','css/components.css','js/app.js','js/home.js','js/views.js','js/state.js','js/moments.js','js/revision.js','js/revision-view.js','js/moment-view.js','js/question-content.js','js/ui.js','js/loader.js','js/storage.js','js/domain.js','js/scoring.js','js/timer.js','manifest.webmanifest','assets/logo.svg','assets/icon-192.png','assets/icon-512.png','data/registry.json'];
self.addEventListener('install',event=>event.waitUntil((async()=>{
 const cache=await caches.open(CACHE);await cache.addAll([...SHELL,'js/corpus.js','js/answer-input.js','data/ae/manifest.json','data/ae/verification.json']);
 const registry=await (await cache.match('data/registry.json')).json();
 for(const entry of registry){await cache.add(entry.path);const set=await (await cache.match(entry.path)).json();await cache.addAll(set.questions.flatMap(q=>[...(q.figures||[]).map(f=>f.src),...q.options.filter(o=>o.figure).map(o=>o.figure.src)]));}
 const manifest=await (await cache.match('data/ae/manifest.json')).json();
 for(const entry of manifest.years.filter(entry=>entry.ingestionStatus==='complete')){await cache.add(entry.path);const paper=await (await cache.match(entry.path)).json();await cache.addAll([...new Set(paper.questions.flatMap(q=>[...(q.figures||[]).map(f=>f.src),...q.options.filter(o=>o.figure).map(o=>o.figure.src)]))]);}
 await cache.put('offline-ready',new Response('ready'));await self.skipWaiting();
})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('gate-workspace-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();for(const client of await self.clients.matchAll())client.postMessage('OFFLINE_READY');})()));
self.addEventListener('message',event=>{if(event.data==='STATUS')event.waitUntil((async()=>{const cache=await caches.open(CACHE);if(await cache.match('offline-ready'))event.source?.postMessage('OFFLINE_READY');})());});
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);if(event.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.includes('/internal/')||/\.(pdf|zip)$/i.test(url.pathname)||url.pathname.includes('/Aptitude%20Sets/')||url.pathname.includes('/Aptitude Sets/'))return;
 event.respondWith((async()=>{const cache=await caches.open(CACHE);if(/\/figures\//.test(url.pathname)){const existing=await cache.match(event.request);if(existing)return existing;}
 try{const response=await fetch(event.request);if(response.ok)await cache.put(event.request,response.clone());return response;}catch{const cached=await cache.match(event.request);if(cached)return cached;if(event.request.mode==='navigate')return await cache.match('index.html');return new Response('Unavailable offline',{status:503});}})());
});

