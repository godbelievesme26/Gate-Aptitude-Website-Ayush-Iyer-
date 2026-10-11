# GATE PYQ Platform — Autonomous Stabilization Sprint Tracker (Stage B)

Branch: `stabilization/stage-b-sprint`  
Baseline: Stage A Complete (181/181 passing tests, all 20 AE papers + 16 GA sets valid)

---

## Sprint Overview & Progress Matrix

| Task ID | Phase & Description | Priority | Status | Verification Summary |
|---|---|---|---|---|
| **1.1** | Remove dead verification mutation code from public server | High | COMPLETED | Dead mutation code removed from `scripts/serve.mjs`; write verification isolated to `scripts/serve-forensic.mjs`; tests verified |
| **1.2** | Review verification data visibility (read-only minimal schema) | Medium | COMPLETED | `readVerification()` returns strictly sanitized `{ status, verifiedAt }` schema; zero private audit data exposed |
| **1.3** | Strengthen public asset isolation in `isPublicAllowedPath()` | High | COMPLETED | Enforced traversal/backslash/control char/double-slash/dotfile guards; query string & hash safe parsing; regression tests expanded |
| **2.1** | Resolve Service Worker registration conflict (`index.html` vs `app.js`) | High | COMPLETED | Removed unregister script from `index.html`; `app.js` registers `sw.js` cleanly |
| **2.2** | Audit caching behavior & versioning strategy | Medium | COMPLETED | Verified CacheStorage cache name isolation (`gate-workspace-v31`); student progress in `localStorage` never cleared; added `data/ae/verification.json` to precached resources |
| **2.3** | Offline reliability verification & automated scenarios | Medium | COMPLETED | Created `tests/offline.test.js` (7 tests) verifying shell files, manifests, datasets, cache versioning, and offline fallback |
| **3.1** | Dynamic practice year selector for all 20 AE years in `views.js` | High | COMPLETED | Dynamically extracts all archive years (`a.questions`) in `bank()` and `practice()`; eliminates hardcoded `[2026, 2025]` |
| **3.2** | Dynamic analytics year selection across historical papers | Medium | COMPLETED | Dynamically computes `Coverage by year` across all historical papers; updated home screen footer year span |
| **3.3** | Regression tests for dynamic year selection | High | COMPLETED | Added `tests/dynamic-years.test.js` (4 tests) covering dynamic dropdowns, blueprint builder, historical coverage, and home span |
| **4.1** | Mathematical syntax audit across datasets (`MATH_NOTATION_INVENTORY.md`) | High | NOT STARTED | Pending |
| **4.2** | Mathematical rendering upgrade & hardening (zero CDN risk) | High | NOT STARTED | Pending |
| **4.3** | Mathematical rendering tests across real exam expressions | High | NOT STARTED | Pending |
| **5.1** | Full exam session lifecycle audit (start to finish trace) | High | NOT STARTED | Pending |
| **5.2** | Timer integrity & refresh persistence testing | High | NOT STARTED | Pending |
| **5.3** | State persistence, corruption protection & quota defense | High | NOT STARTED | Pending |
| **5.4** | Automated test session journey simulation | Medium | NOT STARTED | Pending |
| **6.1** | Accessibility audit (keyboard, ARIA, focus, contrast) | Medium | NOT STARTED | Pending |
| **6.2** | Responsive layout validation across 4 viewports | Medium | NOT STARTED | Pending |
| **6.3** | User feedback states & network handling | Low | NOT STARTED | Pending |
| **7.1** | Content completeness audit (`CONTENT_QUALITY_AUDIT.md`) | Medium | NOT STARTED | Pending |
| **7.2** | Source verification coverage audit | Low | NOT STARTED | Pending |
| **7.3** | Future branch expansion architectural recommendations | Low | NOT STARTED | Pending |
| **8.1** | Test coverage expansion for discovered edge cases | High | NOT STARTED | Pending |
| **8.2** | Continuous Integration minimal workflow configuration | Low | NOT STARTED | Pending |
| **8.3** | Final regression check (full check, test, validate) | High | NOT STARTED | Pending |
| **9.0** | Final reports (`STAGE_B_STABILIZATION_REPORT.md`, registers) | High | NOT STARTED | Pending |
| **10.0** | Independent verification package (`gate-pyq-stage-b-verification.zip`) | High | NOT STARTED | Pending |

---

## Detailed Task Entries

### Phase 1: Security Cleanup
- **Task 1.1**: Dead write verification logic removed from public student server (`scripts/serve.mjs`). Workstation mutation logic safely isolated to `scripts/serve-forensic.mjs`. Tests in `tests/verification.test.js` updated to import workstation handler in test sandbox.
- **Task 1.2**: Inspected `data/ae/verification.json`. Sanitized public read schema in `scripts/serve.mjs` ensuring only `{ status, verifiedAt }` properties can be serialized to students; no reviewer identities or private audit trails leaked.
- **Task 1.3**: Strengthened `isPublicAllowedPath()` against URL encoded attacks, control characters (`\0` to `\x1f`, `\x7f`), path traversal (`..`, `\\`, `//`), dotfiles (`.hidden.png`), and validated query parameter / hash parsing. Expanded regression tests in `tests/stage-a-regression.test.js`.
- **Phase 1 Verification**: 181/181 automated tests passing, syntax check pass, all 20 AE datasets and 16 GA datasets valid.

### Phase 2: Service Worker & Offline Reliability
- **Task 2.1**: Eliminated contradictory `<script>` in `index.html` that called `registration.unregister()` on every reload. `js/app.js` handles Service Worker registration predictably via `registerOffline()`.
- **Task 2.2**: Verified precache shell list against physical files on disk; added `data/ae/verification.json` to install precache; confirmed cache key eviction isolates strictly to `gate-workspace-*` without modifying or purging user `localStorage`.
- **Task 2.3**: Added `tests/offline.test.js` containing 7 automated tests covering shell assets existence, stylesheet alignment, dataset precaching readiness, cache versioning isolation, and network failure fallback.
- **Phase 2 Verification**: 188/188 automated tests passing (7 new offline tests), syntax check pass, all 20 AE and 16 GA datasets valid.

### Phase 3: Dynamic Year Selection
- **Task 3.1**: Replaced hardcoded `[2026, 2025]` in `js/views.js` (`bank()` and `practice()`) with dynamic extraction from `a.questions.map(q => q.year)` sorted descending. All 20 AE years (2007–2026) are selectable.
- **Task 3.2**: Replaced static year loop in `analytics()` with dynamic historical coverage across all 20 years. Updated `js/home.js` footer to compute exact archive year span dynamically.
- **Task 3.3**: Created `tests/dynamic-years.test.js` with 4 automated tests verifying dynamic population of bank filters, session builder options, analytics coverage rows, and home summary span.
- **Phase 3 Verification**: 192/192 automated tests passing (4 new dynamic year tests), syntax check pass, all datasets valid.



