import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = process.cwd();

const fileEntries = [
  { path: '.github/workflows/ci.yml', status: 'CREATED', phase: 'Phase 8', description: 'GitHub Actions CI matrix workflow testing Node 18, 20, and 22 across check, test, and validate.' },
  { path: 'CONTENT_QUALITY_AUDIT.md', status: 'CREATED', phase: 'Phase 7', description: 'Comprehensive content quality audit of 1,475 questions across 20 AE papers and 16 GA sets.' },
  { path: 'MANUAL_REVIEW_CHECKLIST.md', status: 'CREATED', phase: 'Phase 9', description: 'Systematic manual QA review checklist spanning 6 domains and 24 concrete audit items.' },
  { path: 'MATH_NOTATION_INVENTORY.md', status: 'CREATED', phase: 'Phase 4', description: 'Inventory of mathematical notations, symbols, Greek characters, and zero-CDN rendering.' },
  { path: 'REMAINING_ISSUES.md', status: 'CREATED', phase: 'Phase 9', description: 'Prioritized issue log categorized into P0 (0), P1 (2), P2 (4), and P3 (3) with risk analysis.' },
  { path: 'STABILIZATION_SPRINT_TRACKER.md', status: 'CREATED', phase: 'Phases 1-10', description: 'Living progress tracker recording implementation status and verification across all 10 phases.' },
  { path: 'STAGE_B_STABILIZATION_REPORT.md', status: 'CREATED', phase: 'Phase 9', description: 'Comprehensive 15-section technical report detailing architectural, security, and quality upgrades.' },
  { path: 'INDEPENDENT_VERIFICATION_INSTRUCTIONS.md', status: 'CREATED', phase: 'Phase 10', description: 'Step-by-step external auditor guide for independent verification and test execution.' },
  { path: 'STAGE_B_TEST_RUN.log', status: 'CREATED', phase: 'Phase 10', description: 'Complete automated test execution log validating all 217 tests across 10 test suites.' },
  { path: 'css/quiz.css', status: 'MODIFIED', phase: 'Phases 4, 6', description: 'Added math notation styling (roots, vectors, matrices) and WCAG AAA focus-visible indicators.' },
  { path: 'index.html', status: 'MODIFIED', phase: 'Phase 2', description: 'Removed conflicting inline Service Worker unregistration script to restore PWA offline reliability.' },
  { path: 'js/home.js', status: 'MODIFIED', phase: 'Phase 3', description: 'Updated dynamic year range display and paper count calculation on the landing page.' },
  { path: 'js/question-content.js', status: 'MODIFIED', phase: 'Phase 4', description: 'Implemented robust tokenizer for zero-CDN math notation rendering.' },
  { path: 'js/views.js', status: 'MODIFIED', phase: 'Phase 3', description: 'Replaced hardcoded [2026, 2025] year filter with dynamic extraction across all 20 historical AE years.' },
  { path: 'scripts/package-stage-b.mjs', status: 'CREATED', phase: 'Phase 10', description: 'Packaging script creating self-contained, offline-runnable verification archive.' },
  { path: 'scripts/generate-manifest.mjs', status: 'CREATED', phase: 'Phase 10', description: 'Manifest generation script calculating cryptographic hashes and file metrics.' },
  { path: 'scripts/serve-forensic.mjs', status: 'MODIFIED', phase: 'Phase 1', description: 'Isolated internal forensic review workstation server handling audit trail mutations.' },
  { path: 'scripts/serve.mjs', status: 'MODIFIED', phase: 'Phase 1', description: 'Secured public server with strict path traversal validation and read-only verification endpoints.' },
  { path: 'sw.js', status: 'MODIFIED', phase: 'Phase 2', description: 'Precached verification metadata and strengthened cache-first offline asset delivery.' },
  { path: 'tests/accessibility.test.js', status: 'CREATED', phase: 'Phase 6', description: 'Automated test suite verifying WCAG AAA color contrast, touch target dimensions, and ARIA landmarks.' },
  { path: 'tests/dynamic-years.test.js', status: 'CREATED', phase: 'Phase 3', description: 'Automated test suite validating dynamic year extraction and rendering.' },
  { path: 'tests/exam-session.test.js', status: 'CREATED', phase: 'Phase 5', description: 'Automated test suite verifying exam session state lifecycle and timer persistence.' },
  { path: 'tests/notation.test.js', status: 'CREATED', phase: 'Phase 4', description: 'Automated test suite verifying zero-CDN math tokenization and typography.' },
  { path: 'tests/offline.test.js', status: 'CREATED', phase: 'Phase 2', description: 'Automated test suite verifying Service Worker precache manifest and offline routing.' },
  { path: 'tests/stage-a-regression.test.js', status: 'MODIFIED', phase: 'Phase 1', description: 'Updated regression tests for hardened path traversal validation and isolated API endpoints.' },
  { path: 'tests/verification.test.js', status: 'MODIFIED', phase: 'Phase 1', description: 'Updated verification test assertions for read-only public API enforcement.' }
];

const manifestFiles = fileEntries.map(entry => {
  const fullPath = path.join(ROOT, entry.path);
  let sizeBytes = 0;
  let sha256 = 'FILE_NOT_FOUND';
  if (fs.existsSync(fullPath)) {
    const buf = fs.readFileSync(fullPath);
    sizeBytes = buf.length;
    sha256 = crypto.createHash('sha256').update(buf).digest('hex');
  }
  return {
    path: entry.path,
    status: entry.status,
    phase: entry.phase,
    sizeBytes,
    sha256,
    description: entry.description
  };
});

const manifest = {
  manifestVersion: '1.0.0',
  sprint: 'Stage B Autonomous Stabilization Sprint',
  generatedAt: new Date().toISOString(),
  gitBranch: 'stabilization/stage-b-sprint',
  totalFiles: manifestFiles.length,
  files: manifestFiles
};

const outputPath = path.join(ROOT, 'FILE_CHANGES_MANIFEST.json');
fs.writeFileSync(outputPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
console.log(`Successfully generated FILE_CHANGES_MANIFEST.json with ${manifestFiles.length} file records.`);
