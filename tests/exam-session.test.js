import test from 'node:test';
import assert from 'node:assert/strict';
import {Store, defaults, STORAGE_KEY} from '../js/storage.js';
import {ApplicationState} from '../js/state.js';
import {
  generateSession,
  move,
  interruptSession,
  resumeSession,
  abandonSession,
  submit,
  commitQuestionAttempt
} from '../js/domain.js';
import {CountdownTimer, PracticeTimer, createSessionTimer, clock} from '../js/timer.js';
import {saveNumericAnswer} from '../js/answer-input.js';
import {quiz, result, renderExamMode} from '../js/views.js';

function memoryAdapter(initialRaw = null) {
  let raw = initialRaw;
  let throwOnSet = false;
  return {
    getItem: key => (key === STORAGE_KEY ? raw : null),
    setItem: (key, value) => {
      if (throwOnSet) throw new Error('QuotaExceededError: DOMException quota exceeded');
      if (key === STORAGE_KEY) raw = value;
    },
    raw: () => raw,
    setThrowOnSet: val => { throwOnSet = val; }
  };
}

function createSampleArchive() {
  const questions = [
    {
      id: 'gate-2026-test-mcq-01',
      number: 1,
      type: 'MCQ',
      marks: 1,
      negativeMarks: 1 / 3,
      answer: 'B',
      options: [{label: 'A', text: 'Opt A'}, {label: 'B', text: 'Opt B'}, {label: 'C', text: 'Opt C'}, {label: 'D', text: 'Opt D'}],
      year: 2026,
      paper: 'AE',
      section: 'GA',
      question: 'Which is correct?',
      solution: 'Detailed solution for MCQ 1',
      hasFigure: false,
      figures: []
    },
    {
      id: 'gate-2026-test-mcq-02',
      number: 2,
      type: 'MCQ',
      marks: 2,
      negativeMarks: 2 / 3,
      answer: 'C',
      options: [{label: 'A', text: 'Opt A'}, {label: 'B', text: 'Opt B'}, {label: 'C', text: 'Opt C'}, {label: 'D', text: 'Opt D'}],
      year: 2026,
      paper: 'AE',
      section: 'AE',
      question: 'Two mark question',
      solution: 'Detailed solution for MCQ 2',
      hasFigure: false,
      figures: []
    },
    {
      id: 'gate-2026-test-msq-03',
      number: 3,
      type: 'MSQ',
      marks: 2,
      negativeMarks: 0,
      answer: ['A', 'D'],
      options: [{label: 'A', text: 'Opt A'}, {label: 'B', text: 'Opt B'}, {label: 'C', text: 'Opt C'}, {label: 'D', text: 'Opt D'}],
      year: 2026,
      paper: 'AE',
      section: 'AE',
      question: 'Select all correct',
      solution: 'Detailed solution for MSQ 3',
      hasFigure: false,
      figures: []
    },
    {
      id: 'gate-2026-test-nat-04',
      number: 4,
      type: 'NAT',
      marks: 2,
      negativeMarks: 0,
      answer: [42.0, 42.5], // Accepted range
      options: [],
      year: 2026,
      paper: 'AE',
      section: 'AE',
      question: 'Calculate value',
      solution: 'Detailed solution for NAT 4',
      hasFigure: false,
      figures: []
    },
    {
      id: 'gate-2026-test-mta-05',
      number: 5,
      type: 'MCQ',
      marks: 1,
      negativeMarks: 0,
      gradingRule: 'marks-to-all',
      answer: 'MTA',
      options: [{label: 'A', text: 'Opt A'}, {label: 'B', text: 'Opt B'}],
      year: 2026,
      paper: 'AE',
      section: 'AE',
      question: 'Defective official question awarded MTA',
      solution: 'Marks to all officially given',
      hasFigure: false,
      figures: []
    }
  ];
  return {
    questions,
    byId: new Map(questions.map(q => [q.id, q]))
  };
}

// ---------------------------------------------------------------------------
// 1. Session Lifecycle: Initialization, Config & Timers
// ---------------------------------------------------------------------------

test('Exam Session: initializes test mode with duration, deadline and position', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  const startMs = 1700000000000;
  const originalNow = Date.now;
  Date.now = () => startMs;

  try {
    const session = generateSession(
      content.questions,
      app.progress,
      {mode: 'test', minutes: 60, origin: 'paper'},
      'session-exam-01'
    );
    app.addDraft(session);

    assert.equal(session.id, 'session-exam-01');
    assert.equal(session.mode, 'test');
    assert.equal(session.plannedDuration, 3600000); // 60 min * 60,000 ms
    assert.equal(session.deadline, startMs + 3600000);
    assert.equal(session.currentPosition, 0);
    assert.equal(session.status, 'active');
    assert.deepEqual(session.questionIds, content.questions.map(q => q.id));
    assert.equal(session.visited['gate-2026-test-mcq-01'], true);

    // Activate session with CountdownTimer
    const draft = app.activateSession('session-exam-01', s => createSessionTimer(s, () => startMs));
    assert.ok(draft);
    assert.equal(app.session.activeId, 'session-exam-01');
    assert.ok(app.session.timer instanceof CountdownTimer);
    assert.equal(app.session.timer.remaining(), 3600000);
    assert.equal(app.session.timer.expired(), false);
  } finally {
    Date.now = originalNow;
  }
});

