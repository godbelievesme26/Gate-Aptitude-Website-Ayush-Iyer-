import test, { after } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { scoreQuestion, scoreSession, answered, matchNatRange } from '../js/scoring.js';
import { saveNumericAnswer } from '../js/answer-input.js';
import { questionAnswer } from '../js/question-content.js';
import { server, isPublicAllowedPath } from '../scripts/serve.mjs';
import { defaults, validateState, Store } from '../js/storage.js';

// Load real canonical question datasets for affected questions
const ae2016 = JSON.parse(fs.readFileSync('data/ae/2016.json', 'utf8'));
const ae2018 = JSON.parse(fs.readFileSync('data/ae/2018.json', 'utf8'));
const ae2019 = JSON.parse(fs.readFileSync('data/ae/2019.json', 'utf8'));
const ae2021 = JSON.parse(fs.readFileSync('data/ae/2021.json', 'utf8'));
const ae2022 = JSON.parse(fs.readFileSync('data/ae/2022.json', 'utf8'));

const findQuestion = (dataset, id) => dataset.questions.find(q => q.id === id);

// -------------------------------------------------------------
// PHASE 1: NAT SCORING FOR MULTIPLE ACCEPTED RANGES
// -------------------------------------------------------------

test('Phase 1: matchNatRange handles single numbers and intervals', () => {
  assert.equal(matchNatRange(42, 42), true);
  assert.equal(matchNatRange(41.9, 42), false);
  assert.equal(matchNatRange(10, [10, 20]), true);
  assert.equal(matchNatRange(20, [10, 20]), true);
  assert.equal(matchNatRange(15, [10, 20]), true);
  assert.equal(matchNatRange(9.99, [10, 20]), false);
  assert.equal(matchNatRange(20.01, [10, 20]), false);
});

test('Phase 1: matchNatRange handles disjoint intervals and negative numbers', () => {
  const disjoint = [[10, 20], [30, 40]];
  assert.equal(matchNatRange(10, disjoint), true);
  assert.equal(matchNatRange(20, disjoint), true);
  assert.equal(matchNatRange(15, disjoint), true);
  assert.equal(matchNatRange(30, disjoint), true);
  assert.equal(matchNatRange(40, disjoint), true);
  assert.equal(matchNatRange(35, disjoint), true);
  // Between disjoint intervals
  assert.equal(matchNatRange(25, disjoint), false);
  assert.equal(matchNatRange(9.9, disjoint), false);
  assert.equal(matchNatRange(40.1, disjoint), false);

  const negativeIntervals = [[49, 51], [-51, -49]];
  assert.equal(matchNatRange(50, negativeIntervals), true);
  assert.equal(matchNatRange(-50, negativeIntervals), true);
  assert.equal(matchNatRange(-51, negativeIntervals), true);
  assert.equal(matchNatRange(-49, negativeIntervals), true);
  assert.equal(matchNatRange(0, negativeIntervals), false);
  assert.equal(matchNatRange(-51.01, negativeIntervals), false);
  assert.equal(matchNatRange(-48.99, negativeIntervals), false);
});

test('Phase 1: Real GATE Question 1: gate-2016-ae-ae-36 ([[162,166],[1147,1150]])', () => {
  const q = findQuestion(ae2016, 'gate-2016-ae-ae-36');
  assert.ok(q, 'gate-2016-ae-ae-36 exists');
  assert.deepEqual(q.answer, [[162.0, 166.0], [1147.0, 1150.0]]);
  assert.equal(q.marks, 2);

  // First range: [162, 166]
  assert.equal(scoreQuestion(q, '162').marks, 2);
  assert.equal(scoreQuestion(q, '166').marks, 2);
  assert.equal(scoreQuestion(q, '164.5').marks, 2);

  // Second range: [1147, 1150]
  assert.equal(scoreQuestion(q, '1147').marks, 2);
  assert.equal(scoreQuestion(q, '1150').marks, 2);
  assert.equal(scoreQuestion(q, '1148.2').marks, 2);

  // Between and outside intervals
  assert.equal(scoreQuestion(q, '500').marks, 0);
  assert.equal(scoreQuestion(q, '161.9').marks, 0);
  assert.equal(scoreQuestion(q, '166.1').marks, 0);
  assert.equal(scoreQuestion(q, '1146.9').marks, 0);
  assert.equal(scoreQuestion(q, '1150.1').marks, 0);
  assert.equal(scoreQuestion(q, '500').penalty, 0); // No negative marks for NAT
});

