import fs from 'node:fs';

const manifest = JSON.parse(fs.readFileSync('data/ae/manifest.json', 'utf8'));

const yearIndex = manifest.years.findIndex(y => y.year === 2015);
if (yearIndex >= 0) {
  manifest.years[yearIndex] = {
    year: 2015,
    paper: "AE",
    title: "GATE 2015 Aerospace Engineering",
    path: "data/ae/2015.json",
    ingestionStatus: "complete",
    verificationStatus: "source-verified",
    totalQuestions: 65,
    totalMarks: 100,
    sections: [
      {
        id: "GA",
        title: "General Aptitude",
        questionIds: [
          "gate-2015-ae-ga-01",
          "gate-2015-ae-ga-02",
          "gate-2015-ae-ga-03",
          "gate-2015-ae-ga-04",
          "gate-2015-ae-ga-05",
          "gate-2015-ae-ga-06",
          "gate-2015-ae-ga-07",
          "gate-2015-ae-ga-08",
          "gate-2015-ae-ga-09",
          "gate-2015-ae-ga-10"
        ],
        totalMarks: 15
      },
      {
        id: "AE",
        title: "Aerospace Engineering",
        questionIds: [
          "gate-2015-ae-ae-11",
          "gate-2015-ae-ae-12",
          "gate-2015-ae-ae-13",
          "gate-2015-ae-ae-14",
          "gate-2015-ae-ae-15",
          "gate-2015-ae-ae-16",
          "gate-2015-ae-ae-17",
          "gate-2015-ae-ae-18",
          "gate-2015-ae-ae-19",
          "gate-2015-ae-ae-20",
          "gate-2015-ae-ae-21",
          "gate-2015-ae-ae-22",
          "gate-2015-ae-ae-23",
          "gate-2015-ae-ae-24",
          "gate-2015-ae-ae-25",
          "gate-2015-ae-ae-26",
          "gate-2015-ae-ae-27",
          "gate-2015-ae-ae-28",
          "gate-2015-ae-ae-29",
          "gate-2015-ae-ae-30",
          "gate-2015-ae-ae-31",
          "gate-2015-ae-ae-32",
          "gate-2015-ae-ae-33",
          "gate-2015-ae-ae-34",
          "gate-2015-ae-ae-35",
          "gate-2015-ae-ae-36",
          "gate-2015-ae-ae-37",
          "gate-2015-ae-ae-38",
          "gate-2015-ae-ae-39",
          "gate-2015-ae-ae-40",
          "gate-2015-ae-ae-41",
          "gate-2015-ae-ae-42",
          "gate-2015-ae-ae-43",
          "gate-2015-ae-ae-44",
          "gate-2015-ae-ae-45",
          "gate-2015-ae-ae-46",
          "gate-2015-ae-ae-47",
          "gate-2015-ae-ae-48",
          "gate-2015-ae-ae-49",
          "gate-2015-ae-ae-50",
          "gate-2015-ae-ae-51",
          "gate-2015-ae-ae-52",
          "gate-2015-ae-ae-53",
          "gate-2015-ae-ae-54",
          "gate-2015-ae-ae-55",
          "gate-2015-ae-ae-56",
          "gate-2015-ae-ae-57",
          "gate-2015-ae-ae-58",
          "gate-2015-ae-ae-59",
          "gate-2015-ae-ae-60",
          "gate-2015-ae-ae-61",
          "gate-2015-ae-ae-62",
          "gate-2015-ae-ae-63",
          "gate-2015-ae-ae-64",
          "gate-2015-ae-ae-65"
        ],
        totalMarks: 85
      }
    ],
    questionTypeCounts: {
      MCQ: 45,
      MSQ: 0,
      NAT: 20
    },
    figureAssetCount: 5,
    newFigureAssetCount: 5,
    answerAvailability: {
      officialKey: 65,
      gradedAnswers: 65,
      marksToAll: 0,
      unavailable: 0
    },
    provenance: {
      paperSource: "internal/ae/AE2015.pdf",
      keySource: "internal/ae/AE2015-key.json"
    },
    sourcePdf: "internal/ae/AE2015.pdf",
    questionCount: 65,
    newQuestionCount: 65,
    reusedGAQuestionCount: 0,
    reusedFigureAssetCount: 0,
    optionFigureCount: 0,
    structuredTableCount: 0,
    questionGroupCount: 0,
    verifiedOn: "2026-10-07"
  };
}

fs.writeFileSync('data/ae/manifest.json', JSON.stringify(manifest, null, 2) + '\n');
console.log('Updated manifest.json for AE2015');
