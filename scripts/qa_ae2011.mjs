import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2011() {
  console.log('--- Running Browser QA for AE2011 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2011-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9243',
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
        const res = await fetch('http://127.0.0.1:9243/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2011
    console.log('Navigating to AE2011 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2011' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q01 (curl)
    console.log('Navigating to AE2011 AE Q01...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-01' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_03_q01_curl.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q11 (beam figure)
    console.log('Navigating to AE2011 AE Q11...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-11' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_04_q11_beam_fig.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q26 (NAT cantilever beam)
    console.log('Navigating to AE2011 AE Q26...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-26' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_05_q26_nat_beam.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q37 (Airy stress function)
    console.log('Navigating to AE2011 AE Q37...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-37' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_06_q37_airy_fig.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q44 (expansion corner)
    console.log('Navigating to AE2011 AE Q44...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-44' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_07_q44_expansion_corner.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q48 (Common Data)
    console.log('Navigating to AE2011 AE Q48...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-48' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_08_q48_common_data.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail AE Q52 (Linked Answer table)
    console.log('Navigating to AE2011 AE Q52...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ae-52' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_09_q52_linked_table.png'), Buffer.from(res.data, 'base64'));

    // 10. Question Detail GA Q64 (Bullseye target & scores)
    console.log('Navigating to AE2011 GA Q64...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2011-ae-ga-64' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2011_qa_10_q64_target_table.png'), Buffer.from(res.data, 'base64'));

    console.log('AE2011 Browser QA Complete! All 10 screenshots captured.');
    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

runQA2011().catch(e => {
  console.error(e);
  process.exit(1);
});
