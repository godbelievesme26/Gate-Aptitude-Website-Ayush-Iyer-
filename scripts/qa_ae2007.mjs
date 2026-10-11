import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function runQA2007() {
  console.log('--- Running Browser QA for AE2007 ---');
  const profileDir = path.join(process.cwd(), 'tmp', 'qa-chrome-2007-' + Date.now());
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9247',
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
        const res = await fetch('http://127.0.0.1:9247/json/list');
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
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_01_hub.png'), Buffer.from(res.data, 'base64'));

    // 2. Paper overview 2007
    console.log('Navigating to AE2007 overview...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2007' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_02_overview.png'), Buffer.from(res.data, 'base64'));

    // 3. Question Detail AE Q03
    console.log('Navigating to AE2007 AE Q03...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-03' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_03_q03_matrix.png'), Buffer.from(res.data, 'base64'));

    // 4. Question Detail AE Q25 (Euler Bernoulli beam figure)
    console.log('Navigating to AE2007 AE Q25...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-25' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_04_q25_beam.png'), Buffer.from(res.data, 'base64'));

    // 5. Question Detail AE Q44 (Circular composite shaft)
    console.log('Navigating to AE2007 AE Q44...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-44' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_05_q44_composite_shaft.png'), Buffer.from(res.data, 'base64'));

    // 6. Question Detail AE Q54 (Rectangular beam shear)
    console.log('Navigating to AE2007 AE Q54...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-54' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_06_q54_shear_stress.png'), Buffer.from(res.data, 'base64'));

    // 7. Question Detail AE Q57 (Control volume)
    console.log('Navigating to AE2007 AE Q57...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-57' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_07_q57_control_volume.png'), Buffer.from(res.data, 'base64'));

    // 8. Question Detail AE Q60 (Biplane)
    console.log('Navigating to AE2007 AE Q60...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-60' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_08_q60_biplane.png'), Buffer.from(res.data, 'base64'));

    // 9. Question Detail AE Q67 (Expansion corner)
    console.log('Navigating to AE2007 AE Q67...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-67' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_09_q67_expansion.png'), Buffer.from(res.data, 'base64'));

    // 10. Question Detail AE Q68 (Span-wise lift distribution)
    console.log('Navigating to AE2007 AE Q68...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-68' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_10_q68_span_lift.png'), Buffer.from(res.data, 'base64'));

    // 11. Question Detail AE Q74 (Spring mass system)
    console.log('Navigating to AE2007 AE Q74...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-74' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_11_q74_spring_mass.png'), Buffer.from(res.data, 'base64'));

    // 12. Question Detail AE Q76 (Power required vs True airspeed)
    console.log('Navigating to AE2007 AE Q76...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2007-ae-ae-76' });
    await new Promise(r => setTimeout(r, 1500));
    res = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'ae2007_qa_12_q76_power_required.png'), Buffer.from(res.data, 'base64'));

    console.log('QA completed successfully. All 12 screenshots saved.');
    ws.close();
  } finally {
    chrome.kill();
    try {
      fs.rmSync(profileDir, { recursive: true, force: true });
    } catch (e) {}
  }
}

runQA2007().catch(err => {
  console.error('QA Error:', err);
  process.exit(1);
});
