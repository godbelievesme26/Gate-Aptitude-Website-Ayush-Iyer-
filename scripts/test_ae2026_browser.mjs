import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ARTIFACTS_DIR = 'C:\\Users\\godbe\\.gemini\\antigravity\\brain\\c05ba5de-1c22-4609-a6ec-bfdf2114d4f1';

// Static file server
function createServer() {
  const root = process.cwd();
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.pdf': 'application/pdf',
    '.woff2': 'font/woff2'
  };

  const server = http.createServer((req, res) => {
    let reqPath = decodeURIComponent(req.url.split('?')[0]);
    if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
    const filePath = path.join(root, reqPath);
    
    fs.stat(filePath, (err, stats) => {
      if (err || !stats.isFile()) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      const contentType = mimeTypes[ext] || 'application/octet-stream';
      res.writeHead(200, {
        'Content-Type': contentType,
        'Cache-Control': 'no-cache',
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp'
      });
      fs.createReadStream(filePath).pipe(res);
    });
  });

  return new Promise((resolve) => {
    server.listen(4173, '127.0.0.1', () => {
      console.log('Static server listening on http://127.0.0.1:4173');
      resolve(server);
    });
  });
}

async function main() {
  console.log('--- Starting Chrome Headless QA for AE2026 ---');
  const server = await createServer();
  const profileDir = path.join(process.cwd(), 'tmp', 'chrome-qa-ae2026-' + Date.now());

  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9225',
    '--window-size=1440,900',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=' + profileDir
  ]);

  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9225/json/list');
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
    throw new Error('Could not connect to Chrome DevTools port 9225');
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
    const buffer = Buffer.from(res.data, 'base64');
    const outPath = path.join(ARTIFACTS_DIR, filename);
    fs.writeFileSync(outPath, buffer);
    console.log(`Saved screenshot: ${filename}`);
  }

  try {
    await send('Page.enable');
    await send('Runtime.enable');

    // 1. Navigate to Aerospace Hub
    console.log('Navigating to http://127.0.0.1:4173/#/aerospace');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace' });
    await new Promise(r => setTimeout(r, 2000));

    await screenshot('ae2026_qa_01_aerospace_hub.png');
    const hubText = await evaluate('document.body.innerText');
    console.log('Aerospace Hub check:', hubText.includes('Aerospace Engineering') ? 'PASS' : 'FAIL');

    // 2. Open AE2026 Paper Overview via #/aerospace/2026
    console.log('Navigating to http://127.0.0.1:4173/#/aerospace/2026');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2026' });
    await new Promise(r => setTimeout(r, 1500));
    await screenshot('ae2026_qa_02_paper_overview.png');
    const overviewText = await evaluate('document.body.innerText');
    console.log('AE2026 Overview check:', overviewText.includes('GATE Aerospace 2026') ? 'PASS' : 'FAIL');

    // 3. Question Bank filtered by AE 2026
    console.log('Navigating to #/bank?year=2026&paper=AE');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/bank?year=2026&paper=AE' });
    await new Promise(r => setTimeout(r, 1500));
    await screenshot('ae2026_qa_03_bank_view.png');
    const bankCount = await evaluate('document.querySelectorAll(".question-row").length');
    console.log(`AE2026 questions rendered in bank (page 1): ${bankCount}`);

    // 4. Question Detail: Q11 (Figure Question)
    console.log('Navigating to #/question/gate-2026-ae-ae-11');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2026-ae-ae-11' });
    await new Promise(r => setTimeout(r, 1200));
    await screenshot('ae2026_qa_04_q11_detail.png');
    const hasFig11 = await evaluate('Boolean(document.querySelector("img[src*=\'gate-2026-ae-ae-11-figure-1.png\']"))');
    console.log('Q11 figure rendered:', hasFig11 ? 'PASS' : 'FAIL');

    // 5. Question Detail: Q02 (Option Figures)
    console.log('Navigating to #/question/gate-2026-ae-ga-02');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2026-ae-ga-02' });
    await new Promise(r => setTimeout(r, 1200));
    await screenshot('ae2026_qa_05_q02_option_figures.png');
    const optFigCount = await evaluate('document.querySelectorAll("img[src*=\'gate-2026-ae-ga-02-option\']").length');
    console.log(`Q02 option figures rendered: ${optFigCount} (expected 4)`);

    // 6. Question Detail: Q37 (Matrix / Equation)
    console.log('Navigating to #/question/gate-2026-ae-ae-37');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/question/gate-2026-ae-ae-37' });
    await new Promise(r => setTimeout(r, 1200));
    await screenshot('ae2026_qa_06_q37_detail.png');
    const hasMatrix = await evaluate('document.body.innerHTML.includes("math-matrix")');
    console.log('Q37 math-matrix rendered:', hasMatrix ? 'PASS' : 'FAIL');

    // 7. Launch Timed Test CBT Mode from paper overview
    console.log('Returning to paper overview to launch Timed Test CBT...');
    await send('Page.navigate', { url: 'http://127.0.0.1:4173/#/aerospace/2026' });
    await new Promise(r => setTimeout(r, 1200));

    await evaluate(`
      const cbtBtn = document.querySelector('[data-action="time-paper"]');
      if (cbtBtn) cbtBtn.click();
    `);
    await new Promise(r => setTimeout(r, 2000));
    await screenshot('ae2026_qa_07_cbt_launched.png');

    const cbtPaletteButtons = await evaluate('document.querySelectorAll(".cbt-palette button").length');
    console.log(`CBT Palette buttons count in visible section: ${cbtPaletteButtons}`);

    // 8. Test MCQ Selection in CBT (Q1)
    await evaluate(`
      const optA = document.querySelector('.cbt-option-input[data-value="A"], [data-action="answer"][data-value="A"]');
      if (optA) optA.click();
    `);
    await new Promise(r => setTimeout(r, 600));
    await screenshot('ae2026_qa_08_cbt_mcq_selected.png');

    // 9. Switch to AE section and jump to Q31 (NAT)
    await evaluate(`
      const tabs = Array.from(document.querySelectorAll('.cbt-tab'));
      const aeTab = tabs.find(t => t.textContent.includes('AE'));
      if (aeTab) aeTab.click();
    `);
    await new Promise(r => setTimeout(r, 600));

    await evaluate(`
      const q31Btn = Array.from(document.querySelectorAll('.cbt-palette button')).find(el => el.textContent.trim() === '31');
      if (q31Btn) q31Btn.click();
    `);
    await new Promise(r => setTimeout(r, 1000));
    await screenshot('ae2026_qa_09_cbt_q31_nat.png');

    // Use Virtual Keypad to type '60'
    await evaluate(`
      const btn6 = Array.from(document.querySelectorAll('.cbt-nat-btn')).find(b => b.textContent.trim() === '6');
      const btn0 = Array.from(document.querySelectorAll('.cbt-nat-btn')).find(b => b.textContent.trim() === '0');
      if (btn6) btn6.click();
      if (btn0) btn0.click();
    `);
    await new Promise(r => setTimeout(r, 600));
    await screenshot('ae2026_qa_10_cbt_nat_entered.png');

    const natVal = await evaluate('document.querySelector("#nat-answer")?.value');
    console.log(`NAT Keypad input result for Q31: "${natVal}"`);

    // 10. Submit CBT Session
    console.log('Submitting CBT session...');
    await evaluate(`
      const submitBtn = document.querySelector('[data-action="exam-submit-confirm"]');
      if (submitBtn) submitBtn.click();
    `);
    await new Promise(r => setTimeout(r, 800));
    await screenshot('ae2026_qa_11_cbt_confirm_dialog.png');

    // Confirm dialog final submit
    await evaluate(`
      const finalBtn = document.querySelector('[data-action="exam-submit-final"]');
      if (finalBtn) finalBtn.click();
    `);
    await new Promise(r => setTimeout(r, 1500));
    await screenshot('ae2026_qa_12_cbt_results.png');

    const resultText = await evaluate('document.body.innerText');
    const resultPass = resultText.includes('Session recorded') || resultText.includes('Your practice summary') || resultText.includes('Answer feedback');
    console.log('CBT Result screen verification:', resultPass ? 'PASS' : 'FAIL');

    console.log('--- Headless Chrome QA completed successfully for AE2026 ---');
  } finally {
    ws.close();
    chrome.kill();
    server.close();
  }
}

main().catch(err => {
  console.error('QA Script Error:', err);
  process.exit(1);
});
