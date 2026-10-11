import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {defaults} from '../js/storage.js';
import {quiz, result, renderExamMode} from '../js/views.js';
import {modal, toast, button, esc} from '../js/ui.js';

const read = path => fs.readFileSync(path, 'utf8');

// ---------------------------------------------------------------------------
// 1. Semantic Landmarks & Skip Link
// ---------------------------------------------------------------------------

test('Accessibility: index.html has skip link, language attribute and viewport meta', () => {
  const html = read('index.html');
  assert.match(html, /<html\s+lang="en">/i);
  assert.match(html, /<meta\s+name="viewport"\s+content="width=device-width,initial-scale=1">/i);
  assert.match(html, /<a\s+class="skip"\s+href="#main">Skip to content<\/a>/i);
  assert.match(html, /<div\s+id="app">/);
  assert.match(html, /<div\s+id="toast"\s+role="status"\s+aria-live="polite"><\/div>/);
  assert.match(html, /<dialog\s+id="dialog"><\/dialog>/);
});

test('Accessibility: application shell provides landmark regions and accessible navigation', () => {
  const appJs = read('js/app.js');
  // Navigation landmarks
  assert.match(appJs, /<aside class="sidebar">/);
  assert.match(appJs, /<header class="topbar">/);
  assert.match(appJs, /<nav class="nav-groups" aria-label="Primary navigation">/);
  assert.match(appJs, /<main id="main" tabindex="-1">/);
  // Current page indicator
  assert.match(appJs, /aria-current="page"/);
  // Connection status indicator
  assert.match(appJs, /<span id="connection">/);
});

// ---------------------------------------------------------------------------
// 2. Focus Management, Outlines & Touch Target Sizing
// ---------------------------------------------------------------------------

test('Accessibility: interactive controls define WCAG-compliant touch target sizes (min 44px)', () => {
  const systemCss = read('css/system.css');
  const quizCss = read('css/quiz.css');
  const styleCss = read('css/style.css');

  // Minimum height for buttons, inputs, selects, textareas
  assert.match(systemCss, /min-height:44px/);
  assert.match(quizCss, /min-height:66px/ || /min-height:60px/); // Option cards
  assert.match(quizCss, /min-height:48px/); // Submit / continue primary button

  // Focus visible rings
  assert.match(systemCss, /:focus-visible\{outline:var\(--focus-ring\);outline-offset:var\(--focus-offset\)\}/);
  assert.match(styleCss, /:focus-visible\{outline:3px solid var\(--primary\);outline-offset:3px\}/);
  assert.match(quizCss, /\.answer-panel \.option:focus-visible\{outline:var\(--focus-ring\);outline-offset:4px\}/);
});

// ---------------------------------------------------------------------------
// 3. Modals & Dialog Accessibility
// ---------------------------------------------------------------------------

test('Accessibility: modal dialogs utilize native HTML5 dialog with ARIA attributes and focus restoration', () => {
  const uiJs = read('js/ui.js');
  assert.match(uiJs, /d\.setAttribute\('aria-labelledby','dialog-title'\)/);
  assert.match(uiJs, /confirm\.setAttribute\('aria-busy','true'\)/);
  assert.match(uiJs, /d\.onclose=\(\)=>before\?\.focus\(\)/);
  assert.match(uiJs, /d\.showModal\(\)/);
  assert.match(uiJs, /d\.close\(\)/);
});

// ---------------------------------------------------------------------------
// 4. Color Contrast & Semantic Color Tokens
// ---------------------------------------------------------------------------

