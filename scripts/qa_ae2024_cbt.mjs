import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runCBTTest() {
  console.log('--- Testing CBT / Timed Test Flow for AE2024 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-cbt-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9231',
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
        const res = await fetch('http://127.0.0.1:9231/json/list');
        const tabs = await res.json();
        const pageTab = tabs.find(t => t.type === 'page');
        if (pageTab && pageTab.webSocketDebuggerUrl) {
          wsUrl = pageTab.webSocketDebuggerUrl;
          break;
        }
      } catch (e) {}
    }

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

    // 1. Navigate to AE2024 overview
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2024' });
    await new Promise(r => setTimeout(r, 1500));

    // 2. Click "Timed Test" button (data-action="time-paper")
    await send('Runtime.evaluate', {
      expression: `document.querySelector('button[data-action="time-paper"]').click()`
    });
    await new Promise(r => setTimeout(r, 2000));

    let res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2024_qa_05_cbt_timed_test.png'), Buffer.from(res.data, 'base64'));

    ws.close();
    console.log('Timed test screenshot captured!');
  } finally {
    chrome.kill();
  }
}

runCBTTest().catch(err => {
  console.error(err);
  process.exit(1);
});
