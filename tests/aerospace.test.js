import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {generatePaperSession,resolvePaper} from '../js/corpus.js';
import {applyQuestionMarking} from '../js/loader.js';
import {ApplicationState} from '../js/state.js';
import {Store, defaults} from '../js/storage.js';

const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));

function createArchive() {
  const registry = read('data/registry.json');
  const sets = registry.map(e => read(e.path));
  const ga = sets.flatMap(s => s.questions.map(applyQuestionMarking));
  const gaById = new Map(ga.map(q => [q.id, q]));
  const raw2026 = read('data/ae/2026.json');
  const paper2026 = resolvePaper(raw2026, gaById);
  const raw2025 = read('data/ae/2025.json');
  const paper2025 = resolvePaper(raw2025, gaById);
  const manifest = read('data/ae/manifest.json');
  const allQs = [...ga, ...paper2026.questions.slice(10), ...paper2025.questions.slice(10)];
  const byId = new Map(allQs.map(q => [q.id, q]));
  return { registry, sets, questions: allQs, byId, papers: [paper2026, paper2025], corpusManifest: manifest };
}

function createMockStore() {
  let data = JSON.stringify(defaults());
  return new Store({
    getItem: () => data,
    setItem: (k, v) => data = v
  });
}

test('Aerospace corpus loading and manifest properties', async (t) => {
  const archive = createArchive();
  assert.ok(archive.corpusManifest, 'Manifest is loaded');
  assert.equal(archive.corpusManifest.exam, 'GATE');
  assert.equal(archive.corpusManifest.paper, 'AE');
  
  const ae2026Entry = archive.corpusManifest.years.find(y => y.year === 2026);
  assert.equal(ae2026Entry.ingestionStatus, 'complete', '2026 is complete');
  
  const ae2025Entry = archive.corpusManifest.years.find(y => y.year === 2025);
  assert.equal(ae2025Entry.ingestionStatus, 'complete', '2025 is complete');
});


test('AE2026 paper generation and ordering', async (t) => {
  const archive = createArchive();
  const paper = archive.papers.find(p => p.year === 2026);
  assert.ok(paper, 'AE2026 paper exists');
  assert.equal(paper.totalQuestions, 65, 'Has 65 questions');
  assert.equal(paper.totalMarks, 100, 'Has 100 marks');
  
  // Verify ordering and question counts
  const gaSection = paper.sections.find(s => s.id === 'GA');
  const aeSection = paper.sections.find(s => s.id === 'AE');
  assert.equal(gaSection.questionIds.length, 10, '10 GA questions');
  assert.equal(aeSection.questionIds.length, 55, '55 AE questions');
  
  // Create a session
  const state = new ApplicationState(createMockStore());
  state.initializeContent(archive);
  
  const session = generatePaperSession(paper, state.progress, {mode: 'practice'});
  assert.equal(session.questionIds.length, 65, 'Session has 65 questions');
  
  // Verify no duplication and no omission
  const uniqueIds = new Set(session.questionIds);
  assert.equal(uniqueIds.size, 65, 'No duplicated questions');
  
  // Verify ordering matches original paper Order
  assert.deepEqual(session.questionIds, paper.questionOrder, 'Questions remain in original paper order');
  
  // Verify question numbering is preserved internally
  const firstQuestion = archive.byId.get(session.questionIds[0]);
  assert.equal(firstQuestion.number, 1, 'First question is Q1');
  const lastQuestion = archive.byId.get(session.questionIds[64]);
  assert.equal(lastQuestion.number, 65, 'Last question is Q65');
  
  // Verify Question Types are accurately loaded
  const mcqs = paper.questions.filter(q => q.type === 'MCQ');
  const msqs = paper.questions.filter(q => q.type === 'MSQ');
  const nats = paper.questions.filter(q => q.type === 'NAT');
  assert.equal(mcqs.length, 29, '29 MCQs');
  assert.equal(msqs.length, 14, '14 MSQs');
  assert.equal(nats.length, 22, '22 NATs');
});

test('Session integration, marks, and Results system compatibility', async (t) => {
  const archive = createArchive();
  const paper = archive.papers.find(p => p.year === 2026);
  const state = new ApplicationState(createMockStore());
  state.initializeContent(archive);
  
  const draft = generatePaperSession(paper, state.progress, {mode: 'test'});
  state.addDraft(draft);
  state.activateSession(draft.id);
  
  assert.equal(state.activeSession.mode, 'test', 'Test mode starts cleanly');
  assert.equal(state.activeSession.origin, 'paper', 'Origin tracks paper context');
  assert.equal(state.activeSession.configuration.year, 2026, 'Year tracked');
  
  // Submit abandoned to test results integration without breaking invariants
  const record = state.completeSession(state.activeSession, archive.byId);
  assert.ok(record.result, 'Result generated');
  assert.equal(record.result.maxMarks, 100, 'Max marks are 100');
});
import {quiz} from '../js/views.js';
import {CountdownTimer} from '../js/timer.js';

test('Exam UI rendering and controls', async (t) => {
  const archive = createArchive();
  const paper = archive.papers.find(p => p.year === 2026);
  const state = new ApplicationState(createMockStore());
  state.initializeContent(archive);
  
  const draft = generatePaperSession(paper, state.progress, {mode: 'test'});
  const timer = new CountdownTimer(draft, () => Date.now());
  const html = quiz(state.progress, archive, draft, timer);
  
  assert.match(html, /class="cbt-container"/, 'Exam mode UI is triggered');
  assert.match(html, /Time Left /, 'Timer is present');
  assert.match(html, /General Aptitude/, 'GA section button present');
  assert.match(html, /Aerospace/, 'AE section button present');
  
  draft.showSubmitConfirm = true;
  const htmlConfirm = quiz(state.progress, archive, draft, timer);
  assert.match(htmlConfirm, /Exam Summary/, 'Confirmation screen renders');
});
