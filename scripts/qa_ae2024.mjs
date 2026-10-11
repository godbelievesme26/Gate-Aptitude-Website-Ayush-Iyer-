import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA() {
  console.log('--- Running Browser QA for AE2024 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9230',
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
        const res = await fetch('http://127.0.0.1:9230/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2024
    console.log('Navigating to AE2024 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2024' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail Q14 (has vibration curve)
    console.log('Navigating to AE2024 Q14...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2024-ae-ae-14' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_03_q14.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail Q20 (option figures)
    console.log('Navigating to AE2024 Q20...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2024-ae-ae-20' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_04_q20_option_figs.png'), Buffer.from(res.data, 'base64'));

    // 5. CBT Mock interface
    console.log('Navigating to AE2024 CBT...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/cbt/gate-2024-ae' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_05_cbt.png'), Buffer.from(res.data, 'base64'));

    ws.close();
    console.log('All QA screenshots captured successfully!');
  } finally {
    chrome.kill();
  }
}

runQA().catch(err => {
  console.error(err);
  process.exit(1);
});
