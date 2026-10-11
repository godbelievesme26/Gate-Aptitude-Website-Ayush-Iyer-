# Premium visual direction and system plan

**Status:** Design specification for the next implementation phase, 4 October 2026. The existing `css/system.css` and `css/components.css` are the starting implementation. Values below are a proposed contract to test in context; this document does not redesign screens or change application behavior.

## Product character

The interface should feel like a precise academic instrument with the ease of modern consumer software. Source questions and solving should carry the visual identity. Typography, reading comfort, clear decisions, and responsive composition should communicate value. Trust comes from honest source labeling, reliable controls, and transparent limitations, not from animated rewards or decorative effects.

Three design principles govern every route:

1. **One task at a time.** The strongest type, surface, and accent belong to the next useful study action or the current question. Stats and tools remain accessible but quieter.
2. **Space is structure.** Use open canvas and separation between ideas before adding a border. A card must signal a contained interaction, a useful grouping, or a distinct state.
3. **Precision earns trust.** Keep source provenance, ungraded states, timing, and saved responses visually legible. Every control state should be obvious by more than color alone.

## Typography and font strategy

Use local/system fonts initially. Avoid a network font dependency during the foundation pass; review any candidate replacement later for licensing, offline availability, math symbols, variable weights, and rendering on Windows/Android/iOS.

| Role | Current starting token | Proposed use and guardrail |
| --- | --- | --- |
| Display / invitation | `--font-display: Georgia`, `--text-display: 1.75–2rem`, 400 | Use sparingly for a meaningful invitation or question-session heading, never for dense data. Tracking around `-0.02em`, line height 1.25–1.35. |
| Page title | `--text-page: 2–2.5rem`, Georgia 400 | One `h1` per route. Keep to 1–2 lines at common widths; 1.15–1.2 line height. |
| Section title | `--text-section: 1.125rem`, Segoe UI 600 | Organize content without competing with the page or question. 1.35 line height. |
| Question reading | 1–1.125rem target for any verified HTML question text | Favor 1.55–1.7 line height and a roughly 60–75 character measure. Original paper crops remain unaltered. |
| Body | `--text-body: 1rem`, Segoe UI 400 | 1.55–1.65 line height. Default for explanatory text and personal notes. |
| Secondary | `--text-sm: .8125rem` today; target at least .875rem when essential | 1.45–1.55 line height. Do not let source, timing, state, or action guidance become miniature metadata. |
| Eyebrow / data label | `--text-xs: .75rem`, Segoe UI 600 | Short, rare, and letterspaced modestly. Avoid all-caps labels on every section. |
| Stat / timer | `--text-stat: 1.75rem`, `--text-timer: 1.5rem` | Tabular numerals; size depends on importance. Timing must remain readable without becoming the hero in practice mode. |
| Control | `--text-control: .875rem`, Segoe UI 600 | 44px minimum target on standard controls; stable label and sufficient contrast. |

The serif/sans pairing should create a meaningful change in cadence, not make every heading ornamental. Use hierarchy, measure, and line height before adding weight. Avoid faux-bold paper text: the original PDF crop is evidence and must stay faithful.

## Color roles

Preserve the current neutral/indigo family as a defensible base. Audit contrast and tune in real screens before changing values globally.

| Role | Light starting point | Dark starting point | Usage |
| --- | --- | --- | --- |
| Canvas | `#f4f5f7` | `#15171c` | Open page ground. |
| Main surface | `#ffffff` | `#1d2027` | Contained interaction or reading support. |
| Subtle/elevated neutral | `#fafbfc` | `#242832` | Quiet grouping; dark theme needs visible separation without glow. |
| Primary text | `#202636` | `#edf0f5` | Questions, headings, control labels. |
| Muted text | `#626c7d` | `#abb3c2` | Secondary content, never the sole indicator of important status. |
| Border | `#dce1e9` | `#363b47` | Delimit a real boundary; avoid full boxes by default. |
| Accent | `#4148aa` | `#afb3ff` | Main action, current selection, essential links. |
| Accent soft | `#eef0fb` | `#2c304b` | Selected/supporting emphasis, not a general decorative fill. |
| Success | `#226c55` | `#79cdb0` | Verified correct/completion only. |
| Warning | `#875d17` | `#ddb56b` | Caution or missing information, paired with text. |
| Error | `#a23f46` | `#ef9299` | Destructive/error states, paired with text. |
| Focus | `#5961d7` | `#c4c7ff` | Visible 3px ring with 3px offset. |

Separate semantic aliases for action, selection, focus, progress, and status even if values match at first. Use no accent for decorative charts or arbitrary badges. Test WCAG contrast for actual text/background pairs and component states after implementation; token values alone do not prove contrast.

## Layout, space, shape, and depth

- **Spacing scale:** retain `4, 8, 12, 16, 20, 24, 32, 40, 48, 64px`. Use 4–8px within a label/control, 12–16px between related content, 24–32px between section ideas, and 40–64px for major page breaks. Treat these as relationships rather than a command to fill whitespace.
- **Gutters:** current 40px desktop / 28px medium / 18px compact are sound starting points. Cap reading measure independently of the content grid; data tables can use wider space.
- **Radius:** 4px for compact markers, 6px for controls, 9px for interactive surfaces, 12px for dialogs. Do not increase radii simply to signal premium quality. Paper-source frames may have a smaller radius to retain document character.
- **Elevation:** one barely visible panel shadow (`--shadow-panel`) for rare raised interactions; one stronger overlay shadow (`--shadow-overlay`) for dialogs. A border, tonal difference, and shadow should not all be applied by default.