test('Phase 1: Real GATE Question 2: gate-2018-ae-ae-54 ([[7.8,7.8],[7800,7802]])', () => {
  const q = findQuestion(ae2018, 'gate-2018-ae-ae-54');
  assert.ok(q, 'gate-2018-ae-ae-54 exists');
  assert.deepEqual(q.answer, [[7.8, 7.8], [7800, 7802]]);
  assert.equal(q.marks, 2);

  // Exact point in first interval
  assert.equal(scoreQuestion(q, '7.8').marks, 2);
  assert.equal(scoreQuestion(q, '7.80').marks, 2);

  // Second interval: [7800, 7802]
  assert.equal(scoreQuestion(q, '7800').marks, 2);
  assert.equal(scoreQuestion(q, '7801').marks, 2);
  assert.equal(scoreQuestion(q, '7802').marks, 2);

  // Incorrect
  assert.equal(scoreQuestion(q, '7.7').marks, 0);
  assert.equal(scoreQuestion(q, '7.9').marks, 0);
  assert.equal(scoreQuestion(q, '7799').marks, 0);
  assert.equal(scoreQuestion(q, '7803').marks, 0);
  assert.equal(scoreQuestion(q, '100').marks, 0);
});

test('Phase 1: Real GATE Question 3: gate-2019-ae-ae-46 ([[3.5,3.7],[2.3,2.5]])', () => {
  const q = findQuestion(ae2019, 'gate-2019-ae-ae-46');
  assert.ok(q, 'gate-2019-ae-ae-46 exists');
  assert.deepEqual(q.answer, [[3.5, 3.7], [2.3, 2.5]]);
  assert.equal(q.marks, 2);

  // Range 1: [3.5, 3.7]
  assert.equal(scoreQuestion(q, '3.5').marks, 2);
  assert.equal(scoreQuestion(q, '3.6').marks, 2);
  assert.equal(scoreQuestion(q, '3.7').marks, 2);

  // Range 2: [2.3, 2.5]
  assert.equal(scoreQuestion(q, '2.3').marks, 2);
  assert.equal(scoreQuestion(q, '2.4').marks, 2);
  assert.equal(scoreQuestion(q, '2.5').marks, 2);

  // Between and outside
  assert.equal(scoreQuestion(q, '3.0').marks, 0);
  assert.equal(scoreQuestion(q, '2.2').marks, 0);
  assert.equal(scoreQuestion(q, '3.8').marks, 0);
});

test('Phase 1: Real GATE Question 4: gate-2021-ae-ae-29 ([[264,264],[833,835]])', () => {
  const q = findQuestion(ae2021, 'gate-2021-ae-ae-29');
  assert.ok(q, 'gate-2021-ae-ae-29 exists');
  assert.deepEqual(q.answer, [[264, 264], [833, 835]]);
  assert.equal(q.marks, 1);

  assert.equal(scoreQuestion(q, '264').marks, 1);
  assert.equal(scoreQuestion(q, '833').marks, 1);
  assert.equal(scoreQuestion(q, '834').marks, 1);
  assert.equal(scoreQuestion(q, '835').marks, 1);

  assert.equal(scoreQuestion(q, '263').marks, 0);
  assert.equal(scoreQuestion(q, '265').marks, 0);
  assert.equal(scoreQuestion(q, '832').marks, 0);
  assert.equal(scoreQuestion(q, '836').marks, 0);
});

test('Phase 1: Real GATE Question 5: gate-2021-ae-ae-35 ([[7.75,7.77],[7750,7770]])', () => {
  const q = findQuestion(ae2021, 'gate-2021-ae-ae-35');
  assert.ok(q, 'gate-2021-ae-ae-35 exists');
  assert.deepEqual(q.answer, [[7.75, 7.77], [7750, 7770]]);
  assert.equal(q.marks, 1);

  assert.equal(scoreQuestion(q, '7.75').marks, 1);
  assert.equal(scoreQuestion(q, '7.76').marks, 1);
  assert.equal(scoreQuestion(q, '7.77').marks, 1);

  assert.equal(scoreQuestion(q, '7750').marks, 1);
  assert.equal(scoreQuestion(q, '7760').marks, 1);
  assert.equal(scoreQuestion(q, '7770').marks, 1);

  assert.equal(scoreQuestion(q, '7.74').marks, 0);
  assert.equal(scoreQuestion(q, '7.78').marks, 0);
  assert.equal(scoreQuestion(q, '7749').marks, 0);
  assert.equal(scoreQuestion(q, '7771').marks, 0);
  assert.equal(scoreQuestion(q, '500').marks, 0);
});

