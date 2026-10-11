# GATE Study Workspace

A dependency-free, browser-local GATE General Aptitude practice application built from the 16 supplied PDFs.

## Run

Run `npm start`, then open http://127.0.0.1:4173. Alternatively, open `index.html` with VS Code Live Server. Do not use a `file://` URL: browsers block JSON module loading there.

Use the same hostname and port each time: browser-local progress belongs to that origin. The verification origin `http://localhost:4173` contains QA activity; the delivered `127.0.0.1` origin is separate.

## Verify

- `npm test` — engine and data tests.
- `npm run validate` — dataset structure, IDs, sources, options and image paths.
- `npm run check` — JavaScript syntax.

No package installation or build step is required. Runtime uses only browser APIs; Node is needed only for the included server and tests.

## Academic integrity

- 16 local papers, first 10 General Aptitude questions per paper: **160 paper-specific records**.
- Day 1 = 2026 AE; Day 2 = 2025 AE. Remaining papers: 2026 alphabetical, then 2025 alphabetical. The single registry is `data/registry.json`.
- The **70 GATE 2026 questions in Days 1 and 3–8** use visually checked text, mathematical notation, tables and figure-only assets. Each paper has its own official answer-key link. All 70 are MCQ, with 1 mark for Q1–5 and 2 marks for Q6–10. Editorial solutions are independently checked and labelled separately from the official keys.
- The remaining 90 questions retain full source crops and explicitly labelled machine-extracted search transcripts. They have no populated key, solution or verified type. **2025 content is unchanged.**
- Supplied PDFs and original source screenshots remain preserved. Per-question PDF hashes and page coordinates retain their lineage; official key provenance is recorded separately. Topic, chapter and difficulty are not invented.
- Answer controls show the actual text or graphical option for verified content. Unverified content still directs the learner to the original paper. MCQ, MSQ and NAT controls retain the existing answer behavior.
- Some General Aptitude questions may repeat across papers. IDs identify the source paper and question, not a deduplicated concept. Coverage is explicitly question-record coverage.
- Missing keys yield **ungraded**, never a guessed answer or false incorrect mark. A session total is unavailable if any question lacks a key. The existing user-specified one-third negative-mark rule is unchanged. Tests cover official MCQ data and separate MSQ/NAT fixtures.

See [the 2026 implementation report](docs/CONTENT_2026_IMPLEMENTATION.md) for the complete question scope, keys, solution verification, exact asset inventory, browser checks and remaining limitations.

## Source reproduction

Python dependencies: `pdfplumber`, `pypdf`, `pypdfium2`, `Pillow`.

1. `python scripts/inspect_sources.py` extracts all PDF text for inspection.
2. `python scripts/extract_sources.py` locates Q1–Q10 and renders complete question regions. Multi-page questions are joined in reading order. Final option table boundaries trim excess blank space.
3. `python scripts/annotate_figures.py` applies the manually checked figure mapping and eight standalone diagram crops for Days 1–2.
4. `python scripts/prepare-2026-content.py` reapplies the reviewed 2026 transcriptions, official keys, editorial solutions and extracted diagram assets. Run this after base extraction, which otherwise produces the original unverified datasets.
5. `python scripts/verify-2026-figures.py` independently checks rotation, repeated tiles and puzzle assembly.
6. `npm run validate` and `npm test` check output and preservation of out-of-scope data.
7. Visually inspect source contact sheets and resulting assets before accepting content changes.

Page coordinates and source SHA-256 values live in every question record. Source PDFs are never modified. `docs/source-audit.json` records page boundaries; `docs/figure-map.json` records figure-bearing questions. `docs/content-2026/asset-manifest.json` records the new 2026 assets and their extraction bounds.

## Adding a set

Create `data/day17.json` using the current schema, include its original source/crops, add one entry to `data/registry.json`, then validate. Keep IDs stable. Only verified source fields should be added. Increment the service-worker cache version after adding/changing offline assets. Future days are unavailable until their data actually exists; the journey target is 118.

## Project responsibilities

- `js/loader.js`: registry, JSON loading, stable question index and normalized search.
- `js/storage.js`: centralized persistence, schema validation, protected corrupt-data handling.
- `js/state.js`: canonical application state boundary and named progress write operations. See `docs/STATE_MODEL.md`.
- `js/scoring.js`: one scoring implementation with missing-key and missing-penalty handling.
- `js/timer.js`: active session time, current visit time, accumulated question time, checkpoint.
- `js/domain.js`: common session generator, history, completion, XP, streak, mastery, recommendations, flashcard scheduling.
- `js/home.js`, `js/views.js`, `js/ui.js`: escaped view templates and reusable UI helpers.
- `js/app.js`: routing, event wiring, lifecycle and persistence integration.
- `sw.js`: app, dataset and crop caching; original full PDFs excluded from offline precaching.

## Explicit behavior

- **Daily completion**: a submitted daily session with all questions answered. Partial sessions are history, not completion.
- **Streak**: at least one answered, submitted question per local calendar date. Multiple same-day sessions count once. A missed date breaks the current streak; longest is retained.
- **XP**: 10 points once per stable question ID for participation, independent of correctness. Session IDs prevent duplicate submission. Reset XP retains zero-valued award records to avoid duplicate rewards.
- **Mastery**: three consecutive correct attempts on three distinct local dates. One correct answer is not mastery.
- **Practice time**: counts active quiz time upward; pauses off the quiz or while the tab is hidden. A new visit begins on return. Stored question totals accumulate across visits.
- **Checkpoint**: once after 120 continuous seconds on a question visit, nonblocking; sound follows settings. Returning starts a new visit.
- **Timed test**: wall-clock deadline continues away from the quiz. While the app is running, expired drafts submit even on another route. If the browser is closed, submission occurs on reopening; no background process is claimed.
- **Recommendation**: saved draft, then first incomplete daily set, unresolved mistakes, due cards, then bank. Every suggestion has a visible reason.
- **Import**: schema validation and confirmation before replacement; download current backup first. Future versions are rejected without erasure.
- **Storage conflicts**: another-tab writes pause this tab and ask for reload rather than silently overwriting newer progress. No cloud synchronization.

See `docs/BUILD_REPORT.md` for verified journeys, remaining limitations, and file inventory.
