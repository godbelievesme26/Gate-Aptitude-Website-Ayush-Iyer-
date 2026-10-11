# Build and verification report

Verified 28 September 2026. Work resumed after the usage-limit pause; existing application files and browser progress were preserved.

## Delivery

The local application is implemented in this folder and runs without package installation. Run `npm start`, then open `http://127.0.0.1:4173`, or serve `index.html` using Live Server. The included server is running at delivery. Use the same origin for subsequent visits: hostname and port changes create a separate browser storage area.

The core practice workflow is usable with the supplied questions. It cannot provide verified grades or solutions because the supplied PDFs contain no answer keys or solutions. The broader master specification is not claimed as fully complete; the limitations below distinguish the implemented product from features requiring more data or development.

## Sources and extraction

All 16 supplied PDFs under `Aptitude Sets` were inspected. Their first ten General Aptitude questions produced 16 datasets and 160 paper-specific question records. Day 1 is 2026 AE and Day 2 is 2025 AE.

| Day | Source paper | Records |
| --- | --- | --- |
| 1 | 2026 AE | 10 |
| 2 | 2025 AE | 10 |
| 3 | 2026 CE1 | 10 |
| 4 | 2026 CE2 | 10 |
| 5 | 2026 CS1 | 10 |
| 6 | 2026 CS2 | 10 |
| 7 | 2026 DA | 10 |
| 8 | 2026 EC | 10 |
| 9 | 2026 XE | 10 |
| 10 | 2025 CE1 | 10 |
| 11 | 2025 CE2 | 10 |
| 12 | 2025 CS1 | 10 |
| 13 | 2025 CS2 | 10 |
| 14 | 2025 EC | 10 |
| 15 | 2025 EE | 10 |
| 16 | 2025 ME | 10 |

There are 160 complete question crops, including source options, and eight additional standalone diagram crops for Days 1–2. The figure map identifies 56 figure-bearing question records. Contact sheets were visually inspected, including the multipage 2025 CE2 Question 5. Stable question IDs, PDF SHA-256 hashes, page numbers and crop coordinates preserve provenance. Original PDFs were not modified.

Source crops are authoritative. Machine-extracted transcripts are labelled as potentially inaccurate and are used for search; they are not verified accessible mathematical transcriptions. No answer, solution, topic, chapter, difficulty, question type or negative penalty was invented. No independent external authentication of the supplied PDFs was performed. Repeated questions in separate papers remain distinct source records.

## Implemented

- Home dashboard, real progress counters, daily goal, reasoned next action, recent activity and 118-day journey with only 16 available days.
- Daily practice, answer selection/clearing, navigation, review flags, palette, saved drafts, submission summaries, attempt history and retry sessions.
- Unlimited active-practice timer, current-visit and accumulated-question timers, and a nonblocking two-minute checkpoint. Practice does not auto-submit.
- Separate timed tests with a wall-clock deadline and expiry handling, including while on another app route.
- Central scoring engine supporting explicit MCQ/MSQ/NAT metadata, missing-key handling and explicit negative penalties. All supplied records currently remain ungraded.
- Daily completion only after submitting all ten responses; participation XP awarded once per stable question; local-date streak and longest streak; idempotent submission.
- Searchable PYQ bank, source display and enlargement, year/paper filters, custom sessions, saved practice configurations and shared session generation.
- Bookmarks with categories, personal notes, notebooks, local source-issue reports, and review views for mistakes/recovery/mastery when graded evidence exists.
- User-authored flashcards with self-rated recall and simple due scheduling.
- Basic date/minutes study planner, archive-backed session actions, coverage/activity analytics and weekly/monthly summaries.
- Light/dark themes, responsive navigation, guarded keyboard shortcuts, command search, settings, centralized local persistence and cross-tab conflict protection.
- Backup export, validated import with confirmation, reset confirmations, and protection against corrupt or unsupported stored schemas.
- Offline service-worker caching for the app, all datasets and question crops; web manifest and installation icons.

## Verification evidence

Automated verification: **18 tests passed, 0 failed**. JavaScript syntax checks passed. Dataset validation returned 16 sets, 160 questions, 160 ungraded records and no warnings.

Tests cover scoring and missing metadata, session filtering, duplicate submission, completion, XP, streaks, recovery, timers, storage validation, flashcard scheduling, source hashes and paths, unique IDs, absence of fabricated fields, mastery rules, recommendation behavior, escaped content, and route rendering with empty/populated state.

Browser journeys exercised:

