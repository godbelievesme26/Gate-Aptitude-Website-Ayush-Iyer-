import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { server } from './serve.mjs';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';
const VERIFICATION_FILE = path.resolve(process.cwd(), 'data/ae/verification.json');

async function main() {
  console.log('=== Starting Browser QA for Aerospace Manual Verification System ===');

  // Ensure verification.json starts clean
  fs.writeFileSync(VERIFICATION_FILE, '{}\n', 'utf8');

  // Start server on port 4178 to avoid collisions
  const PORT = 4178;
  await new Promise((resolve) => {
    server.listen(PORT, '127.0.0.1', () => {
      console.log(`Server listening on http://127.0.0.1:${PORT}`);
      resolve();
    });
  });

  const profileDir = path.join(process.cwd(), 'tmp', 'chrome-qa-verify-' + Date.now());
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9226',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9226/json/list');
      const tabs = await res.json();
      const pageTab = tabs.find(t => t.type === 'page');
      if (pageTab && pageTab.webSocketDebuggerUrl) {
        wsUrl = pageTab.webSocketDebuggerUrl;
        break;
      }
    } catch (e) {}
  }

  if (!wsUrl) {
    chrome.kill();
    server.close();
    throw new Error('Could not connect to Chrome DevTools port 9226');
  }
  console.log('Connected to Chrome DevTools:', wsUrl);

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

  async function evaluate(expression) {
    const res = await send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result?.value;
  }

  async function screenshot(name) {
    const res = await send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(res.data, 'base64');
    const filePath = path.join(ARTIFACTS_DIR, name + '.png');
    fs.writeFileSync(filePath, buffer);
    console.log(`Saved screenshot: ${name}.png`);
  }

  await send('Page.enable');
  await send('Runtime.enable');
  await send('DOM.enable');

  try {
    // 1. Navigate to question gate-2026-ae-ae-11
    console.log('\n--- Step 1: Navigate to AE2026 Q11 ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/question/gate-2026-ae-ae-11` });
    await new Promise(r => setTimeout(r, 1200));

    const initialBtn = await evaluate(`
      (() => {
        const btn = document.querySelector('[data-action="toggle-verify-question"]');
        return btn ? { text: btn.textContent.trim(), value: btn.dataset.value, className: btn.className } : null;
      })()
    `);
    console.log('Initial Button State:', initialBtn);
    if (!initialBtn || !initialBtn.text.includes('Mark as Verified') || initialBtn.value !== 'gate-2026-ae-ae-11') {
      throw new Error(`Expected unverified button, got: ${JSON.stringify(initialBtn)}`);
    }
    await screenshot('verify_qa_01_initial_unverified');

    // 2. Click Mark as Verified
    console.log('\n--- Step 2: Click Mark as Verified ---');
    await evaluate(`
      document.querySelector('[data-action="toggle-verify-question"]').click();
    `);
    await new Promise(r => setTimeout(r, 800));

    const verifiedBtn = await evaluate(`
      (() => {
        const btn = document.querySelector('[data-action="toggle-verify-question"]');
        return btn ? { text: btn.textContent.trim(), value: btn.dataset.value, className: btn.className } : null;
      })()
    `);
    console.log('After Click Button State:', verifiedBtn);
    if (!verifiedBtn || !verifiedBtn.text.includes('Verified') || !verifiedBtn.className.includes('primary')) {
      throw new Error(`Expected verified button, got: ${JSON.stringify(verifiedBtn)}`);
    }
    await screenshot('verify_qa_02_clicked_verified');

    // 3. Confirm disk persistence
    console.log('\n--- Step 3: Check data/ae/verification.json on disk ---');
    const diskContent1 = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
    console.log('Disk content:', diskContent1);
    if (!diskContent1['gate-2026-ae-ae-11'] || diskContent1['gate-2026-ae-ae-11'].status !== 'verified') {
      throw new Error(`Disk does not contain verified entry for gate-2026-ae-ae-11`);
    }

    // 4. Reload browser and check state
    console.log('\n--- Step 4: Browser Reload ---');
    await send('Page.reload');
    await new Promise(r => setTimeout(r, 1200));

    const reloadedBtn = await evaluate(`
      (() => {
        const btn = document.querySelector('[data-action="toggle-verify-question"]');
        return btn ? { text: btn.textContent.trim(), value: btn.dataset.value, className: btn.className } : null;
      })()
    `);
    console.log('Reloaded Button State:', reloadedBtn);
    if (!reloadedBtn || !reloadedBtn.text.includes('Verified') || !reloadedBtn.className.includes('primary')) {
      throw new Error(`State did not persist across browser reload`);
    }
    await screenshot('verify_qa_03_reloaded_state');

    // 5. Verify second question (gate-2026-ae-ga-01)
    console.log('\n--- Step 5: Navigate and verify second question (gate-2026-ae-ga-01) ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/question/gate-2026-ae-ga-01` });
    await new Promise(r => setTimeout(r, 1000));
    await evaluate(`
      document.querySelector('[data-action="toggle-verify-question"]').click();
    `);
    await new Promise(r => setTimeout(r, 800));

    const diskContent2 = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
    console.log('Disk content after 2nd verification:', diskContent2);
    if (!diskContent2['gate-2026-ae-ga-01'] || !diskContent2['gate-2026-ae-ae-11']) {
      throw new Error(`Disk does not contain both verified entries`);
    }

    // 6. Check Aerospace Hub and Paper Overview counters
    console.log('\n--- Step 6: Check Aerospace Hub counters ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/aerospace` });
    await new Promise(r => setTimeout(r, 1000));
    const hubCounter = await evaluate(`
      (() => {
        const badges = Array.from(document.querySelectorAll('.verification-counter-badge, .paper-meta-badge'));
        return badges.map(b => b.textContent.trim());
      })()
    `);
    console.log('Hub Badges:', hubCounter);
    await screenshot('verify_qa_04_aerospace_hub');

    console.log('\n--- Step 7: Check AE2026 Paper Overview counters ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/aerospace/2026` });
    await new Promise(r => setTimeout(r, 1000));
    const overviewCounter = await evaluate(`
      (() => {
        const badges = Array.from(document.querySelectorAll('.verification-counter-badge, .paper-meta-badge'));
        return badges.map(b => b.textContent.trim());
      })()
    `);
    console.log('Overview Badges:', overviewCounter);
    await screenshot('verify_qa_05_paper_overview');

    // 8. Test unverify / toggle off
    console.log('\n--- Step 8: Toggle unverify on gate-2026-ae-ga-01 ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/question/gate-2026-ae-ga-01` });
    await new Promise(r => setTimeout(r, 1000));
    await evaluate(`
      document.querySelector('[data-action="toggle-verify-question"]').click();
    `);
    await new Promise(r => setTimeout(r, 800));

    const toggledBtn = await evaluate(`
      (() => {
        const btn = document.querySelector('[data-action="toggle-verify-question"]');
        return btn ? { text: btn.textContent.trim(), value: btn.dataset.value, className: btn.className } : null;
      })()
    `);
    console.log('Toggled back to unverified:', toggledBtn);
    if (!toggledBtn || !toggledBtn.text.includes('Mark as Verified')) {
      throw new Error(`Failed to toggle back to unverified`);
    }

    const diskContent3 = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
    console.log('Disk content after unverify:', diskContent3);
    if (diskContent3['gate-2026-ae-ga-01'] || !diskContent3['gate-2026-ae-ae-11']) {
      throw new Error(`Unverify did not remove gate-2026-ae-ga-01 or deleted wrong question`);
    }

    // 9. Verify CBT mode isolation (no verification controls during exam)
    console.log('\n--- Step 9: Verify CBT Exam Mode Isolation ---');
    await send('Page.navigate', { url: `http://127.0.0.1:${PORT}/#/aerospace/2026` });
    await new Promise(r => setTimeout(r, 1000));
    // Click start exam
    await evaluate(`
      document.querySelector('[data-action="start-cbt"]').click();
    `);
    await new Promise(r => setTimeout(r, 1000));

    const cbtVerifyBtn = await evaluate(`
      document.querySelector('[data-action="toggle-verify-question"]')
    `);
    console.log('CBT Mode Verify Button Present:', cbtVerifyBtn);
    if (cbtVerifyBtn !== null) {
      throw new Error('Verification button should NOT be present in CBT exam mode');
    }
    await screenshot('verify_qa_06_cbt_exam_isolation');

    console.log('\n=== ALL BROWSER QA TESTS PASSED SUCCESSFULLY ===');
  } finally {
    ws.close();
    chrome.kill();
    server.close();
  }
}

main().catch(err => {
  console.error('Browser QA Failed:', err);
  process.exit(1);
});
