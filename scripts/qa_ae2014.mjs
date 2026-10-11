import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2014() {
  console.log('--- Running Browser QA for AE2014 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2014-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9240',
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
        const res = await fetch('http://127.0.0.1:9240/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2014
    console.log('Navigating to AE2014 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2014' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail GA Q10 (Monthly rainfall chart)
    console.log('Navigating to AE2014 GA Q10...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2014-ae-ga-10' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_03_ga_q10_rainfall.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q7 (Diamond airfoil)
    console.log('Navigating to AE2014 AE Q17...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2014-ae-ae-17' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_04_q17_diamond.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q13 (Mohr stress option figures)
    console.log('Navigating to AE2014 AE Q23...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2014-ae-ae-23' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_05_q23_option_figures.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q38 (Steel beam with overhangs)
    console.log('Navigating to AE2014 AE Q48...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2014-ae-ae-48' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_06_q48_beam.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q43 (Spring mass on beam)
    console.log('Navigating to AE2014 AE Q53...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2014-ae-ae-53' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2014_qa_07_q53_spring_beam.png'), Buffer.from(res.data, 'base64'));

    console.log('Browser QA completed successfully for AE2014!');
  } finally {
    try { chrome.kill(); } catch (e) {}
  }
}

runQA2014().catch(err => {
  console.error(err);
  process.exit(1);
});
