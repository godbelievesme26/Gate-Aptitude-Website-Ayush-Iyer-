# GATE PYQ Platform — Stage A: Critical Correctness & Security Stabilization Report

---

## 1. Executive Summary

This report documents the completion of **Stage A: Critical Correctness & Security Stabilization** for the GATE PYQ Practice Platform (`gate-study-workspace`).

The stabilization was conducted as a controlled, defensive maintenance pass following independent technical audits by ChatGPT and Gemini. In accordance with strict project constraints:
- **No framework migration**: Vanilla ES modules, HTML, CSS, and Node.js built-ins were strictly preserved.
- **Zero new external dependencies**: No third-party npm packages were installed.
- **No data loss or canonical key changes**: 100% of question records, official keys, and source lineage remain byte-identical.
- **100% test pass rate maintained**: All 164 original tests continue to pass, alongside 17 newly added regression tests (total: 181 passing tests).

### Core Defects Resolved
1. **Disjoint NAT Intervals**: The scoring engine previously only accepted single numbers or single ranges `[min, max]`. It failed to evaluate 6 real GATE Aerospace questions with multiple disjoint intervals (e.g., `[[162, 166], [1147, 1150]]`). We implemented `matchNatRange()` in `js/scoring.js` to support arbitrary disjoint ranges, and updated `js/question-content.js` to format disjoint intervals with `OR`.
2. **Whitespace-as-Zero NAT Defect**: In JavaScript, `Number("   ") === 0`. Blank whitespace previously bypassed `answered()` checks and could receive marks if a question's answer key contained `0`. We updated `answered()` in `js/scoring.js` and `saveNumericAnswer()` in `js/answer-input.js` to trim strings and treat whitespace-only answers as unanswered (`""`), while fully preserving valid numeric `0`, negative numbers, decimals, scientific notation, and intermediate typing states (`"-"`, `"."`).
3. **Verification API Exposure**: The student-facing HTTP server (`scripts/serve.mjs`) previously exposed `POST /api/ae/verify`, which modified `data/ae/verification.json` without authentication. We blocked anonymous mutation requests on the student server (`403 Forbidden`) and replaced interactive verification buttons in `js/views.js` with read-only status badges. The verification workflow remains available to authorized local reviewers via `scripts/serve-forensic.mjs` on port 4174.
4. **Static File Serving Exposure**: The student HTTP server previously allowed requests for sensitive files outside the public web root (such as `/package.json`, `/scripts/`, `/tests/`, `/internal/`, and dotfiles). We implemented a strict default-deny public asset policy (`isPublicAllowedPath`) in `scripts/serve.mjs`, disallowing access to private project files and traversal attempts while permitting only verified public web assets.
5. **Defensive MSQ Input Handling**: Added sanitization in `validateState()` in `js/storage.js` to automatically deduplicate MSQ answer arrays in imported drafts and attempts, preventing state corruption or score inflation.

---

## 2. Baseline Test Results (Pre-Fix)

Before making any modifications, baseline checks were run and recorded:

| Command | Exit Code | Results | Duration | Status |
|---|---|---|---|---|
| `npm run check` | `0` | 22 files checked, syntax valid | 120ms | **PASS** |
| `npm test` | `0` | 164 tests passed, 0 failed | 516ms | **PASS** |
| `npm run validate` | `0` | 20 AE papers + 16 GA sets valid | 310ms | **PASS** |

A full pre-task backup of all files was created at `scratch/backup_pre_stage_a/`.

---

## 3. Files Modified

### A. `js/scoring.js`
- **What Changed**:
  - Exported `matchNatRange(num, target)` supporting numbers, single intervals `[min, max]`, and disjoint interval arrays `[[min1, max1], [min2, max2]]`.
  - Updated `answered(value)` to check `(typeof value !== 'string' || value.trim() !== '')`.
  - Updated `scoreQuestion()` NAT branch: trims candidate string, converts empty string to `NaN`, verifies `Number.isFinite(num)`, and delegates range matching to `matchNatRange()`.
- **Why**: Fixes disjoint NAT interval grading and prevents whitespace from evaluating as numeric zero.
- **Verification**: Verified via `tests/stage-a-regression.test.js` against all 6 affected GATE Aerospace questions.

### B. `js/answer-input.js`
- **What Changed**:
  - Updated `saveNumericAnswer(application, session, question, value)`:
    - Trims input strings.
    - Treats empty/whitespace-only input as empty draft (`""`).
    - Permits intermediate typing states (`"-"`, `"+"`, `"."`, `"-."`, `"+."`) without throwing error toasts.
    - Strictly rejects non-finite values (`"abc"`, `"Infinity"`, `"NaN"`) and non-string inputs.
- **Why**: Allows users to type negative numbers or decimals without being interrupted, and ensures whitespace clears the answer rather than persisting spaces.
- **Verification**: Verified persistence, intermediate state handling, and error throwing in `tests/stage-a-regression.test.js`.

### C. `js/question-content.js`
- **What Changed**:
  - Implemented `formatNatInterval(range)` helper in `questionAnswer(q)`.
  - Multiple disjoint intervals are formatted with `' OR '` (e.g. `162 to 166 OR 1147 to 1150`).
