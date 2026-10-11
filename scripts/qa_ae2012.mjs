import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2012() {
  console.log('--- Running Browser QA for AE2012 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2012-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9242',
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
        const res = await fetch('http://127.0.0.1:9242/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2012
    console.log('Navigating to AE2012 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2012' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q02 (diff eq)
    console.log('Navigating to AE2012 AE Q02...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-02' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_03_q02_diff_eq.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q13 (sqrt diff eq)
    console.log('Navigating to AE2012 AE Q13...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-13' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_04_q13_sqrt.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q26 (trapezoidal NAT)
    console.log('Navigating to AE2012 AE Q26...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-26' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_05_q26_trapezoidal_nat.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q30 (2-DOF mode shapes NAT)
    console.log('Navigating to AE2012 AE Q30...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-30' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_06_q30_mode_shapes_nat.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q33 (matrix eigenvalue)
    console.log('Navigating to AE2012 AE Q33...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-33' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_07_q33_matrix.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q48 (Common Data)
    console.log('Navigating to AE2012 AE Q48...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ae-48' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_08_q48_common_data.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail GA Q62 (table)
    console.log('Navigating to AE2012 GA Q62...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2012-ae-ga-62' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2012_qa_09_q62_table.png'), Buffer.from(res.data, 'base64'));

    console.log('AE2012 Browser QA Complete! All screenshots captured.');
    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

runQA2012().catch(e => {
  console.error(e);
  process.exit(1);
});
