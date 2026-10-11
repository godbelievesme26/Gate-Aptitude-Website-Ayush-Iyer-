# Home: a focused study starting point

Implemented 4 October 2026. This is a presentation redesign of the existing Home route, using the established neutral/indigo tokens, system typography and native controls.

## What changed

- One main study surface contains the recommendation, available time, existing question estimate and Start/Continue action. The invitation carries the largest type; the action is the strongest accent.
- Greeting uses the existing profile name when provided, escaped as text. No weakness, forecast, rank or fabricated personalization is introduced.
- On desktop, an asymmetric invitation/action composition provides separation without nested cards. On mobile, context leads directly to the time selector and action; the recommendation reason follows.
- Goal and seven-day activity sit below the invitation. The four existing statistics form a restrained row, with a two-column layout on phones.
- Journey, review links, recent sessions and practice record use open sections and separators. All available day links remain visible. Unavailable future days are grouped under a native disclosure instead of filling the page with 102 empty squares.
- Home-only shell styling quiets the sidebar action, current navigation state, search, XP and avatar. Tablet navigation uses the existing menu at 768px and 1024px. Every original destination remains reachable.
- Empty activity and unavailable content remain honest. The unavailable state disables Start and explains why. Timed-session continuation keeps the existing deadline warning.
- CTA hover, press and keyboard focus are restrained. Reduced-motion rules suppress decorative movement. No new dependencies or assets were added.

## Implementation boundaries

`css/home.css` owns Home presentation; superseded Home rules were removed from `css/components.css`. `js/home.js` changes markup and display copy. `js/app.js` adds the Home route class and connects the existing custom-time estimate to input events. The service worker includes the new stylesheet and has a new shell cache version.

The custom budget previously placed `start-budget-custom` on a label, although the existing handler reads its `.value` and focuses it. That ID is now on the numeric input, with a visible label, the same 1–360 bounds, and the unchanged budget validator. Typing updates the existing estimate immediately. Session generation and budget calculations were not changed.

SHA-256 comparisons confirm every data file, `domain.js`, `scoring.js`, `timer.js`, `state.js` and `storage.js` remained byte-for-byte unchanged. Progress calculations, recommendation selection, question order, scoring, routes and user persistence behavior are preserved. Displayed counts and progress still use the original functions and expressions.

## Verification

- Full suite: **70 tests passed**. Added coverage for non-mutating Home rendering, progress values, resumable session, original destinations, escaped profile text and the custom-input contract. Updated obsolete visual assertions to match the new presentation.
- JavaScript check passed. Data validator passed: **16 datasets / 160 question records**.
- Live browser inspection at 1440×1000, 1024×900, 768×1024, 390×844, 375×812 and 320×740. No horizontal document overflow, measured against the document's client width, including the scrollbar gutter.
- Primary action bottom at approximately 401px on 390/375 phones and 444px on the 320px phone: visible in the first viewport.
- Light and dark themes inspected on desktop and mobile. Entire page reviewed, including recent practice and source limitations.
- Start created an eight-question session for a 17-minute custom budget. Preset 10 minutes displayed five questions. Invalid zero was rejected with the existing plain-language error. Final custom preview displayed eight questions / 17 minutes while typing.
- Continue reopened the exact same session ID. Refresh retained the saved session. A test session submitted through the normal UI appeared in recent practice; its link opened the correct result.
- All nine non-Home sidebar destinations opened successfully, as did Search. Mobile navigation opened and returned to Home.
- Keyboard focus on the primary action was visibly ringed. Original action IDs and native controls remain intact.
- Internal fixtures cover a new user, an unavailable archive, and a saved timed session. Reduced motion was verified by applying the actual production media declarations in the fixture: effective transitions were 0.01ms and arrow movement was suppressed. OS-level preference emulation was unavailable in the browser tool.
- No unexpected application console errors during normal interaction. Deliberately submitting an invalid budget produces the existing logged validation error; it was expected and surfaced to the user.

Browser interaction used a separate local origin on port 4175; existing study progress on ports 4173/4174 was not edited by these checks. The internal fixture uses in-memory state and has no Store/app import or persistence writes.

## Evidence and limitations

- `home-redesign/desktop-light.png`: final desktop first viewport.
- `home-redesign/full-light.png`: entire Home, including populated recent practice.
- `home-redesign/desktop-dark.png`: dark theme.
- `home-redesign/mobile-light.png`: 390px first viewport.
- `home-redesign/desktop-dark-resume.png` and `mobile-dark-resume.png`: saved-session state during verification.

Original limitations remain visible: source PDFs do not supply answer keys, so those attempts remain ungraded. The new visuals do not imply adaptive intelligence or independently validated learning outcomes. Paid-user perception has not been tested; the design review verifies composition and behavior, not willingness to pay.
