# GATE 2026 content and solving experience

Completed 4 October 2026. This report supersedes the earlier reports’ statements that the entire archive lacks answer keys.

## Delivered scope

The registry contains **70 GATE 2026 questions in Days 1–8**, not 80 Aerospace questions. Day 2 is 2025 Aerospace and was excluded. Following the explicit clarification, each of the seven 2026 papers was checked against its own official key.

| Day | Paper | Text/math/table only | Requires figures | Official Q1–10 answers |
|---|---|---|---|---|
| 1 | [AE](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf) | 1, 3, 4, 5, 6, 9 | 2, 7, 8, 10 | A B A B C D A D C C |
| 3 | [CE1](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf) | 1, 3, 4, 6, 10 | 2, 5, 7, 8, 9 | A A A C B A B A B D |
| 4 | [CE2](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf) | 1, 2, 4, 5, 6, 7 | 3, 8, 9, 10 | C A A D C B B C B B |
| 5 | [CS1](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf) | 1, 3, 4, 5, 6, 9, 10 | 2, 7, 8 | B C C D C B D A A C |
| 6 | [CS2](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf) | 1, 3, 4, 5, 6, 10 | 2, 7, 8, 9 | A C A A C A A A B C |
| 7 | [DA](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf) | 1, 2, 4, 5, 6, 7, 8, 9 | 3, 10 | B B A C D A B D C C |
| 8 | [EC](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf) | 1, 2, 4, 5, 6, 7, 8 | 3, 9, 10 | B A D B B A C C C C |

Totals: **45 text/math/table-only questions, 25 figure questions, 70 official answers, 70 independently checked editorial solutions, 84 extracted figure assets**. All 70 official records are MCQ. Questions 1–5 carry 1 mark each; questions 6–10 carry 2 marks each. The existing one-third negative-mark rule remains unchanged.

No in-scope solution remains unpopulated. The official PDFs supply answer letters, types and marks; the explanations are explicitly labelled editorial, not official solutions.

## Presentation and content

- Verified questions now render selectable text, semantic tables, subscripts, superscripts, segment overlines and only necessary figures. No full-question screenshot is rendered for these 70 questions.
- MCQ/MSQ options are vertical full-row controls containing the actual option text or figure. Selection uses a checkmark and an emphasized border as well as color. Keyboard focus remains visible. Numeric input and existing answer handlers are retained.
- The Home invitation, time selector, recommendation order, journey and recent-practice layout remain intact. Shared tokens add a cool neutral canvas, a restrained indigo emphasis surface and subtle option backgrounds in both themes.
- The question bank previews use the safe notation renderer. Question Detail exposes the four options, official key link and checked solution.
- Availability wording now reflects partial key coverage. Fully keyed daily sets do not show the missing-key warning. Mixed sessions retain the engine’s existing rule: no total score unless every question has a key; graded accuracy can still be available.
- The service worker caches the new content module and figure/option assets. Its cache version was advanced to v9.

Original IDs, order, PDF paths, page/bounding-box provenance, PDF hashes and source screenshots remain available. Byte comparisons confirm that Day 2 and Days 9–16, the registry, and the canonical state/persistence/session/scoring/timer files covered by the baseline were unchanged. No application-state schema migration or retrospective regrading was introduced.

## Source and solution verification

All 70 source questions were visually inspected against the supplied PDF crops. Extracted text was corrected where it lost exponents, logarithm bases, fractions, segment notation or option labels. Examples include DA Q4’s exponents, EC Q4’s nested logarithm bases, CE2 Q2’s powers and EC Q3’s P/Q/R/S option mapping.

Figures were extracted from the PDFs’ original image objects, flattened onto white where transparency required it, and cropped at diagram boundaries. Composite panels were separated into stem/reference diagrams and individual option images. No diagrams were regenerated. All 84 resulting assets were visually inspected in contact sheets against the source. Text inside EC Q10’s transformation drawings is essential visual content and remains in the diagram images.

Solutions were checked through direct mathematical derivation, source-based logical reasoning and visual comparison. Independent executable checks additionally cover:

