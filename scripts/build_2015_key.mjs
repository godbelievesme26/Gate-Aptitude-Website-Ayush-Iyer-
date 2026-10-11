import fs from 'node:fs';
import crypto from 'node:crypto';

const hash = path => crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
const pdfSha = hash('internal/ae/AE2015.pdf');

const paper = JSON.parse(fs.readFileSync('data/ae/2015.json', 'utf8'));

const rows = paper.questions.map((q) => {
  let rawKey;
  if (q.type === 'MCQ') {
    rawKey = q.answer;
  } else if (q.type === 'NAT') {
    if (Array.isArray(q.answer)) {
      rawKey = `${q.answer[0]} to ${q.answer[1]}`;
    } else {
      rawKey = String(q.answer);
    }
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
console.log('Saved internal/ae/AE2015-key.json');