- Answer, next/previous, clear, review flag and reload restoration of a daily draft.
- Partial submission remaining incomplete; a ten-answer daily submission completing one day; history and retry.
- Participation XP and streak displayed from actual QA submissions.
- PYQ search, bookmark categorization, personal note, notebook and flashcard creation; flashcard review advancing its due date.
- Filtered custom practice and retry retaining submitted answers.
- A live two-minute checkpoint observed after more than three minutes without navigation or automatic submission.
- Timed test expiry while away from the quiz, retaining the answered response.
- Dark theme persistence; desktop and mobile layouts; source image enlargement.
- Unsupported backup version rejected, valid backup reaching confirmation, and cancellation preserving existing data.
- With the local server stopped, the cached app reopened with saved progress, loaded the bank and displayed/enlarged a source image. The server was then restarted successfully.

No warning/error console entries appeared in the final inspected browser state. The Home preview is saved as `docs/home-preview.png`.

## Partial, unavailable and unverified areas

- Verified grades, accuracy, correct/wrong explanations, negative-mark outcomes, genuine mistake recovery and mastery cannot be demonstrated on the supplied archive without authoritative keys and applicable metadata. Engine behavior is covered with abstract test fixtures, not invented academic answers.
- Days 17–118 require additional source papers. They are unavailable, not fabricated.
- Topic/difficulty filters and topic-level diagnostics require verified metadata. Search transcripts have extraction errors; full accessible equation/diagram transcription remains unfinished.
- Planning is a basic date/minutes implementation. A detailed adaptive weekly-availability scheduler and the full advanced planning specification are not implemented.
- Analytics are basic observed-activity and coverage views, not predictive rank, readiness or topic-strength models. No AI tutor, generated academic explanations or remote AI integration is connected.
- Flashcards use a simple local interval rule; they are not a validated personalized learning model.
- Export triggers a JSON download, but the embedded browser's download event timed out during verification. Successful file delivery therefore remains unverified. Import replacement and destructive reset were not executed against the retained browser data. Backup initiation does not prove the browser saved the file; confirm a usable export before resetting important progress.
- Checkpoint audio is wired to settings but was not audibly verified. Installed-PWA behavior, all browser engines, screen-reader usability and exhaustive keyboard-only interaction were not tested.
- Offline caching requires an initial successful online/local load. Full original PDFs are excluded from precaching. Browser eviction or clearing can remove local progress. There is no account, cloud sync, push notification or server-side backup.
- A closed browser cannot execute a test deadline; expiry is applied on reopening. Active practice time intentionally excludes time away from the quiz.
- `localhost:4173` contains verification activity and retained preferences; it was not reset. `127.0.0.1:4173` is a separate origin. Keep whichever origin contains your intended progress.

## Files created or modified

The application was created in the supplied folder; source PDFs were left unchanged. Generated question filenames are grouped here rather than listing 168 near-identical paths.

| Files | Responsibility |
| --- | --- |
| `index.html`, `css/style.css` | App entry point and responsive visual system |
| `js/app.js` | Routing, UI events, lifecycle and persistence integration |
| `js/home.js`, `js/views.js`, `js/ui.js` | Dashboard, product views and shared UI helpers |
| `js/domain.js` | Sessions, submission, history, XP, streaks, recommendations and cards |
| `js/scoring.js`, `js/timer.js` | Central scoring and timer engines |
| `js/storage.js`, `js/loader.js` | Validated persistence and registry/data loading |
| `data/registry.json`, `data/day01.json` through `data/day16.json` | Source-backed archive |
| `figures/day01-q01.png` through each day's `q10.png` | 160 authoritative question crops |
| `figures/*-diagram.png` | Eight supplementary diagram crops |
| `assets/logo.svg`, `assets/icon-192.png`, `assets/icon-512.png` | Branding/install assets |
| `sw.js`, `manifest.webmanifest` | Offline cache and install metadata |
| `scripts/serve.mjs` | Dependency-free local HTTP server |
| `scripts/check.mjs`, `scripts/validate-data.mjs` | Syntax and archive validation |
| `scripts/inspect_sources.py`, `scripts/extract_sources.py`, `scripts/annotate_figures.py` | Source inspection and reproducible crop pipeline |
| `scripts/create_icons.py` | Install icon generation |
| `scripts/check_boundaries.py` | Exploratory extraction-boundary inspection; not the acceptance validator |
| `tests/engines.test.js`, `tests/archive.test.js`, `tests/views.test.js` | 18 automated checks |
| `docs/source-audit.json`, `docs/figure-map.json`, `docs/validation-report.json` | Extraction provenance and validation evidence |
| `docs/BUILD_REPORT.md`, `docs/home-preview.png` | This report and final visual preview |
| `package.json`, `README.md`, `.gitignore` | Run commands, documentation and temporary-file exclusions |

Ignored `tmp/` files hold intermediate PDF text, contact sheets, browser test inputs and server logs. They are not application dependencies.