test('Phase 1: Real GATE Question 6: gate-2022-ae-ae-55 ([[49,51],[-51,-49]])', () => {
  const q = findQuestion(ae2022, 'gate-2022-ae-ae-55');
  assert.ok(q, 'gate-2022-ae-ae-55 exists');
  assert.deepEqual(q.answer, [[49.0, 51.0], [-51.0, -49.0]]);
  assert.equal(q.marks, 2);

  // Positive range [49, 51]
  assert.equal(scoreQuestion(q, '49').marks, 2);
  assert.equal(scoreQuestion(q, '50').marks, 2);
  assert.equal(scoreQuestion(q, '51').marks, 2);

  // Negative range [-51, -49]
  assert.equal(scoreQuestion(q, '-51').marks, 2);
  assert.equal(scoreQuestion(q, '-50').marks, 2);
  assert.equal(scoreQuestion(q, '-49').marks, 2);

  // Outside / between
  assert.equal(scoreQuestion(q, '0').marks, 0);
  assert.equal(scoreQuestion(q, '48.9').marks, 0);
  assert.equal(scoreQuestion(q, '51.1').marks, 0);
  assert.equal(scoreQuestion(q, '-51.1').marks, 0);
  assert.equal(scoreQuestion(q, '-48.9').marks, 0);
});

test('Phase 1: questionAnswer() formats disjoint intervals with OR', () => {
  const qDisjoint = { type: 'NAT', answer: [[162, 166], [1147, 1150]] };
  assert.equal(questionAnswer(qDisjoint), '162 to 166 OR 1147 to 1150');

  const qPointAndInterval = { type: 'NAT', answer: [[7.8, 7.8], [7800, 7802]] };
  assert.equal(questionAnswer(qPointAndInterval), '7.8 OR 7800 to 7802');

  const qSingle = { type: 'NAT', answer: [10, 20] };
  assert.equal(questionAnswer(qSingle), '10 to 20');

  const qExact = { type: 'NAT', answer: 42 };
  assert.equal(questionAnswer(qExact), '42');
});

// -------------------------------------------------------------
// PHASE 2: NUMERIC INPUT VALIDATION
// -------------------------------------------------------------

test('Phase 2: answered() treats empty and whitespace-only as false', () => {
  assert.equal(answered(''), false);
  assert.equal(answered(' '), false);
  assert.equal(answered('   '), false);
  assert.equal(answered(' \t\n '), false);
  assert.equal(answered(undefined), false);
  assert.equal(answered(null), false);
  assert.equal(answered([]), false);

  // Valid values evaluate to true
  assert.equal(answered('0'), true);
  assert.equal(answered('0.0'), true);
  assert.equal(answered('-0'), true);
  assert.equal(answered(0), true);
  assert.equal(answered(-5), true);
  assert.equal(answered('12.5'), true);
  assert.equal(answered('-12.5'), true);
  assert.equal(answered('  12.5  '), true);
  assert.equal(answered(['A']), true);
  assert.equal(answered('A'), true);
});

test('Phase 2: scoreQuestion() never awards marks to whitespace even when key contains zero', () => {
  const qZero = { type: 'NAT', answer: 0, marks: 2, negativeMarks: 0 };
  const qIntervalWithZero = { type: 'NAT', answer: [-1, 1], marks: 2, negativeMarks: 0 };

  // Whitespace-only must be blank, never correct
  assert.deepEqual(scoreQuestion(qZero, ''), { result: 'blank', marks: 0, penalty: 0 });
  assert.deepEqual(scoreQuestion(qZero, ' '), { result: 'blank', marks: 0, penalty: 0 });
  assert.deepEqual(scoreQuestion(qZero, '   '), { result: 'blank', marks: 0, penalty: 0 });
  assert.deepEqual(scoreQuestion(qIntervalWithZero, '   '), { result: 'blank', marks: 0, penalty: 0 });

  // Valid zero
  assert.deepEqual(scoreQuestion(qZero, '0'), { result: 'correct', marks: 2, penalty: 0 });
  assert.deepEqual(scoreQuestion(qZero, '0.0'), { result: 'correct', marks: 2, penalty: 0 });
  assert.deepEqual(scoreQuestion(qZero, '-0'), { result: 'correct', marks: 2, penalty: 0 });
  assert.deepEqual(scoreQuestion(qZero, 0), { result: 'correct', marks: 2, penalty: 0 });
});