- dice probabilities, the bulb-update sequence, integer mean/median/mode enumeration and the digit puzzle;
- circle tangency, string-length geometry, revenue equations, logarithm identities and shaded areas;
- exhaustive chess-elimination and parent-child match constraints;
- pixel comparisons for the CE1 clockwise rotation, each of CE2’s three repeated tiles and DA’s four-piece assembly.

`scripts/prepare-2026-content.py` reproduces the data and assets from the source PDFs and reviewed authoring file. Repeated preparation produced identical data hashes. `scripts/verify-2026-figures.py` independently checks the three image puzzles. These authoring utilities require Python, Pillow and pypdf; the browser app gains no runtime dependency.

## Schema additions

The existing question objects now use `answer`, `type`, `solution`, `solutionStatus`, `answerSource`, and `transcriptionStatus: "source-verified"`. Optional `table`, `afterTable` and `figureSequence` describe source layout. `figures[]` and `options[].figure` hold image paths, alt text and extraction provenance. Existing `question`, option labels, marks and source lineage remain authoritative content fields.

The small escaped notation grammar supports `^{...}`, `_{...}` and `\overline{...}` including nested bases/exponents. It does not accept arbitrary HTML. Content and solutions are never hardcoded into UI components. Complex visual puzzles have contextual alternative text, but not every spatial option has a complete nonvisual equivalent; visual inspection is still necessary for those puzzles.

## Validation

| Check | Result |
|---|---|
| `npm test` | **78 passed, 0 failed** |
| `npm run check` | Passed |
| `npm run validate` | Passed: 16 sets, 160 unique questions, 70 keyed/solved, 90 ungraded, 84 new figure references valid |
| Independent figure checks | Passed: rotation B, repeated tile B in all three positions, puzzle assembly A |
| Deterministic preparation | Passed; repeated data hashes identical |
| Out-of-scope content and engine preservation | Passed SHA-256 comparisons |

Browser testing used isolated local origins, so existing user progress was not used for test submissions. Verified routes and interactions: Home, Question Bank, Question Detail, Daily Set, Practice, Test mode, selected answers, keyboard selection/submission, Continue, timer displays, results, bookmarks, notes, recent practice and mobile navigation.

Specific browser results:

- A full Aerospace daily set advanced through questions 1–10 exactly once. Nine correct answers and a deliberate wrong one-mark answer produced **13.67/15 and 90% accuracy**. Double-clicking final confirmation left one completed session and ten feedback records.
- Refresh retained selected answers, completed results, bookmarks and a personal note. Home showed the completed day and the two expected history entries.
- An isolated MCQ/MSQ/NAT fixture used the real app, handlers and canonical state. MSQ retained two selections after refresh; numeric keystrokes retained 42 after refresh. Submission produced **3/3** with the correct selected values.
- A one-minute test fixture began at 00:59 and safely submitted at expiry with 01:00 elapsed. Practice continued to use count-up timing.
- Mixed keyed/unkeyed sessions showed correct per-attempt feedback and no fabricated total score.
- No errors or warnings were captured in the production-content QA tab’s console.

Inspected viewport sizes: **1440×900 desktop, 390×844 mobile, and 320×800 narrow mobile**. The 320-pixel price table fits its container. Text, graph and figure-option layouts were checked for page overflow; none was observed. Light/dark Home and solving surfaces were inspected. Keyboard focus was observed on the selected option. Reduced-motion behavior was verified through existing code/style checks; an operating-system preference change was not performed.

Measured token contrast ratios (light / dark): body text 15.09 / 14.27; supporting text on the emphasis surface 4.53 / 6.43; selected-option text 6.77 / 6.57; primary button text 7.69 / 8.93; focus against study surface 5.10 / 10.06; option boundary 3.13 / 3.40.

## Remaining boundaries

