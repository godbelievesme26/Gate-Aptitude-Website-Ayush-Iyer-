import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const port = Number(process.env.PORT) || 4173;
const mime = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.mjs': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webmanifest': 'application/manifest+json',
  '.pdf': 'application/pdf'
};

const VERIFICATION_FILE = path.resolve(root, 'data/ae/verification.json');

function readVerification() {
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

function writeVerification(data) {
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

export function isPublicAllowedPath(pathname) {
  if (typeof pathname !== 'string') return false;
  // Strictly prevent directory traversal or control characters
  if (pathname.includes('..') || pathname.includes('\\') || pathname.includes('\0')) return false;

  // Root and index document
  if (pathname === '/' || pathname === '/index.html') return true;

  // Web app manifest, service worker, favicon
  if (pathname === '/sw.js' || pathname === '/manifest.webmanifest' || pathname === '/favicon.ico') return true;

  // Public application stylesheets (css/*.css)
  if (/^\/css\/[a-zA-Z0-9_-]+\.css$/.test(pathname)) return true;

  // Public application modules (js/*.js)
  if (/^\/js\/[a-zA-Z0-9_-]+\.js$/.test(pathname)) return true;

  // Public assets (assets/*)
  if (/^\/assets\/[a-zA-Z0-9_.-]+\.(png|svg|ico|webp)$/i.test(pathname)) return true;

  // Public figures (figures/*)
  if (/^\/figures\/[a-zA-Z0-9_.-]+\.(png|svg|webp|jpg|jpeg)$/i.test(pathname)) return true;

  // Public datasets
  if (pathname === '/data/registry.json') return true;
  if (/^\/data\/day\d{2}\.json$/.test(pathname)) return true;
  if (pathname === '/data/ae/manifest.json') return true;
  if (pathname === '/data/ae/verification.json') return true;
  if (/^\/data\/ae\/\d{4}\.json$/.test(pathname)) return true;

  return false;
}

export const server = http.createServer((req, res) => {
  try {
    const parsedUrl = new URL(req.url, 'http://localhost');
    const pathname = decodeURIComponent(parsedUrl.pathname);

    // Verification endpoint handling on the student server:
    // Unauthorized verification modification is blocked.
    if (pathname === '/api/ae/verify') {
      if (req.method === 'POST') {
        res.writeHead(403, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          ok: false,
          error: 'Forbidden: Verification mutation is disabled on the student server. Use the forensic review workstation.'
        }));
        return;
      }
      if (req.method === 'GET') {
        const data = readVerification();
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache'
        });
        res.end(JSON.stringify({ ok: true, verification: data }));
        return;
      }
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: 'Method not allowed' }));
      return;
    }

    // Default-deny static file policy
    if (!isPublicAllowedPath(pathname)) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }

    // Only GET and HEAD methods are permitted for static public assets
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.writeHead(405);
      res.end('Method not allowed');
      return;
    }

    const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));

    if (
      !file.startsWith(root + path.sep) ||
      !fs.existsSync(file) ||
      fs.statSync(file).isDirectory()
    ) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }

    res.writeHead(200, {
      'Content-Type': mime[path.extname(file)] || 'application/octet-stream',
      'Cache-Control': 'no-cache'
    });
    if (req.method === 'HEAD') {
      res.end();
      return;
    }
    fs.createReadStream(file).pipe(res);
  } catch {
    res.writeHead(400);
    res.end('Bad request');
  }
});

if (process.argv[1] && process.argv[1].endsWith('serve.mjs')) {
  server.listen(port, '127.0.0.1', () => {
    console.log(`GATE workspace: http://127.0.0.1:${port}`);
  });
}