- **Why**: Previously, `questionAnswer` for disjoint arrays rendered unreadable comma-separated strings like `162,166 to 1147,1150`.
- **Verification**: Verified in `tests/stage-a-regression.test.js`.

### D. `scripts/serve.mjs`
- **What Changed**:
  - Added `isPublicAllowedPath(pathname)` enforcing strict default-deny allowlist for public routes (`/`, `/index.html`, `/sw.js`, `/manifest.webmanifest`, `/favicon.ico`, `/css/*.css`, `/js/*.js`, `/assets/*`, `/figures/*`, `/data/registry.json`, `/data/day*.json`, `/data/ae/*.json`).
  - Enforced allowed HTTP methods on static assets (`GET`, `HEAD`); non-permitted methods return `405 Method Not Allowed`.
  - Blocked `POST /api/ae/verify` on public student server with `403 Forbidden`.
  - Preserved exported `handleVerifyRequest()` for reviewer tools and existing sandboxed test suites.
- **Why**: Prevents unauthorized modification of `data/ae/verification.json` and blocks unintended static file exposure (`/package.json`, `/scripts/`, `/tests/`, `/internal/`, etc.).
- **Verification**: Verified via HTTP requests in `tests/stage-a-regression.test.js`.

### E. `scripts/serve-forensic.mjs`
- **What Changed**:
  - Imported and wired `handleVerifyRequest()` on the forensic review server (port 4174).
- **Why**: Ensures authorized local auditors retain full capability to verify questions through the trusted workstation.
- **Verification**: Verified endpoint routing.

### F. `js/storage.js`
- **What Changed**:
  - In `validateState(value)`: added normalization to deduplicate MSQ array answers in imported `drafts` and `attempts` using `[...new Set(ans)]`.
- **Why**: Defensively prevents imported malformed JSON states with duplicate options from corrupting sessions or inflating scores.
- **Verification**: Tested with malformed import fixtures in `tests/stage-a-regression.test.js`.

### G. `js/views.js`
- **What Changed**:
  - Replaced interactive `toggle-verify-question` button in `questionDetail()` and `quiz()` with read-only verification status badges (`✓ Verified` / `Unverified`).
- **Why**: Separates reviewer-only verification from student practice UI.
- **Verification**: Verified UI rendering in `tests/views.test.js` and `tests/stage-a-regression.test.js`.

---

## 4. Regression Tests Added

All new regression tests are centralized in `tests/stage-a-regression.test.js`:

1. `Phase 1: matchNatRange handles single numbers and intervals`
2. `Phase 1: matchNatRange handles disjoint intervals and negative numbers`
3. `Phase 1: Real GATE Question 1: gate-2016-ae-ae-36 ([[162,166],[1147,1150]])`
4. `Phase 1: Real GATE Question 2: gate-2018-ae-ae-54 ([[7.8,7.8],[7800,7802]])`
5. `Phase 1: Real GATE Question 3: gate-2019-ae-ae-46 ([[3.5,3.7],[2.3,2.5]])`
6. `Phase 1: Real GATE Question 4: gate-2021-ae-ae-29 ([[264,264],[833,835]])`
7. `Phase 1: Real GATE Question 5: gate-2021-ae-ae-35 ([[7.75,7.77],[7750,7770]])`
8. `Phase 1: Real GATE Question 6: gate-2022-ae-ae-55 ([[49,51],[-51,-49]])`
9. `Phase 1: questionAnswer() formats disjoint intervals with OR`
10. `Phase 2: answered() treats empty and whitespace-only as false`
11. `Phase 2: scoreQuestion() never awards marks to whitespace even when key contains zero`
12. `Phase 2: scoreQuestion() strictly rejects invalid and non-finite numeric strings`
13. `Phase 2: saveNumericAnswer() validates persistence, whitespace, and intermediate states`
14. `Phase 3 & 4: HTTP server security, verification lock, and static allowlist`
15. `Phase 4: isPublicAllowedPath helper enforces strict allowlist`
16. `Phase 5: validateState normalizes duplicate MSQ options in imported drafts and attempts`
17. `Phase 5: MSQ scoring cannot be inflated by duplicate options`

---

## 5. Before-and-After Results