The other 90 questions retain their original source-image presentation and unavailable-key behavior. All 2025 content is untouched. Historical ungraded attempts are retained as recorded. There are no real MSQ/NAT questions in this 70-question scope; those controls were tested with explicit fixtures. Original figure resolution is preserved, so exceptionally enlarged diagrams can reveal raster pixels. Browser testing covered Chromium through the in-app browser; other browsers and full screen-reader walkthroughs remain unverified.

## Exact maintained files changed or added

Data:

- `data/day01.json`
- `data/day03.json`
- `data/day04.json`
- `data/day05.json`
- `data/day06.json`
- `data/day07.json`
- `data/day08.json`

Application presentation and caching:

- `js/question-content.js` (new)
- `js/views.js`
- `js/home.js`
- `css/system.css`
- `css/home.css`
- `css/quiz.css`
- `sw.js`

Authoring and validation:

- `scripts/prepare-2026-content.py` (new)
- `scripts/verified-2026-transcriptions.json` (new)
- `scripts/verify-2026-figures.py` (new)
- `scripts/validate-data.mjs`
- `tests/archive.test.js`
- `tests/views.test.js`
- `tests/verified-content.test.js` (new)
- `tests/fixtures/official-2026-ga-keys.json` (new)
- `tests/fixtures/content-preservation.json` (new)

Reports and evidence:

- `README.md`
- `docs/validation-report.json`
- `docs/CONTENT_2026_IMPLEMENTATION.md` (this report)
- `docs/content-2026/asset-manifest.json`
- `docs/content-2026/home-desktop.jpg`
- `docs/content-2026/home-dark-desktop.jpg`
- `docs/content-2026/home-mobile.jpg`
- `docs/content-2026/solving-desktop.jpg`
- `docs/content-2026/solving-mobile.jpg`
- `docs/content-2026/graph-desktop.jpg`
- `docs/content-2026/graph-dark-desktop.jpg`
- `docs/content-2026/graph-mobile.jpg`
- `docs/content-2026/graph-dark-mobile.jpg`
- `docs/content-2026/table-320.jpg`

Temporary source contact sheets, raw extraction checks and the disposable fixture server live under the already-ignored `tmp/` directory. They are not application files. The repository has no Git checkout, so preservation was checked with the saved pre-task SHA-256 baseline rather than a Git diff.

The following generated asset inventory gives every new figure filename. The adjacent [asset manifest](content-2026/asset-manifest.json) also records question IDs, source PDF/page/image objects and crop bounds.

## Exact figure assets