// ---------------------------------------------------------------------------
// 2. Answering NAT, MSQ, MCQ & Marking for Review
// ---------------------------------------------------------------------------

test('Exam Session: handles MCQ, MSQ, NAT inputs, review flags and navigation', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  let currentMs = 1700000000000;
  const now = () => currentMs;

  const originalNow = Date.now;
  Date.now = () => currentMs;
  let session;
  try {
    session = generateSession(
      content.questions,
      app.progress,
      {mode: 'test', minutes: 30},
      'session-journey-02'
    );
  } finally {
    Date.now = originalNow;
  }

  app.addDraft(session);
  const timer = createSessionTimer(session, now);
  timer.start();

  // Question 1: MCQ (single choice)
  currentMs += 15000; // 15s
  session.answers['gate-2026-test-mcq-01'] = 'B';
  session.review['gate-2026-test-mcq-01'] = true; // marked for review
  timer.leave();
  move(session, 1);
  timer.start();
  app.save();

  assert.equal(session.answers['gate-2026-test-mcq-01'], 'B');
  assert.equal(session.review['gate-2026-test-mcq-01'], true);
  assert.equal(session.times['gate-2026-test-mcq-01'], 15000);
  assert.equal(session.visited['gate-2026-test-mcq-02'], true);

  // Question 2: MCQ 2-mark (change choice)
  currentMs += 30000; // 30s
  session.answers['gate-2026-test-mcq-02'] = 'A'; // initially A
  session.answers['gate-2026-test-mcq-02'] = 'C'; // changed to correct C
  timer.leave();
  move(session, 2);
  timer.start();
  app.save();

  assert.equal(session.answers['gate-2026-test-mcq-02'], 'C');
  assert.equal(session.times['gate-2026-test-mcq-02'], 30000);

  // Question 3: MSQ (multi-select)
  currentMs += 25000; // 25s
  // User selects A, then B, then unselects B, then selects D
  const msqId = 'gate-2026-test-msq-03';
  session.answers[msqId] = ['A'];
  session.answers[msqId] = [...session.answers[msqId], 'B'];
  assert.deepEqual(session.answers[msqId], ['A', 'B']);
  // Toggle off B
  session.answers[msqId] = session.answers[msqId].filter(x => x !== 'B');
  assert.deepEqual(session.answers[msqId], ['A']);
  // Toggle on D
  session.answers[msqId] = [...session.answers[msqId], 'D'];
  assert.deepEqual(session.answers[msqId], ['A', 'D']);
  timer.leave();
  move(session, 3);
  timer.start();
  app.save();

  // Question 4: NAT (numeric input)
  currentMs += 40000; // 40s
  const natQ = content.byId.get('gate-2026-test-nat-04');
  // Intermediate inputs should be allowed
  saveNumericAnswer(app, session, natQ, '-');
  assert.equal(session.answers[natQ.id], '-');
  saveNumericAnswer(app, session, natQ, '42.3');
  assert.equal(session.answers[natQ.id], '42.3');
  timer.leave();
  move(session, 4);
  timer.start();
  app.save();

  // Question 5: MTA question left blank
  currentMs += 10000; // 10s
  timer.leave();
  app.save();

  assert.equal(session.elapsed, 120000); // 15 + 30 + 25 + 40 + 10 = 120s
});

// ---------------------------------------------------------------------------
// 3. Tab Reload / Refresh Persistence & Timer Resumption
// ---------------------------------------------------------------------------

