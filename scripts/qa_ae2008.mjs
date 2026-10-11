import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2008() {
  console.log('--- Running Browser QA for AE2008 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2008-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9246',
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
        const res = await fetch('http://127.0.0.1:9246/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2008
    console.log('Navigating to AE2008 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2008' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q01
    console.log('Navigating to AE2008 AE Q01...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-01' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_03_q01_math.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q32 (Cm vs alpha)
    console.log('Navigating to AE2008 AE Q32...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-32' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_04_q32_cm_alpha.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q51 (wedge supersonic shock)
    console.log('Navigating to AE2008 AE Q51...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-51' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_05_q51_wedge.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q63 (parallelogram plate)
    console.log('Navigating to AE2008 AE Q63...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-63' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_06_q63_parallelogram.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q65 (circular tube web)
    console.log('Navigating to AE2008 AE Q65...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-65' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_07_q65_circular_tube.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q66 (simply supported beam)
    console.log('Navigating to AE2008 AE Q66...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-66' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_08_q66_beam_sfd.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail AE Q67 (boom section)
    console.log('Navigating to AE2008 AE Q67...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-67' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_09_q67_booms.png'), Buffer.from(res.data, 'base64'));

    // 10. Question Detail AE Q69 (beam coords)
    console.log('Navigating to AE2008 AE Q69...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-69' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_10_q69_beam_coords.png'), Buffer.from(res.data, 'base64'));

    // 11. Question Detail AE Q84 (two-cell box beam)
    console.log('Navigating to AE2008 AE Q84...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2008-ae-ae-84' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2008_qa_11_q84_box_beam.png'), Buffer.from(res.data, 'base64'));

    console.log('AE2008 Visual QA screenshots captured successfully.');
    ws.close();
  } finally {
    chrome.kill();
  }
}

runQA2008().catch(err => {
  console.error(err);
  process.exit(1);
});
