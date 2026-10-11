import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2022() {
  console.log('--- Running Browser QA for AE2022 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2022-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9232',
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
        const res = await fetch('http://127.0.0.1:9232/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2022
    console.log('Navigating to AE2022 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2022' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail Q2 (number line options)
    console.log('Navigating to AE2022 Q2...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2022-ae-ga-02' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_03_q2_options.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail Q16 (flat plate figure)
    console.log('Navigating to AE2022 Q16...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2022-ae-ae-16' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_04_q16_figure.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail Q55 (expansion waves nozzle)
    console.log('Navigating to AE2022 Q55...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2022-ae-ae-55' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_05_q55_figure.png'), Buffer.from(res.data, 'base64'));

    // 6. Timed Test (CBT mode)
    console.log('Starting CBT timed test...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2022' });
    await new Promise(r => setTimeout(r, 1500));
    await send('Runtime.evaluate', {
      expression: `document.querySelector('button[data-action="time-paper"]').click()`
    });
    await new Promise(r => setTimeout(r, 2000));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2022_qa_06_cbt.png'), Buffer.from(res.data, 'base64'));

    ws.close();
    console.log('All AE2022 QA screenshots captured successfully!');
  } finally {
    chrome.kill();
  }
}

runQA2022().catch(err => {
  console.error(err);
  process.exit(1);
});
