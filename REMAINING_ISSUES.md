# GATE PYQ Platform — Remaining Issues & Operational Roadmaps

**Date**: October 11, 2026  
**Status**: Stage B Stabilization Complete (0 blocking software defects, 217/217 automated tests passing)  
**Classification**: Categorized by Severity Priority (P0, P1, P2, P3)

---

## 1. Issue Classification Overview

All critical functional, architectural, security, accessibility, and offline defects identified in Stage A and Stage B audits have been resolved and verified with automated regression tests.

The items below represent operational verification workflows, content processing tasks, and future product roadmap enhancements.

---

## 2. Prioritized Register of Issues & Roadmaps

### P0 — Critical (0 Issues)
- **None**. Zero blocking defects remain in the codebase. All 217 automated tests pass, syntax checks pass, and data validation passes.

---

### P1 — High (Operational Verification Queue)
- **Issue ID**: `P1-01`
- **Component**: Archival Question Verification (`internal/ae/ocr_queue.json`)
- **Description**: 425 questions from older Aerospace Engineering papers (2007–2014) originate from scanned raster PDFs published by organizing IITs. Furthermore, 110 figure cases remain in the human review queue.
- **Strict Policy**: Automated OCR or vision AI must **never** automatically overwrite canonical question records. Forensic comparison by a subject expert against the original source PDF is strictly required.
- **Mitigation & Tooling**: The internal Forensic Review Workstation is encapsulated in `scripts/serve-forensic.mjs` (runs on port 3001, isolated from the public server on port 3000). 10 pilot questions (`gate-2026-ae-ga-01` to `gate-2026-ae-ga-10`) are verified in `data/ae/verification.json`.
- **Recommended Action**: Continue human forensic review of unresolved items in controlled batches of 20.

---

### P2 — Medium (Discipline & Platform Expansion)
- **Issue ID**: `P2-01`
- **Component**: Multi-Branch Question Ingestion
- **Description**: The platform currently supports General Aptitude (all branches) and Aerospace Engineering (AE). High demand exists for Computer Science (CS), Mechanical Engineering (ME), Electrical Engineering (EE), Electronics & Communication (EC), and Civil Engineering (CE).
- **Architectural Readiness**:
  - The flat-file schema (`data/{branch}/manifest.json`, `data/{branch}/{year}.json`) is branch-agnostic.
  - The 16 General Aptitude sets (`data/day01.json`–`data/day16.json`) are universally shared across all branches without duplication.
  - The scoring engine (`js/scoring.js`) and mathematical notation tokenizer (`js/question-content.js`) require zero modification.
- **Recommended Action**: Ingest Computer Science (CS) 2026–2015 as the first expansion branch using the existing flat-file schema.

---

### P3 — Low (Enhancements & Non-Functional Polish)
- **Issue ID**: `P3-01`
- **Component**: Custom PWA Install Prompt Banner
- **Description**: PWA manifest (`manifest.webmanifest`) and service worker (`sw.js`) are fully functional with offline caching (`gate-workspace-v31`). However, the install prompt relies on browser default UI or settings view button.
- **Recommended Action**: Add a floating install banner on first visit when the browser emits `beforeinstallprompt`.

- **Issue ID**: `P3-02`
- **Component**: PDF Scorecard Export
- **Description**: After completing a timed mock exam, students can review their results in the browser at `#/result/<id>`, but cannot currently export a formatted printable PDF score report.
- **Recommended Action**: Implement a client-side print stylesheet (`@media print`) or SVG/HTML canvas export for student scorecards.

---

## 3. Register of Verified Safe Non-Issues

The following behaviors were audited and verified to be safe and intentional:
1. **Public Server Returns 403 for Verification Mutations**: By design. The public student server (`scripts/serve.mjs`) must be read-only to prevent unauthorized student manipulation of official verified markers.
2. **Offline Local Storage vs Cloud DB**: By design. Storing student progress in browser `localStorage` guarantees total user privacy, zero subscription/database hosting overhead, and instantaneous offline capability.
3. **Zero CDN Math Rendering**: By design. Replacing external MathJax/KaTeX CDNs with client-side AST tokenization guarantees 100% offline uptime and eliminates third-party security vulnerabilities.
