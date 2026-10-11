import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { server } from './serve.mjs';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function test() {
  const PORT = 4180;
  await new Promise(r => server.listen(PORT, '127.0.0.1', r));
  const profileDir = path.join(process.cwd(), 'tmp', 'test-cbt-btn-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9228',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9228/json/list');
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

  // 1. Navigate to /#/aerospace/2026
  await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/aerospace/2026` });
  await new Promise(r => setTimeout(r, 1000));
  let res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'verify_ui_01_paper_overview.png'), Buffer.from(res.data, 'base64'));

  // 2. Click Timed Test to enter TCS CBT mock mode
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="time-paper"]').click()`
  });
  await new Promise(r => setTimeout(r, 1000));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'verify_ui_02_cbt_unverified.png'), Buffer.from(res.data, 'base64'));

  // 3. Click the verify button inside CBT mode!
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="toggle-verify-question"]').click()`
  });
  await new Promise(r => setTimeout(r, 800));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'verify_ui_03_cbt_verified.png'), Buffer.from(res.data, 'base64'));

  // 4. Open Question Detail
  await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/question/gate-2026-ae-ga-01` });
  await new Promise(r => setTimeout(r, 1000));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'verify_ui_04_question_detail.png'), Buffer.from(res.data, 'base64'));

  ws.close();
  chrome.kill();
  server.close();
  console.log('SUCCESS: Captured all UI verification screenshots');
}

test().catch(e => { console.error(e); process.exit(1); });
