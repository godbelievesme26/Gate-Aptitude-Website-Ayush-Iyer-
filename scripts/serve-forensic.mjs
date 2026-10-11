import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { exec } from 'node:child_process';
const root = process.cwd();
const port = 4174;
const mime = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.pdf': 'application/pdf'
};

const VERIFICATION_FILE = path.resolve(root, 'data/ae/verification.json');

export function readVerification() {
  try {
    if (fs.existsSync(VERIFICATION_FILE)) {
      const data = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
      if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
        return data;
      }
    }
  } catch (err) {
    console.error('Error reading verification.json:', err);
  }
  return {};
}

export function writeVerification(data) {
  const dir = path.dirname(VERIFICATION_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const content = JSON.stringify(data, null, 2) + '\n';
  const tmpFile = VERIFICATION_FILE + '.tmp';
  try {
    fs.writeFileSync(tmpFile, content, 'utf8');
    fs.renameSync(tmpFile, VERIFICATION_FILE);
  } catch {
    fs.writeFileSync(VERIFICATION_FILE, content, 'utf8');
  }
}

export function handleVerifyRequest(req, res, pathname) {
  if (pathname !== '/api/ae/verify') return false;

  if (req.method === 'GET') {
    const data = readVerification();
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache'
    });
    res.end(JSON.stringify({ ok: true, verification: data }));
    return true;
  }

  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 65536) {
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: 'Payload too large' }));
        req.destroy();
      }
    });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body || '{}');
        const { questionId, status } = payload;
        if (typeof questionId !== 'string' || !/^[a-zA-Z0-9_-]{1,100}$/.test(questionId)) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: false, error: 'Invalid questionId' }));
          return;
        }
        if (status !== 'verified' && status !== 'unverified') {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: false, error: 'Invalid status' }));
          return;
        }
        const current = readVerification();
        if (status === 'verified') {
          current[questionId] = {
            status: 'verified',
            verifiedAt: new Date().toISOString().slice(0, 10)
          };
        } else {
          delete current[questionId];
        }
        writeVerification(current);
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache'
        });
        res.end(JSON.stringify({
          ok: true,
          questionId,
          status: current[questionId]?.status || 'unverified',
          verification: current
        }));
      } catch {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: 'Malformed request JSON' }));
      }
    });
    return true;
  }

  res.writeHead(405, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ ok: false, error: 'Method not allowed' }));
  return true;
}

const STATE_FILE = path.resolve(root, 'internal/ae/forensic_review_state.json');
const AUDIT_FILE = path.resolve(root, 'internal/ae/forensic_audit_trail.jsonl');
const QUEUE_FILE = path.resolve(root, 'internal/ae/ocr_queue.json');

