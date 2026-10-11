import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read=path=>fs.readFileSync(path,'utf8');

test('semantic visual system is loaded and available offline',()=>{
 const index=read('index.html'),worker=read('sw.js');
 assert.match(index,/css\/system\.css/);
 assert.match(index,/css\/components\.css/);
 assert.match(worker,/css\/system\.css/);
 assert.match(worker,/css\/components\.css/);
 assert.match(index,/css\/home\.css/);
 assert.match(worker,/css\/home\.css/);
});

test('component system defines surfaces, control states, icons and restrained motion',()=>{
 const css=read('css/components.css'),app=read('js/app.js'),home=read('js/home.js');
 for(const name of ['surface-plain','surface-subtle','surface-elevated','surface-bordered','surface-emphasis'])assert.match(css,new RegExp('\\.'+name));
 for(const name of ['primary','secondary','ghost','destructive','icon-button','selected'])assert.match(css,new RegExp('\\.'+name));
 assert.match(css,/button:disabled/);
 assert.match(css,/button\[aria-busy=true\]/);
 assert.match(css,/@media\(prefers-reduced-motion:reduce\)/);
 assert.match(app,/const navGroups=/);
 assert.match(app,/class="ui-icon"/);
 assert.match(home,/aria-labelledby="recommended-title"/);
 assert.match(home,/class="home-action"/);
 assert.match(home,/class="home-stats"/);
});

test('visual tokens cover both themes and core semantic roles',()=>{
 const css=read('css/system.css');
 for(const token of ['color-canvas','color-surface','color-surface-elevated','color-text','color-text-muted','color-border','color-accent','color-success','color-warning','color-error','color-focus','space-1','space-16','radius-panel','shadow-panel','text-page','text-section','text-body','text-stat','text-timer','focus-ring'])assert.match(css,new RegExp('--'+token+':'),token);
 assert.match(css,/\[data-theme=dark\]/);
 assert.match(css,/\[hidden\]\{display:none!important\}/);
 assert.match(css,/@media\(max-width:680px\)/);
});