test('Phase 2: scoreQuestion() strictly rejects invalid and non-finite numeric strings', () => {
  const q = { type: 'NAT', answer: 10, marks: 1, negativeMarks: 0 };
  assert.equal(scoreQuestion(q, 'abc').result, 'incorrect');
  assert.equal(scoreQuestion(q, 'Infinity').result, 'incorrect');
  assert.equal(scoreQuestion(q, '-Infinity').result, 'incorrect');
  assert.equal(scoreQuestion(q, 'NaN').result, 'incorrect');

  // Scientific notation consistent with Number parsing
  const q1000 = { type: 'NAT', answer: 1000, marks: 1, negativeMarks: 0 };
  assert.equal(scoreQuestion(q1000, '1e3').result, 'correct');
  assert.equal(scoreQuestion(q1000, '  1000  ').result, 'correct');
});

test('Phase 2: saveNumericAnswer() validates persistence, whitespace, and intermediate states', () => {
  const makeMockApp = () => {
    const s = defaults();
    const session = { id: 's1', questionIds: ['q1'], currentPosition: 0, answers: {} };
    s.drafts.s1 = session;
    return {
      progress: s,
      updateProgress(fn) { fn(this.progress); },
      session,
      q: { id: 'q1', type: 'NAT' }
    };
  };

  // Valid numbers
  const app1 = makeMockApp();
  assert.equal(saveNumericAnswer(app1, app1.session, app1.q, '12.5'), true);
  assert.equal(app1.session.answers.q1, '12.5');

  // Whitespace-only trims to empty string (unanswered)
  const app2 = makeMockApp();
  assert.equal(saveNumericAnswer(app2, app2.session, app2.q, '   '), true);
  assert.equal(app2.session.answers.q1, '');
  assert.equal(answered(app2.session.answers.q1), false);

  // Leading and trailing whitespace around valid number
  const app3 = makeMockApp();
  assert.equal(saveNumericAnswer(app3, app3.session, app3.q, '  42.5  '), true);
  assert.equal(app3.session.answers.q1, '42.5');

  // Valid zeroes and negatives
  const app4 = makeMockApp();
  saveNumericAnswer(app4, app4.session, app4.q, '0');
  assert.equal(app4.session.answers.q1, '0');
  saveNumericAnswer(app4, app4.session, app4.q, '-0');
  assert.equal(app4.session.answers.q1, '-0');
  saveNumericAnswer(app4, app4.session, app4.q, '-12.5');
  assert.equal(app4.session.answers.q1, '-12.5');

  // Intermediate states: '-', '.', '-.' do NOT throw
  const app5 = makeMockApp();
  assert.doesNotThrow(() => saveNumericAnswer(app5, app5.session, app5.q, '-'));
  assert.equal(app5.session.answers.q1, '-');
  assert.doesNotThrow(() => saveNumericAnswer(app5, app5.session, app5.q, '.'));
  assert.equal(app5.session.answers.q1, '.');
  assert.doesNotThrow(() => saveNumericAnswer(app5, app5.session, app5.q, '-.'));
  assert.equal(app5.session.answers.q1, '-.');

  // Invalid numbers throw
  const app6 = makeMockApp();
  assert.throws(() => saveNumericAnswer(app6, app6.session, app6.q, 'abc'), /valid number/);
  assert.throws(() => saveNumericAnswer(app6, app6.session, app6.q, 'Infinity'), /valid number/);
  assert.throws(() => saveNumericAnswer(app6, app6.session, app6.q, 'NaN'), /valid number/);
  assert.throws(() => saveNumericAnswer(app6, app6.session, app6.q, 123), /valid number/);
});

// -------------------------------------------------------------
// PHASE 3 & 4: HTTP SERVER SECURITY & STATIC ASSET POLICY
// -------------------------------------------------------------

