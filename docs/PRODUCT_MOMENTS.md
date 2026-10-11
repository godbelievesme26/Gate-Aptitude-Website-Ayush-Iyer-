# Product moments: architecture audit and implementation

## Audit before implementation

- Home: `js/home.js`, styled by `css/home.css`. Recommendations and budgets already exist; no introductory carousel is needed.
- Progress: `ApplicationState` in `js/state.js` owns the Store boundary. `js/storage.js` owns the single `gate-preparation-v1` record, schema migration and corruption recovery.
- Completion: `ApplicationState.completeSession()` calls `domain.submit()`. Attempts are append-only and session completion is idempotent. Some attempts are committed before session completion, so comparing only the last write would miss a streak/goal reached earlier in the session.
- Streak: `domain.streak()` derives active dates from answered attempts. There is no independent streak counter to update.
- Goal: Home counts today's answered attempts against `settings.goal`. This is a question-attempt goal, not a time goal.
- Journey: `completedDays()` counts fully answered daily sets by their existing day identity. A set number is not a calendar day of attendance.
- XP: unique question participation awards in `xpEvents`; no additional awards are appropriate.
- Presentation: native `#dialog` is used for confirmations and commands. Tokens live in `css/system.css`; lightweight keyframes and reduced-motion overrides already exist in `css/components.css`.
- Responsive behaviour: Home and solving layouts have existing tablet/mobile breakpoints. Moments need a local responsive stage without altering those screens.
- Tests: Node test runner covers state, migrations, idempotency, timers, answer transitions and rendered views. Baseline: 84 passing tests from the preceding completed pass.

## Design decisions

One optional completion scene groups simultaneous events. The strongest new event gets the visual stage; real session statistics and a goal completion line remain visible beside it. Continue and Review answers are available immediately, including during animation. No sound, haptics, confetti, rewards or AI dependency is added.

Eligibility requires a newly committed completed session with every ordered question answered and matching canonical answered attempts. Partial/blank/abandoned/interrupted sessions produce no completion scene. Existing submission and scoring behaviour is retained.

Moment receipts are presentation metadata inside the existing persisted record. They are committed with session completion, before display. Runtime payloads are temporary and never restored on load. A crash between committing and displaying may skip a celebration; it cannot replay one indefinitely. The result/history remain available.

## Implemented architecture

- `js/moments.js`: pure event derivation, eligibility, shared milestone definitions, deterministic story selection and receipt creation. It reads existing domain helpers rather than maintaining parallel streak/goal counters.
- `js/state.js`: completion builds a candidate state containing the existing session/attempt/XP writes and the moment receipts. It saves once before publishing the runtime payload. On write failure, the old in-memory progress is restored and no moment is published.
- `js/storage.js`: schema 6 adds `momentReceipts`, a map from stable event ID to timestamp, under the existing storage key. Version 5 migrates by adding an empty map; existing progress is retained and no historical celebration is backfilled. Receipt validation and import/export use the existing boundary.
- `js/moment-view.js`: reusable scene renderer and editorial insight card. A dedicated native dialog host avoids racing the existing asynchronous submission-confirmation dialog. It uses native focus containment and Escape; Continue goes Home, Review answers returns to the existing result page. Controls never wait for animation. Navigation dismisses the scene.
- `css/moments.css`: local semantic aliases, number transition, completing arc, confirmation line and responsive composition. The existing button micro-motion remains unchanged. The service worker includes the new assets.

### Events and timing

| Moment | Trigger | Presentation |
| --- | --- | --- |
| Session / first study | A new fully answered session is saved | Actual answered/correct counts, elapsed time and only XP already awarded by the existing engine. First completed study receives its own introductory context. |
| Ordinary streak | This session supplies today's first answered activity and extends the derived streak | Previous number exits upward, new number enters, arc completes, confirmation settles; 1.2 seconds. |
| Streak milestone | New 3, 7, 14, 30, 50, 100 or 365 streak; milestone receipt absent | Shared definitions, gold arc and consistency title; 2.4 seconds, or 3.4 seconds for 100/365 with a stronger finishing rule. |
| Daily goal | This completed session crosses the existing daily answered-attempt goal | A separate gold completion line with the actual numerator and target; a check/arc stage when it is the leading event. |
| Question target | Distinct answered coverage crosses 25, 50, 100 or 150 | Highest newly crossed target; repeats of the same question do not advance coverage. |
| Journey | Fully answered unique daily sets reach 1, 7, 14, 30, 50, 100 or 118 | Names completed daily sets, never pretends set count is calendar attendance. Only currently available content can contribute. |
| Story / supported improvement | Canonical records show a newly recovered mistake, otherwise more than one complete session in the trailing seven local dates | One editorial sentence. Recovery takes priority. No predicted outcomes, unsupported accuracy trends or broad improvement claims. |

