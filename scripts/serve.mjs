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
        const sanitized = {};
        for (const [key, val] of Object.entries(data)) {
          if (val && typeof val === 'object') {
            sanitized[key] = {
              status: val.status === 'verified' ? 'verified' : 'unverified',
              verifiedAt: typeof val.verifiedAt === 'string' ? val.verifiedAt : undefined
            };
          }
        }
        return sanitized;
      }
    }
  } catch (err) {
    console.error('Error reading verification.json:', err);
  }
  return {};
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
    res.writeHead(403, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ok: false,
      error: 'Forbidden: Verification mutation is disabled on the student server. Use the forensic review workstation.'
    }));
    return true;
  }

  res.writeHead(405, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ ok: false, error: 'Method not allowed' }));
  return true;
}


export function isPublicAllowedPath(pathname) {
  if (typeof pathname !== 'string') return false;
  // Clean path of optional query string or fragment if evaluated directly
  const cleanPath = pathname.split(/[?#]/)[0];
  // Strictly prevent directory traversal, backslashes, control characters, or double slashes
  if (
    cleanPath.includes('..') ||
    cleanPath.includes('\\') ||
    cleanPath.includes('//') ||
    /[\x00-\x1f\x7f]/.test(cleanPath)
  ) return false;

  // Root and index document
  if (cleanPath === '/' || cleanPath === '/index.html') return true;

  // Web app manifest, service worker, favicon
  if (cleanPath === '/sw.js' || cleanPath === '/manifest.webmanifest' || cleanPath === '/favicon.ico') return true;

  // Public application stylesheets (css/*.css)
  if (/^\/css\/[a-zA-Z0-9_-]+\.css$/.test(cleanPath)) return true;

  // Public application modules (js/*.js)
  if (/^\/js\/[a-zA-Z0-9_-]+\.js$/.test(cleanPath)) return true;

  // Public assets (assets/*)
  if (/^\/assets\/[a-zA-Z0-9_-][a-zA-Z0-9_.-]*\.(png|svg|ico|webp)$/i.test(cleanPath)) return true;

  // Public figures (figures/*)
  if (/^\/figures\/[a-zA-Z0-9_-][a-zA-Z0-9_.-]*\.(png|svg|webp|jpg|jpeg)$/i.test(cleanPath)) return true;

  // Public datasets
  if (cleanPath === '/data/registry.json') return true;
  if (/^\/data\/day\d{2}\.json$/.test(cleanPath)) return true;
  if (cleanPath === '/data/ae/manifest.json') return true;
  if (cleanPath === '/data/ae/verification.json') return true;
  if (/^\/data\/ae\/\d{4}\.json$/.test(cleanPath)) return true;

  return false;
}

export const server = http.createServer((req, res) => {
  try {
    const parsedUrl = new URL(req.url, 'http://localhost');
    const pathname = decodeURIComponent(parsedUrl.pathname);

    // Verification endpoint handling on the student server:
    // Unauthorized verification modification is blocked.
    if (pathname === '/api/ae/verify') {
      handleVerifyRequest(req, res, pathname);
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
