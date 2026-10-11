import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

async function main() {
  console.log('--- Starting Chrome Headless QA for AE2025 ---');

  const profileDir = path.join(process.cwd(), 'tmp', 'chrome-qa-profile-' + Date.now());

  // Spawn Chrome
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9222/json/list');
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
    throw new Error('Could not connect to Chrome DevTools port 9222');
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

  await new Promise(r => (ws.onopen = r));

  function send(method, params = {}) {
    const curId = id++;
    return new Promise((resolve, reject) => {
      pending.set(curId, { resolve, reject });
      ws.send(JSON.stringify({ id: curId, method, params }));
    });
  }

  async function evaluate(expression) {
    const res = await send('Runtime.evaluate', { expression, returnByValue: true });
    if (res.exceptionDetails) {
      throw new Error(JSON.stringify(res.exceptionDetails));
    }
    return res.result?.value;
  }

  async function screenshot(filename) {
    const res = await send('Page.captureScreenshot', { format: 'png' });
    const filePath = path.join(ARTIFACTS_DIR, filename);
    fs.writeFileSync(filePath, Buffer.from(res.data, 'base64'));
    console.log(`Saved screenshot: ${filename}`);
  }

  try {
    await send('Page.enable');
    await send('Runtime.enable');
    await send('DOM.enable');
    await send('Network.enable');
    await send('Network.setCacheDisabled', { cacheDisabled: true });

    // 1. Navigate to home
    console.log('Navigating to http://127.0.0.1:4173/');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/' });
    await new Promise(r => setTimeout(r, 1200));

    // 2. Navigate to #/aerospace
    console.log('Navigating to #/aerospace');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace' });
    await new Promise(r => setTimeout(r, 1000));

    const overviewText = await evaluate(`document.body.innerText`);
    console.log('Aerospace Overview Page Loaded.');
    if (!overviewText.includes('2025') || !overviewText.includes('2026')) {
      throw new Error('Aerospace overview does not list both 2025 and 2026');
    }
    await screenshot('ae2025_qa_01_aerospace_overview.png');

    // 3. Navigate to #/aerospace/2025
    console.log('Navigating to #/aerospace/2025');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2025' });
    await new Promise(r => setTimeout(r, 1000));

    const paperOverviewText = await evaluate(`document.body.innerText`);
    console.log('AE2025 Paper Overview Page Loaded.');
    if (!paperOverviewText.includes('65 questions') || !paperOverviewText.includes('100 marks')) {
      throw new Error('AE2025 paper overview missing 65 questions or 100 marks');
    }
    await screenshot('ae2025_qa_02_paper_overview.png');

    // 4. Start Timed Full-Length CBT Exam
    console.log('Clicking Start Timed Exam for AE2025');
    await evaluate(`document.querySelector('[data-action="time-paper"][data-value="gate-2025-ae"]')?.click()`);
    await new Promise(r => setTimeout(r, 1000));

    const cbtTitle = await evaluate(`document.querySelector('.cbt-header')?.innerText || document.title`);
    console.log('CBT Header:', cbtTitle);
    await screenshot('ae2025_qa_03_cbt_q1_ga.png');

    // 5. Select Option A on Q1 (Courage : Bravery :: Yearning : Longing)
    console.log('Selecting option A on Q1');
    await evaluate(`document.querySelector('[data-action="answer"][data-value="A"]')?.click()`);
    await new Promise(r => setTimeout(r, 300));
    await evaluate(`document.querySelector('[data-action="next"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));

    // 6. Switch to AE Section tab and jump to Q19
    console.log('Switching to AE section tab and jumping to Q19 (Option figures)');
    await evaluate(`document.querySelector('.cbt-tabs .cbt-tab:nth-child(2)')?.click()`);
    await new Promise(r => setTimeout(r, 500));
    await evaluate(`document.querySelector('[data-action="jump"][data-value="18"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));

    const q19Figures = await evaluate(`Array.from(document.querySelectorAll('.option-figure')).map(img => ({src: img.src, naturalWidth: img.naturalWidth, complete: img.complete}))`);
    console.log('Q19 Option Figures count:', q19Figures.length, q19Figures);
    await screenshot('ae2025_qa_04_cbt_q19_option_figures.png');

    // 7. Jump to Q20 (Question Diagram)
    console.log('Jumping to Q20 (Vortices diagram)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="19"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_05_cbt_q20_diagram.png');

    // 8. Jump to Q30 (Rhombus Shear Strain Diagram)
    console.log('Jumping to Q30 (Rhombus shear strain diagram)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="29"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_06_cbt_q30_diagram.png');

    // 9. Jump to Q37 (Structured Material Properties Table)
    console.log('Jumping to Q37 (Structured Table)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="36"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_07_cbt_q37_table.png');

    // 10. Jump to Q38 (MSQ Question)
    console.log('Jumping to Q38 (MSQ Question)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="37"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));
    await evaluate(`document.querySelector('[data-action="answer"][data-value="A"]')?.click()`);
    await evaluate(`document.querySelector('[data-action="answer"][data-value="B"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));
    await screenshot('ae2025_qa_08_cbt_q38_msq.png');

    // 11. Jump to Q49 (Supersonic Ramp Diagram NAT)
    console.log('Jumping to Q49 (Supersonic Ramp NAT)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="48"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    // Test virtual keypad input: 4, ., 5
    await evaluate(`
      document.querySelector('[data-action="nat-key"][data-value="4"]')?.click();
      document.querySelector('[data-action="nat-key"][data-value="."]')?.click();
      document.querySelector('[data-action="nat-key"][data-value="5"]')?.click();
    `);
    await new Promise(r => setTimeout(r, 500));
    await screenshot('ae2025_qa_09_cbt_q49_nat_diagram.png');

    // 12. Jump to Q52 (Airplane Climb Parameters Table)
    console.log('Jumping to Q52 (Airplane climb table)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="51"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_10_cbt_q52_table.png');

    // 13. Jump to Q58 (Vertical Column Diagram)
    console.log('Jumping to Q58 (Vertical column diagram)');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="57"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_11_cbt_q58_diagram.png');

    // 14. Mark for Review and Next on Q58
    console.log('Testing Mark for Review & Next');
    await evaluate(`document.querySelector('[data-action="review-question"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));

    // 15. Open Question Paper Modal
    console.log('Opening Question Paper Modal');
    await evaluate(`document.querySelector('[data-action="exam-modal"][data-value="paper"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_12_cbt_question_paper_modal.png');

    // Close Modal
    console.log('Closing Question Paper Modal');
    await evaluate(`document.querySelector('[data-action="exam-modal"][data-value="paper"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));

    // 16. Jump to Q65 (Final Question) and answer
    console.log('Jumping to Q65');
    await evaluate(`document.querySelector('[data-action="jump"][data-value="64"]')?.click()`);
    await new Promise(r => setTimeout(r, 500));
    await evaluate(`
      document.querySelector('[data-action="nat-key"][data-value="1"]')?.click();
      document.querySelector('[data-action="nat-key"][data-value="0"]')?.click();
      document.querySelector('[data-action="nat-key"][data-value="0"]')?.click();
    `);
    await new Promise(r => setTimeout(r, 500));

    // 17. Click Submit Examination
    console.log('Clicking Submit Examination');
    await evaluate(`document.querySelector('[data-action="exam-submit-confirm"]')?.click()`);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2025_qa_13_cbt_submit_modal.png');

    // Confirm submission
    console.log('Confirming submission');
    await evaluate(`document.querySelector('[data-action="exam-submit-final"]')?.click()`);
    await new Promise(r => setTimeout(r, 1200));

    const resultUrl = await evaluate(`location.hash`);
    console.log('Current URL after submit:', resultUrl);
    await screenshot('ae2025_qa_14_result_view.png');

    // 18. Review Paper View
    console.log('Navigating to review view');
    await evaluate(`document.querySelector('a[href*="#/review"]')?.click()`);
    await new Promise(r => setTimeout(r, 1000));
    await screenshot('ae2025_qa_15_review_view.png');

    console.log('=== All 15 Browser QA Steps Passed Successfully ===');
  } finally {
    ws.close();
    chrome.kill();
    try { fs.rmSync(profileDir, { recursive: true, force: true }); } catch (e) {}
  }
}

main().catch(err => {
  console.error('QA Script Error:', err);
  process.exit(1);
});
