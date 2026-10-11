import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function testAudit() {
  console.log('--- Testing Live 4173 Server ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'audit-chrome-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9229/json/list');
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

  // Step 1: Open Aerospace PYQs -> GATE 2026
  console.log('Navigating to http://127.0.0.1:4173/#/aerospace/2026');
  await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2026' });
  await new Promise(r => setTimeout(r, 1200));
  let res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_01_aerospace_2026_overview.png'), Buffer.from(res.data, 'base64'));

  // Step 2: Click Timed Test (CBT Mode)
  console.log('Entering Timed Test (CBT mode)');
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="time-paper"]').click()`
  });
  await new Promise(r => setTimeout(r, 1200));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_02_cbt_q1_initial.png'), Buffer.from(res.data, 'base64'));

  // Check button exists
  const btnInfo = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.querySelector('[data-action="toggle-verify-question"]');
      return btn ? { text: btn.textContent.trim(), val: btn.dataset.value } : null;
    })()`,
    returnByValue: true
  });
  console.log('Button info in CBT Q1:', btnInfo.result.value);

  // Step 3: Click Mark as Verified on Q1
  console.log('Clicking Mark as Verified');
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="toggle-verify-question"]').click()`
  });
  await new Promise(r => setTimeout(r, 800));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_03_cbt_q1_verified.png'), Buffer.from(res.data, 'base64'));

  // Step 4: Advance to Q2
  console.log('Clicking Save & Next to advance to Q2');
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="next"]').click()`
  });
  await new Promise(r => setTimeout(r, 800));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_04_cbt_q2_initial.png'), Buffer.from(res.data, 'base64'));

  // Step 5: Mark Q2 Verified as well
  console.log('Clicking Mark as Verified on Q2');
  await send('Runtime.evaluate', {
    expression: `document.querySelector('[data-action="toggle-verify-question"]').click()`
  });
  await new Promise(r => setTimeout(r, 800));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_05_cbt_q2_verified.png'), Buffer.from(res.data, 'base64'));

  // Step 6: Navigate back to Paper Overview
  console.log('Navigating back to Paper Overview');
  await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2026' });
  await new Promise(r => setTimeout(r, 1200));
  res = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(ARTIFACTS_DIR, 'audit_06_aerospace_2026_updated_counter.png'), Buffer.from(res.data, 'base64'));

  ws.close();
  chrome.kill();
  console.log('--- ALL AUDIT TESTS COMPLETED ---');
}

testAudit().catch(e => { console.error('Audit failed:', e); process.exit(1); });
