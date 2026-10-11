# Application state model

`ApplicationState` in `js/state.js` is the application-facing state boundary. `Store` in `js/storage.js` is the only component that reads or writes browser storage. UI code may read state for rendering, but persistent changes are committed through `ApplicationState` operations or its general `updateProgress`/`save` transaction boundary.

## Persistent state

Persistent state is stored under `gate-preparation-v1`, validated against the latest schema, migrated when necessary, and included in backup exports.

- User identity and preferences: profile, settings, planner.
- Practice workspace: saved drafts, pending answers, accumulated draft timing, review marks and current session position.
- Session history: canonical completed-session metadata and aggregate result summaries.
- Attempt history: append-only canonical question-attempt events.
- User material: bookmarks, notes, notebooks and flashcards.
- Supporting progress: blueprints, locally recorded source reports and XP award events.

Named writes for drafts, completed sessions and attempts, bookmarks, notes, and quiz-progress clearing live on `ApplicationState`. Session completion writes the completed session and its attempt events in one persistence transaction.

## Temporary state

Temporary state exists only for the current page lifetime and is not exported or restored after refresh.

- Loaded content archive reference. The underlying question JSON remains source content rather than user progress.
- Active session ID and live `QuizTimer` instance. The active session resolves to its persistent draft instead of copying it.
- Flashcard reveal state, offline-ready status, pending install event, periodic-save counter and cross-tab conflict flag.
- Audio context, current route, dialog state, DOM state and transient toast messages.

## Derived state

Derived values are calculated from persistent state and source content when needed. They are not separate writable progress records.

- Active session, resolved from the active ID and saved draft map.
- Completed days, streaks, XP totals, levels, question status, mastery and recommendations.
- Question coverage, daily counts, accuracy views and other existing display summaries.
- Filtered question lists, due-card lists and session result rows reconstructed from attempt events.

On refresh, a new `Store` instance reloads persistent state, while temporary state returns to defaults and derived values are recalculated.
