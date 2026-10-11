import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2009() {
  console.log('--- Running Browser QA for AE2009 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2009-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  try {
    let wsUrl = null;
    for (let i = 0; i < 30; i++) {
      await new Promise(r => setTimeout(r, 300));
      try {
        const res = await fetch('http://127.0.0.1:9245/json/list');
        const tabs = await res.json();
        const pageTab = tabs.find(t => t.type === 'page');
        if (pageTab && pageTab.webSocketDebuggerUrl) {
          wsUrl = pageTab.webSocketDebuggerUrl;
          break;
        }
      } catch (e) {}
    }

    if (!wsUrl) throw new Error('Could not connect to Chrome debugging port');

    const ws = new WebSocket(wsUrl);
    let id = 1;
    const pending = new Map();
    ws.onmessage = msg => {
      const data = JSON.parse(msg.data);
      if (data.id && pending.has(data.id)) {
        const { resolve, reject } = pending.get(data.id);
        pending.delete(data.id);
        if (data.error) reject(data.error);
        else resolve(data.result);
      }
    };
    await new Promise(r => ws.onopen = r);

    function send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const msgId = id++;
        pending.set(msgId, { resolve, reject });
        ws.send(JSON.stringify({ id: msgId, method, params }));
      });
    }

    await send('Page.enable');
    await send('Runtime.enable');

    // 1. Hub
    console.log('Navigating to Hub...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace' });
    await new Promise(r => setTimeout(r, 1500));
    let res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2009
    console.log('Navigating to AE2009 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2009' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q01 (Prandtl-Meyer)
    console.log('Navigating to AE2009 AE Q01...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-01' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_03_q01_prandtl_meyer.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q19 (rectangular tube figure)
    console.log('Navigating to AE2009 AE Q19...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-19' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_04_q19_tube_fig.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q20 (shear center beam figure)
    console.log('Navigating to AE2009 AE Q20...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-20' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_05_q20_shear_centre.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q36 (variable area duct)
    console.log('Navigating to AE2009 AE Q36...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-36' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_06_q36_duct.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q37 (vortices)
    console.log('Navigating to AE2009 AE Q37...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-37' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_07_q37_vortices.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q39 (beam & BMD diagrams)
    console.log('Navigating to AE2009 AE Q39...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-39' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_08_q39_bmd.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail AE Q42 (booms)
    console.log('Navigating to AE2009 AE Q42...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-42' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_09_q42_booms.png'), Buffer.from(res.data, 'base64'));

    // 10. Question Detail AE Q44 (2-celled tube)
    console.log('Navigating to AE2009 AE Q44...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-44' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_10_q44_twocells.png'), Buffer.from(res.data, 'base64'));

    // 11. Question Detail AE Q59 (piston compressing air)
    console.log('Navigating to AE2009 AE Q59...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2009-ae-ae-59' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2009_qa_11_q59_piston.png'), Buffer.from(res.data, 'base64'));

    console.log('AE2009 Browser QA Complete! All 11 screenshots captured.');
    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

runQA2009().catch(e => {
  console.error(e);
  process.exit(1);
});