test('Exam Session: persists draft across simulated tab reload with exact timer anchor', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const initialStore = new Store(adapter);
  const initialApp = new ApplicationState(initialStore);
  initialApp.initializeContent(content);

  const testStartTime = 1700000000000;
  let simulatedWallClock = testStartTime;
  const now = () => simulatedWallClock;

  const originalNow = Date.now;
  Date.now = () => simulatedWallClock;
  let session;
  try {
    session = generateSession(
      content.questions,
      initialApp.progress,
      {mode: 'test', minutes: 30},
      'persistent-session-03'
    );
  } finally {
    Date.now = originalNow;
  }

  initialApp.addDraft(session);
  const timer = createSessionTimer(session, now);
  timer.start();

  // Work on Q1 for 60s and answer
  simulatedWallClock += 60000;
  timer.flush();
  session.answers['gate-2026-test-mcq-01'] = 'B';
  session.review['gate-2026-test-mcq-01'] = true;
  move(session, 1);
  initialApp.save();

  // Tab is closed / reloaded 5 minutes later
  simulatedWallClock += 300000; // 5 min elapsed while away

  // New browser tab loads
  const restoredStore = new Store(adapter);
  const restoredApp = new ApplicationState(restoredStore);
  restoredApp.initializeContent(content);

  assert.ok(restoredApp.progress.drafts['persistent-session-03']);
  const restoredSession = restoredApp.activateSession('persistent-session-03', s => createSessionTimer(s, now));

  assert.equal(restoredSession.id, 'persistent-session-03');
  assert.equal(restoredSession.answers['gate-2026-test-mcq-01'], 'B');
  assert.equal(restoredSession.review['gate-2026-test-mcq-01'], true);
  assert.equal(restoredSession.currentPosition, 1);
  assert.equal(restoredSession.times['gate-2026-test-mcq-01'], 60000);

  // Timer remains anchored to absolute wall clock deadline
  // 30 min duration (1800000 ms) - 1 min answering (60000 ms) - 5 min away (300000 ms) = 24 min remaining (1440000 ms)
  const remainingMs = restoredApp.session.timer.remaining();
  assert.equal(remainingMs, 1440000);
  assert.equal(restoredApp.session.timer.expired(), false);

  // Resume work on Q2 for 2 minutes
  restoredApp.session.timer.start();
  simulatedWallClock += 120000;
  restoredApp.session.timer.flush();
  restoredSession.answers['gate-2026-test-mcq-02'] = 'C';
  restoredApp.save();

  assert.equal(restoredSession.times['gate-2026-test-mcq-02'], 120000);
});

// ---------------------------------------------------------------------------
// 4. Deadline Expiry & Auto-Submission
// ---------------------------------------------------------------------------

test('Exam Session: triggers timer expiration when wall clock exceeds deadline', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  const startMs = 1700000000000;
  let simulatedTime = startMs;
  const now = () => simulatedTime;

  const originalNow = Date.now;
  Date.now = () => simulatedTime;
  let session;
  try {
    session = generateSession(
      content.questions,
      app.progress,
      {mode: 'test', minutes: 10}, // 10 min = 600,000 ms
      'expiring-session-04'
    );
  } finally {
    Date.now = originalNow;
  }

  app.addDraft(session);
  const timer = createSessionTimer(session, now);
  timer.start();

  assert.equal(timer.remaining(), 600000);
  assert.equal(timer.expired(), false);

  // Jump to 10 minutes and 1 second later
  simulatedTime += 600001;
  assert.equal(timer.remaining(), 0);
  assert.equal(timer.expired(), true);

  // Completing expired session succeeds and records session
  timer.stop();
  const record = app.completeSession(session, content.byId, new Date(simulatedTime));
  assert.equal(record.status, 'completed');
  assert.equal(app.progress.sessions.length, 1);
  assert.equal(app.progress.drafts['expiring-session-04'], undefined);
});

// ---------------------------------------------------------------------------
// 5. Complete Submission, Scoring & Results Verification
// ---------------------------------------------------------------------------

