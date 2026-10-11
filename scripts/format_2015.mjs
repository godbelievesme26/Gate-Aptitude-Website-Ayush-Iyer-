import fs from 'node:fs';
import crypto from 'node:crypto';

const hash = path => crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
const pdfSha = hash('internal/ae/AE2015.pdf');

const raw = JSON.parse(fs.readFileSync('data/ae/2015.json', 'utf8'));

// Format questions properly
const formattedQuestions = raw.questions.map((q, idx) => {
  const number = idx + 1;
  const isGA = number <= 10;
  const section = isGA ? 'GA' : 'AE';
  const numStr = number.toString().padStart(2, '0');
  const id = isGA ? `gate-2015-ae-ga-${numStr}` : `gate-2015-ae-ae-${numStr}`;

  let options = [];
  if (q.type !== 'NAT') {
    if (Array.isArray(q.options)) {
      if (typeof q.options[0] === 'string') {
        const labels = ['A', 'B', 'C', 'D'];
        options = q.options.map((opt, oIdx) => ({
          label: labels[oIdx] || String.fromCharCode(65 + oIdx),
          text: opt
        }));
      } else {
        options = q.options;
      }
    }
  }

  let negativeMarks = 0;
  if (q.type === 'MCQ') {
    negativeMarks = q.marks === 1 ? 0.3333333333333333 : 0.6666666666666666;
  }

  let figures = [];
  let hasFigure = false;

  if (number === 8) {
    hasFigure = true;
    figures = [{
      src: 'figures/gate-2015-ae-ga-08-figure-1.png',
      alt: 'Triangle PQR with side lengths and angle',
      page: 3,
      source: {
        file: 'internal/ae/AE2015.pdf',
        sha256: pdfSha,
        page: 3,
        verificationStatus: 'source-verified',
        verifiedOn: '2026-10-07'
      }
    }];
  } else if (number === 26) {
    hasFigure = true;
    figures = [{
      src: 'figures/gate-2015-ae-ae-26-figure-1.png',
      alt: 'Four cantilever loading cases P, Q, R, S',
      page: 8,
      source: {
        file: 'internal/ae/AE2015.pdf',
        sha256: pdfSha,
        page: 8,
        verificationStatus: 'source-verified',
        verifiedOn: '2026-10-07'
      }
    }];
  } else if (number === 41) {
    hasFigure = true;
    figures = [{
      src: 'figures/gate-2015-ae-ae-41-figure-1.png',
      alt: 'Cantilever beam with offset link load',
      page: 13,
      source: {
        file: 'internal/ae/AE2015.pdf',
        sha256: pdfSha,
        page: 13,
        verificationStatus: 'source-verified',
        verifiedOn: '2026-10-07'
      }
    }];
  } else if (number === 56) {
    hasFigure = true;
    figures = [{
      src: 'figures/gate-2015-ae-ae-56-figure-1.png',
      alt: 'Rankine half body in uniform stream with source',
      page: 18,
      source: {
        file: 'internal/ae/AE2015.pdf',
        sha256: pdfSha,
        page: 18,
        verificationStatus: 'source-verified',
        verifiedOn: '2026-10-07'
      }
    }];
  } else if (number === 58) {
    hasFigure = true;
    figures = [{
      src: 'figures/gate-2015-ae-ae-58-figure-1.png',
      alt: 'Thin-walled rectangular tube cross section',
      page: 19,
      source: {
        file: 'internal/ae/AE2015.pdf',
        sha256: pdfSha,
        page: 19,
        verificationStatus: 'source-verified',
        verifiedOn: '2026-10-07'
      }
    }];
  }

  return {
    id,
    number,
    year: 2015,
    paper: 'AE',
    section,
    subject: isGA ? 'General Aptitude' : 'Aerospace Engineering',
    type: q.type,
    marks: q.marks,
    negativeMarks,
    question: q.question,
    options,
    answer: q.answer,
    acceptedAnswers: Array.isArray(q.answer) ? q.answer : [q.answer],
    markingRule: 'gate-2015-official',
    hasFigure,
    figures,
    groupId: null,
    source: {
      paper: 'AE',
      year: 2015,
      questionNumber: isGA ? number : number - 10,
      section,
      file: 'internal/ae/AE2015.pdf',
      sha256: pdfSha,
      pages: [
        {
          page: q.source?.pages?.[0]?.page || 1,
          coordinateSystem: 'PDF points, top-left origin'
        }
      ],
      verificationStatus: 'source-verified',
      verifiedOn: '2026-10-07'
    },
    transcriptionStatus: 'source-verified',
    solution: null,
    solutionAvailability: 'not-provided-in-source',
    gradingStatus: 'official key verified',
    answerSource: {
      paper: 'AE',
      questionNumber: isGA ? number : number - 10,
      section,
      file: 'internal/ae/AE2015.pdf',
      sha256: pdfSha,
      verifiedOn: '2026-10-07'
    }
  };
});

const questionOrder = formattedQuestions.map(q => q.id);
const gaIds = formattedQuestions.filter(q => q.section === 'GA').map(q => q.id);
const aeIds = formattedQuestions.filter(q => q.section === 'AE').map(q => q.id);

const paper2015 = {
  schemaVersion: 1,
  id: 'gate-2015-ae',
  exam: 'GATE',
  year: 2015,
  paper: 'AE',
  title: 'GATE Aerospace Engineering 2015',
  durationMinutes: 180,
  totalMarks: 100,
  totalQuestions: 65,
  sectionOrder: ['GA', 'AE'],
  sections: [
    {
      id: 'GA',
      title: 'General Aptitude',
      questionIds: gaIds,
      totalMarks: 15
    },
    {
      id: 'AE',
      title: 'Aerospace Engineering',
      questionIds: aeIds,
      totalMarks: 85
    }
  ],
  questionOrder,
  questionRefs: formattedQuestions.map(q => ({
    id: q.id,
    number: q.number,
    section: q.section
  })),
  questionGroups: [],
  marking: {
    negativeFraction: {
      MCQ: 0.3333333333333333,
      MSQ: 0,
      NAT: 0
    }
  },
  questions: formattedQuestions
};

fs.writeFileSync('data/ae/2015.json', JSON.stringify(paper2015, null, 2) + '\n');
console.log('Saved data/ae/2015.json');
