# AE2025 Ingestion Plan

## Overview
This document outlines the standard operating procedure for ingesting the GATE 2025 Aerospace Engineering (AE) PYQ corpus into the Study OS. The architecture successfully supports `data/ae/2026.json`, meaning the application state, timer, UI, CBT exam mode, and palette logic are already perfectly aligned for AE papers. Ingestion is purely a data-pipeline task.

## Prerequisites
1. **Raw Paper PDF**: Ensure `Aptitude Sets/2025/AE (2).pdf` is available.
2. **Official Key PDF**: Download the official GATE 2025 Aerospace Answer Key.

## Phase 1: Data Extraction & Provenance (internal/ae/)
1. **Lineage File (`internal/ae/AE2025-lineage.json`)**
   - Run PyMuPDF (or equivalent) to determine page dimensions and bounding boxes for all 65 questions.
   - Output structured JSON mapping each question (1 to 65) to its exact location in the PDF.
2. **Key Extraction (`internal/ae/AE2025-key.json`)**
   - Transcribe the official key.
   - Format: `[ { "q": 1, "type": "MCQ", "section": "GA", "key": "A", "marks": 1 }, ... ]`
   - Handle NAT ranges (e.g. `2.5:2.7`) and MTA (Marks to All) explicitly.

## Phase 2: Content Transcription (`scripts/ae2025-transcriptions.json`)
1. **Manual or LLM Transcription**
   - Extract raw text for the question stem and all options.
   - Convert inline math to standard notation layout using the Study OS format `$$ math $$` or plain unicode.
   - Identify questions requiring figure assets.

## Phase 3: Figure Extraction
1. **Cropping Pipeline**
   - Create `scripts/verify-2025-figures.py` (similar to 2026).
   - Use the lineage bounding boxes combined with manual offsets to crop charts, diagrams, and complex matrices.
   - Save directly to `figures/ae/2025/`.

## Phase 4: Compilation (`scripts/prepare-ae2025.py`)
1. **Build Script**
   - Duplicate and adapt `prepare-ae2026.py` as `prepare-ae2025.py`.
   - Merge lineage, keys, transcriptions, and figures.
   - Map GA (1-10) and AE (11-65).
   - Inject the official metadata block (Title, Date, Time).
   - Output to `data/ae/2025.json`.

## Phase 5: Validation
1. **Data Validation**
   - Adapt `scripts/validate-ae.mjs` to loop over all files in `data/ae/` instead of just 2026.
   - Assert: 65 questions, 100 marks, correct section totals, no missing image references.
2. **Manifest Update**
   - Update `data/ae/manifest.json` to include `2025`.
   - Ensure the UI year selector dynamic rendering lists 2025.

## Conclusion
Because the UI and Exam State Machine are now completely decoupled from year-specific hardcoding, simply dropping a valid `2025.json` and updating the manifest will instantly light up the 2025 Full-Length CBT mode. No frontend JS modifications are required outside of standard validation.
