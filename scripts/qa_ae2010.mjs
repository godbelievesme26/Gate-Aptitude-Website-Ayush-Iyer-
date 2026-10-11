import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2010() {
  console.log('--- Running Browser QA for AE2010 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2010-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9244',
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
        const res = await fetch('http://127.0.0.1:9244/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2010
    console.log('Navigating to AE2010 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2010' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q01 (diffuser)
    console.log('Navigating to AE2010 AE Q01...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-01' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_03_q01_diffuser.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q13 (Von Mises plate)
    console.log('Navigating to AE2010 AE Q13...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-13' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_04_q13_von_mises.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q17 (beam cross section)
    console.log('Navigating to AE2010 AE Q17...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-17' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_05_q17_beam_sec.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q28 (pendulum)
    console.log('Navigating to AE2010 AE Q28...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-28' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_06_q28_pendulum.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q31 (thin wall shear center)
    console.log('Navigating to AE2010 AE Q31...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-31' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_07_q31_shear_center.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q46 (finite wing circulation)
    console.log('Navigating to AE2010 AE Q46...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-46' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_08_q46_wing_circulation.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail AE Q48 (Common Data beam & BMD)
    console.log('Navigating to AE2010 AE Q48...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-48' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_09_q48_common_data_bmd.png'), Buffer.from(res.data, 'base64'));

    // 10. Question Detail AE Q50 (Common Data cylinder)
    console.log('Navigating to AE2010 AE Q50...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ae-50' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_10_q50_spinning_cylinder.png'), Buffer.from(res.data, 'base64'));

    // 11. Question Detail GA Q62 (octal math)
    console.log('Navigating to AE2010 GA Q62...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2010-ae-ga-62' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2010_qa_11_q62_octal.png'), Buffer.from(res.data, 'base64'));

    console.log('AE2010 Browser QA Complete! All 11 screenshots captured.');
    ws.close();
  } finally {
    chrome.kill('SIGKILL');
  }
}

runQA2010().catch(e => {
  console.error(e);
  process.exit(1);
});