function readJson(file, defaultVal = {}) {
  try {
    if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (err) {}
  return defaultVal;
}

function writeJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function appendAudit(entry) {
  fs.appendFileSync(AUDIT_FILE, JSON.stringify(entry) + '\n');
}

export const server = http.createServer((req, res) => {
  try {
    const parsedUrl = new URL(req.url, 'http://localhost');
    const pathname = decodeURIComponent(parsedUrl.pathname);

    if (handleVerifyRequest(req, res, pathname)) {
      return;
    }

    if (pathname.startsWith('/api/')) {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        res.setHeader('Content-Type', 'application/json');
        
        if (req.method === 'GET' && pathname === '/api/queue') {
          const queue = readJson(QUEUE_FILE, []);
          const state = readJson(STATE_FILE, {});
          return res.end(JSON.stringify({ queue, state }));
        }
        
        if (req.method === 'GET' && pathname.startsWith('/api/question/')) {
          const id = pathname.split('/').pop();
          const year = id.split('-')[1];
          const yearData = readJson(path.resolve(root, 'data/ae/' + year + '.json'), {questions:[]});
          const q = yearData.questions.find(x => x.id === id);
          return res.end(JSON.stringify(q || {}));
        }

        if (req.method === 'POST' && pathname === '/api/state') {
          const payload = JSON.parse(body);
          const state = readJson(STATE_FILE, {});
          state[payload.id] = {
             state: payload.state,
             fields: payload.fields || {},
             lastReviewedAt: new Date().toISOString()
          };
          writeJson(STATE_FILE, state);
          return res.end(JSON.stringify({ ok: true }));
        }

        if (req.method === 'POST' && pathname === '/api/update-canonical') {
          const { id, field, previousValue, newValue, reviewerAction, sourcePage } = JSON.parse(body);
          const allowedFields = ['question', 'math', 'options', 'type', 'marks', 'groups', 'answer', 'solution', 'figure'];
          if (!allowedFields.includes(field)) {
             return res.end(JSON.stringify({ ok: false, error: 'Invalid field' }));
          }
          
          const year = id.split('-')[1];
          const yearFile = path.resolve(root, 'data/ae/' + year + '.json');
          const yearData = readJson(yearFile, {questions:[]});
          const qIdx = yearData.questions.findIndex(x => x.id === id);
          
          if (qIdx >= 0) {
            // Write audit trail FIRST as intent to commit
            const auditEntry = {
              questionId: id,
              field,
              previousValue,
              newValue,
              reviewerAction,
              timestamp: new Date().toISOString(),
              sourcePage
            };
            try {
               appendAudit(auditEntry);
            } catch (err) {
               return res.end(JSON.stringify({ ok: false, error: 'Audit log failed' }));
            }
            
            // Now apply to canonical
            yearData.questions[qIdx][field] = newValue;
            try {
               // Use atomic rename for canonical json
               const tempFile = yearFile + '.tmp';
               fs.writeFileSync(tempFile, JSON.stringify(yearData, null, 2));
               fs.renameSync(tempFile, yearFile);
            } catch (err) {
               return res.end(JSON.stringify({ ok: false, error: 'Canonical write failed' }));
            }
            
            return res.end(JSON.stringify({ ok: true }));
          }
          return res.end(JSON.stringify({ ok: false, error: 'Not found' }));
        }

        if (req.method === 'POST' && pathname === '/api/render-crop') {
          const { year, page, bbox } = JSON.parse(body);
          const pdfPath = 'internal/ae/AE' + year + '.pdf';
          const outPath = 'internal/ae/audit_renders/preview_' + year + '_' + page + '.png';
          const pyScript = 'import fitz\\n' +
                           'doc = fitz.open("' + pdfPath + '")\\n' +
                           'page = doc[' + (page - 1) + ']\\n' +
                           'rect = fitz.Rect(' + JSON.stringify(bbox) + ')\\n' +
                           'page.get_pixmap(clip=rect, dpi=150).save("' + outPath + '")\\n';
          fs.writeFileSync('internal/ae/temp_preview.py', pyScript);
          exec('py internal/ae/temp_preview.py', (err) => {
             if (err) return res.end(JSON.stringify({ ok: false }));
             res.end(JSON.stringify({ ok: true, url: '/' + outPath + '?t=' + Date.now() }));
          });
          return;
        }
      });
      return;
    }

    let file = path.resolve(root, 'internal/ae' + (pathname === '/' ? '/workstation.html' : pathname.replace('/internal/ae', '')));
    
    if (pathname.startsWith('/internal/ae/AE')) file = path.resolve(root, pathname.substring(1));
    if (pathname.startsWith('/internal/ae/audit_renders/')) file = path.resolve(root, pathname.substring(1));

    if (!fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404);
      return res.end('Not found');
    }

    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  } catch (err) {
    res.writeHead(500);
    res.end('Server error');
  }
});

if (process.argv[1] && process.argv[1].endsWith('serve-forensic.mjs')) {
  server.listen(port, '127.0.0.1', () => {
    console.log('Forensic Workstation: http://127.0.0.1:' + port + '/');
  });
}

