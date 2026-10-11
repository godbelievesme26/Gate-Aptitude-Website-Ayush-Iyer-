import test from 'node:test';
import assert from 'node:assert/strict';
import { bank, practice, analytics } from '../js/views.js';
import { home } from '../js/home.js';
import { defaults } from '../js/storage.js';

function makeMockArchive(years = [2007, 2015, 2020, 2026]) {
  const questions = years.flatMap((y, yIdx) => [
    {
      id: `q-${y}-1`,
      year: y,
      paper: 'AE',
      number: 1,
      type: 'MCQ',
      marks: 1,
      options: [{ label: 'A' }, { label: 'B' }],
      answer: 'A',
      search: `question for ${y}`
    },
    {
      id: `q-${y}-2`,
      year: y,
      paper: 'AE',
      number: 2,
      type: 'NAT',
      marks: 2,
      options: [],
      answer: 10,
      search: `second question for ${y}`
    }
  ]);

  return {
    questions,
    papers: years.map(y => ({ year: y, id: `ae-${y}`, questionOrder: [`q-${y}-1`, `q-${y}-2`] })),
    sets: [],
    byId: new Map(questions.map(q => [q.id, q]))
  };
}

test('Dynamic Years 1: bank() dropdown populates all archive years dynamically', () => {
  const s = defaults();
  const archive = makeMockArchive([2007, 2011, 2018, 2026]);
  const html = bank(s, archive, new URLSearchParams());

  for (const year of [2007, 2011, 2018, 2026]) {
    assert.match(html, new RegExp(`<option value="${year}"`), `bank() must include option for year ${year}`);
  }
  // Years not in archive must not appear as options
  assert.doesNotMatch(html, /<option value="1999"/);
});

test('Dynamic Years 2: practice() blueprint form populates all archive years dynamically', () => {
  const s = defaults();
  const archive = makeMockArchive([2008, 2014, 2022, 2025]);
  const html = practice(s, archive);

  for (const year of [2008, 2014, 2022, 2025]) {
    assert.match(html, new RegExp(`<option value="${year}">`), `practice() must include option for year ${year}`);
  }
});

test('Dynamic Years 3: analytics() renders Coverage by year for every historical archive year', () => {
  const s = defaults();
  const testYears = [2007, 2008, 2015, 2021, 2024, 2026];
  const archive = makeMockArchive(testYears);
  const html = analytics(s, archive);

  for (const year of testYears) {
    assert.match(html, new RegExp(`<span>${year}</span><strong>0 / 2</strong>`), `analytics() must show coverage row for year ${year}`);
  }
});

test('Dynamic Years 4: home() displays dynamic year span reflecting archive contents', () => {
  const s = defaults();
  const archive = makeMockArchive([2007, 2015, 2026]);
  const html = home(s, archive);

  assert.match(html, /2007–2026/, 'home() must display 2007–2026 year span');
});
