# Current corpus audit — 5 October 2026

**CURRENT CORPUS: 160 / 160 VERIFIED**

This report supersedes the earlier 70-question coverage report. The registry remains 16 sets and 160 stable question IDs. Days 1 and 3–8 retain their existing verified content; Days 2 and 9–16 now have official keys, reviewed structured transcriptions and independently derived editorial solutions. No questions were added.

## Coverage

| Measure | Count |
|---|---:|
| Current questions | 160 |
| Official key or ruling | 160 |
| Ordinary keyed answers | 159 |
| Editorial solutions | 160 |
| MCQ | 160 |
| MSQ | 0 |
| NAT | 0 |
| Questions requiring figures or visual options | 54 |
| Text / math / table only | 106 |
| Semantic tables | 10 |
| Question and option figure assets | 153 |
| New assets | 69 |

No blocked questions or unresolved master-order discrepancies remain. MSQ and NAT behavior is covered by existing synthetic tests; none of the current official GA rows is MSQ or NAT.

## Sources and mapping

- [IIT Roorkee 2025 official master-paper and final-key index](https://gate2025.iitr.ac.in/question-papers.html). Eight paper codes: AE, CE1, CE2, CS1, CS2, EC, EE and ME.
- [IIT Guwahati 2026 official paper/key index](https://gate2026.iitg.ac.in/QPs-answer-keys.html). The newly completed 2026 set is XE.
- Each new key record includes session, question number, type, marks, key URL, key SHA-256, master-paper URL, verification date and mapping status.
- All source GA pages for the 90 newly completed questions match their official master paper in extracted text and embedded image bytes. This establishes the question and option ordering; it does not merely assume that array positions match. See [page comparison evidence](corpus-pass/master-mapping.json).
- Figures were checked visually against the supplied source pages. The crop review corrected XE Q2 and CE1 Q8 image-resource ordering, and trimmed incomplete or extraneous crop edges before release. Original source PDFs and screenshot provenance are retained internally.
- The previous 70 verified question records pass byte-preservation checks. Their existing source figures were not rewritten by the new preparation script.

## Official exception: 2025 EC Q8

The official key says **MTA**, not A/B/C/D. It awards 2 marks to every response, including a blank response. A new `awarded` attempt result records this ruling without treating it as correct or incorrect. It is excluded from graded accuracy. The detail screen and post-submission feedback explain the ruling; no normal correct option is invented. The editorial traces the inconsistent elimination sequence: U is removed in round two but referenced again in round four.

The scoring change is restricted to that explicit official ruling. Ordinary question marks and the existing one-third negative-mark rule remain unchanged. Persistence accepts the additive result value; there is no state rewrite or retrospective regrading. Old ungraded results remain ungraded, and their feedback distinguishes the original grade from a newly available key.

## Rendering correction

The root cause was the shared `sourceQuestion` fallback: records without source-verified transcriptions rendered a full `sourceImage`, accompanied by a searchable transcript and an enlargement action. The same helper was used by solving and detail views.

Two full-page image entry points were removed: the shared inline fallback and the enlargement dialog. The source-PDF link was removed from normal question detail. Paper files and lineage remain available internally. Unverified structured content now produces an honest unavailable notice instead of a paper image.

`question-content.js` supplies the canonical text, safe notation, tables, figure and option rendering. Question previews use the same verification and notation rules. Question-specific asset paths are required; invalid figure paths produce an unavailable notice.

| Surface | Rendering |
|---|---|
| Daily set | Verified, selectable question previews |
| Practice and timed test | Structured stem/table/figure + canonical option content |
| Resume | Same quiz renderer and persisted session |
| Question detail | Structured question/options + labelled editorial solution |
| Question bank and review lists | Canonical verified previews |
| Results | Concise feedback, with keyboard-operable question-and-solution disclosure |

No full source-page image appears in the tested normal solving views or the automated render checks for all 160 records. The service worker caches structured figures rather than the legacy paper screenshots. Solutions and keys are absent from the active solving HTML; detail and submitted results deliberately expose them for review.

## Home visual audit and direction

Before editing, Home was inspected at 1440, 1024, 390 and 320 pixels. Its primary action and order of information were strong. The hero/canvas separation was weak, the small statistics had too little visual weight, goal and week activity felt detached, and lower sections repeated similar emphasis.

The implemented direction uses a warm neutral light canvas or quiet charcoal dark canvas, an ink-indigo study surface, an inset tonal action area, cream editorial headline, larger tabular statistics and a restrained brass progress accent. Goal and week activity share a subtle band. Journey, review and history retain open, quieter rows. No illustrations, new product features, gradients or animation sequences were added. Home-specific colors are centralized in the existing token sheet. Destinations, recommendation, budgets and session generation are unchanged.

## Verification

- `npm test`: **84 passed, 0 failed**.
- `npm run check`: JavaScript syntax passed.
- `npm run validate`: 16 sets, 160 unique questions, 160 official keys/rulings, 160 solutions, 153 source figure assets, zero ungraded records.
- Added corpus-wide key/type/marks/provenance and renderer tests, regression guards for the corrected visual-option mapping, MTA scoring and persistence tests, historical-result immutability checks, and independent numerical enumerations.
- Existing persistence, initialization/migration, idempotence, timer, ordering and refresh tests remain passing. Domain, state, timer and registry pass byte-preservation checks.

### Browser checks

Home: 1440×900, 1024×900, 768×1024, 390×844, 375×812 and 320×740 in both themes. Solving: 1440×900, 1024×900, 768×1024, 390×844 and 320×800 in both themes. Screenshots and DOM checks confirmed loaded cropped images, selectable text and no source screenshot elements.

Exercised Home Start Now with a 6-minute custom budget (3 questions), rejected custom value 0 with a clear message, refreshed and resumed a selected answer, and advanced in session order. A submitted session with one correct, one incorrect and one blank scored 0.67/3 with 50% graded accuracy; refresh retained the same result. Tested the 2025 AE daily set and its semantic pixel table, 2026 XE cube figures, a 2025 CE1 timed test with visual choices, 2025 EE bank filtering/detail/bookmark/review, and an unanswered MTA question scoring 2/2 without a correctness grade. A discovered mobile results overflow was fixed and rechecked.

Browser coverage is representative, not a claim of 160 manual browser solving sessions. All 160 records are covered by automated rendering/content checks; all 69 new crops were visually reviewed. OS-level reduced-motion emulation and physical-device testing were not available; the existing reduced-motion CSS is retained.

The isolated Home presentation harness was also checked with a new user, unavailable archive, both themes and its reduced-motion toggle. The unavailable action is disabled and explains the missing content. Final console inspection returned no errors or warnings. Browser screenshots show QA progress on the isolated preview origin, not the user's personal study record.

### Visual evidence

- [Final Home desktop](corpus-pass/home-final-desktop.png)
- [Home with Start Now, light](corpus-pass/home-light-1440.png) and [dark](corpus-pass/home-dark-1440.png)
- [Mobile Home](corpus-pass/home-dark-390.png)
- [New-user fixture](corpus-pass/home-empty-light.png) and [unavailable fixture](corpus-pass/home-unavailable-dark.png)
- [Desktop figure solving](corpus-pass/question-light-1440.png) and [mobile figure solving](corpus-pass/question-dark-390.png)
- [Timed test with visual choices](corpus-pass/test-visual-options.png)
- [Corrected mobile result and solution](corpus-pass/result-solution-mobile.png)

All Home and solving sizes listed above have individual captures in `docs/corpus-pass/`.

## Changed areas

- `css/system.css`, `css/home.css`: Home tokens, tonal surfaces, typography and layout rhythm.
- `js/question-content.js`, `js/views.js`, `js/app.js`, `css/quiz.css`: shared structured rendering, removed page viewer, semantic tables/previews, result solution disclosure and responsive fix.
- `js/home.js`: current verified coverage wording.
- `data/day02.json`, `data/day09.json` through `data/day16.json`, 69 question/option crops.
- `js/scoring.js`, `js/storage.js`: narrowly scoped official MTA ruling.
- `scripts/prepare-remaining-content.py`, `scripts/verified-remaining-transcriptions.json`, official key fixtures, corpus tests, validator and service worker.

## Question-by-question audit

The same table is available as [CSV](corpus-pass/question-audit.csv).

|Question ID|Day|Year|Paper|Question number|Type|Marks|Official answer|Solution status|Answer-source|Source verification status|
|---|---|---|---|---|---|---|---|---|---|---|
|gate-2026-ae-ga-01|1|2026|AE|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-02|1|2026|AE|2|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-03|1|2026|AE|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-04|1|2026|AE|4|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-05|1|2026|AE|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-06|1|2026|AE|6|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-07|1|2026|AE|7|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-08|1|2026|AE|8|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-09|1|2026|AE|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ae-ga-10|1|2026|AE|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/AE_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2025-ae-ga-01|2|2025|AE|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-02|2|2025|AE|2|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-03|2|2025|AE|3|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-04|2|2025|AE|4|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-05|2|2025|AE|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-06|2|2025|AE|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-07|2|2025|AE|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-08|2|2025|AE|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-09|2|2025|AE|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ae-ga-10|2|2025|AE|10|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/AE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-ce1-ga-01|3|2026|CE1|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-02|3|2026|CE1|2|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-03|3|2026|CE1|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-04|3|2026|CE1|4|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-05|3|2026|CE1|5|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-06|3|2026|CE1|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-07|3|2026|CE1|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-08|3|2026|CE1|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-09|3|2026|CE1|9|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce1-ga-10|3|2026|CE1|10|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-01|4|2026|CE2|1|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-02|4|2026|CE2|2|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-03|4|2026|CE2|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-04|4|2026|CE2|4|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-05|4|2026|CE2|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-06|4|2026|CE2|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-07|4|2026|CE2|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-08|4|2026|CE2|8|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-09|4|2026|CE2|9|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ce2-ga-10|4|2026|CE2|10|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CE2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-01|5|2026|CS1|1|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-02|5|2026|CS1|2|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-03|5|2026|CS1|3|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-04|5|2026|CS1|4|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-05|5|2026|CS1|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-06|5|2026|CS1|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-07|5|2026|CS1|7|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-08|5|2026|CS1|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-09|5|2026|CS1|9|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs1-ga-10|5|2026|CS1|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-01|6|2026|CS2|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-02|6|2026|CS2|2|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-03|6|2026|CS2|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-04|6|2026|CS2|4|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-05|6|2026|CS2|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-06|6|2026|CS2|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-07|6|2026|CS2|7|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-08|6|2026|CS2|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-09|6|2026|CS2|9|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-cs2-ga-10|6|2026|CS2|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-01|7|2026|DA|1|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-02|7|2026|DA|2|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-03|7|2026|DA|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-04|7|2026|DA|4|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-05|7|2026|DA|5|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-06|7|2026|DA|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-07|7|2026|DA|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-08|7|2026|DA|8|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-09|7|2026|DA|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-da-ga-10|7|2026|DA|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/DA_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-01|8|2026|EC|1|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-02|8|2026|EC|2|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-03|8|2026|EC|3|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-04|8|2026|EC|4|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-05|8|2026|EC|5|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-06|8|2026|EC|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-07|8|2026|EC|7|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-08|8|2026|EC|8|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-09|8|2026|EC|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-ec-ga-10|8|2026|EC|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/EC_Keys.pdf)|Verified master mapping; original 70 retained|
|gate-2026-xe-ga-01|9|2026|XE|1|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-02|9|2026|XE|2|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-03|9|2026|XE|3|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-04|9|2026|XE|4|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-05|9|2026|XE|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-06|9|2026|XE|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-07|9|2026|XE|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-08|9|2026|XE|8|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-09|9|2026|XE|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2026-xe-ga-10|9|2026|XE|10|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2026.iitg.ac.in/doc/download/2026/Keys/XE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-01|10|2025|CE1|1|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-02|10|2025|CE1|2|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-03|10|2025|CE1|3|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-04|10|2025|CE1|4|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-05|10|2025|CE1|5|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-06|10|2025|CE1|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-07|10|2025|CE1|7|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-08|10|2025|CE1|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-09|10|2025|CE1|9|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce1-ga-10|10|2025|CE1|10|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-01|11|2025|CE2|1|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-02|11|2025|CE2|2|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-03|11|2025|CE2|3|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-04|11|2025|CE2|4|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-05|11|2025|CE2|5|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-06|11|2025|CE2|6|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-07|11|2025|CE2|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-08|11|2025|CE2|8|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-09|11|2025|CE2|9|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ce2-ga-10|11|2025|CE2|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CE2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-01|12|2025|CS1|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-02|12|2025|CS1|2|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-03|12|2025|CS1|3|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-04|12|2025|CS1|4|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-05|12|2025|CS1|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-06|12|2025|CS1|6|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-07|12|2025|CS1|7|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-08|12|2025|CS1|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-09|12|2025|CS1|9|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs1-ga-10|12|2025|CS1|10|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS1_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-01|13|2025|CS2|1|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-02|13|2025|CS2|2|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-03|13|2025|CS2|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-04|13|2025|CS2|4|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-05|13|2025|CS2|5|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-06|13|2025|CS2|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-07|13|2025|CS2|7|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-08|13|2025|CS2|8|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-09|13|2025|CS2|9|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-cs2-ga-10|13|2025|CS2|10|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/CS2_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-01|14|2025|EC|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-02|14|2025|EC|2|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-03|14|2025|EC|3|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-04|14|2025|EC|4|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-05|14|2025|EC|5|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-06|14|2025|EC|6|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-07|14|2025|EC|7|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-08|14|2025|EC|8|MCQ|2|MTA|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-09|14|2025|EC|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ec-ga-10|14|2025|EC|10|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EC_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-01|15|2025|EE|1|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-02|15|2025|EE|2|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-03|15|2025|EE|3|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-04|15|2025|EE|4|MCQ|1|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-05|15|2025|EE|5|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-06|15|2025|EE|6|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-07|15|2025|EE|7|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-08|15|2025|EE|8|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-09|15|2025|EE|9|MCQ|2|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-ee-ga-10|15|2025|EE|10|MCQ|2|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/EE_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-01|16|2025|ME|1|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-02|16|2025|ME|2|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-03|16|2025|ME|3|MCQ|1|C|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-04|16|2025|ME|4|MCQ|1|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-05|16|2025|ME|5|MCQ|1|A|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-06|16|2025|ME|6|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-07|16|2025|ME|7|MCQ|2|D|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-08|16|2025|ME|8|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-09|16|2025|ME|9|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
|gate-2025-me-ga-10|16|2025|ME|10|MCQ|2|B|Verified editorial (not official)|[Official key](https://gate2025.iitr.ac.in/doc/2025/2025_Key/ME_Keys.pdf)|Verified: source pages match official master text and embedded images|
