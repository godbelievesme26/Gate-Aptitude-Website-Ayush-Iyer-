# Home colour refinement

Implemented 5 October 2026. This pass preserves the existing Home layout and makes colour identify study actions, progress and streaks consistently across themes.

## Palette and implementation

| Role | Light | Dark |
| --- | --- | --- |
| Canvas | Cool blue neutral `#edf0f8` | Neutral charcoal `#17191f` |
| Sidebar | `#f7f8fc` | `#1d2029` |
| Active navigation | Indigo ink on `#e2e4f6` | Lavender ink on `#30334e` |
| Study hero | Deep indigo `#27294f` | Deep indigo `#292d50` |
| Hero action region | Tonal indigo `#32365c` | Tonal indigo `#333a61` |
| Primary action | Lavender `#bcbcff`, dark ink | Same |
| Goal and activity | Gold `#886017` on warm `#f6f1e4` | Gold `#e0ba70` on neutral `#25252a` |
| Streak | Clay orange `#a74720` | Warm orange `#f0a477` |

Home tokens are centralized in `css/system.css`; `css/home.css` consumes them. Other screens retain their global palette. The four existing metrics remain inline, with small indigo, blue and gold dots and a restrained outline flame beside the streak number. The flame is hidden from assistive technology; the adjacent number and “day streak” label convey its meaning. No animation was added.

`js/home.js` changes only presentation classes and the streak markup. The Home sections, actions, calculations and destinations are retained.

## Before and after

The earlier light theme used a warm grey canvas, white sidebar and nearly white goal section. The new cool canvas separates the cream progress band, while indigo identifies the current destination and study action. In dark mode, supporting surfaces remain neutral. Both themes now connect goal completion and weekly activity through gold, with orange reserved for the streak. No new cards, imagery or gradients were added.

- [Light before](home-colour-pass/before-light.png) / [light after](home-colour-pass/after-light.png)
- [Dark before](home-colour-pass/before-dark.png) / [dark after](home-colour-pass/after-dark.png)

## Verification

- Inspected both themes at 1440×900, 1024×900, 768×1024, 390×844, 375×812 and 320×740. All twelve viewport checks report document width equal to available width. Existing mobile stacking is preserved; long labels can wrap naturally at narrow sizes.
- Also inspected the in-memory new-user fixture, including the budget selector, in light and dark at 320px. This fixture does not write user progress. Its native time selector is tight at this width; its dimensions and behaviour were not changed in this colour-only pass.
- Measured 26 contrast pairs per theme using rendered CSS tokens: body/muted text, hero text, CTA normal/hover, navigation, goal/activity, streak, metric accents, input boundaries and focus rings. All 52 pass their selected thresholds. Lowest sampled text ratio: **4.65:1** (threshold 4.5:1). Lowest sampled non-text ratio: **3.50:1** (threshold 3:1). The activity checkmark uses a dedicated ink token after its initial light-theme contrast failed. These sampled checks are not a whole-application accessibility certification.
- `npm test`: **84 passed**, zero failures.
- `npm run check`: passed.
- `npm run validate`: passed — 16 sets, 160 question records with official keys and editorial solutions, 153 figure assets.
- Hash comparison against the pre-edit snapshot confirms protected data, scoring, state, persistence, timer, recommendation/session and route files are unchanged.
- No browser warnings or errors were reported during final inspection. Browser theme restored to light; no study action was executed during this pass.

Evidence: [viewport measurements](home-colour-pass/browser-checks.json), [contrast measurements](home-colour-pass/contrast.json), [rendered tokens](home-colour-pass/rendered-tokens.json), [protected-file snapshot](home-colour-pass/preservation.json). Full-page captures for all twelve combinations are in `home-colour-pass/`. Viewport captures above are the preferred before/after evidence; the browser's full-page capture can omit the scrollbar strip at the right edge.
