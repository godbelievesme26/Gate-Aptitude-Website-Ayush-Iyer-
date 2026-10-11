# GATE PYQ Platform — Independent Verification & Audit Instructions

**Target Package**: `gate-pyq-stage-b-verification.zip`  
**Purpose**: Guide an independent auditor (ChatGPT, human QA engineer, or automated CI) through verifying the code, tests, datasets, and execution of the GATE PYQ Platform.

---

## 1. Prerequisites

- **Node.js**: Modern Node.js LTS (v18.0.0 or higher recommended). Check with `node -v`.
- **NPM**: Standard npm bundled with Node.js.
- **Operating System**: Cross-platform (Windows, Linux, macOS).

---

## 2. Quick-Start Verification (Terminal / CLI)

Extract the ZIP archive into any clean directory and navigate into it:

```bash
# 1. Unzip the package
unzip gate-pyq-stage-b-verification.zip -d gate-pyq-verification
cd gate-pyq-verification/gate-pyq-stage-b-verification

# 2. Install dependencies (strictly standard development fixtures e.g. jsdom)
npm install

# 3. Verify JavaScript Syntax across all source and test modules
npm run check
# Expected output: "PASS: JavaScript syntax" (0 errors, exit code 0)

# 4. Execute the complete Automated Test Suite
npm test
# Expected output: 217 tests passing, 0 failing (exit code 0)

# 5. Execute Question Database and Figure Validation
npm run validate
# Expected output: PASS across all 20 AE papers (2007–2026) and 16 GA sets (exit code 0)
```

---

## 3. Targeted Test Suites Breakdown

To run individual test suites added or hardened during Stage B:

```bash
# Offline Reliability & Service Worker Lifecycle (7 tests)
node --test tests/offline.test.js

# Dynamic 20-Year Archive Selection (4 tests)
node --test tests/dynamic-years.test.js

# Zero-CDN Mathematical Notation & AST Tokenizer (9 tests)
node --test tests/notation.test.js

# Full Exam Session Lifecycle, Timer Persistence & Storage Defense (8 tests)
node --test tests/exam-session.test.js

# Accessibility, ARIA Landmarks, Touch Targets & Responsive Viewports (8 tests)
node --test tests/accessibility.test.js

# Security, Read-Only Public API & Path Traversal Guards (12 tests)
node --test tests/verification.test.js
```

---

## 4. Interactive Browser Verification

To run and visually inspect the student application:

```bash
# Start the lightweight public student server
npm start
```
Open your browser to: `http://localhost:3000`

Key items to verify in the browser:
1. **Dynamic Year Filter**: Visit `#/bank` (Question Bank) and `#/practice` (Session Builder). Verify all 20 historical AE papers (2007 through 2026) appear in the dropdown.
2. **GATE CBT Exam Simulator**: Visit `#/aerospace` -> Select 2026 -> Take timed paper. Verify countdown timer, question palette colors, NAT keypad, MSQ checkboxes, review flags, and final Exam Summary table.
3. **Offline Resilience**: Open Chrome DevTools (`F12`) -> Network -> Toggle "Offline" -> Refresh (`F5`). Verify the app loads instantly from Service Worker cache.
4. **Zero-CDN Mathematical Typography**: View questions with square roots, fractions, Greek symbols, and vectors. Verify equations render cleanly without external CDN dependencies.
5. **Accessibility**: Tab through the interface; verify skip-link, focus-visible rings, and modal focus traps.

---

## 5. Audit Documentation References

- `STAGE_B_STABILIZATION_REPORT.md` — Complete engineering report with before/after bug analyses.
- `STABILIZATION_SPRINT_TRACKER.md` — Phase-by-phase task matrix with verification statuses.
- `CONTENT_QUALITY_AUDIT.md` — Statistical breakdown across all 1,475 questions and 425 figure assets.
- `MATH_NOTATION_INVENTORY.md` — Complete inventory of mathematical symbols and syntax.
- `REMAINING_ISSUES.md` — Prioritized operational register (P0, P1, P2, P3).
- `FILE_CHANGES_MANIFEST.json` — Manifest with SHA-256 hashes of all changed and added files.
- `STAGE_B_TEST_RUN.log` — Full test run log.