- `figures/gate-2026-ae-ga-02-figure-1.png`
- `figures/gate-2026-ae-ga-02-option-A.png`
- `figures/gate-2026-ae-ga-02-option-B.png`
- `figures/gate-2026-ae-ga-02-option-C.png`
- `figures/gate-2026-ae-ga-02-option-D.png`
- `figures/gate-2026-ae-ga-07-figure-1.png`
- `figures/gate-2026-ae-ga-07-figure-2.png`
- `figures/gate-2026-ae-ga-07-figure-3.png`
- `figures/gate-2026-ae-ga-08-figure-1.png`
- `figures/gate-2026-ae-ga-10-figure-1.png`
- `figures/gate-2026-ce1-ga-02-figure-1.png`
- `figures/gate-2026-ce1-ga-02-option-A.png`
- `figures/gate-2026-ce1-ga-02-option-B.png`
- `figures/gate-2026-ce1-ga-02-option-C.png`
- `figures/gate-2026-ce1-ga-02-option-D.png`
- `figures/gate-2026-ce1-ga-05-figure-1.png`
- `figures/gate-2026-ce1-ga-05-option-A.png`
- `figures/gate-2026-ce1-ga-05-option-B.png`
- `figures/gate-2026-ce1-ga-05-option-C.png`
- `figures/gate-2026-ce1-ga-05-option-D.png`
- `figures/gate-2026-ce1-ga-07-figure-1.png`
- `figures/gate-2026-ce1-ga-08-figure-1.png`
- `figures/gate-2026-ce1-ga-09-figure-1.png`
- `figures/gate-2026-ce2-ga-03-figure-1.png`
- `figures/gate-2026-ce2-ga-03-option-A.png`
- `figures/gate-2026-ce2-ga-03-option-B.png`
- `figures/gate-2026-ce2-ga-03-option-C.png`
- `figures/gate-2026-ce2-ga-03-option-D.png`
- `figures/gate-2026-ce2-ga-08-figure-1.png`
- `figures/gate-2026-ce2-ga-09-figure-1.png`
- `figures/gate-2026-ce2-ga-10-figure-1.png`
- `figures/gate-2026-ce2-ga-10-option-A.png`
- `figures/gate-2026-ce2-ga-10-option-B.png`
- `figures/gate-2026-ce2-ga-10-option-C.png`
- `figures/gate-2026-ce2-ga-10-option-D.png`
- `figures/gate-2026-cs1-ga-02-figure-1.png`
- `figures/gate-2026-cs1-ga-02-figure-2.png`
- `figures/gate-2026-cs1-ga-02-option-A.png`
- `figures/gate-2026-cs1-ga-02-option-B.png`
- `figures/gate-2026-cs1-ga-02-option-C.png`
- `figures/gate-2026-cs1-ga-02-option-D.png`
- `figures/gate-2026-cs1-ga-07-figure-1.png`
- `figures/gate-2026-cs1-ga-07-option-A.png`
- `figures/gate-2026-cs1-ga-07-option-B.png`
- `figures/gate-2026-cs1-ga-07-option-C.png`
- `figures/gate-2026-cs1-ga-07-option-D.png`
- `figures/gate-2026-cs1-ga-08-figure-1.png`
- `figures/gate-2026-cs2-ga-02-figure-1.png`
- `figures/gate-2026-cs2-ga-02-option-A.png`
- `figures/gate-2026-cs2-ga-02-option-B.png`
- `figures/gate-2026-cs2-ga-02-option-C.png`
- `figures/gate-2026-cs2-ga-02-option-D.png`
- `figures/gate-2026-cs2-ga-07-figure-1.png`
- `figures/gate-2026-cs2-ga-07-option-A.png`
- `figures/gate-2026-cs2-ga-07-option-B.png`
- `figures/gate-2026-cs2-ga-07-option-C.png`
- `figures/gate-2026-cs2-ga-07-option-D.png`
- `figures/gate-2026-cs2-ga-08-figure-1.png`
- `figures/gate-2026-cs2-ga-09-figure-1.png`
- `figures/gate-2026-cs2-ga-09-option-A.png`
- `figures/gate-2026-cs2-ga-09-option-B.png`
- `figures/gate-2026-cs2-ga-09-option-C.png`
- `figures/gate-2026-cs2-ga-09-option-D.png`
- `figures/gate-2026-da-ga-03-figure-1.png`
- `figures/gate-2026-da-ga-03-figure-2.png`
- `figures/gate-2026-da-ga-03-figure-3.png`
- `figures/gate-2026-da-ga-03-figure-4.png`
- `figures/gate-2026-da-ga-03-option-A.png`
- `figures/gate-2026-da-ga-03-option-B.png`
- `figures/gate-2026-da-ga-03-option-C.png`
- `figures/gate-2026-da-ga-03-option-D.png`
- `figures/gate-2026-da-ga-10-figure-1.png`
- `figures/gate-2026-ec-ga-03-figure-1.png`
- `figures/gate-2026-ec-ga-03-option-A.png`
- `figures/gate-2026-ec-ga-03-option-B.png`
- `figures/gate-2026-ec-ga-03-option-C.png`
- `figures/gate-2026-ec-ga-03-option-D.png`
- `figures/gate-2026-ec-ga-09-figure-1.png`
- `figures/gate-2026-ec-ga-10-figure-1.png`
- `figures/gate-2026-ec-ga-10-figure-2.png`
- `figures/gate-2026-ec-ga-10-option-A.png`
- `figures/gate-2026-ec-ga-10-option-B.png`
- `figures/gate-2026-ec-ga-10-option-C.png`
- `figures/gate-2026-ec-ga-10-option-D.png`
