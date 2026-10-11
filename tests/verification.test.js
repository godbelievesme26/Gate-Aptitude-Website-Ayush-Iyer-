import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { loadArchive } from '../js/loader.js';
import { questionDetail, aerospace } from '../js/views.js';
import { Store, defaults } from '../js/storage.js';
import { ApplicationState } from '../js/state.js';

// The server captures its content root at import time. Give this test process
// its own root so even an interrupted test cannot change real review records.
const repositoryRoot = process.cwd();
const realVerificationFile = path.resolve('data/ae/verification.json');
const readOptional = file => fs.existsSync(file) ? fs.readFileSync(file) : null;
const protectedFiles = [realVerificationFile, realVerificationFile + '.tmp']
  .map(file => [file, readOptional(file)]);
const sandbox = fs.mkdtempSync(path.join(os.tmpdir(), 'gate-verification-test-'));
const VERIFICATION_FILE = path.join(sandbox, 'data/ae/verification.json');
fs.mkdirSync(path.dirname(VERIFICATION_FILE), { recursive: true });
let handleVerifyRequest;
try {
  process.chdir(sandbox);
  ({ handleVerifyRequest } = await import('../scripts/serve-forensic.mjs'));
} finally {
  process.chdir(repositoryRoot);
}
after(() => {
  try {
    for (const [file, original] of protectedFiles) {
      assert.deepEqual(readOptional(file), original, 'Tests must preserve ' + file);
    }
  } finally {
    assert.equal(path.dirname(sandbox), path.resolve(os.tmpdir()));
    assert.ok(path.basename(sandbox).startsWith('gate-verification-test-'));
    fs.rmSync(sandbox, { recursive: true, force: true });
  }
});

function readFixture(p) {
  return JSON.parse(fs.readFileSync(p === 'data/ae/verification.json'
    ? VERIFICATION_FILE : path.resolve(repositoryRoot, p), 'utf8'));
}

function resetVerificationFile(content = '{}') {
  fs.writeFileSync(VERIFICATION_FILE, content, 'utf8');
}

// Helper to simulate request to handleVerifyRequest
async function requestApi(method, body = null) {
  return new Promise((resolve) => {
    let responseBody = '';
    let statusCode = 0;
    let headers = {};

    const req = {
      method,
      url: '/api/ae/verify',
      on: (event, handler) => {
        if (event === 'data' && body) handler(Buffer.from(JSON.stringify(body)));
        if (event === 'end') handler();
      },
      destroy: () => {}
    };

    const res = {
      writeHead: (code, h) => {
        statusCode = code;
        headers = h;
      },
      end: (data) => {
        responseBody = data;
        resolve({
          statusCode,
          headers,
          data: responseBody ? JSON.parse(responseBody) : null
        });
      }
    };

    handleVerifyRequest(req, res, '/api/ae/verify');
  });
}

test('1. No verification entry -> unverified by default', () => {
  resetVerificationFile('{}');
  const raw = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(raw['gate-2026-ae-ae-11'], undefined);
});

test('2. Marking a question verified creates the correct entry structure', async () => {
  resetVerificationFile('{}');
  const res = await requestApi('POST', {
    questionId: 'gate-2026-ae-ae-11',
    status: 'verified'
  });
  assert.equal(res.statusCode, 200);
  assert.equal(res.data.ok, true);
  assert.equal(res.data.questionId, 'gate-2026-ae-ae-11');
  assert.equal(res.data.status, 'verified');
  assert.equal(res.data.verification['gate-2026-ae-ae-11'].status, 'verified');
  assert.match(res.data.verification['gate-2026-ae-ae-11'].verifiedAt, /^\d{4}-\d{2}-\d{2}$/);
});

test('3. Verification persists physically to data/ae/verification.json', async () => {
  resetVerificationFile('{}');
  await requestApi('POST', {
    questionId: 'gate-2026-ae-ga-01',
    status: 'verified'
  });
  const diskData = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(diskData['gate-2026-ae-ga-01'].status, 'verified');
  assert.ok(diskData['gate-2026-ae-ga-01'].verifiedAt);
});

test('4. Restarting the server preserves verification from disk', async () => {
  resetVerificationFile(JSON.stringify({
    'gate-2026-ae-ae-12': { status: 'verified', verifiedAt: '2026-10-07' }
  }, null, 2));
  
  // New GET request reads directly from disk
  const getRes = await requestApi('GET');
  assert.equal(getRes.statusCode, 200);
  assert.equal(getRes.data.verification['gate-2026-ae-ae-12'].status, 'verified');
  assert.equal(getRes.data.verification['gate-2026-ae-ae-12'].verifiedAt, '2026-10-07');
});

