# GATE PYQ Platform — Remaining Issues & Future Roadmaps

**Date**: October 11, 2026  
**Status**: Stage B Stabilization Complete (0 blocking defects, 217/217 tests passing)  
**Classification**: Operational Milestones & Future Expansion Tasks

---

## 1. Overview

All critical functional, architectural, security, accessibility, and offline defects identified in audits have been resolved in Stage A and Stage B.

The items listed below represent **operational workflows, planned content forensic verification, and future product roadmap enhancements** rather than unresolved software defects.

---

## 2. Priority Operational Tracks

### 2.1 Human Forensic Source Review of Scanned Papers (2007–2014)
- **Context**: 425 questions from older GATE Aerospace papers (2007 through 2014) originate from low-resolution raster scanned PDFs published by organizing IITs.
- **Strict Policy**: Automated OCR or vision AI must **never** automatically overwrite canonical question records. Forensic comparison by a subject expert against the original source PDF is strictly required.
- **Current State**:
  - The review queue is maintained in `internal/ae/ocr_queue.json`.
  - The internal Forensic Review Workstation is encapsulated in `scripts/serve-forensic.mjs` (runs on port 3001, isolated from the student server on port 3000).
  - 10 pilot questions (`gate-2026-ae-ga-01` to `gate-2026-ae-ga-10`) are verified in `data/ae/verification.json`.
  - 425 scanned items + 110 figure items remain in the human review queue.
- **Next Action**: Execute human forensic verification in controlled batches of 20 using the Forensic Review Workstation.

### 2.2 Corpus Expansion to Additional GATE Branches
- **Context**: The platform currently supports General Aptitude (all branches) and Aerospace Engineering (AE).
- **Target Branches**:
  - Computer Science & Information Technology (CS / IT)
  - Mechanical Engineering (ME)
  - Electrical Engineering (EE)
  - Electronics & Communication Engineering (EC)
  - Civil Engineering (CE)
- **Architectural Readiness**:
  - The flat-file schema (`data/{branch}/manifest.json`, `data/{branch}/{year}.json`) is branch-agnostic.
  - The 16 General Aptitude sets (`data/day01.json`–`data/day16.json`) are universally shared across all branches without duplication.
  - The scoring engine (`js/scoring.js`) and mathematical notation tokenizer (`js/question-content.js`) require zero modification.

### 2.3 Progressive Web App (PWA) Install Prompt Enhancements
- **Current State**: `manifest.webmanifest` and `sw.js` are fully configured with complete offline caching under `gate-workspace-v31`.
- **Potential Enhancement**: Add a prominent custom in-app install banner triggered when the browser emits `beforeinstallprompt` (currently handled on the settings screen).

### 2.4 Advanced Student Analytics & Printable Reports
- **Current State**: Analytics view computes accuracy, time per question, mastery, streaks, and historical coverage across all 20 years.
- **Future Enhancement**: Add a printable / PDF exam score card generation feature for students simulating full GATE mock exams.

---

## 3. Register of Safe Non-Issues

The following behaviors were audited and verified to be safe and intentional:
1. **Public Server Returns 403 for Verification Mutations**: By design. The public student server (`scripts/serve.mjs`) must be read-only to prevent unauthorized student manipulation of official verified markers.
2. **Offline Local Storage vs Cloud DB**: By design. Storing student progress in browser `localStorage` guarantees total user privacy, zero subscription/database hosting overhead, and instantaneous offline capability.
3. **Zero CDN Math Rendering**: By design. Replacing external MathJax/KaTeX CDNs with client-side AST tokenization guarantees 100% offline uptime and eliminates third-party security vulnerabilities.