test('Exam Session: verifies end-to-end scoring, attempt records, MTA and XP', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  const submitTime = new Date('2026-10-11T12:00:00.000Z');
  const session = generateSession(
    content.questions,
    app.progress,
    {mode: 'test', minutes: 30},
    'scoring-session-05'
  );
  app.addDraft(session);

  // Configure answers:
  // Q1 (1-mark MCQ): Correct B (+1)
  session.answers['gate-2026-test-mcq-01'] = 'B';
  session.times['gate-2026-test-mcq-01'] = 20000;

  // Q2 (2-mark MCQ): Incorrect A (-0.6666666666666666)
  session.answers['gate-2026-test-mcq-02'] = 'A';
  session.times['gate-2026-test-mcq-02'] = 45000;

  // Q3 (2-mark MSQ): Correct ['A', 'D'] (+2)
  session.answers['gate-2026-test-msq-03'] = ['A', 'D'];
  session.times['gate-2026-test-msq-03'] = 50000;

  // Q4 (2-mark NAT): Correct 42.2 within [42.0, 42.5] (+2)
  session.answers['gate-2026-test-nat-04'] = '42.2';
  session.times['gate-2026-test-nat-04'] = 35000;

  // Q5 (1-mark MCQ MTA): Blank (Marks to all awards +1 to everyone)
  session.times['gate-2026-test-mta-05'] = 5000;

  session.elapsed = 155000;

  const record = app.completeSession(session, content.byId, submitTime);

  assert.equal(record.id, 'scoring-session-05');
  assert.equal(record.status, 'completed');
  assert.equal(record.endedAt, submitTime.toISOString());
  assert.equal(app.progress.drafts['scoring-session-05'], undefined);

  // Total marks:
  // Q1: +1
  // Q2: -2/3 = -0.6666666666666666
  // Q3: +2
  // Q4: +2
  // Q5: +1 (MTA awarded)
  // Total score = 1 - 2/3 + 2 + 2 + 1 = 6 - 0.6666666666666666 = 5.333333333333334
  assert.equal(record.result.correct, 3); // Q1, Q3, Q4
  assert.equal(record.result.incorrect, 1); // Q2
  assert.equal(record.result.awarded, 1); // Q5
  assert.equal(record.result.answered, 4);
  assert.equal(record.result.blank, 0); // Q5 result is 'awarded', not 'blank'
  assert.equal(record.result.maxMarks, 8); // 1 + 2 + 2 + 2 + 1
  assert.ok(Math.abs(record.result.score - (6 - 2/3)) < 1e-6);

  // Attempt records in state
  assert.equal(app.progress.attempts.length, 5);
  const q5Attempt = app.progress.attempts.find(a => a.questionId === 'gate-2026-test-mta-05');
  assert.equal(q5Attempt.correctness, 'awarded');

  // Participation XP awarded for 4 answered questions
  const xpCount = Object.keys(app.progress.xpEvents).length;
  assert.equal(xpCount, 4);

  // Render Result view
  const resultHtml = result(app.progress, content, record.id);
  assert.ok(resultHtml.includes('Feedback') || resultHtml.includes('feedback-row'));
  assert.ok(resultHtml.includes('Question 1'));
  assert.ok(resultHtml.includes('Question 5'));
});

// ---------------------------------------------------------------------------
// 6. Exam Mode CBT UI & Submission Confirmation View
// ---------------------------------------------------------------------------

test('Exam Session: CBT exam mode view renders questions and submission summary correctly', () => {
  const content = createSampleArchive();
  const session = generateSession(
    content.questions,
    defaults(),
    {mode: 'test', origin: 'paper'},
    'cbt-view-session-06'
  );
  session.answers['gate-2026-test-mcq-01'] = 'B';
  session.review['gate-2026-test-mcq-02'] = true;
  session.visited['gate-2026-test-mcq-01'] = true;
  session.visited['gate-2026-test-mcq-02'] = true;

  const timer = new CountdownTimer(session);

  // Question render
  const html = quiz(defaults(), content, session, timer);
  assert.ok(html.includes('AE Aerospace Engineering') || html.includes('solve-experience') || html.includes('cbt-'));

  // Submit confirmation dialog render
  session.showSubmitConfirm = true;
  const confirmHtml = renderExamMode(defaults(), content, session, timer);
  assert.ok(confirmHtml.includes('Exam Summary'));
  assert.ok(confirmHtml.includes('Are you sure you want to submit the exam?'));
  assert.ok(confirmHtml.includes('data-action="exam-submit-final"'));
  assert.ok(confirmHtml.includes('data-action="exam-submit-cancel"'));
});

// ---------------------------------------------------------------------------
// 7. Storage Quota Exceeded & Read-Only Defense
// ---------------------------------------------------------------------------

test('Exam Session: quota exceeded triggers read-only lock and preserves original data', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  // First save succeeds
  app.updateProgress(p => { p.notes['note-1'] = 'Initial save'; });
  assert.equal(store.readOnly, false);
  const lastGoodRaw = adapter.raw();
  assert.ok(lastGoodRaw);

  // Simulate QuotaExceededError on next write
  adapter.setThrowOnSet(true);

  assert.throws(() => {
    app.updateProgress(p => { p.notes['note-2'] = 'Will fail quota'; });
  }, /Progress could not be saved/);

  // Store is locked to read-only to protect corrupting state
  assert.equal(store.readOnly, true);
  assert.equal(store.recovery.kind, 'write-failed');
  assert.equal(store.recovery.rawAvailable, true);
  assert.equal(store.raw(), lastGoodRaw); // Original data was NOT wiped or corrupted
});

// ---------------------------------------------------------------------------
// 8. Multi-Tab Conflict Defense
// ---------------------------------------------------------------------------

test('Exam Session: concurrent tab conflict blocks unsynchronized progress overwrites', () => {
  const content = createSampleArchive();
  const adapter = memoryAdapter();
  const store = new Store(adapter);
  const app = new ApplicationState(store);
  app.initializeContent(content);

  // User sets tab conflict flag (as triggered by window.storage event)
  app.ui.conflict = true;

  assert.throws(() => {
    app.save();
  }, /Another tab changed your progress/);
});
