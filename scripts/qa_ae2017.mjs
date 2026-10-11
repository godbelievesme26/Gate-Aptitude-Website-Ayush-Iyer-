import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2017() {
  console.log('--- Running Browser QA for AE2017 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2017-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9237',
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
        const res = await fetch('http://127.0.0.1:9237/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2017
    console.log('Navigating to AE2017 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2017' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail GA Q10 (Contour map)
    console.log('Navigating to AE2017 GA Q10...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2017-ae-ga-10' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_03_ga_q10_figure.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q09 / Q19 (T-s diagram)
    console.log('Navigating to AE2017 AE Q19...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2017-ae-ae-19' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_04_q19_ts_figure.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q38 / Q48 (Cm vs alpha graph)
    console.log('Navigating to AE2017 AE Q48...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2017-ae-ae-48' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_05_q48_cm_alpha.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q54 / Q64 (2-cell wing box shear flow)
    console.log('Navigating to AE2017 AE Q64...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2017-ae-ae-64' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2017_qa_06_q64_wingbox.png'), Buffer.from(res.data, 'base64'));

    console.log('Browser QA completed successfully for AE2017!');
  } finally {
    try { chrome.kill(); } catch (e) {}
  }
}

runQA2017().catch(err => {
  console.error(err);
  process.exit(1);
});
