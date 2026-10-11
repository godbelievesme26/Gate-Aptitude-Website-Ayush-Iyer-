# Question-solving redesign

Implemented and verified on 4 October 2026.

## Design decisions

- One central study surface holds the authentic source paper, answer selection, and Continue/Submit action. The old nested support card has been removed.
- Question number and position lead a compact header. Source provenance and marking are readable supporting text. Timers sit in an open side area on wide desktop and follow the answer area on tablet/mobile.
- Answer controls preserve the A–D mapping, numeric input, and multiple-selection semantics. Selected answers use a border, tone, the word “Selected,” and a checkmark. Focus remains on the answer after a rerender.
- The primary action is separated from Clear, review, and Save tools. On smaller screens, source → answers → action → support remains the reading order.
- The original paper image is unchanged. Desktop reading width is capped at 720px. On phones, a bounded 600px-wide paper viewport retains readable text and scrolls internally; the page itself does not overflow. The existing enlarge dialog provides a larger source view. This deliberate document-reader tradeoff is necessary because the authentic source is a fixed-layout image, not reflowable text.
- Keyboard arrows scroll the source region while it has focus; existing question shortcuts continue elsewhere. Question transitions focus the new heading and use a brief 180ms appearance with reduced-motion support.
- Recorded correct/incorrect/ungraded/blank feedback uses text and small semantic markers. No grading is revealed during an active question. The supplied archive remains ungraded because it has no verified answer keys.
- Quiz styling lives in `css/quiz.css`, loaded after shared tokens/components. Only the quiz shell is visually subdued; all navigation destinations remain available, including through the menu on tablet.

## Verification

| Check | Result |
| --- | --- |
| Automated suite | 68/68 passed, including added source/action/answer mapping and MSQ/NAT presentation contracts |
| Syntax and archive validation | Passed; 16 source sets / 160 question records |
| Content and engine integrity | SHA-256 comparison confirmed data files plus domain, timer, scoring, state, and storage modules were unchanged |
| Desktop | Inspected at 1440 × 1000 in both themes |
| Tablet | Inspected at 1024 × 900 and 768 × 1024; source remains before supporting status; tablet navigation is reachable |
| Mobile | Inspected at 390 × 844 and 320 × 740; no document-width overflow; standard answer targets are at least 60px tall |
| Selected / focus | Pointer and keyboard selection inspected; focus remains on the selected answer; text and checkmark supplement color |
| Session flow | Continue, previous, keyboard submission, confirmation, result, and refresh exercised in an isolated browser origin on port 4174 |
| Persistence smoke test | Selected answer and question position survived refresh; recorded result stayed at 12 feedback rows after refresh |
| Source reader | Original image preserved, region scrolls with keyboard, enlarge opens, Done returns focus to its trigger |
| Correct / incorrect / ungraded / blank | Actual result renderer inspected using clearly marked in-memory fixture data; no synthetic keys were written to the archive or user storage |
| Disabled / busy / countdown display | Inspected via internal visual fixtures using the production quiz renderer |
| Reduced motion | Real reduced-motion CSS declarations applied in the fixture and computed styles checked: question animation is none; control/spinner motion is effectively zero. OS preference emulation was unavailable in the browser API. |
| Browser errors | No JavaScript errors observed in the app or fixture console |

Contrast calculations for the selected control palette: light primary 7.69:1, dark primary 8.93:1, light selected text 6.77:1, dark selected text 6.57:1. Normal option borders are 3.30:1 on the light surface and 3.83:1 on the dark surface. These are targeted component checks, not a full application accessibility certification.

## Internal visual review

`tests/visual/solving.html` is a developer-only fixture page. It uses production render functions and CSS with in-memory data, reads/writes no browser storage, and is not linked from the app. It includes a reduced-motion simulation because browser tooling cannot change the OS media preference. Synthetic grading appears only in this harness.

Review images:

- [Desktop, light theme](solving-preview/desktop-light.jpg)
- [Desktop, dark theme](solving-preview/desktop-dark.jpg)
- [Mobile selection and primary action](solving-preview/mobile-selection.jpg)
- [Recorded feedback fixture](solving-preview/feedback-fixture.jpg)

The remaining visual constraint is the source papers themselves: their table lines, whitespace, and watermark are part of the supplied image. They are preserved faithfully. A future verified accessible transcription could improve reflow, but it is outside this visual redesign.
