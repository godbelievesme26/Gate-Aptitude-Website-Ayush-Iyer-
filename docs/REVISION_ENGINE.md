# Mistake & Revision Engine — Phase 1

## Architecture audit before changes

The existing ApplicationState / Store boundary persists schema 6 under gate-preparation-v1. Answered attempts are immutable events identified by sessionId:questionId. They contain selected answer, correctness (correct, incorrect, blank, ungraded or awarded), timestamp, captured local date, elapsed question time and session/source context. A later solve uses a new session ID and appends a new attempt. Next may commit an attempt before the session finishes; final submission preserves those records.

Completed sessions retain ordered stable question IDs, timing and a score summary; attempt records own responses. The loader enriches verified questions with their supplied day/set mapping. Year, paper, number and General Aptitude subject are reliable; topic/chapter labels are absent. No topic weakness claims are appropriate.

Review Library currently filters unresolved mistakes and offers bookmarks, notes and notebooks. Its question rows link to Question Detail, which exposes solutions. The normal solver already hides solutions until submission. generateSession filters in input-array order, so review priority must be passed as an ordered question array rather than expecting its IDs filter to reorder the archive. Existing practice entry points stay intact.

Results already link to retry, question details and Review Library. Home has a compact Return to your material list suitable for one due-review row. Existing tokens, buttons, native focus states, wrapped tabs and responsive solving layouts can be reused.

## Scope and model

Revision is a pure projection of canonical attempts. There is no second queue database, persisted learning-state field or stored due date. Schema 6 remains unchanged. Imports, exports and old known-schema migrations continue to carry source history. Unknown optional review metadata is ignored by this engine.

Due is separate from learning state. Questions are never attempted, ungraded, correct, wrong, repeated mistake or recovered. Only answered, graded evidence can change a correctness-based state. Blank responses do not count; ungraded/marks-to-all responses do not erase prior graded evidence or imply correctness. All reviewed means questions with answered history, including ordinary practice.

Mistake classification is deferred. A future optional annotation can reference attemptId through the canonical Store; editing append-only attempt events or attaching a reason globally to a question would be inappropriate.

## Derivation and scheduling

Answered attempts are processed chronologically, retaining append order for timestamp ties. The latest graded answer determines the current correctness-based state. Historical incorrect counts distinguish a first mistake from a repeated mistake. Wrong → correct becomes Recovered; wrong → correct → wrong becomes Repeated mistake because it contains two historical errors without a later recovery. Recovery context records the attempt number at which recovery occurred.

| Latest relevant event | Next opportunity |
| --- | --- |
| First incorrect response, or a new error after recovery | 1 local calendar day later |
| Another incorrect response before recovery | 3 local calendar days later |
| Correct after an earlier mistake | 7 local calendar days later |
| Correct again after recovery | 14 local calendar days later |

Later consecutive correct answers keep the 14-day interval. Correct-only history is not automatically scheduled. These are transparent MVP product rules, not a claim of scientifically optimal spacing. Blank, ungraded and marks-to-all answers cannot falsely recover a mistake or reset its schedule.

The captured attempt localDate is preferred and remains stable across timezone changes. Date-only arithmetic handles month/year boundaries, leap days and daylight-saving changes. For older records without a valid captured local date, the timestamp is interpreted in the current local timezone; the original timezone cannot be reconstructed. Due means dueDate is today or earlier. Queue calculations happen on rendering and session creation; no background midnight alarm or notification is installed.

## Queue and session behavior

The default Review Library tab is Due now. Mistakes, Recovered and All reviewed remain available beside Bookmarks, Notebooks and Notes. Each compact row shows source metadata, question number, state, attempt/error counts, latest result/date and review date. Per-question and general disclosures explain the schedule. A caught-up state links to unattempted practice questions without manufactured urgency.

Only due questions enter a batch review session, ordered by:

1. Repeated mistakes.
2. Other overdue questions.
3. Other wrong questions due today.
4. Recovered questions due today.

Ties use oldest due date, then stable question ID. Duplicate question IDs appear once. The capacity selector offers 5, 10 or 20 questions; the estimate uses two minutes per included question. Individual Review actions allow an early reattempt of a question with answered history, even if its next scheduled date has not arrived.

The review generator passes its ordered question array into the existing canonical session generator. Sessions use normal practice mode with origin=revision and the policy identifier in session configuration. Review enters the normal solver with answers and solutions hidden until normal submission/results. Each new session gives the attempt a distinct ID; previous attempts remain intact. Existing commit, completion, persistence, scoring and timing paths handle the solve.

After recovery, the item leaves Mistakes, appears in Recovered and receives its next date. Result feedback and Question Detail expose concise recovery/review context. A never-attempted detail page shows no invented revision history. Home adds only a compact due-count link in its existing secondary material list. Daily Sets, Question Bank, custom sessions and continuation remain available.