The foreground completion path in `app.finish()` consumes the runtime payload immediately after the save and opens the scene over the result page. Background timed-session expiry saves the same canonical result and receipts but discards its display payload, retaining the existing expiry notification. Loading Home, opening a result, refresh, import and ordinary navigation do not call the presenter.

Events use `session:<id>`, `streak:<local-date>`, `streak-milestone:<value>`, `goal:<local-date>`, `questions:<value>` and `journey:<value>` receipts. Only IDs/timestamps persist, not derived results or animation state. A repeated threshold receives no new receipt or repeat celebration. Multiple events share one scene; there is no forced sequence of popups.

## Accessibility and user control

The dialog has a named heading, descriptive context and immediately operable buttons. Animated numeral layers are hidden from assistive technology; the streak visual has a single final-value label. Native Escape dismissal and focus restoration are supported. Under `prefers-reduced-motion: reduce`, all scene animations/transitions/transforms are removed, the previous number is hidden, and the final number, text and completed ring remain visible. Mobile actions remain visible while the details scroll. No audio or vibration is emitted, including when the app's unrelated checkpoint sound setting is enabled.

## Verification, 5 October 2026

- **102 tests passed**: the original 84 plus 18 focused tests for ordinary/milestone/major streaks, first session, goals, same-day deduplication, midnight boundaries, precommitted attempts, refresh/import/navigation consumption, partial/abandoned sessions, persistence failure, existing record aliases, distinct question/journey thresholds, recovery insight, schema-5 migration, valid long IDs, controls and responsive/reduced-motion CSS.
- `npm run check`: passed. `npm run validate`: passed (16 datasets, 160 official keys, 160 editorial solutions, 153 source figure assets).
- The existing byte-preservation fixture's `js/state.js` hash was updated for the authorized completion-boundary change. Its assertions were retained. Domain/scoring/timer logic and question data remain unchanged; dedicated state tests additionally cover the new transaction and receipts.
- Actual app checks on isolated origin `127.0.0.1:4186`: first completed session, ordinary 1→2 streak, 6→7 milestone, daily goal, Continue to Home, Review answers, Escape dismissal, refresh with the moment open, and Home/back navigation. No repeat scene appeared after refresh/navigation.
- Light and dark responsive previews inspected at **1440×900, 768×1024, 390×844, 320×740**. Every measured dialog had equal client/scroll widths, and Continue remained in the viewport. The 390/320 daily-goal checks also ran through the real app submission flow.
- Reduced-motion QA used a clearly labelled internal fixture that applies the exact production media-query rules without changing OS settings. Computed styles confirmed no number/ring animation, no numeral transform, hidden old number and fully visible title. OS-level preference switching and other browser engines were not tested.
- The internal fixture's launch controls prepare synthetic history only on port 4186. In-memory previews use the real state boundary and renderer. The user's personal workspace on port 4177 was not used to submit test answers.

Screenshots and measured responsive results are in [product-moments-qa](product-moments-qa/layout-checks.json): [first session](product-moments-qa/first-session-light.png), [ordinary streak](product-moments-qa/ordinary-streak-light.png), [seven-day milestone](product-moments-qa/seven-day-dark.png), [daily goal on mobile](product-moments-qa/daily-goal-mobile.png), [responsive overview](product-moments-qa/responsive-overview.png).

## Intentional limits and extension points

- Completion eligibility is deliberately conservative: partial tests keep their result/history but receive no completion scene. Attempts still affect the existing canonical streak and daily goal; this layer never changes those calculations.
- Receipt-before-display favours no duplicate playback over guaranteed delivery after a crash. Background expiry is intentionally quiet beyond its existing notification.
- The first-study moment follows useful work. There is no new onboarding gate before solving.
- Add future deterministic moment rules in `moments.js` and a treatment in the renderer; keep receipts in the same Store schema. `insightCard()` accepts a small factual descriptor. There is no speculative AI, sound or haptic subsystem to maintain.
- No leagues, leaderboards, additional XP, badges, notifications, monetization or question-content changes were introduced.
