import fs from 'node:fs';
import crypto from 'node:crypto';

const hash = path => crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
const pdfSha = hash('internal/ae/AE2015.pdf');

const natRanges = {
  8: [280, 280],
  15: [24.99, 25.01],
  23: [2131.1, 2139.1],
  25: [0.97, 1.01],
  27: [4.9, 5.1],
  28: [43.9, 44.1],
  31: [6.27, 6.29],
  32: [0.99, 1.01],
  36: [1.9, 2.1],
  37: [0.49, 0.51],
  39: [49.99, 50.01],
  40: [0.24, 0.26],
  41: [5.45, 5.6],
  42: [39.5, 40.5],
  43: [0.15, 0.18],
  44: [0.99, 1.01],
  46: [53.9, 54.1],
  50: [1742, 1752],
  51: [5.42, 5.48],
  54: [1.27, 1.32],
  56: [8.9, 9.1],
  57: [1.33, 1.4],
  58: [990, 1020],
  59: [2046, 2075],
  60: [17.2, 17.3],
  62: [1.9, 2.1],
  63: [0.37, 0.39],
  64: [20.5, 21.3],
  65: [824.0, 832.1]
};

const paper = JSON.parse(fs.readFileSync('data/ae/2015.json', 'utf8'));

// Update answers for NAT
for (const q of paper.questions) {
  if (q.type === 'NAT') {
    const range = natRanges[q.number];
    if (!range) throw new Error(`Missing NAT range for Q${q.number}`);
    q.answer = range;
    q.acceptedAnswers = [range];
  }
}

fs.writeFileSync('data/ae/2015.json', JSON.stringify(paper, null, 2) + '\n');

// Build key json
const rows = paper.questions.map(q => {
  let rawKey;
  if (q.type === 'MCQ') {
    rawKey = q.answer;
  } else if (q.type === 'NAT') {
    const r = natRanges[q.number];
    rawKey = `${r[0]} to ${r[1]}`;
  }
  return {
    number: q.number,
    section: q.section,
    sectionQuestionNumber: q.section === 'GA' ? q.number : q.number - 10,
    type: q.type,
    rawKey,
    marks: q.marks
  };
});

const keyData = {
  exam: 'GATE',
  year: 2015,
  paper: 'AE',
  source: 'internal/ae/AE2015.pdf',
  sha256: pdfSha,
  totalQuestions: 65,
  totalMarks: 100,
  rows
};

fs.writeFileSync('internal/ae/AE2015-key.json', JSON.stringify(keyData, null, 2) + '\n');

// Update manifest
const manifest = JSON.parse(fs.readFileSync('data/ae/manifest.json', 'utf8'));
const yIdx = manifest.years.findIndex(y => y.year === 2015);
manifest.years[yIdx].questionTypeCounts = {
  MCQ: 36,
  MSQ: 0,
  NAT: 29
};

fs.writeFileSync('data/ae/manifest.json', JSON.stringify(manifest, null, 2) + '\n');
console.log('Synchronized AE2015 files.');
