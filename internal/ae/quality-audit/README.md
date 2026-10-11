# Full-corpus quality audit — working evidence

The full task is **incomplete**. This directory separates the initial baseline from future repairs and post-repair verification. No canonical content, product code, figure, manual verification record, or persistence schema has been changed during this audit. The earlier verification-test isolation fix is the sole protected-file difference.

## Reconciliation and coverage

The production loader resolves **1,475 unique question IDs**: 1,315 direct AE JSON records plus 160 existing GA records. Full AE paper orders reference 1,335 questions, including 20 GA records shared with the existing GA corpus. These references must not be counted twice.

All 20 AE PDF files match the supplied original archive by SHA-256. This proves file identity, not transcription correctness. Source question counts remain independently audited year by year. The 2026, 2025, 2024 and 2023 papers each contain 65 visually checked printed questions; their current source review is recorded by ID.

`checkpoint.json` contains current per-year counts and the exact resume position. Source comparison is complete for 260 questions across 2026–2023. Subsequent years and remaining GA papers still require full source comparison. Complex student-facing visual review is also incomplete. There are currently 148 source/rendering issue entries in the source ledger, in addition to the whole-corpus automated findings; entries can overlap and must not be summed as unique defects.

## Evidence files

- `initial-automated.json`: 1,475 loaded records, 5,900 production-view invocations in JSDOM; 944 distinct visible mathematical-markup issues affecting 423 questions. This detector does **not** catch every source corruption (for example flattened exponents and matrices).
- `initial-browser-*.json`: the same corpus in four real browser views at 1440×1000 and 390×844, light and dark. Each report has 5,900 view records, with zero JavaScript exceptions. Desktop has 1,269 view records flagged; mobile has 2,323. These are flags, not unique confirmed defect counts.
- `initial-source-inventory.json` and `source-text/`: PDF hashes, archive reconciliation, extracted text and numbering candidates. Extracted text is candidate evidence only.
- `initial-source-review.jsonl`: explicit agent source-comparison observations, separate from manual verification.
- `initial-source-issues.jsonl`: source-backed individual issues with fields, evidence, safety and review status.
- `initial-key-comparison*.json`: fresh visual reading of the locally preserved key PDFs and canonical key/type/marks comparison. Use the non-superseded files. Exact numeric values and equal-endpoint ranges compare as equivalent. All 260 rows for 2026–2023 match. These results supersede earlier “NOT YET AUDITED” key substatuses in source-review events; they do not change product provenance flags. AE2023 demonstrates why a matching answer key is insufficient: Q17 has the wrong question, Q31 the wrong equations, Q36 invented absolute values, Q41 altered options, Q43 an altered vector coefficient, and Q57 incorrect source strengths.
- `initial-shared-layout-issues.json`: visually confirmed mobile exam-width defect.
- `visual/`: current asset contact sheets, original PDF page sheets and actual browser screenshots. Viewing a source sheet is not viewing the website. Internal harness controls visible at the bottom of browser screenshots are not product UI.
- `integrity-checkpoint.json`: hashes against the 1,067-file protected baseline. Original data, sources, assets, product code and user verification are unchanged.

## Superseded evidence

`initial-automated-v1-superseded.json` counted hidden exam-modal options as active options. Those false positives were removed by checking exposure; use `initial-automated.json`.

`initial-key-comparison-2024-v1-superseded.json` compared singleton numeric key rows incorrectly with equal-endpoint ranges, yielding seven false mismatches. The corrected comparison is `initial-key-comparison-2024.json`; all rows pass. Canonical answers were not changed.

## Protection and checks

The baseline ZIP preserves content/code before repairs; figure files and PDFs are hashed. Back up each old figure before changing it. Preserve the existing forensic review states and user verification trail; this audit does not write them. Browser harness sessions are memory-only and do not use local storage or write APIs.

Baseline checks: 164 tests passed; JavaScript syntax check and content validation passed. Those results do not establish source fidelity. Run the complete required checks again after repairs. The audit scripts refuse to overwrite initial evidence unless a specific superseded version is retained.

## Next work

Resume at **AE2022 Q1**. Complete the remaining initial source and complex-rendering baseline before any canonical repair. Then repair verified defects, log old/new values and source evidence, and perform the required independent full-corpus post-repair audit. Repair ledger and final unresolved list are not yet final deliverables.