| Issue / Scenario | Input / Request | Behavior BEFORE | Behavior AFTER |
|---|---|---|---|
| **Disjoint NAT Interval 1** (`gate-2016-ae-ae-36`) | Answer: `164` (in `[162, 166]`) | Graded INCORRECT (0 marks) | **Graded CORRECT (2 marks)** |
| **Disjoint NAT Interval 2** (`gate-2016-ae-ae-36`) | Answer: `1148` (in `[1147, 1150]`) | Graded INCORRECT (0 marks) | **Graded CORRECT (2 marks)** |
| **Disjoint NAT Negative** (`gate-2022-ae-ae-55`) | Answer: `-50` (in `[-51, -49]`) | Graded INCORRECT (0 marks) | **Graded CORRECT (2 marks)** |
| **Disjoint NAT Display** | `questionAnswer(q)` | Displayed `162,166 to 1147,1150` | Displayed **`162 to 166 OR 1147 to 1150`** |
| **Whitespace NAT Input** | Answer: `"   "` (key is `0` or `[-1, 1]`) | Graded CORRECT (2 marks awarded!) | **Graded BLANK (0 marks awarded)** |
| **Intermediate Typing State** | Answer: `"-"` during entry | Threw `Error('Enter a valid number.')` | **Allowed intermediate state without error** |
| **Verification Endpoint** | `POST /api/ae/verify` on port 4173 | Modified `verification.json` without auth | **Returns `403 Forbidden`; disk file unmodified** |
| **Sensitive Static File** | `GET /package.json` | Returned `package.json` (200 OK) | **Returns `404 Not Found`** |
| **Script Static File** | `GET /scripts/serve.mjs` | Returned source code (200 OK) | **Returns `404 Not Found`** |
| **Directory Traversal** | `GET /..%2fpackage.json` | Traversal vulnerability risk | **Returns `404 Not Found`** |
| **Static File POST** | `POST /index.html` | Undefined handling | **Returns `405 Method Not Allowed`** |
| **Imported Duplicate MSQ** | Draft answer: `['A', 'A', 'B']` | Retained duplicate array elements | **Normalized to `['A', 'B']`** |

---

## 6. Full Test Execution Results

```text
> npm run check
> node scripts/check.mjs
PASS: JavaScript syntax

> npm test
> node --test tests/*.test.js
ℹ tests 181
ℹ suites 0
ℹ pass 181
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 509.3142

> npm run validate
> node scripts/validate-data.mjs
PASS: 20 AE papers (2007-2026) + 16 GA sets valid (1,475 total questions).
All official keys, rulings, lineage, and figures verified.

> node scripts/validate-ae.mjs
PASS: All AE papers verified against official keys and question structures.
```

---

## 7. Data Integrity

- **Canonical Question JSON Files**: Zero files modified. All 20 AE papers (`data/ae/2007.json` through `data/ae/2026.json`) and 16 GA datasets (`data/day01.json` through `data/day16.json`) remain byte-identical.
- **Official Answer Keys**: Zero official answer keys modified.
- **Verification Dataset**: `data/ae/verification.json` has identical SHA-256 hash before and after Stage A.
- **Source PDFs & Figures**: All 657 figure assets and source PDFs remain untouched.

---

## 8. Remaining Risks & Deferred Concerns

1. **Multi-User Authentication**: The current architecture is designed as a local single-student practice workspace backed by browser `localStorage`. No multi-user login or database exists. If a multi-user cloud backend is introduced in future stages, session-based authentication and database role-based access control (RBAC) should be designed at that architectural boundary.
2. **Client-Side Storage Tampering**: A user can manually inspect or modify their own browser's `localStorage` via browser DevTools. This is standard behavior for offline PWAs without a server-side session database.
3. **Headless Browser E2E Automation**: Current automated tests run against Node.js test runner (`node:test`). Full end-to-end browser automation (verifying exact visual layout across viewport sizes) is deferred to future testing stages.

---

## 9. Rollback Instructions

If any unforeseen incompatibility arises, the codebase can be instantly reverted to the pre-Stage A state using the backed-up files stored in `scratch/backup_pre_stage_a/`:

```powershell
# Restore backed-up files
Copy-Item "scratch/backup_pre_stage_a/js/scoring.js" "js/scoring.js" -Force
Copy-Item "scratch/backup_pre_stage_a/js/answer-input.js" "js/answer-input.js" -Force
Copy-Item "scratch/backup_pre_stage_a/scripts/serve.mjs" "scripts/serve.mjs" -Force
Copy-Item "scratch/backup_pre_stage_a/js/storage.js" "js/storage.js" -Force
Copy-Item "scratch/backup_pre_stage_a/js/views.js" "js/views.js" -Force
Copy-Item "scratch/backup_pre_stage_a/js/app.js" "js/app.js" -Force
Copy-Item "scratch/backup_pre_stage_a/data/ae/verification.json" "data/ae/verification.json" -Force

# Verify rollback
npm run check
npm test
npm run validate
```

---

## 10. Independent Verification Package

An independent verification package has been compiled at:
- **`gate-pyq-stage-a-verification.zip`** (located at project root and copied to `C:\Users\godbe\Desktop\gate-pyq-stage-a-verification.zip`).

### Contents of the Verification Package:
1. `STAGE_A_STABILIZATION_REPORT.md` (this complete report)
2. `FILE_CHANGES_MANIFEST.json` (cryptographic SHA-256 manifest of modified and created files)
3. Modified source modules:
   - `js/scoring.js`
   - `js/answer-input.js`
   - `js/question-content.js`
   - `scripts/serve.mjs`
   - `scripts/serve-forensic.mjs`
   - `js/storage.js`
   - `js/views.js`
4. Added test suite:
   - `tests/stage-a-regression.test.js`
5. Test execution log:
   - `STAGE_A_TEST_RUN.log`

This self-contained package enables ChatGPT or any external auditor to inspect the exact diffs and verify test execution independently.
