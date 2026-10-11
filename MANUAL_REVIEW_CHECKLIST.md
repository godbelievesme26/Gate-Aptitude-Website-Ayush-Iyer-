# GATE PYQ Platform — Manual Verification & Reviewer Checklist

**Purpose**: Provide an independent reviewer or developer with a step-by-step checklist to manually test and inspect all core capabilities of the GATE PYQ platform in a browser.

---

## 1. Environment & Prerequisites

- **Node.js**: Modern Node.js LTS (v18.0.0 or higher).
- **Browser**: Modern Chromium-based browser (Chrome, Edge), Firefox, or Safari.
- **Port Availability**: Port 3000 (Student Platform), Port 3001 (Internal Forensic Workstation).

---

## 2. Automated Quality Gates Verification

Open a terminal in the project root directory and execute:

```bash
# 1. Verify JavaScript syntax (0 errors expected)
npm run check

# 2. Execute automated test suite (217 tests passing expected)
npm test

# 3. Validate all 1,475 question records and assets (20 AE + 16 GA sets)
npm run validate
```

Expected result: All three commands pass cleanly with exit code 0.

---

## 3. Browser Manual Verification Checklist

### Step 1: Start the Student Web Server
```bash
npm start
```
Open your browser and navigate to: `http://localhost:3000`

- [ ] **Shell Loading**: Verify the application loads cleanly without blank screens or console errors.
- [ ] **Theme Switching**: Click the theme toggle icon in the topbar; verify instant transition between light and dark themes with high-contrast text.
- [ ] **Command Center**: Press `Ctrl+K` (or `Cmd+K`); verify the search modal opens with focus trapped, search for "Day 2", and press `Enter` to navigate.
- [ ] **Skip Link**: Refresh the page, press `Tab` once; verify "Skip to content" appears visibly and pressing `Enter` moves focus to the main content area.

---

### Step 2: Dynamic Year Selection & Question Bank
Navigate to `#/bank` (Question Bank) via the sidebar.

- [ ] **Year Filter Dropdown**: Click the "Year" filter dropdown. Verify all 20 historical AE years (**2007 through 2026**) are present in descending order.
- [ ] **Filter Interaction**: Select year `2016`, set Type to `NAT`, click "Filter". Verify filtered results display 2016 NAT questions.
- [ ] **Session Builder**: Navigate to `#/practice`. Verify the year dropdown includes all 20 years.

---

### Step 3: Full GATE CBT Exam Simulator
Navigate to `#/aerospace` and click on **2026** -> **Take timed paper (180 min)**.

- [ ] **Exam Surface**: Verify the clean CBT layout with sections for General Aptitude (GA) and Aerospace Engineering (AE).
- [ ] **Countdown Timer**: Verify the timer starts at 180:00 (or planned minutes) and ticks down smoothly.
- [ ] **Question Palette**:
  - Unvisited questions appear gray/white.
  - Answering a question turns the palette button green.
  - Marking a question for review adds the purple/yellow review indicator.
- [ ] **MCQ Answering**: Select an option; verify immediate selection state.
- [ ] **MSQ Answering**: On an MSQ question, select multiple options; verify toggling works cleanly.
- [ ] **NAT Answering**: On a NAT question, enter numeric values via keypad or keyboard; test decimals and negative numbers.
- [ ] **Exam Submit Modal**: Click "Submit" in the bottom right; verify the Exam Summary table renders displaying counts for Answered, Not Answered, Marked for Review, and Not Visited.
- [ ] **Submission & Results**: Confirm submission; verify navigation to `#/result/<id>` with complete score breakdown and review links.

---

### Step 4: Mathematical Typography & Offline Test
Navigate to `#/aerospace` -> Select **2023** or **2024** paper.

- [ ] **Formulas & Radicals**: Inspect questions with mathematical formulas. Verify square roots render with proper radical overlines, fractions render with horizontal division bars, and Greek characters (`α`, `β`, `γ`, `θ`, `ω`) display sharply.
- [ ] **Vectors & Accents**: Verify vector arrows and dot accents align correctly over symbols.
- [ ] **Service Worker Offline Test**:
  1. Open DevTools (`F12`) -> **Application** -> **Service Workers** -> Verify `sw.js` is active and running.
  2. In DevTools -> **Network** tab -> Check the **Offline** checkbox.
  3. Hard refresh the page (`Ctrl+F5`).
  4. Verify the entire application loads instantly offline, navigation functions, and the sidebar badge updates to `Offline · Local workspace`.

---

### Step 5: Data Persistence & Tab Reload Test
1. Start any practice session and answer 3 questions.
2. Note the question number and selected answers.
3. Reload the tab (`F5`).
4. Verify the session resumes automatically with all answers, question position, and elapsed time preserved.

---

## 4. Verification Sign-Off

- **Inspector**: ___________________________
- **Date**: _______________________________
- **Verdict**: [ ] PASS   [ ] FAIL