test('Accessibility: theme system defines high contrast palette tokens for light and dark modes', () => {
  const css = read('css/system.css');

  // Verify core color tokens in light mode
  assert.match(css, /--color-canvas:#f4f5f7/);
  assert.match(css, /--color-text:#202636/);
  assert.match(css, /--color-accent:#4148aa/);
  assert.match(css, /--color-focus:#5961d7/);

  // Verify dark theme overrides
  assert.match(css, /\[data-theme=dark\]\{--color-canvas:#15171c/);
  assert.match(css, /--color-text:#edf0f5/);
  assert.match(css, /--color-accent:#afb3ff/);
  assert.match(css, /--color-focus:#c4c7ff/);

  // Helper to compute luminance & contrast ratio
  function hexToRgb(hex) {
    const bigint = parseInt(hex.slice(1), 16);
    return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255];
  }
  function relativeLuminance([r, g, b]) {
    const sRGB = [r, g, b].map(v => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * sRGB[0] + 0.7152 * sRGB[1] + 0.0722 * sRGB[2];
  }
  function contrastRatio(hex1, hex2) {
    const l1 = relativeLuminance(hexToRgb(hex1));
    const l2 = relativeLuminance(hexToRgb(hex2));
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  // Light theme: text (#202636) on canvas (#f4f5f7)
  const lightContrast = contrastRatio('#202636', '#f4f5f7');
  assert.ok(lightContrast >= 7.0, `Light theme contrast ${lightContrast.toFixed(2)} must exceed WCAG AAA 7:1`);

  // Dark theme: text (#edf0f5) on canvas (#15171c)
  const darkContrast = contrastRatio('#edf0f5', '#15171c');
  assert.ok(darkContrast >= 7.0, `Dark theme contrast ${darkContrast.toFixed(2)} must exceed WCAG AAA 7:1`);

  // Accent on light: #4148aa on #ffffff
  const accentContrast = contrastRatio('#4148aa', '#ffffff');
  assert.ok(accentContrast >= 4.5, `Accent contrast ${accentContrast.toFixed(2)} must exceed WCAG AA 4.5:1`);
});

// ---------------------------------------------------------------------------
// 5. Responsive Layout Breakpoints
// ---------------------------------------------------------------------------

test('Responsive Layout: defines media queries covering mobile, tablet, and desktop viewports', () => {
  const styleCss = read('css/style.css');
  const quizCss = read('css/quiz.css');
  const systemCss = read('css/system.css');

  // Mobile viewport rules (<=680px and ultra-compact <=380px)
  assert.match(styleCss, /@media\(max-width:680px\)/);
  assert.match(quizCss, /@media\(max-width:380px\)/);
  assert.match(systemCss, /@media\(max-width:680px\)/);

  // Tablet viewport rules (<=900px)
  assert.match(styleCss, /@media\(max-width:900px\)/);

  // Desktop standard (<=1150px)
  assert.match(styleCss, /@media\(max-width:1150px\)/);
  assert.match(quizCss, /@media\(max-width:1200px\)/);

  // Desktop large (>=1600px)
  assert.match(styleCss, /@media\(min-width:1600px\)/);

  // Mobile menu button toggles sidebar
  assert.match(styleCss, /\.mobile-menu\{display:none\}/);
  assert.match(styleCss, /@media\(max-width:680px\)\{\.sidebar\{display:none/);
  assert.match(styleCss, /\.sidebar\.open\{display:flex/);
  assert.match(styleCss, /\.mobile-menu\{display:inline-flex\}/);
});

// ---------------------------------------------------------------------------
// 6. Motion Sensitivity (prefers-reduced-motion)
// ---------------------------------------------------------------------------

test('Motion: respects prefers-reduced-motion in both CSS and JavaScript', () => {
  const styleCss = read('css/style.css');
  const quizCss = read('css/quiz.css');
  const appJs = read('js/app.js');

  // CSS eliminates animation and transition
  assert.match(styleCss, /@media\(prefers-reduced-motion:reduce\)\{\*\{scroll-behavior:auto!important;animation:none!important;transition:none!important\}\}/);
  assert.match(quizCss, /@media\(prefers-reduced-motion:reduce\)\{\.question-surface\.question-enter\{animation:none\}/);

  // JS checks matchMedia before triggering animations
  assert.match(appJs, /if\(matchMedia\('\(prefers-reduced-motion: reduce\)'\)\.matches\)return;/);
});

// ---------------------------------------------------------------------------
// 7. Exam Session ARIA Attributes (Option Buttons & Progress Palettes)
// ---------------------------------------------------------------------------

test('Accessibility: exam session views include full ARIA attributes on options and question palettes', () => {
  const sampleQuestion = {
    id: 'gate-2026-ae-01',
    number: 1,
    type: 'MCQ',
    marks: 1,
    negativeMarks: 1 / 3,
    answer: 'A',
    options: [{label: 'A', text: 'Option A text'}, {label: 'B', text: 'Option B text'}],
    year: 2026,
    paper: 'AE',
    question: 'Sample stem',
    transcriptionStatus: 'source-verified',
    hasFigure: false,
    figures: []
  };
  const archive = {
    questions: [sampleQuestion],
    byId: new Map([[sampleQuestion.id, sampleQuestion]])
  };
  const session = {
    id: 'test-session',
    currentPosition: 0,
    index: 0,
    mode: 'test',
    origin: 'custom',
    questionIds: [sampleQuestion.id],
    answers: {'gate-2026-ae-01': 'A'},
    review: {'gate-2026-ae-01': true},
    visited: {'gate-2026-ae-01': true},
    times: {},
    elapsed: 1000
  };
  const mockTimer = {
    remaining: () => 1800000,
    visit: 1000,
    checkpoint: () => false,
    checkpointVisible: () => false
  };

  const html = quiz(defaults(), archive, session, mockTimer);

  // aria-pressed on selected option button
  assert.match(html, /aria-pressed="true"/);
  // Screen-reader-only label prefix
  assert.match(html, /<span class="sr-only">Option <\/span>A/);
  // Palette button aria-label with state (answered and review)
  assert.match(html, /aria-label="Question 1, answered, marked for review"/);
  // Progress bar label
  assert.match(html, /aria-label="Question position"/);
});
