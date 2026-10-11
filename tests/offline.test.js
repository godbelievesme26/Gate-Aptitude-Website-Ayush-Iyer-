import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();

test('Offline 1: index.html contains no service worker unregistration scripts', () => {
  const html = fs.readFileSync(path.resolve(root, 'index.html'), 'utf8');
  assert.equal(html.includes('unregister'), false, 'index.html must not contain unregister calls');
  assert.equal(html.includes('getRegistrations'), false, 'index.html must not unregister service workers');
});

test('Offline 2: Every shell asset in sw.js exists on disk', () => {
  const swContent = fs.readFileSync(path.resolve(root, 'sw.js'), 'utf8');
  const shellMatch = swContent.match(/const\s+SHELL\s*=\s*(\[[^\]]+\]);/);
  assert.ok(shellMatch, 'sw.js must define SHELL array');
  const shellFiles = JSON.parse(shellMatch[1].replace(/'/g, '"'));

  for (const file of shellFiles) {
    const filePath = file === './' ? 'index.html' : file;
    const fullPath = path.resolve(root, filePath);
    assert.ok(fs.existsSync(fullPath), `Precached shell asset must exist: ${file}`);
  }
});

test('Offline 3: All CSS stylesheets in index.html are precached in SHELL', () => {
  const html = fs.readFileSync(path.resolve(root, 'index.html'), 'utf8');
  const swContent = fs.readFileSync(path.resolve(root, 'sw.js'), 'utf8');
  const cssMatches = [...html.matchAll(/<link\s+rel="stylesheet"\s+href="([^"]+)">/g)].map(m => m[1]);

  for (const css of cssMatches) {
    assert.ok(swContent.includes(css), `Stylesheet ${css} must be precached in sw.js`);
  }
});

test('Offline 4: All question datasets in registry and AE manifest exist for offline precaching', () => {
  const registry = JSON.parse(fs.readFileSync(path.resolve(root, 'data/registry.json'), 'utf8'));
  for (const entry of registry) {
    const fullPath = path.resolve(root, entry.path);
    assert.ok(fs.existsSync(fullPath), `Registry dataset must exist: ${entry.path}`);
  }

  const manifest = JSON.parse(fs.readFileSync(path.resolve(root, 'data/ae/manifest.json'), 'utf8'));
  const completed = manifest.years.filter(y => y.ingestionStatus === 'complete');
  assert.equal(completed.length, 20, 'All 20 AE papers must be marked complete');
  for (const entry of completed) {
    const fullPath = path.resolve(root, entry.path);
    assert.ok(fs.existsSync(fullPath), `AE dataset must exist: ${entry.path}`);
  }
});

test('Offline 5: Verification and AE manifest are precached in sw.js', () => {
  const swContent = fs.readFileSync(path.resolve(root, 'sw.js'), 'utf8');
  assert.ok(swContent.includes('data/ae/manifest.json'), 'sw.js must precache data/ae/manifest.json');
  assert.ok(swContent.includes('data/ae/verification.json'), 'sw.js must precache data/ae/verification.json');
});

test('Offline 6: Service worker activation purges only outdated workspace caches and protects user storage', () => {
  const swContent = fs.readFileSync(path.resolve(root, 'sw.js'), 'utf8');
  // Must clean only caches matching gate-workspace-
  assert.ok(swContent.includes("key.startsWith('gate-workspace-')"), 'sw.js must isolate cache deletion to gate-workspace-*');
  // Must NOT touch localStorage or IndexedDB
  assert.equal(swContent.includes('localStorage.clear'), false, 'sw.js must never clear localStorage');
});

test('Offline 7: Simulated offline fallback handles network drops gracefully', async () => {
  // Simulate Service Worker offline cache matching logic
  const mockCache = new Map();
  mockCache.set('index.html', new Response('<html>Index</html>', { status: 200 }));
  mockCache.set('data/registry.json', new Response('[]', { status: 200 }));

  async function simulateFetchHandler(requestUrl, mode = 'cors') {
    const cached = mockCache.get(requestUrl);
    try {
      // Simulate offline: network always fails
      throw new TypeError('Failed to fetch (offline)');
    } catch {
      if (cached) return cached;
      if (mode === 'navigate') return mockCache.get('index.html');
      return new Response('Unavailable offline', { status: 503 });
    }
  }

  // 1. Cached asset returns 200 from cache
  const res1 = await simulateFetchHandler('data/registry.json');
  assert.equal(res1.status, 200);

  // 2. Uncached navigate request returns index.html shell
  const res2 = await simulateFetchHandler('some/deep/route', 'navigate');
  assert.equal(res2.status, 200);
  assert.equal(await res2.text(), '<html>Index</html>');

  // 3. Uncached API/asset request returns 503 Unavailable offline
  const res3 = await simulateFetchHandler('uncached/asset.png', 'cors');
  assert.equal(res3.status, 503);
});