function makeRequest(port, method, reqPath, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: '127.0.0.1',
      port,
      path: reqPath,
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    const req = http.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        let json = null;
        try { json = JSON.parse(data); } catch {}
        resolve({ statusCode: res.statusCode, headers: res.headers, body: data, json });
      });
    });
    req.on('error', reject);
    if (body) {
      req.write(typeof body === 'string' ? body : JSON.stringify(body));
    }
    req.end();
  });
}

test('Phase 3 & 4: HTTP server security, verification lock, and static allowlist', async () => {
  // Bind server to ephemeral port
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const testPort = server.address().port;

  try {
    // 1. Phase 3: POST /api/ae/verify is strictly FORBIDDEN on student server
    const verifyBefore = fs.readFileSync('data/ae/verification.json', 'utf8');
    const postVerify = await makeRequest(testPort, 'POST', '/api/ae/verify', {
      questionId: 'gate-2026-ae-ae-11',
      status: 'verified'
    });
    assert.equal(postVerify.statusCode, 403, 'POST /api/ae/verify must return 403 Forbidden');
    assert.equal(postVerify.json.ok, false);
    // Verification file MUST be unmodified
    const verifyAfter = fs.readFileSync('data/ae/verification.json', 'utf8');
    assert.equal(verifyBefore, verifyAfter, 'data/ae/verification.json must not be modified');

    // 2. GET /api/ae/verify returns 200 with read-only verification
    const getVerify = await makeRequest(testPort, 'GET', '/api/ae/verify');
    assert.equal(getVerify.statusCode, 200);
    assert.equal(getVerify.json.ok, true);

    // 3. PUT /api/ae/verify returns 405 Method Not Allowed
    const putVerify = await makeRequest(testPort, 'PUT', '/api/ae/verify', {});
    assert.equal(putVerify.statusCode, 405);

    // 4. Phase 4: Public assets ALLOWED (200 OK)
    const allowedCases = [
      '/',
      '/index.html',
      '/sw.js',
      '/manifest.webmanifest',
      '/css/style.css',
      '/js/app.js',
      '/js/scoring.js',
      '/assets/logo.svg',
      '/data/registry.json',
      '/data/day01.json',
      '/data/ae/manifest.json',
      '/data/ae/verification.json',
      '/data/ae/2026.json'
    ];
    for (const p of allowedCases) {
      const res = await makeRequest(testPort, 'GET', p);
      assert.equal(res.statusCode, 200, `Expected 200 for allowed public resource: ${p}`);
    }

    // HEAD request on public asset
    const headRes = await makeRequest(testPort, 'HEAD', '/index.html');
    assert.equal(headRes.statusCode, 200);

    // 5. Phase 4: Private project files and dangerous paths BLOCKED (404 Not Found)
    const blockedCases = [
      '/package.json',
      '/package-lock.json',
      '/scripts/serve.mjs',
      '/scripts/check.mjs',
      '/tests/verification.test.js',
      '/.gitignore',
      '/internal/ae/ocr_queue.json',
      '/internal/ae/forensic_review_state.json',
      '/internal/ae/forensic_audit_trail.jsonl',
      '/native/tcs-calculator.exe',
      '/README.md',
      '/scratch/backup_pre_stage_a/js/scoring.js',
      // Directory traversal attempts
      '/..%2fpackage.json',
      '/css/../../package.json',
      '/data/ae/../package.json'
    ];
    for (const p of blockedCases) {
      const res = await makeRequest(testPort, 'GET', p);
      assert.equal(res.statusCode, 404, `Expected 404 for blocked resource: ${p}`);
    }

    // 6. Non-GET/HEAD methods on static assets return 405
    const postStatic = await makeRequest(testPort, 'POST', '/index.html', {});
    assert.equal(postStatic.statusCode, 405);
    const deleteStatic = await makeRequest(testPort, 'DELETE', '/data/registry.json');
    assert.equal(deleteStatic.statusCode, 405);

  } finally {
    await new Promise(resolve => server.close(resolve));
  }
});