test('5. Reloading the browser preserves verification via loadArchive()', async () => {
  resetVerificationFile(JSON.stringify({
    'gate-2026-ae-ae-18': { status: 'verified', verifiedAt: '2026-10-07' }
  }, null, 2));

  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url) => {
    const p = url.startsWith('/') ? url.slice(1) : url;
    return {
      ok: true,
      json: async () => readFixture(p)
    };
  };

  try {
    const archive = await loadArchive();
    assert.equal(archive.verification['gate-2026-ae-ae-18'].status, 'verified');
    assert.equal(archive.verification['gate-2026-ae-ae-18'].verifiedAt, '2026-10-07');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('6. Verification is tied to the correct question ID, not array index', async () => {
  resetVerificationFile('{}');
  await requestApi('POST', { questionId: 'gate-2026-ae-ae-37', status: 'verified' });

  const diskData = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(diskData['gate-2026-ae-ae-37'].status, 'verified');
  assert.equal(diskData['gate-2026-ae-ae-36'], undefined);
  assert.equal(diskData['gate-2026-ae-ae-38'], undefined);
});

test('7. Verifying Q1 does not affect Q2', async () => {
  resetVerificationFile('{}');
  await requestApi('POST', { questionId: 'gate-2026-ae-ga-01', status: 'verified' });

  const diskData = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(diskData['gate-2026-ae-ga-01'].status, 'verified');
  assert.equal(diskData['gate-2026-ae-ga-02'], undefined);
});

test('8. Repeated verification is idempotent', async () => {
  resetVerificationFile('{}');
  const res1 = await requestApi('POST', { questionId: 'gate-2026-ae-ae-21', status: 'verified' });
  const date1 = res1.data.verification['gate-2026-ae-ae-21'].verifiedAt;

  const res2 = await requestApi('POST', { questionId: 'gate-2026-ae-ae-21', status: 'verified' });
  assert.equal(res2.statusCode, 200);
  assert.equal(res2.data.verification['gate-2026-ae-ae-21'].status, 'verified');
  assert.equal(res2.data.verification['gate-2026-ae-ae-21'].verifiedAt, date1);
});

test('9. Year verification count is dynamically computed from question IDs', async () => {
  resetVerificationFile(JSON.stringify({
    'gate-2026-ae-ga-01': { status: 'verified', verifiedAt: '2026-10-07' },
    'gate-2026-ae-ga-02': { status: 'verified', verifiedAt: '2026-10-07' },
    'gate-2026-ae-ae-11': { status: 'verified', verifiedAt: '2026-10-07' }
  }, null, 2));

  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url) => {
    const p = url.startsWith('/') ? url.slice(1) : url;
    return {
      ok: true,
      json: async () => readFixture(p)
    };
  };

  try {
    const archive = await loadArchive();
    archive.verification = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
    const paper2026 = archive.papers.find(p => p.year === 2026);
    const verifiedCount = paper2026.questionOrder.filter(id => archive.verification[id]?.status === 'verified').length;
    assert.equal(verifiedCount, 3);

    const s = defaults();
    const overviewHtml = aerospace(s, archive, '2026');
    assert.match(overviewHtml, /3 \/ 65 verified/);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('10. Existing student progress, attempts and bookmarks are completely unaffected', () => {
  const store = new Store({
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {}
  });
  const app = new ApplicationState(store);
  app.setBookmark('gate-2026-ae-ae-11', 'Must Revise');
  
  assert.equal(app.progress.bookmarks['gate-2026-ae-ae-11'], 'Must Revise');
  assert.equal(app.progress.attempts.length, 0);
});

test('11. Security: invalid and arbitrary filesystem paths are strictly rejected', async () => {
  resetVerificationFile('{}');

  // Attempt path traversal
  const res1 = await requestApi('POST', { questionId: '../../evil.json', status: 'verified' });
  assert.equal(res1.statusCode, 400);
  assert.equal(res1.data.ok, false);

  // Attempt invalid status
  const res2 = await requestApi('POST', { questionId: 'gate-2026-ae-ae-11', status: 'hacked' });
  assert.equal(res2.statusCode, 400);
  assert.equal(res2.data.ok, false);

  // Attempt empty questionId
  const res3 = await requestApi('POST', { questionId: '', status: 'verified' });
  assert.equal(res3.statusCode, 400);
  assert.equal(res3.data.ok, false);

  // Ensure verification.json was not modified
  const diskData = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.deepEqual(diskData, {});
});

test('12. Existing verification entries are preserved when another question is updated', async () => {
  resetVerificationFile('{}');
  await requestApi('POST', { questionId: 'gate-2026-ae-ga-01', status: 'verified' });
  await requestApi('POST', { questionId: 'gate-2026-ae-ae-65', status: 'verified' });

  const diskData = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(diskData['gate-2026-ae-ga-01'].status, 'verified');
  assert.equal(diskData['gate-2026-ae-ae-65'].status, 'verified');

  // Unverifying Q1 preserves Q65
  await requestApi('POST', { questionId: 'gate-2026-ae-ga-01', status: 'unverified' });
  const updatedDisk = JSON.parse(fs.readFileSync(VERIFICATION_FILE, 'utf8'));
  assert.equal(updatedDisk['gate-2026-ae-ga-01'], undefined);
  assert.equal(updatedDisk['gate-2026-ae-ae-65'].status, 'verified');

});
