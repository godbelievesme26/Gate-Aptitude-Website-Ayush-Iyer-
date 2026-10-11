import fs from 'node:fs';import {execFileSync} from 'node:child_process';
for(const dir of ['js','scripts','tests'])for(const file of fs.readdirSync(dir).filter(f=>/\.(mjs|js)$/.test(f)))execFileSync(process.execPath,['--check',`${dir}/${file}`]);
execFileSync(process.execPath,['--check','sw.js']);console.log('PASS: JavaScript syntax');