test('Phase 4: isPublicAllowedPath helper enforces strict allowlist', () => {
  assert.equal(isPublicAllowedPath('/'), true);
  assert.equal(isPublicAllowedPath('/index.html'), true);
  assert.equal(isPublicAllowedPath('/css/style.css'), true);
  assert.equal(isPublicAllowedPath('/js/scoring.js'), true);
  assert.equal(isPublicAllowedPath('/data/day16.json'), true);
  assert.equal(isPublicAllowedPath('/data/ae/2026.json'), true);
  assert.equal(isPublicAllowedPath('/assets/logo.svg'), true);
  assert.equal(isPublicAllowedPath('/figures/q1_fig.png'), true);

  // Query strings and fragments handled safely
  assert.equal(isPublicAllowedPath('/index.html?v=1.0'), true);
  assert.equal(isPublicAllowedPath('/css/style.css#main'), true);

  // Blocked
  assert.equal(isPublicAllowedPath('/package.json'), false);
  assert.equal(isPublicAllowedPath('/package-lock.json'), false);
  assert.equal(isPublicAllowedPath('/scripts/serve.mjs'), false);
  assert.equal(isPublicAllowedPath('/tests/views.test.js'), false);
  assert.equal(isPublicAllowedPath('/.env'), false);
  assert.equal(isPublicAllowedPath('/internal/ae/ocr_queue.json'), false);
  assert.equal(isPublicAllowedPath('../package.json'), false);
  assert.equal(isPublicAllowedPath('/css/../package.json'), false);
  assert.equal(isPublicAllowedPath('/data/ae/evil.json'), false);
  assert.equal(isPublicAllowedPath('//index.html'), false);
  assert.equal(isPublicAllowedPath('/assets/.hidden.png'), false);
  assert.equal(isPublicAllowedPath('/figures/.secret.jpg'), false);
  assert.equal(isPublicAllowedPath('/index.html\0'), false);
  assert.equal(isPublicAllowedPath('/index.html\x1b'), false);
});

// -------------------------------------------------------------
// PHASE 5: DEFENSIVE MSQ INPUT HANDLING
// -------------------------------------------------------------

test('Phase 5: validateState normalizes duplicate MSQ options in imported drafts and attempts', () => {
  const imported = defaults();
  imported.drafts.testDraft = {
    id: 'testDraft',
    startedAt: '2026-09-28T08:00:00.000Z',
    endedAt: null,
    mode: 'practice',
    plannedDuration: null,
    questionIds: ['gate-2026-ae-ae-11'],
    currentPosition: 0,
    status: 'active',
    origin: 'custom',
    configuration: {},
    answers: {
      'gate-2026-ae-ae-11': ['A', 'A', 'B', 'B', 'C'] // Malformed with duplicates
    },
    times: { 'gate-2026-ae-ae-11': 1000 },
    visited: { 'gate-2026-ae-ae-11': true },
    review: {},
    elapsed: 1000,
    deadline: null
  };

  imported.attempts.push({
    attemptId: 'testDraft:gate-2026-ae-ae-11',
    questionId: 'gate-2026-ae-ae-11',
    sessionId: 'testDraft',
    selectedAnswer: ['A', 'B', 'A'], // Malformed with duplicates
    correctness: 'correct',
    timeSpent: 1000,
    mode: 'practice',
    sourceContext: { origin: 'custom' },
    timestamp: '2026-09-28T08:00:01.000Z'
  });

  const validated = validateState(imported);
  assert.deepEqual(validated.drafts.testDraft.answers['gate-2026-ae-ae-11'], ['A', 'B', 'C']);
  assert.deepEqual(validated.attempts[0].selectedAnswer, ['A', 'B']);
});

test('Phase 5: MSQ scoring cannot be inflated by duplicate options', () => {
  const msqQ = {
    id: 'msq-1',
    type: 'MSQ',
    answer: ['A', 'C'],
    marks: 2,
    negativeMarks: 0
  };

  // Exact set matching
  assert.equal(scoreQuestion(msqQ, ['A', 'C']).marks, 2);
  assert.equal(scoreQuestion(msqQ, ['C', 'A']).marks, 2);
  assert.equal(scoreQuestion(msqQ, ['A', 'A', 'C']).marks, 2); // Duplicates do not corrupt

  // Partial or superset receives 0 marks
  assert.equal(scoreQuestion(msqQ, ['A']).marks, 0);
  assert.equal(scoreQuestion(msqQ, ['C']).marks, 0);
  assert.equal(scoreQuestion(msqQ, ['A', 'B', 'C']).marks, 0);
  assert.equal(scoreQuestion(msqQ, ['A', 'A']).marks, 0);
  assert.equal(scoreQuestion(msqQ, []).marks, 0);
});
