# GATE Aerospace 2007-2026 Forensic Audit Report

## Executive Summary
- **Total Questions:** 1315
- **PASS:** 161
- **FAIL:** 729
- **UNVERIFIABLE:** 425
- **REQUIRES HUMAN REVIEW:** 0

## Per-Year Status Breakdown
- **AE2026:** 55 PASS, 0 FAIL, 0 UNVERIFIABLE
- **AE2025:** 44 PASS, 11 FAIL, 0 UNVERIFIABLE
- **AE2024:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2023:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2022:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2021:** 0 PASS, 0 FAIL, 65 UNVERIFIABLE
- **AE2020:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2019:** 0 PASS, 0 FAIL, 65 UNVERIFIABLE
- **AE2018:** 62 PASS, 3 FAIL, 0 UNVERIFIABLE
- **AE2017:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2016:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2015:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2014:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2013:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2012:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2011:** 0 PASS, 65 FAIL, 0 UNVERIFIABLE
- **AE2010:** 0 PASS, 0 FAIL, 65 UNVERIFIABLE
- **AE2009:** 0 PASS, 0 FAIL, 60 UNVERIFIABLE
- **AE2008:** 0 PASS, 0 FAIL, 85 UNVERIFIABLE
- **AE2007:** 0 PASS, 0 FAIL, 85 UNVERIFIABLE

## Categorical Failure Analysis
### 1. Figure Margin Failures (130)
These questions have tight crops or lack bounding boxes entirely. They must be re-rendered via the safe-margin algorithm.
Sample IDs: gate-2025-ae-ae-20, gate-2025-ae-ae-27, gate-2025-ae-ae-29, gate-2025-ae-ae-30, gate-2025-ae-ae-49 ...

### 2. Answer Provenance Failures (715)
These questions were tagged official key verified but lack a valid PDF source lineage (nswerSource.url).
Sample IDs: gate-2024-ae-ga-01, gate-2024-ae-ga-02, gate-2024-ae-ga-03, gate-2024-ae-ga-04, gate-2024-ae-ga-05 ...

### 3. Numbering Discrepancies (0)
The JSON numbering differs from the physical printed PDF max question number.

### 4. Image-Only / OCR-Unverifiable (425)
These questions belong to scanned PDFs (e.g., AE2007, AE2008, AE2009, AE2010, AE2019, AE2021). The textual JSON content cannot be programmatically validated without OCR.
Sample IDs: gate-2021-ae-ga-01, gate-2021-ae-ga-02, gate-2021-ae-ga-03, gate-2021-ae-ga-04, gate-2021-ae-ga-05 ...

## Recommended Repair Categories
1. **Mass Demote Provenance:** Any question lacking a .pdf URL should have gradingStatus changed to provided answer key.
2. **Run Global Safe-Margins:** Apply the collision-aware safe_margins_algo.py to all remaining years (2025-2011).
3. **Manual OCR Verification Pass:** Implement a UI tool or human-review workflow for the 425 UNVERIFIABLE scanned questions.

## Status Conclusion
**AUDITED - REPAIR REQUIRED**