### Practical surface hierarchy

| Level | Visual treatment | Use | Avoid |
| --- | --- | --- | --- |
| **Open canvas** | No card, no border | Page titles, brief guidance, stats, section headings, chronological rows, source notes | Wrapping information only because it exists. |
| **Subtle grouping** | Neutral tonal field **or** one quiet divider | Goals, contextual status, grouped filters, compact review summaries | A full nested card inside another full card. |
| **Primary interactive surface** | Deliberate edge/contrast, medium radius, clear focus and state | Recommendation decision, question/answer interaction, modal decision | Multiple equally strong surfaces in one viewport. |

The existing `.surface-plain`, `.surface-subtle`, `.surface-elevated`, `.surface-bordered`, and `.surface-emphasis` utilities remain available. They are implementation modifiers within the three-level model, not five equal visual priorities. Existing `.panel` should be retired by route, after screenshots and behavior checks, rather than deleted globally.

## Reusable component contract

| Component | Current implementation | Future redesign requirement |
| --- | --- | --- |
| App shell and navigation | `.sidebar`, `.topbar`, grouped `navGroups`, mobile menu in `app.js` | Keep all routes; reduce permanent chrome near solving; maintain active and focus states and a clear Start/Continue path. |
| Page heading | `head()` in `ui.js`, `.page-head` | Consistent title/subtitle spacing and responsive wrap; don't repeat metadata already in the body. |
| Action/links | `button()` and `link()` helpers, generic button CSS | Primary, secondary, ghost, destructive, icon, selected, disabled, pressed, and busy states with usage rules; preserve action IDs. |
| Inputs/filter bar | Native controls in `views.js`, `.filters`, `.form-grid` | Readable labels, equal heights, error/help positioning, clear focus, distinct compact layout. |
| Surface/row | `.panel`, `.question-row`, `.row`, `.home-section` | Decide canvas/divider/interactive surface by purpose. Favor rows for scan-heavy banks and histories. |
| Source question | `sourceQuestion()`, `.source-frame`, `.question-image` | Protect image fidelity, maintain zoom, and offer comfortable width on mobile. Do not replace verified source with unverified transcript. |
| Answer controls | Quiz `fieldset`, `.option`, selected state | Make selected/hover/focus states unambiguous; keep the true choice/answer mapping and keyboard behavior. |
| Timing/status | `.quiz-support`, `.timing`, `.status-summary`, `.checkpoint` | Practice time is useful context; test countdown remains urgent only when genuinely near expiry. Keep support subordinate to the question. |
| Feedback/notice/empty | `.feedback-row`, `.notice`, `empty()` | Message → implication → next action. Avoid generic blank centered panels; use semantic state and plain language. |
| Dialog/toast/loading | `modal()`, `toast()`, `.loading` | Stable focus and reduced-motion behavior; avoid delayed task completion. |

## Interaction and motion

- Preserve existing 120ms control and 180ms view tokens as maximum starting points. Use opacity/color/border/position changes to show causality; avoid bounce, large scale, blur, or spatial movement over roughly 6px.
- Hover communicates clickability; press confirms activation; selected state persists without relying on hover; success animation is brief and never necessary to understand the result; loading indicates waiting without pretending progress.
- Question transitions should convey continuity only after the next question is ready. Animation must never postpone answer selection or the next action.
- Respect `prefers-reduced-motion` by eliminating nonessential animations and smooth scrolling. Check keyboard focus and timer updates during motion testing.

## Responsive principles

- **Desktop:** navigation can remain present, while the central solving area has a controlled reading width. Use a supporting column only when its contents help the current decision.
- **Tablet:** treat 681–900px as its own layout. A narrower persistent sidebar plus a two-column quiz may crowd the question; validate both orientation and short heights. Do not automatically move status above source material.
- **Mobile:** order the task as question → answer → primary action → timing/navigation support. Keep persistent controls compact and targetable. Use scroll, disclosure, or a sticky action only where it improves the real solving flow. Long source images need deliberate zoom affordance and no horizontal document overflow.
- At 200% zoom and narrow widths, labels, actions, and source images must remain readable and reachable. Do not shrink text to preserve a desktop grid.

## Recommended redesign order

1. **Visual verification and component pilot:** capture active quiz, keyed/ungraded result fixtures, light theme, tablet, and compact viewport. Establish contrast and keyboard baselines. Choose one question interaction to prototype using the three-level surface model.
2. **Question experience:** source reading width, answer control composition, Continue/Submit hierarchy, timing support, keyboard/focus, and question transition. Verify question and scoring behavior stay unchanged.
3. **Question detail and bank:** move scan-heavy results toward refined rows; organize action clusters around the source; simplify nested panels.
4. **Daily sets and review:** establish reusable list, progress, saved-state, and empty-state patterns.
5. **Home refinement:** align recommendation and progress support with the approved question language; remove remaining dashboard density. Keep the existing recommendation logic.
6. **Analytics, planner, history, settings:** apply the system to dense information and forms after the core study patterns are proven.
7. **System consolidation:** remove superseded CSS declarations and inline visual values incrementally. Run route tests, keyboard checks, both themes, reduced motion, and desktop/tablet/mobile screenshots before deleting legacy styles.

## Approval criteria for the next visual implementation

A redesign is successful when a student can identify the current question and next action immediately, read for a long session without tiny support text or excess borders, recognize selected and feedback states without color alone, and reach every existing destination. Both themes and mobile must remain clear. Visual novelty, more animation, or more rounded containers are not success criteria.