## Persistence and scope protection

No schema migration, storage key, stored due date, copied attempt history or new persistence write path was introduced. Canonical schema 6 is unchanged. Existing users, imports and exports retain the source events from which revision is recomputed. Optional unknown review metadata is not consumed and cannot corrupt the derived queue.

No new XP, badges, AI, topic claims or mastery scores were added. Existing product moments remain unchanged. Verified corpus data, answer keys, editorial solutions, scoring rules and timer logic were not edited. An integrity comparison against the existing preservation manifest checked 21 protected data/domain/scoring/timer/loader files with zero changes.

## Changed files

| File | Responsibility |
| --- | --- |
| js/revision.js | Pure revision projection, local-date policy, deterministic queue and canonical review-session adapter |
| js/revision-view.js | Review tabs, compact queue, scheduling disclosures and detail summary |
| css/revision.css | Token-based queue layout, neutral states, due emphasis and responsive controls |
| js/views.js | Review Library, question rows/detail, retry actions and recovery feedback integration |
| js/app.js | Review routes/actions and capacity estimate handling through existing state APIs |
| js/home.js | Minimal due-review signal |
| index.html, sw.js | Stylesheet/module loading and service-worker cache refresh |
| tests/revision.test.js | 29 focused model, persistence, date, session and rendering tests |
| tests/visual/revision.html, tests/visual/revision-fixture.js | Explicit disposable-origin browser scenarios and inspection controls |
| docs/REVISION_ENGINE.md, docs/revision-qa/* | Implementation report and saved QA evidence |

## Verification

Required checks passed: npm test (131 tests, including 29 new revision tests), npm run check, and npm run validate (16 datasets, 160 answer keys, 160 editorial solutions, 153 figure assets). Existing tests were not weakened.

The new tests cover never/blank/ungraded history, first/repeated errors, recovery/relapse, correct-only history, each interval, future/overdue eligibility, priority/ties, unique queues, append-only attempts, canonical commits and refresh, early individual review, capacity, normal generation, old-schema migration, ignored corrupt optional metadata, import/export, source escaping and retrieval-safe rendering. Date coverage includes midnight, a session crossing midnight, same-day attempts, leap/year boundaries, DST and three process timezones.

Browser QA used only synthetic state on isolated origin 127.0.0.1:4186; personal progress on port 4177 was not used for test submissions. Scenarios A–H were exercised on October 5–6, 2026:

| Scenario | Observed result |
| --- | --- |
| A: First wrong answer | One Wrong item, one canonical attempt, next-day review date and source metadata |
| B: Correct reattempt | Normal solver initially hid solutions; history retained both events, state became Recovered and scheduled seven days later |
| C: Subsequent wrong answer | Three separate attempt/session IDs; Repeated mistake, two historical errors and short interval reset |
| D: Batch review | Four due questions selected in deterministic order, future/correct-only records excluded; normal solving and results persisted |
| E: Refresh | Repeated-mistake state and history retained with one queue item |
| F: Ordinary practice | Daily Set solving/Continue worked; Question Bank and session builder remained available; a new custom session started; an existing daily session resumed at its saved second question |
| G/H: Responsive and themes | Light and dark at 1440×900, 1024×900, 768×1024, 390×844, 375×812 and 320×740; no horizontal overflow; queue buttons at least 44px high |

No browser console warnings/errors were captured during these checks. Automated DOM measurements supplement visual inspection; this is not a formal screen-reader audit or a timed usability study with students.

Evidence: [reattempt records](revision-qa/reattempt-evidence.json), [review and normal session records](revision-qa/session-evidence.json), [12 responsive measurements](revision-qa/layout-checks.json), [responsive contact sheet](revision-qa/responsive-overview.png). Screenshots show synthetic histories, not personal progress.

## Limits and extension points

The due-first heading, count and single Start review action make the next step explicit; individual reattempts take one click into the solver. Why-this-date disclosures keep prioritization explainable. Neutral error labels and restrained semantic colors avoid punitive treatment. These are implementation/design observations, not claims of measured learning outcomes.

All reviewed includes all answered history, not just sessions whose origin is revision. There is no automatic schedule for correct-only or ungraded-only history, no notification service, no topic inference and no scientific optimization claim. Existing question-detail and history links still allow deliberate solution reading; the primary Review action always starts retrieval first.

Future scheduling can replace the pure policy/projection while keeping canonical attempts authoritative. Attempt-ID annotations are the extension point for optional mistake reasons or confidence. Reliable topic metadata would be required before topic analysis. Timing and scoring evidence already remain in canonical history for future analysis; this pass adds none of those analyses or adaptive features.
