# AE2026 foundational corpus: implementation and continuation check

Checked 2026-10-10 against the supplied AE2026-only brief.

## Scope and existing work

The requested AE2026 implementation already exists. This continuation reused it instead of reimporting records or replacing the GA architecture. No product UI, canonical question content, answers, scoring, stable IDs, or learner-state schema was changed.

Important scope discrepancy: AE2007–AE2025 were already imported in this checkout before this continuation. They remain untouched. It would be inaccurate to report those years as not imported or to relabel their manifest entries as such. No additional historical ingestion was performed.

## Canonical architecture reused

- `js/corpus.js`: year-configurable paper model, explicit section and question ordering, reference resolution, MCQ/MSQ/NAT validation, marking configuration, common-data and linked-answer groups, structured blocks and asset lineage. `generatePaperSession` uses explicit IDs rather than archive filtering.
- `data/ae/2026.json`: paper metadata, 55 technical records, and references to the 10 existing GA records. GA identities and original records are reused.
- `data/ae/manifest.json`: paper inventory, sections, types, answers, assets and ingestion/verification status.
- `js/loader.js`: resolves AE papers into the existing archive without duplicating referenced GA records.
- `js/question-content.js`: shared rendering of text, supported mathematical notation, tables, question figures, option figures and shared group context. Student-facing content does not fall back to full PDF pages.
- Existing views, domain/session generation, scoring, revision engine, `ApplicationState` and `Store`: reused for bank/detail/practice/results/review and persisted attempts, sessions, notes and bookmarks.
- `internal/ae/AE2026-lineage.json`: internal question/page/crop provenance and the previous source review record. Source PDFs stay internal.

The notation renderer implements a bounded grammar, not arbitrary LaTeX. Future ingestion must target supported structured notation or explicitly extend and test it.

## Exact AE2026 inventory

| Measure | Count |
| --- | ---: |
| Questions, uniquely numbered 1–65 | 65 |
| GA questions / marks | 10 / 15 |
| AE questions / marks | 55 / 85 |
| Total marks | 100 |
| Duration in minutes | 180 |
| MCQ / MSQ / NAT | 29 / 14 / 22 |
| Distinct figure assets, including reused GA assets | 25 |
| Technical figure assets | 15 |
| Option figures, included in the asset total | 4 |
| Structured tables | 3 |
| Official key rows / graded answers / marks-to-all rulings | 65 / 63 / 2 |
| Common-data / linked-answer groups in this paper | 0 / 0 |

Technical editorial solutions are not supplied and have not been invented. Existing GA solutions remain available.

## Verification evidence and limits

The internal source PDF matches `AE/AE2026.pdf` in the supplied archive byte-for-byte by SHA-256:
`32bb62a076b6312fa20d0ccfb9fb1cc5e14c6293c17579271d00dd6724066e02`.

The existing lineage record documents the prior 2026-10-06 review of all 39 source pages and both key pages. This continuation checked source identity and reran automated validation; it did not repeat a complete 65-question visual comparison or a fresh browser visual audit. Existing verification labels were not changed. Automated validation alone is not evidence of exact visual/source fidelity.

`tests/ae-corpus.test.js` covers totals, numbering, sections, marks, types, key values/rulings, asset resolution, GA preservation, canonical rendering without PDF fallback, scoring, explicit session order, and persistence/revision round trips. It also exercises synthetic historical configurations without importing historical content.

Final commands after the test-isolation repair:

- `npm test`: 164 passed, 0 failed.
- `npm run check`: JavaScript syntax passed.
- `npm run validate`: passed, including the AE2026 inventory above and the existing GA corpus.

No AE2026 structural or integration failure was found by these checks. This is not a new full source-fidelity certification.

## Changes made in this continuation

- `tests/verification.test.js`: moved API verification tests into an isolated temporary content root; fixture reads use that root for review records. Cleanup asserts that both real review files remain byte-identical. Tests no longer temporarily replace the user's verification records.
- `docs/AE2026_IMPLEMENTATION.md`: this report.
- Validation commands regenerated their existing reports, `docs/ae-validation-report.json` and `docs/validation-report.json`.

The initial test run consumed an existing `data/ae/verification.json.tmp` while testing the live review-file writer. Its original bytes were restored from the hash-checked pre-audit ZIP snapshot before the isolated tests were rerun. The authoritative `verification.json` remained identical to the protected baseline. Canonical data, application JavaScript and CSS were checked against that baseline after the repair.
